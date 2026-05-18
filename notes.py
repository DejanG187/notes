
import streamlit as st
import ast


# =====================================================
# PARSER
# =====================================================


def parse_notes(raw_text):

    data = {
        "general": {},
        "PP": {},
        "SP": {},
        "PD": {},
        "SD": {}
    }

    lines = raw_text.splitlines()

    for line in lines:

        if ":" not in line:
            continue

        question, answer = line.split(":", 1)

        question = question.strip()
        answer = answer.strip()

        section = "general"

        if "(Primary pick-up)" in question:
            section = "PP"

        elif "(Secondary pick-up)" in question:
            section = "SP"

        elif "(Primary drop-off)" in question:
            section = "PD"

        elif "(Secondary drop-off)" in question:
            section = "SD"

        data[section][question] = answer

        # GLOBAL QUESTIONS

        if "primary pick-up location on or off military base" in question:
            data["PP"]["BASE"] = answer

        if "secondary pick-up location on or off base" in question:
            data["SP"]["BASE"] = answer

        if "primary destination address on or off military base" in question:
            data["PD"]["BASE"] = answer

        if "secondary destination address on or off military base" in question:
            data["SD"]["BASE"] = answer

        if "primary pick-up location house, apartment or storage unit" in question:
            data["PP"]["TYPE"] = answer

        if "secondary pick-up location house, apartment or storage unit" in question:
            data["SP"]["TYPE"] = answer

        if "primary destination house, apartment or storage unit" in question:
            data["PD"]["TYPE"] = answer

        if "secondary destination house, apartment or storage unit" in question:
            data["SD"]["TYPE"] = answer

    return data


# =====================================================
# HELPERS
# =====================================================


def get_value(section, key, default=""):
    return section.get(key, default).strip()



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


# =====================================================
# GENERAL
# =====================================================


def format_storage(data):

    storage = get_value(
        data["general"],
        "Do you need temporary storage unit?  (company provided storage up to 90 days)"
    )

    if "No" in storage:
        return "No"

    duration = get_value(
        data["general"],
        "For how long you will need temporary storage?"
    )

    return f"Temporary storage required ({duration})"



def format_pro_gear(data):

    pro = get_value(
        data["general"],
        "Are we shipping any pro-gear?"
    )

    if "No" in pro:
        return "No"

    weight = get_value(
        data["general"],
        "What is the approximate weight of the pro-gear?"
    )

    return f"Yes, approximately {weight}"



def format_weapons(data):

    weapons = get_value(
        data["general"],
        "Are we shipping any firearms?"
    )

    if "No" in weapons:
        return "No"

    firearm_info = get_value(
        data["general"],
        "Please enter make, model and serial number for each."
    )

    return f"Yes\n{firearm_info}"


# =====================================================
# ACCESS FORMATTER
# =====================================================


def format_access(section):

    base = get_value(section, "BASE")

    result = []

    if base:
        result.append(clean_text(base) + ".")

    # LOADING DOCK

    loading_dock = ""

    for key in section.keys():
        if "loading dock available" in key.lower():
            loading_dock = section[key]

    if "Yes" in loading_dock or "Loading dock available" in loading_dock:
        result.append("Loading dock available.")

    # PARKING

    for key in section.keys():

        if "street parking" in key.lower() or "parking lot" in key.lower():

            parking = normalize_list(section[key])

            if parking:
                result.append(parking.capitalize() + ".")

            break

    # RESTRICTIONS

    for key in section.keys():

        if "permits or restrictions" in key.lower():

            restriction = clean_text(section[key])

            if restriction:
                result.append(restriction + ".")

            break

    return " ".join(result)


# =====================================================
# HOUSE LAYOUT
# =====================================================


def format_house(section):

    stories = ""
    bedrooms = ""
    extras = ""

    for key in section.keys():

        if "stories does your house have" in key:
            stories = clean_text(section[key])

        if "bedrooms does your house has" in key:
            bedrooms = clean_text(section[key])

        if "garage, shed, attic or basement" in key:
            extras = normalize_list(section[key])

    return f"{stories}, {bedrooms} house with a {extras}."


# =====================================================
# APARTMENT LAYOUT
# =====================================================


