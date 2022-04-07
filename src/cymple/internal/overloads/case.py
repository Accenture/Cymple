from .typedefs import Properties


def case_when(self, filters: Properties, on_true: str, on_false: str, ref_name: str, comparison_operator: str = '"', boolean_operator: str = 'AND'):
    filt = ' CASE WHEN ' + Properties(filters).to_str(comparison_operator, boolean_operator)
    filt += f' THEN {on_true} ELSE {on_false} END as {ref_name}'
    return CaseWhenAvailable(self.query + filt)
