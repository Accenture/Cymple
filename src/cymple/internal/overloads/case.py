from typing import Dict, List, Union


def case(when_then_mapping: Dict[str, Union[List[str], str]], default_result: str, results_ref: str, test_expression: str = None):
    ret = " CASE"
    if test_expression is not None:
        ret += f" {test_expression}"
    for then, when in when_then_mapping.items():
        if type(when) is not list:
            when = [when]
        ret += f" WHEN {', '.join(when)} THEN {then}"
    ret += f" ELSE {default_result} END"
    if results_ref is not None:
        ret += f" AS {results_ref}"
    return CaseAvailable(self.query + ret)
