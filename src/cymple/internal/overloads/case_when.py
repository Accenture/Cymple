

def case_when(self, filters: dict, on_true: str, on_false: str, ref_name: str, comparison_operator: str = '"', boolean_operator: str = 'AND', **kwargs):
    filt = ' CASE WHEN ' + Properties(filters).to_str(comparison_operator, boolean_operator, **kwargs)
    filt += f' THEN {on_true} ELSE {on_false} END as {ref_name}'
    return CaseWhenAvailable(self.query + filt)
