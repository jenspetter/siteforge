JSON_FUNCTION_REFERENCES = {}

def json_func(func):
    """
    Register a function to be referenced through json\n
    If wanting a function to be referenced by json, 
    please use the @json_func above the function definition after importing this file\n
    
    :param func: The function
    """

    JSON_FUNCTION_REFERENCES[func.__name__] = func
    return func