import string
import re


coordinate_pattern_regex: str = (r'([NSns])((?:[ ]*)(?:\([\wÆØÅæøå+\-\*\/\(\)]+\)|[\wÆØÅæøå]|\d){2,3}[° \.]+' +
                                 '(?:\([\wÆØÅæøå+\-\*\/\(\)]+\)|[\wÆØÅæøå]+|\d){2}\.(?:\([\wÆØÅæøå+\-\*\/\(\)]+\)|' +
                                 '[\wÆØÅæøå]+?|\d){3})([ ]+)([EWew])((?:[ ]*)(?:\([\wÆØÅæøå+\-\*\/\(\)]+\)|' +
                                 '[\wÆØÅæøå]|\d){2,3}[° \.]+(?:\([\wÆØÅæøå+\-\*\/\(\)]+\)|[\wÆØÅæøå]|\d){2}\.' +
                                 '(?:\([\wÆØÅæøå+\-\*\/\(\)]+\)|[\wÆØÅæøå]|\d){3})')


def formula_cleanup(coordinate_formula: str) -> str:
    return re.sub(r'^a-zæøåA-ZÆØÅ\.\d \(\)+\-*\/]', '', coordinate_formula).upper()


def validate_coordinate_formula(coordinate_formula: str) -> list | None:
    try:
        formula_parts = list(re.findall(coordinate_pattern_regex, coordinate_formula)[0])
    except IndexError as e:
        # print(repr(sys.exception()))
        print(type(e), e)
        return None

    if len(formula_parts) == 0:
        return None
    else:
        return formula_parts


def clean_numbers_found(found: str) -> str:
    found = "".join([c for c in found if c not in (" ", "|", "\t", ".", ",")])
    return found


def char_2_number(found: str) -> str:
    result = ""
    special_chars = ('Æ', 'Ø', 'Å')
    for c in found:
        if c.isalpha():
            if c in special_chars:
                result += str(27+special_chars.index(c))
            else:
                result += str(ord(c)-64)
        else:
            result += c
    return result


def sort_numbers_found(numbers_found: str) -> dict:
    numbers = list(char_2_number(clean_numbers_found(numbers_found).upper()))
    numbers.sort()
    for n in range(10):
        if str(n) not in numbers:
            numbers.append(str(n))
    keys = list(string.ascii_uppercase + 'ÆØÅ')
    return {keys[i]: numbers[i] for i in range(min(len(keys), len(numbers)))}


def substitute_numbers(coordinate_formula_parts: list, all_numbers: dict) -> list:
    for part_no in (1, 4):
        for letter in all_numbers:
            if letter in coordinate_formula_parts[part_no]:
                coordinate_formula_parts[part_no] = coordinate_formula_parts[part_no].replace(letter, all_numbers[letter])
    return coordinate_formula_parts


def calculation_parser(expr: str) -> list:
    items = []
    item = ''
    level = 0
    for c in expr:
        match c:
            case '(':
                if level == 0:
                    items.append(item)
                    item = ''
                level = level+1
                item = item+c
            case ')':
                level = level-1
                item = item+c
                if level == 0:
                    items.append(item)
                    item = ''
            case _:
                item = item + c
    items.append(item)
    return items


def resolve_calculations(coordinate_formula_parts: list) -> str:
    for part in coordinate_formula_parts:
        if not re.search(r'[+\-\*\/]', part) is None:
            calculations = calculation_parser(part)
            for calculation in calculations:
                result = ''
                if not re.search(r'[+\-\*\/]', calculation) is None:
                    result = str(eval(calculation))
                    calculations = list(map(lambda x: x.replace(calculation, result), calculations))

            coordinate_formula_parts = list(map(lambda x: x.replace(part, ''.join(calculations)), coordinate_formula_parts))
    return ''.join(coordinate_formula_parts)
