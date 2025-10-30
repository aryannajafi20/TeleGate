import base64

def hash_value(value: str) -> str:
    """
    Encode a value using base64 (reversible).
    Example: 123 -> MTIz
    """
    if not isinstance(value, str):
        value = str(value)
    encoded = base64.urlsafe_b64encode(value.encode()).decode()
    return encoded


def unhash_value(encoded: str) -> str:
    """
    Decode a base64-encoded string.
    Example: MTIz -> 123
    """
    try:
        decoded = base64.urlsafe_b64decode(encoded.encode()).decode()
        return decoded
    except Exception:
        return None
