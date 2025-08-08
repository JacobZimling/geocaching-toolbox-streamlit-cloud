import streamlit as st
from modules import gade
from modules import toolbox
from modules import gpscoordinates as gps
import pandas as pd
from streamlit_folium import folium_static
import platform
from st_copy import copy_button

# DONE: Handle regex matching returning an error - try
# TODO: GitHub bug reporting

toolbox.toolbox_header("Beregn Gade")

## Use default values for numbers_found and coordinate_formula when running on test server
default_value = {}
if platform.processor() == "":
    default_value['numbers_found'] = ""
    default_value['coordinate_formula'] = ""
else:
    default_value['numbers_found'] = "1644"
    default_value['coordinate_formula'] = "N55 4e.jae E012 3a.fdd"
    # default_value['coordinate_formula'] = "N 55.38.(1*(J+A))EI E 012 16.JEK"
    # default_value['coordinate_formula'] = "D 55 38.JEI E 012 16.JEK"

numbers_found = st.text_input(
    label="Indtast de fundne tal. Bogstaver konverteres til deres nummer i alfabetet.",
    placeholder="Indtast de fundne tal",
    value=default_value['numbers_found']
)

coordinate_formula = st.text_input(
    label="Indtast formlen til at udregne koordinatet",
    placeholder="Nnn nn.nnn Ennn nn.nnn",
    value=default_value['coordinate_formula']
)

st.button("Beregn Gade")

if numbers_found and coordinate_formula:
    # Check coordinate formula
    coordinate_formula = gade.formula_cleanup(coordinate_formula)
    coordinate_formula_parts = gade.validate_coordinate_formula(coordinate_formula)
    if coordinate_formula_parts is None:
        st.warning('Koordinatformlen kunne ikke valideres.')
        st.stop()

    # Calculate numbers for Gade calculation
    all_numbers = gade.sort_numbers_found(numbers_found)

    # Display all numbers
    # DONE: Remove index when printing dataframe
    st.write('Alle tal til formlen')
    df = pd.DataFrame(data=[all_numbers.values()], columns=list(all_numbers.keys()))
    st.dataframe(df, hide_index=True)
    st.table(df)

    # TODO: Check if number of numbers match formula
    # Check if # numbers found matches pattern

    # Calculate coordinate using the numbers found
    result_coordinate = gade.calculate_coordinate(coordinate_formula_parts, all_numbers)

    # Done: Check if calculated coordinate is a valid coordinate (Nnn nn.nnn Ennn nn.nnn)
    result_is_coordinate = gps.is_coordinate(result_coordinate)
    if not result_is_coordinate:
        st.write('Beregningen giver ikke et koordinat')

    # Done: Standard format of result coordinate
    else:
        result_coordinate = gps.standardize_coordinate(result_coordinate)

    # Display result coordinate
    # TODO: Change font to default app font
    st.write('Beregnet koordinat')
    st.code(result_coordinate, language=None)
    #copy_button(result_coordinate, icon='st', tooltip="Kopier koordinat til udklipsholder", copied_label="Koordinat kopieret...")
    if not result_is_coordinate:
        st.stop()

    # TODO: Calculate checksum and reduced checksum
    st.write('Tværsummer')
    st.table(gps.coordinate_sum_of_digits(result_coordinate))

    # DONE: Show on map
    with st.expander("Vis på kort", icon=":material/map:"):
        if gps.is_coordinate(result_coordinate):
            folium_static(gps.show_on_map(result_coordinate, zoom=14))

#toolbox.toolbox_feedback()













