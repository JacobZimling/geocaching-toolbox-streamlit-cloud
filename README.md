# PihlZimling's Geocaching Toolbox

This is the Streamlit Cloud repository for the PihlZimling Geocaching Toolbox.

## Current tools in the toolbox

### Gade calculation

Gade is a calculation method invented by the geocacher of the same name, to calculate a final coordinate based on the collected digits as described in the cache description by means of a formula that can be revealed beforehand. The major advantage is that the formula is very simple to construct, since there will be at least one variable containing each digit (including zero). 

The tool in this toolbox helps you calculate the resulting coordinate. You need only to enter the numbers/text found and the formula - the result will be calculated for you. The formula can often be copied from the cache listing.

If you enter characters, they will be substituted with their numeric value in the alphabet (a=1, b=2, ... z=26, æ=27, ø=28, å=29).

The formula consist of a text containing a number of variables that are to be substituted with their values.

The method is fairly simple. The digits in the answer are sorted, any  missing digits are added to the list and each of them is assigned to a variable named A, B, C....

The solution is calculated by substituting the variables in the formula with their value and displayed alongside the variable-value mapping. Beside this the sum of digits of the calculated coordinate is displayed and the coordinate is shown on a map.  

[Example of Gade calculation in multiple languages](Gade_calculation.md)

## Planned tools

### Word value calculation

Calculating the word value by converting the letters to their position in the alphabet including the special danish characters 'Æ', 'Ø' and 'Å'. 

### Sum of digits for coordinate

### Coordinate calculation
