
def f3(data):
    # Logic for f3
    return data + 1

def f2(data):
    # Logic for f2, calling f3
    return f3(data) * 2

VALID_TOKENS = {"valid_token_1", "valid_token_2"}  # Example set of valid tokens
def generateOutcome(input_data, token):
    if token not in VALID_TOKENS:
        raise PermissionError("Invalid token")

    # Logic to generate outcome, calling f2
    outcome = f2(input_data)
    return "outcome of AI-plug-in"