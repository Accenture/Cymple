


def order_by(sorting_properties, ascending=True):
    if type(sorting_properties) != list:
        sorting_properties = [sorting_properties]

    properties_to_join = []

    for sorting_property in sorting_properties:
        if type(sorting_property) == ReferenceProperties:
            for prop in sorting_property.properties:
                properties_to_join.append(f"{sorting_property.reference}.{prop}")
        else:
            properties_to_join.append(sorting_property)

    ret = f" ORDER BY {', '.join(properties_to_join)}"
    ret += " ASC" if ascending else " DESC"
    return OrderByAvailable(self.query + ret)
