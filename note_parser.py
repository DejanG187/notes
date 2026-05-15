# helpers.py

import ast


def get_value(data, key, default=""):
    return data.get(key, default).strip()


# Converts:
# ['Garage', 'Shed']
# into:
# garage and shed

def normalize_list(value):
    if not value:
        return ""

    try:
        parsed = ast.literal_eval(value)

        if isinstance(parsed, list):
            cleaned = [x.replace('.', '').strip() for x in parsed]

            if len(cleaned) == 1:
                return cleaned[0]

            if len(cleaned) == 2:
                return f"{cleaned[0]} and {cleaned[1]}"

            return ", ".join(cleaned[:-1]) + f", and {cleaned[-1]}"

    except:
        pass

    return value


# Converts:
# 2-bedroom
# into:
# 2-bedroom
# (placeholder for future cleanup)

def clean_text(value):
    return value.replace('.', '').strip()
    