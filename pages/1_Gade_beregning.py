import streamlit as st
from modules import gade
from modules import toolbox
from modules import gpscoordinates as gps
import pandas as pd
from streamlit_folium import st_folium

# DONE: Handle regex matching returning an error - try
# TODO: GitHub bug reporting

toolbox.toolbox_header("Beregn Gade")

numbers_found = st.text_input(
    label="Indtast de fundne tal. Bogstaver konverteres til deres nummer i alfabetet.",
    placeholder="Indtast de fundne tal",
    # value="1535114"
)

coordinate_formula = st.text_input(
    label="Indtast formlen til at udregne koordinatet",
    placeholder="Nnn nn.nnn Ennn nn.nnn",
    # value="N 55.38.(1*(J+A))EI E 012 16.JEK"
    # value="D 55 38.JEI E 012 16.JEK"
)

st.button("Beregn Gade")

if numbers_found and coordinate_formula:
    # Check coordinate formula
    coordinate_formula = gade.formula_cleanup(coordinate_formula)
    coordinate_formula_parts = gade.validate_coordinate_formula(coordinate_formula)
    if coordinate_formula_parts is None:
        st.write('Koordinatformlen kunne ikke valideres.')
        exit()

    # Calculate numbers for Gade calculation
    all_numbers = gade.sort_numbers_found(numbers_found)

    # Display all numbers
    # DONE: Remove index when printing dataframe
    st.write('Alle tal til formlen')
    df = pd.DataFrame(data=[all_numbers.values()], columns=all_numbers.keys())
    st.dataframe(df, hide_index=True)

    # TODO: Check if number of numbers match formula
    # Check if # numbers found matches pattern

    # Substitute numbers in coordinate formula
    result_coordinate_parts = gade.substitute_numbers(coordinate_formula_parts, all_numbers)

    # Resolve formula elements containing calculations
    result_coordinate = gade.resolve_calculations(coordinate_formula_parts)

    # Done: Check if calculated coordinate is a valid coordinate (Ndd dd.ddd Eddd dd.ddd)
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

    # TODO: Calculate checksum and reduced checksum

    # DONE: Show on map
    # if gps.is_coordinate(result_coordinate):
    #     st_data = st_folium(gps.show_on_map(result_coordinate, zoom=14))
