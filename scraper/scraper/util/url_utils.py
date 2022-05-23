from .model_mapping_utils import map_name_to_uri_resource

def create_url(make: str, models: list) -> str:
    if make == 'alfa romeo':
        make =  'alfa-romeo'
    elif make == 'land rover':
        make = 'landrover'

    baseurl = f'https://www.olx.pl/d/motoryzacja/samochody/{make}'
    base_query_placeholder = 'search%5Bfilter_enum_model%5D%5B{i}%5D={model}'
    model_query = "?"
    i = 0
    for model in models:
        model = map_name_to_uri_resource(model)

        base_query = base_query_placeholder.replace("{i}", str(i))
        model_query += base_query
        model_query += '&'
        model_query = model_query.replace("{model}", model)
        i += 1

    model_query = model_query[:-1]

    return baseurl + model_query
