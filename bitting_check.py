#!/usr/bin/env python3
""" Module with tools to assess security of a locks key bitting.  Can provide
alternative bittings that will work for a given lock, or can list how many
of a locks total combinations use bittings which are unique in that no
alternative bitting exists.
"""

DIGITS = '0123456789'

def convert_to_base(decimal_number, base):
    """ Function to convert from an int to a new base.  Values represented by
    DIGITS constant.
    """
    remainder_stack = []
    while decimal_number > 0:
        remainder = decimal_number % base
        remainder_stack.append(remainder)
        decimal_number = decimal_number // base
    new_digits = []
    while remainder_stack:
        new_digits.append(DIGITS[remainder_stack.pop()])
    return ''.join(new_digits)

def check_key(correct_bitting, alternate_bitting):
    """ Function to check if the alternate bitting could be used to open the
    correct bitting when applying rotational force and removing the key.
    """
    alternate_bitting = [int(digit) for digit in alternate_bitting]
    num_pins = len(alternate_bitting)
    pin_set = [0] * num_pins
    if max(correct_bitting) > max(alternate_bitting):
        return False
    for shift in range(num_pins):
        for pin in range(shift, num_pins):
            if alternate_bitting[pin-shift] < correct_bitting[pin]:
                # Overset
                return False
            if alternate_bitting[pin-shift] == correct_bitting[pin]:
                pin_set[pin] = 1
        if all(pin_set):
            return True
    return False

def find_alternates(bitting, possible_cuts):
    """ Generator yields all possible alternate bittings that could open the
    bitting provided for a given number of possible cuts allowed for that lock.
    """
    num_pins = len(bitting)
    total_combinations = possible_cuts**num_pins
    str_key_bitting = [str(i) for i in bitting]
    string_bitting = int("".join(str_key_bitting),possible_cuts)
    for i in range(string_bitting+1, total_combinations):
        alternate_bitting = convert_to_base(i, possible_cuts)
        alternate_bitting = alternate_bitting.zfill(num_pins)
        if check_key(bitting, alternate_bitting):
            yield alternate_bitting

def get_total_unique(number_pins, number_cuts):
    """ Function returns total number of bittings which are unique in that no
    alternative bitting exists that could also open the lock.
    """
    total_combinations = number_cuts**number_pins
    bitting_with_alternates = 0
    for j in range(total_combinations):
        bitting = convert_to_base(j, number_cuts)
        str_bitting = bitting.zfill(number_pins)
        bitting = [int(l) for l in str_bitting]
        for i in range(total_combinations):
            alternate_bitting = convert_to_base(i, number_cuts)
            alternate_bitting = alternate_bitting.zfill(number_pins)
            if str_bitting != alternate_bitting:
                if check_key(bitting, alternate_bitting):
                    bitting_with_alternates +=1
                    break
    return total_combinations - bitting_with_alternates


# Example looking at a single key bitting
# Key bitting, going left to right, corresponds to key tip to bow
# Counting starts at 0, as in 0 is considered a cut,
# So three cuts would be numbered 0,1,2 and not 1,2,3
KEY_BITTING = [1,1,1,1,3] # Corresponds to a Schlage key bitting of 22224
SCHLAGE_CUTS = 9
RESULTS = list(find_alternates(KEY_BITTING, SCHLAGE_CUTS))
print("Alternates: ", RESULTS)
print("Number of alternates: ", len(RESULTS))
TOTAL_COMBINATIONS = SCHLAGE_CUTS**len(KEY_BITTING)
print("Likelihood user will have duplicate: ", len(RESULTS)/TOTAL_COMBINATIONS*100)

# Example to get statistics on a lock with a certain number of cuts and pins
NUMBER_CUTS = 3
NUMBER_PINS = 3
TOTAL_COMBINATIONS = NUMBER_CUTS**NUMBER_PINS
UNIQUE_COMBINATIONS = get_total_unique(NUMBER_PINS, NUMBER_CUTS)
print("Total combinations: ", TOTAL_COMBINATIONS)
DUPLICATES = TOTAL_COMBINATIONS-UNIQUE_COMBINATIONS
print("Bitting with Duplicates: ", DUPLICATES)
print("Percent with Duplicates: ", DUPLICATES/TOTAL_COMBINATIONS*100)
