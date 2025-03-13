import re
import folium
from modules import math as my_math


degrees_minutes_regex: str = r"([NS])[ ]?(\d{1,3}).+?([0-5]\d)\.(\d{3}).+([EW])[ ]?(\d{1,3}).+?([0-5]\d)\.(\d{3}).*"


def is_coordinate(coordinate: str) -> bool:
    if re.search(r"[NS] ?\d{1,3}.+[0-5]\d\.\d{3} +[EW] ?\d{1,3}.+[0-5]\d\.\d{3}", coordinate, flags=re.IGNORECASE) is None:
        return False
    return True


def standardize_coordinate(coordinate: str) -> str:
    items = re.findall(degrees_minutes_regex, coordinate, flags=re.IGNORECASE)[0]
    std = items[0].upper()+items[1]+' '+items[2]+'.'+items[3]+' '+items[4].upper()+items[5]+' '+items[6]+'.'+items[7]
    return std


def degrees_minutes_2_degrees(lat_long: str) -> float:
    items = re.search(r"([NSEW])(\d{1,3}) ([0-5]\d\.\d{3})", lat_long)
    if items.group(1) in ('N', 'E'):
        sign = 1
    else:
        sign = -1
    degrees = sign * round(float(items.group(2)) + float(items.group(3))/60, 5)
    return degrees


def get_coordinate_notations(degrees_minutes: str) -> dict:
    degrees_minutes = standardize_coordinate(degrees_minutes)
    items = re.search(r"([NS]\d{1,3} [0-5]\d\.\d{3}) ([EW]\d{1,3} [0-5]\d\.\d{3})", degrees_minutes)
    notations = {
        'degrees_minutes': {'lat': items.group(1), 'long': items.group(2)},
        'degrees': {'lat': degrees_minutes_2_degrees(items.group(1)), 'long': degrees_minutes_2_degrees(items.group(2))}
    }
    return notations


def show_on_map(coordinate: str, zoom: int = 13) -> folium.Map:
    notations = get_coordinate_notations(coordinate)
    location = [notations['degrees']['lat'], notations['degrees']['long']]
    m = folium.Map(location=location, zoom_start=zoom)
    folium.Marker(location, popup='Beregnet koordinat').add_to(m)
    return m


def coordinate_sum_of_digits(std_coordinate: str) -> dict:
    # sum_of_digits = {}
    # parts = std_coordinate.split(' ')
    parts = re.search(r"([NS])(\d{1,3} [0-5]\d\.\d{3}) ([EW])(\d{1,3} [0-5]\d\.\d{3})", std_coordinate)

    # lat = str(int(parts[0]))+str(int(parts[1]))
    # long = str(int(parts[2]))+str(int(parts[3]))

    ns = parts.group(1)
    lat = int(re.sub(r"\D", "", parts.group(2)))
    ew = parts.group(3)
    long = int(re.sub(r"\D", "", parts.group(4)))
    lat_long = int(re.sub(r"\D", "", std_coordinate))

    sum_of_digits = {
        'Tværsum': {ns: my_math.sum_of_digits(lat), ew: my_math.sum_of_digits(long), 'Hele koordinatet': my_math.sum_of_digits(lat_long)},
        'Reduceret tværsum': {ns: my_math.sum_of_digits_reduced(lat), ew: my_math.sum_of_digits_reduced(long), 'Hele koordinatet': my_math.sum_of_digits_reduced(lat_long)}
    }
    sum_of_digits = {
        ns: {'Reduceret tværsum': my_math.sum_of_digits_reduced(lat), 'Tværsum': my_math.sum_of_digits(lat)},
        ew: {'Reduceret tværsum': my_math.sum_of_digits_reduced(long), 'Tværsum': my_math.sum_of_digits(long)},
        'Hele koordinatet': {'Reduceret tværsum': my_math.sum_of_digits_reduced(lat_long), 'Tværsum': my_math.sum_of_digits(lat_long)}
        # 'Reduceret tværsum': {ns: my_math.sum_of_digits_reduced(lat), ew: my_math.sum_of_digits_reduced(long), 'Hele koordinatet': my_math.sum_of_digits_reduced(lat_long)},
        # 'Tværsum': {ns: my_math.sum_of_digits(lat), ew: my_math.sum_of_digits(long), 'Hele koordinatet': my_math.sum_of_digits(lat_long)}
    }

    return sum_of_digits
