def remove_prefixes(data: dict) -> dict:
    new_data = {}
    for key in data:
        new_key = key
        if new_key[0] == '_':
            new_key = new_key[1:]

        if isinstance(data[key], dict):
            new_data[new_key] = remove_prefixes(data[key])
        elif isinstance(data[key], list):
            new_seq = [remove_prefixes(el) if isinstance(
                el, dict
            ) else el for el in data[key]]
            new_data[new_key] = new_seq
        else:
            new_data[new_key] = data[key]

    return new_data
