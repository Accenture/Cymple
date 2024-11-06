"""Internal Rendering module, used for creating a new builder implementation."""

import inspect
import json
import os
import pathlib
import preface
import overloads

query_class = getattr(preface, preface.Query.__name__)

MAX_LINE_LEN = 120


def _render_clause(declaration: dict):
    main_output = ''
    decorators_output = ''

    clause_name = declaration['clause_name'].upper()
    clause_name_title = declaration['clause_name'].title().replace(' ', '')

    successors = declaration['successors']
    avilability_class_str = f'class {clause_name_title}Available({", ".join(successors)}):' + '\n    '
    avilability_class_str += f'"""A class decorator declares a {clause_name_title} is available in the current query."""' + '\n\n'
    decorators_output += avilability_class_str

    main_output += f'class {clause_name_title}({query_class.__name__}):' + '\n    '
    main_output += f'"""A class for representing a "{clause_name}" clause."""' + '\n\n'

    methods = declaration.get('methods')

    if not methods and clause_name != 'QUERY START':
        methods = [{'name': clause_name.replace(' ', '_')}]

    for method in methods:
        docstring_summary = method.get('docstring_summary', f'Concatenate the "{clause_name}" clause.')
        method_name = method['name'].lower()
        args = method.get('args')
        args_str = 'self'

        if not docstring_summary.endswith('.'):
            docstring_summary = docstring_summary + '.'
        docstring_summary += '\n        '

        docstring_params = ''
        method_overload = None

        if args:
            for arg_name, arg_meta in args.items():
                arg_description = arg_meta.get('description', '')
                arg_type = arg_meta.get('type', '')
                arg_default = arg_meta.get('default', '')
                args_str += ', ' + \
                    f'{arg_name}{": " + arg_type if arg_type else ""}{" = " + arg_default if arg_default else ""}'

                docstring_params += ':param ' + arg_name + (': ' + arg_description if arg_description else ': ' + arg_name) + (
                    f', defaults to {arg_default}' if arg_default else '') + '\n        '
                docstring_params += ':type ' + arg_name + \
                    (f': {arg_type}' if arg_type else '' + ', optional' if arg_default else '') + '\n        '

        try:
            method_overload = getattr(overloads, method_name)
        except Exception as ex:
            print(f'Note: No overload to method "{method_name}" ({ex}).')

        if method_overload:
            try:
                try:
                    method_overload.__doc__ = ''
                except Exception as exc:
                    print(exc)

                # overload = inspect.getsource(method_overload)
                def_lines = inspect.getsourcelines(method_overload)[0]
                overload = ''
                flag = False
                for line in def_lines:
                    if flag:
                        overload += line
                    elif line.strip().startswith(f'def {method_name}'):
                        flag = True

                overload = overload.replace('\n', '\n    ')

            except Exception as ex:
                print(f'Couldn\'t overload method "{method_name}". Exception: {ex}')
                overload = ''
        else:
            overload = ''

        main_output += f'    def {method_name}({args_str}):' + '\n        '
        main_output += f'"""{docstring_summary}' + '\n        '
        main_output += f'{docstring_params}' + '\n        ' if docstring_params else ''
        main_output += f':return: A Query object with a query that contains the new clause.' + '\n        '
        main_output += f':rtype: {clause_name_title}Available' + '\n        '
        main_output += f'"""' + '\n        '

        if overload:
            main_output += overload.strip()
        else:
            main_output += f'return {clause_name_title}Available(self.query + \' {clause_name}\')'

        main_output += '\n\n'

    lines = main_output.split('\n')
    new_lines = []

    for line in lines:
        if len(line) >= MAX_LINE_LEN:
            white_space_idx = 0
            start_idx = 0

            if ':param' in line:
                start_idx = line.index(':param')

            try:
                while line.index(' ', white_space_idx + 1) < MAX_LINE_LEN:
                    white_space_idx = line.index(' ', white_space_idx + 1)
            except:
                pass

            if start_idx > 0 and white_space_idx > start_idx:
                new_lines.append(line[0:white_space_idx])
                new_lines.append(' ' * start_idx + '    ' + line[white_space_idx+1:])
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    main_output = '\n'.join(new_lines)

    return main_output, decorators_output, clause_name_title


def render_builder_code():
    """Main function to invoke to render a new builder implementation."""
    clauses_output = '"""This is the Cymple query builder module."""\n\n'
    clauses_output += '# pylint: disable=R0901\n'
    clauses_output += '# pylint: disable=R0903\n'
    clauses_output += '# pylint: disable=W0102\n'
    clauses_output += 'from typing import List, Union, Dict, Any\n'
    clauses_output += 'from .typedefs import Mapping, Properties\n\n'
    clauses_output += inspect.getsource(query_class) + '\n\n'

    decorators_output = '\n'

    all_clauses_titles = set()

    declarations_fps = os.listdir(os.path.join(os.path.dirname(__file__), 'declarations'))
    declarations_fps.sort()

    for file in declarations_fps:
        if file.endswith('.json'):
            path = os.path.join(os.path.dirname(__file__), 'declarations', file)

            with open(path) as file:
                declaration = json.load(file)
                add_clause_output, add_decorators_output, clause_name_title = _render_clause(declaration)
                clauses_output += add_clause_output
                decorators_output += add_decorators_output
                all_clauses_titles.add(clause_name_title)

    any_clause_decorator_output = f'class AnyAvailable({", ".join(sorted(all_clauses_titles))}):' + '\n    '
    any_clause_decorator_output += f'"""A class decorator declares anything is available in the current query."""' + '\n\n'

    with open(os.path.join(os.path.dirname(__file__), 'finale.py')) as file:
        finale_output = file.read()

    with open(os.path.join(os.path.dirname(__file__), '../builder.py'), 'w+') as file:
        file.write(clauses_output)
        file.write(decorators_output)
        file.write(any_clause_decorator_output)
        file.write(finale_output)

    builder_path = os.path.join(pathlib.Path(__file__).parent.parent.resolve(), "builder.py")
    os.system(
        f'autopep8 {builder_path} --in-place --max-line-length {MAX_LINE_LEN}')


if __name__ == '__main__':
    render_builder_code()
