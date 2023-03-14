def procedure(self, literal_procedure):
    ret = f" {literal_procedure}"
    return ProcedureAvailable(self.query + ret)
