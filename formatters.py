# formatters.py
        return (
            f"{levels}, {bedrooms} apartment #{apartment} "
            f"on the {floor} floor {locker_text}. "
            f"{elevator}{reservation_text}. "
            f"{coi_text}."
        )

    return ""


# =========================
# PICKUP ACCESS
# =========================

def format_pickup_access_1(data):
    base = clean_text(
        get_value(data, "Is the pick-up location on or off military base?")
    )

    parking = normalize_list(
        get_value(
            data,
            "Do we have street parking, driveway or parking lot available?"
        )
    )

    restrictions = clean_text(
        get_value(
            data,
            "Are there any permits or restrictions for parking on the street or parking lot? (don't consider on-base access as restrictions or permits needed)"
        )
    )

    return f"{base} {parking} available. {restrictions}."


# =========================
# PICKUP ACCESS #2
# =========================

def format_pickup_access_2(data):
    base = clean_text(
        get_value(data, "Is the secondary pick-up location on or off base?"
    ))

    loading_dock = clean_text(
        get_value(data, "Is the loading dock available?")
    )

    parking = clean_text(
        normalize_list(
            get_value(
                data,
                "Do we have street parking or parking lot available?"
            )
        )
    )

    restrictions = clean_text(
        get_value(
            data,
            "Are there any permits or restrictions for parking on the street or parking lot?"
        )
    )

    dock_text = ""

    if "Yes" in loading_dock:
        dock_text = "Loading dock available."

    return f"{base} {dock_text} {parking}. {restrictions}."