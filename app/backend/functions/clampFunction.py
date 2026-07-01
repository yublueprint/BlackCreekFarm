def clamp(value, minimum, maximum):
    """
    Ex: 
    clamp(15, 1, 10) would give 10.
    clamp(-5, 1, 10) would give 1.
    clamp(5, 1, 10) would give 5.
    """
    if value < minimum:
        return minimum
    elif value > maximum:
        return maximum
    return value