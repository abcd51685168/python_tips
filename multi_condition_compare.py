def multi_condition_compare(cp):
    """use any/all instead of many or/and"""
    # case:
    if any([33 <= cp <= 47, 58 <= cp <= 64,
            91 <= cp <= 96, 123 <= cp <= 126]):
        return True
