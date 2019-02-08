import decimal

def DecimalDefault(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError
