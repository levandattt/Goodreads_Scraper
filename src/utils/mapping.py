def dict_to_dict(source, target):
    # return target.update({k: source[k] for k in target if k in source})
    return {k: source[k] if k in source else v for k, v in target.items()}

