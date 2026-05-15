import streamlit as st
import ast


# =========================
# PARSER
# =========================

def parse_notes(raw_text):
    data = {}

    lines = raw_text.splitlines()

    for line in lines:
        if ":" not in line:
            continue

        question, answer = line.split(":", 1)

        question = question.strip()
        answer = answer.strip()

        data[question] = answer

    return data


# =========================
# HELPERS
# =========================

def get_value(data, key, default=""):
    return data.get(key, default).strip()


def clean_text(value):
    return value.replace(".", "").strip()


def normalize_list(value):

    if not value:
        return ""

    try:
        parsed = ast.literal_eval(value)

        if isinstance(parsed, list):

            cleaned = [
                x.replace(".", "").strip().lower()
                for x in parsed
            ]

            if len(cleaned) == 1:
                return cleaned[0]

            if len(cleaned) == 2:
                return f"{cleaned[0]} and {cleaned[1]}"

            return ", ".join(cleaned[:-1]) + f", and {cleaned[-1]}"

    except:
        pass

    return value


# =========================
# STORAGE
# =========================

def format_storage(data):

    storage = get_value(
        data,
        "Do you need temporary storage unit?  (company provided storage up to 90 days)"
    )

    if "No" in storage:
        return "No"

    days = get_value(
        data,
        "For how long you will need temporary storage?"
    )

    return f"Temporary storage required ({days})"


# =========================
# PICKUP ACCESS #1
# =========================

def pickup_access_1(data):

    base = clean_text(
        get_value(
            data,
            "Is the pick-up location on or off military base?"
        )
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

    return f"{base}. {parking.capitalize()} available. {restrictions}."


# =========================
# HOUSE LAYOUT
# =========================

def house_layout(data):

    stories = clean_text(
        get_value(
            data,
            "How many stories does your house have?"
        )
    )

    bedrooms = clean_text(
        get_value(
            data,
            "How many bedrooms does your house has?"
        )
    )

    extras = normalize_list(
        get_value(
            data,
            "Is there any garage, shed, attic or basement?"
        )
    )

    return f"{stories}, {bedrooms} house with a {extras}."


# =========================
# PICKUP ACCESS #2
# =========================

def pickup_access_2(data):

    base = clean_text(
        get_value(
            data,
            "Is the secondary pick-up location on or off base?"
        )
    )

    loading_dock = get_value(
        data,
        "Is the loading dock available?"
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

    return f"{base}. {dock_text} {parking.capitalize()}. {restrictions}."


# =========================
# APARTMENT LAYOUT
# =========================

def apartment_layout(data):

    levels = clean_text(
        get_value(
            data,
            "How many levels is the apartment?"
        )
    )

    bedrooms = clean_text(
        get_value(
            data,
            "How many bedrooms does your apartment has?"
        )
    )

    apartment = get_value(
        data,
        "What is the apartment number?"
    )

    floor = get_value(
        data,
        "What floor is your apartment on?"
    )

    locker = get_value(
        data,
        "Are there any storage lockers in the building?"
    )

    elevator = clean_text(
        get_value(
            data,
            "Is there elevator available?"
        )
    )

    reservation = get_value(
        data,
        "Is reservation of the elevator required?"
    )

    coi = get_value(
        data,
        "Is a certificate of insurance needed? (COI)"
    )

    locker_text = "without storage locker"

    if "With" in locker:
        locker_text = "with storage locker"

    reservation_text = ""

    if "Yes" in reservation:
        reservation_text = " and reservation required"

    coi_text = "COI not required"

    if "Yes" in coi:
        coi_text = "COI required"

    return (
        f"{levels}, {bedrooms} apartment #{apartment} "
        f"on the {floor} floor {locker_text}. "
        f"{elevator}{reservation_text}. "
        f"{coi_text}."
    )


# =========================
# GENERATOR
# =========================

def generate_output(data):

    finalized = get_value(
        data,
        "Do you have finalized destination address? (don't include tentative addresses and in case of NTS select NTS)"
    )

    destination_access = ""
    destination_layout = ""
    destination_truck = ""

    if finalized == "No":
        destination_access = "TBD"
        destination_layout = "TBD"
        destination_truck = "TBD"

    result = f"""Storage: {format_storage(data)}
Pro gear: No
Weapons: No

Packing: FULL CP

Pick-up Access #1: {pickup_access_1(data)}
Layout #1: {house_layout(data)}
Truck #1: TBD

Pick-up Access #2: {pickup_access_2(data)}
Layout #2: {apartment_layout(data)}
Truck #2: TBD

Destination Access #1: {destination_access}
Layout #1: {destination_layout}
Truck #1: {destination_truck}
"""

    return result


# =========================
# STREAMLIT
# =========================

st.set_page_config(page_title="Move Survey Formatter")

st.title("Move Survey Formatter")

raw_text = st.text_area(
    "Paste raw questionnaire",
    height=400
)

if st.button("Convert"):

    data = parse_notes(raw_text)

    output = generate_output(data)

    st.text_area(
        "Formatted Output",
        output,
        height=500
    )