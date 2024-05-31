def generate_average_value(high, low):
    rounded_value = round(((float(high) + float(low)) / 2), 2)
    return f'{rounded_value:.2f}'
