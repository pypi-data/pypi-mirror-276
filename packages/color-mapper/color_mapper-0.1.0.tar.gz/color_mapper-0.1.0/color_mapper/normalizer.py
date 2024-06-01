def normalize(value, min_value, max_value):
    """Normalize the value to a range between 0 and 1."""
    return (value - min_value) / (max_value - min_value)
