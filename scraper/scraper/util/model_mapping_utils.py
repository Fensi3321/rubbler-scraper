def map_name_to_uri_resource(name: str) -> str:
    modelmap = {
        'seria 3': '3-as-sorozat',
        'seria 5': '5-as-sorozat',
        'seria 7': '7-as-sorozat'
    }

    if name in modelmap:
        return modelmap[name]

    return name.replace(" ", "-")
