def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit == to_unit:
        return float(value)
    if from_unit == 'Celsius':
        c = value
    elif from_unit == 'Fahrenheit':
        c = (value - 32) * 5/9
    elif from_unit == 'Kelvin':
        c = value - 273.15
    else:
        raise ValueError(f"Unidade de origem desconhecida: {from_unit}")

    if to_unit == 'Celsius':
        return c
    elif to_unit == 'Fahrenheit':
        return c * 9/5 + 32
    elif to_unit == 'Kelvin':
        return c + 273.15
    else:
        raise ValueError(f"Unidade de destino desconhecida: {to_unit}")
