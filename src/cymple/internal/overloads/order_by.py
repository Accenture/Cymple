


def order_by(sorting_properties, ascending=True):
    if type(sorting_properties) != list:
        sorting_properties = [sorting_properties]

    ret = f" ORDER BY {', '.join(sorting_properties)}"
    ret += " ASC" if ascending else " DESC"
    return OrderByAvailable(self.query + ret)
