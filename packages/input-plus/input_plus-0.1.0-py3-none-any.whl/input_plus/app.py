import sys
import re
import msvcrt
from colorama import Back, Fore, Style
from datetime import datetime
from typing import Callable, Tuple
import Levenshtein
import hashlib

def input_plus(printer: Callable[[str], None], selector: Callable[[str], Tuple[bool, str]],
               validator: Callable[[str], bool] = None, special_actions: Callable[[bytes], None] = None) -> str:
    '''
    A function that allows for more advanced input handling than the built-in input function.

    Printer: A function that takes a string and prints it to the console.

    Selector: A function that takes a string and returns a tuple of a boolean and a string.
    The boolean indicates if the return string is valid, and the string is the value to return.

    Validator: A function that takes a string and returns a boolean indicating if the input is valid.

    Special Actions: A function that takes a byte and performs a special action based on the input.
    '''
    input_string = ''
    printer(input_string)
    while True:
        input_char = msvcrt.getwch() # Get the input character
        is_special_key = False

        # Special actions
        if input_char == '\x00' or input_char == '\xe0':
            is_special_key = True
            input_char += msvcrt.getwch()
        
        char_code = input_char.encode()
        # Control characters
        if char_code == b'\x03': # Ctrl+C
            print()
            sys.exit(1)

        elif char_code == b'\x0d': # Enter key
            is_valid, value = selector(input_string)
            if is_valid:
                print()
                return value
            
        elif char_code == b'\x08': # Backspace
            input_string = input_string[:-1]

        elif char_code == b'\x17': # Ctrl+Backspace
            input_string = re.sub(r'((?<=\s)|(?<=^))\w*\s?$', '', input_string)

        elif is_special_key: # Special keys
            if special_actions is not None:
                special_actions(char_code)

        else:
            if validator is None or validator(f'{input_string}{input_char}'):
                input_string += input_char

        printer(input_string)

def input_regex(prompt: str, regex: str, force_match: bool = False, warn_error: bool = True, placeholder: str = None) -> str:
    cursor_offset = 0
    print_string_length = 0

    # Printer function
    def _printer(input_string):
        nonlocal cursor_offset, print_string_length

        WARNING_COLOR = Fore.RED
        WARNING_RESET = Style.RESET_ALL
        CURSOR_BACK = '\b' # Move the cursor back one character
        CURSOR_FORWARD = '\x1b[C' # Move the cursor forward one character
        REMOVE_ANSI_ESCAPES = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

        # Move the cursor to the beginning of the line
        print(CURSOR_FORWARD * cursor_offset, end='', flush=True)
        cursor_offset = 0

        # Create the string to print
        print_string = input_string
        if not force_match and warn_error:
            # replace all matches with the warning color
            print_string = re.sub(regex, WARNING_RESET + r'\g<0>' + WARNING_COLOR, input_string)
            print_string = f'{WARNING_COLOR}{print_string}{WARNING_RESET}'

        # Add a placeholder if needed in gray
        if placeholder is not None:
            string_to_add = f'     {Fore.LIGHTBLACK_EX}{placeholder}{Style.RESET_ALL}'
            cursor_offset += len(REMOVE_ANSI_ESCAPES.sub('', string_to_add)) # remove ANSI escape codes
            print_string += string_to_add

        # Erase the previous input and print the new one
        erase = '\b' * print_string_length + ' ' * print_string_length + '\b' * print_string_length
        print_string_length = len(REMOVE_ANSI_ESCAPES.sub('', print_string)) # remove ANSI escape codes
        print(erase + print_string, end='', flush=True)

        # Move the cursor back to the correct position
        print(CURSOR_BACK * cursor_offset, end='', flush=True)

    def _selector(input_string):
        is_valid = re.fullmatch(regex, input_string) is not None
        return is_valid, input_string
    
    def _validator(input_string):
        if force_match:
            return re.fullmatch(regex, input_string) is not None
        return True
    
    print(prompt, end='', flush=True)
    return input_plus(_printer, _selector, validator=_validator)

def input_integer(prompt: str) -> int:
    value = input_regex(prompt, r'\-?\d*', force_match=True)
    if value == '' or value == '-':
        return 0        
    return int(value)

def input_float(prompt: str) -> float:
    value = input_regex(prompt, r'\-?\d*\.?\d*?', force_match=True)
    if value == '' or value == '-' or value == '.':
        return 0        
    return float(value)

