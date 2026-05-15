# rules.py

from helpers import get_value
from formatters import (
    format_storage,
    format_pro_gear,
    format_weapons,
    format_house_layout,
    format_apartment_layout,
    format_pickup_access_1,
    format_pickup_access_2,
)


def generate_output(data):

    finalized = get_value(
        data,
        "Do you have finalized destination address? (don't include tentative addresses and in case of NTS select NTS)"
    )

    pickup_1_layout = format_house_layout(data)
    pickup_2_layout = format_apartment_layout(data, secondary=True)

    destination_access = ""
    destination_layout = ""
    destination_truck = ""

    if finalized == "No":
        destination_access = "TBD"
        destination_layout = "TBD"
        destination_truck = "TBD"

    return f"""Storage: {format_storage(data)}
Pro gear: {format_pro_gear(data)}
Weapons: {format_weapons(data)}

Packing: FULL CP

Pick-up Access #1: {format_pickup_access_1(data)}
Layout #1: {pickup_1_layout}
Truck #1: TBD

Pick-up Access #2: {format_pickup_access_2(data)}
Layout #2: {pickup_2_layout}
Truck #2: TBD

Destination Access #1: {destination_access}
Layout #1: {destination_layout}
Truck #1: {destination_truck}
"""