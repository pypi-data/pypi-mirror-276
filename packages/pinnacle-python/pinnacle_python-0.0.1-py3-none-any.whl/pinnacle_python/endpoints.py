endpoints = []

def endpoint(func):
    endpoints.append(func)
    return func