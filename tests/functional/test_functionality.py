import inspect
import sys
import pytest
from cymple import QueryBuilder, builder

any_available_clauses = [
    ("cypher", {"cypher_query_str": ""})
]


@pytest.mark.parametrize("clause, params", any_available_clauses)
def test_any_available(clause, params):
    qb = QueryBuilder()
    callables = [_callable for _callable in dir(getattr(qb.match(), clause)(*params))
                 if not _callable.startswith("__")]
    builder_classes = [_class for _class in inspect.getmembers(
        sys.modules[builder.__name__],
        lambda member: inspect.isclass(member) and member.__module__ == builder.__name__
    ) if not _class[0].lower().endswith("available") and _class[0].lower() != "querybuilder"]
    missing_callables = set()
    for _class in builder_classes:
        missing_callables.update([
            func for func in dir(_class[1]) if not func.startswith("__") and func not in callables
        ])
    assert not missing_callables
