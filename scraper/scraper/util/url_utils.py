

def create_url(make: str, models: list) -> str:
    baseurl = f'https://www.olx.pl/d/motoryzacja/samochody/{make}'
    base_query_placeholder = 'search%5Bfilter_enum_model%5D%5B{i}%5D={model}'
    model_query = "?"
    i = 0
    for model in models:
        base_query = base_query_placeholder.replace("{i}", str(i))
        model_query += base_query
        model_query += '&'
        model_query = model_query.replace("{model}", model)
        i += 1

    model_query = model_query[:-1]

    return baseurl + model_query