def format_apartment(section):

    floor = ""
    bedrooms = ""
    apartment = ""
    locker = ""
    elevator = ""
    reservation = ""
    coi = ""
    levels = ""

    for key in section.keys():

        if "floor is your apartment" in key:
            floor = clean_text(section[key])

        if "bedrooms does your apartment" in key:
            bedrooms = clean_text(section[key])

        if "apartment number" in key:
            apartment = section[key]

        if "storage lockers" in key:
            locker = section[key]

        if "elevator available" in key:
            elevator = clean_text(section[key])

        if "reservation of the elevator" in key:
            reservation = section[key]

        if "certificate of insurance" in key:
            coi = section[key]

        if "levels is the apartment" in key:
            levels = clean_text(section[key])

    locker_text = "without storage locker"

    if "With" in locker:
        locker_text = "with storage locker"

    reservation_text = ""

    if "Yes" in reservation:
        reservation_text = " and reservation required"

    coi_text = "COI not required"

    if "Yes" in coi:
        coi_text = "COI required"

    if levels:
        return (
            f"{levels}, {bedrooms} apartment #{apartment} "
            f"on the {floor} floor {locker_text}. "
            f"{elevator}{reservation_text}. "
            f"{coi_text}."
        )

    return (
        f"{bedrooms} apartment #{apartment} "
        f"on the {floor} floor {locker_text}. "
        f"{elevator}{reservation_text}. "
        f"{coi_text}."
    )


# =====================================================
# STORAGE LAYOUT
# =====================================================


def format_storage_unit(section):

    size = ""
    number = ""
    climate = ""
    access = ""
    indoor_outdoor = ""
    floor = ""

    for key in section.keys():

        if "size of the storage unit" in key:
            size = section[key]

        if "storage unit number" in key:
            number = section[key]

        if "climate controlled" in key:
            climate = section[key]

        if "after hours or on weekends" in key:
            access = section[key]

        if "indoor or outdoor" in key:
            indoor_outdoor = section[key]

        if "floor is the storage unit" in key:
            floor = section[key]

    return (
        f"{indoor_outdoor} {climate} storage unit #{number} "
        f"{floor}. Unit size {size}. {access}"
    )


# =====================================================
# BARRACKS LAYOUT
# =====================================================


def format_barracks(section):

    floor = ""
    room = ""
    elevator = ""
    stairs = ""

    for key in section.keys():

        if "room on" in key:
            floor = clean_text(section[key])

        if "room number" in key:
            room = section[key]

        if "elevator available" in key:
            elevator = clean_text(section[key])

        if "flights of stairs" in key:
            stairs = section[key]

    elevator_text = elevator

    if "No elevator" in elevator:
        elevator_text = f"No elevator. {stairs} flights of stairs"

    return (
        f"Barracks room #{room} on the {floor} floor. "
        f"{elevator_text}."
    )


# =====================================================
# DYNAMIC LAYOUT
# =====================================================


def format_layout(section):

    location_type = get_value(section, "TYPE")

    if "House" in location_type:
        return format_house(section)

    if "Apartment" in location_type:
        return format_apartment(section)

    if "Storage" in location_type:
        return format_storage_unit(section)

    if "Barracks" in location_type:
        return format_barracks(section)

    return ""


# =====================================================
# GENERATOR
# =====================================================


def generate_output(data):

    result = f"""Storage: {format_storage(data)}
Pro gear: {format_pro_gear(data)}
Weapons: {format_weapons(data)}

Packing: FULL CP

Pick-up Access #1: {format_access(data['PP'])}
Layout #1: {format_layout(data['PP'])}
Truck #1:

Pick-up Access #2: {format_access(data['SP'])}
Layout #2: {format_layout(data['SP'])}
Truck #2:

Destination Access #1: {format_access(data['PD'])}
Layout #1: {format_layout(data['PD'])}
Truck #1:

Destination Access #2: {format_access(data['SD'])}
Layout #2: {format_layout(data['SD'])}
Truck #2:
"""

    return result


# =====================================================
# STREAMLIT
# =====================================================


st.set_page_config(page_title="Move Survey Formatter")

st.title("Move Survey Formatter")

raw_text = st.text_area(
    "Paste raw questionnaire",
    height=500
)


if st.button("Convert"):

    data = parse_notes(raw_text)

    output = generate_output(data)

    st.text_area(
        "Formatted Output",
        output,
        height=600
    )