def input_date(prompt: str, strptime_format = "%Y-%m-%d") -> datetime:
    format_mappings  = { # Mapping of strptime format to regex
        '%Y': {'regex': r'\d{4}', 'readable': 'YYYY'},
        '%m': {'regex': r'0[1-9]|1[0-2]', 'readable': 'MM'},
        '%d': {'regex': r'0[1-9]|[12]\d|3[01]', 'readable': 'DD'}
    }

    regex = re.escape(strptime_format)
    readable = strptime_format

    for strp_format, mapping in format_mappings .items():
        regex = regex.replace(re.escape(strp_format), f'({mapping['regex']})')
        readable = readable.replace(strp_format, mapping['readable'])

    result = input_regex(prompt, regex, force_match=False, warn_error=True, placeholder=readable)
    return datetime.strptime(result, strptime_format).date()

def input_select(prompt: str, options: list, list_size: int = 5) -> str:
    height = 0
    select_index = 0
    offset = 0

    def get_options_scores(input_string):
        # get the levenstein distance of each option
        option_scores = [{'option': option, 'score': Levenshtein.distance(input_string, option)} for option in options]
        # sort the options by score descending
        option_scores = sorted(option_scores, key=lambda x: x['score'])
        # get the top list_size options
        option_scores = option_scores[offset:list_size + offset]
        return option_scores

    def _printer(input_string):
        nonlocal height, list_size, select_index, offset

        MOVE_TO_START = '\r' # Move the cursor to the start of the line
        CURSOR_FORWARD = '\x1b[C' # Move the cursor forward one character
        CLEAR_LINE = '\033[J' # Clear the current line

        # store all text to print to remove flickering
        to_print = ''

        # Clear previous lines
        to_print += f'{MOVE_TO_START}{CLEAR_LINE}' * height

        to_print += f'{prompt}{input_string}\n'

        option_scores = get_options_scores(input_string)

        for i, option_score in enumerate(option_scores):
            temp_text = ''
            if i < len(option_scores) - 1:
                temp_text = f'  {option_score['option']}\n'
            else:
                temp_text = f'  {option_score['option']}'

            if i == select_index:
                temp_text = f'{Fore.GREEN}{temp_text}{Style.RESET_ALL}'

            to_print += temp_text
        
        height = len(option_scores)

        # Move cursor back to the beginning of the input
        to_print += f'\033[A' * height
        to_print += f'{MOVE_TO_START}{CURSOR_FORWARD * len(f'{prompt}{input_string}')}'

        print(to_print, end='', flush=True)

    def _selector(input_string):
        nonlocal height, select_index

        MOVE_TO_START = '\r' # Move the cursor to the start of the line
        CLEAR_LINE = '\033[J' # Clear the current line

        # store all text to print to remove flickering
        to_print = ''

        # Clear previous lines
        to_print += f'{MOVE_TO_START}{CLEAR_LINE}' * height
        to_print += MOVE_TO_START

        option_scores = get_options_scores(input_string)
        return_value = option_scores[select_index]['option']

        to_print += f'{prompt}{return_value}'

        print(to_print, end='', flush=True)
        return True, return_value

    def _special_actions(char_code):
        nonlocal select_index, offset

        if char_code == b'\x00H': # Up arrow
            select_index = max(0, select_index - 1)
            if select_index == 0 and offset > 0:
                offset = max(0, offset - 1)
                select_index = min(list_size - 1, select_index + 1)
        elif char_code == b'\x00P': # Down arrow
            select_index = min(list_size - 1, select_index + 1)
            if select_index == list_size - 1 and offset < len(options) - list_size:
                offset = min(len(options) - list_size, offset + 1)
                select_index = max(0, select_index - 1)

    return input_plus(_printer, _selector, special_actions=_special_actions)

def _input_password_default_hash(input_string):
    hash_object = hashlib.sha256()
    hash_object.update(input_string.encode())
    hex_digest = hash_object.hexdigest()
    return hex_digest
def input_password(prompt: str, mask: str = '', hash_function = _input_password_default_hash) -> str:
    # cursor_offset = 0
    print_string_length = 0

    def _printer(input_string):
        nonlocal print_string_length

        # Create the string to print
        print_string = mask * len(input_string)

        # Erase the previous input and print the new one
        erase = '\b' * print_string_length + ' ' * print_string_length + '\b' * print_string_length
        print_string_length = len(print_string) # remove ANSI escape codes
        print(erase + print_string, end='', flush=True)

    def _selector(input_string):
        return True, input_string

    print(prompt, end='', flush=True)
    password = input_plus(_printer, _selector)
    return hash_function(password)





