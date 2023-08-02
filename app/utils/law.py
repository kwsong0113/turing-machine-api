from enum import StrEnum, auto
from typing import List, Callable, Any, Union, Literal


def verify_single_compare(
    index: int, target: int, operator: Literal["==", ">", "<"], *digits: [int, int, int]
) -> bool:
    return eval(f"{digits[index]} {operator} {target}")


def verify_single_parity(index: int, is_even: bool, *digits: [int, int, int]) -> bool:
    return (digits[index] % 2 == 0) == is_even


def verify_count(target: int, num_count: int, *digits: [int, int, int]) -> bool:
    return digits.count(target) == num_count


def verify_sum(eval_string: str, *digits: [int, int, int]) -> bool:
    return eval(f"{sum(digits)} {eval_string}")


def verify_twin(has_twin: bool, *digits: [int, int, int]) -> bool:
    for num in range(1, 6):
        if digits.count(num) == 2:
            return has_twin
    return not has_twin


def verify_ascending(len_sequence: int, *digits: [int, int, int]) -> bool:
    return (
        1 + (digits[1] == digits[0] + 1) + (digits[2] == digits[1] + 1)
    ) == len_sequence


def verify_parity_count(eval_string: str, *digits: [int, int, int]) -> bool:
    return eval(f"{sum([digit % 2 == 0 for digit in digits])} {eval_string}")


def verify_two_compare(
    index_1: int,
    index_2: int,
    operator: Literal["==", ">", "<"],
    *digits: [int, int, int],
) -> bool:
    return eval(f"{digits[index_1]} {operator} {digits[index_2]}")


def verify_two_sum(
    index_1: int, index_2: int, eval_string: str, *digits: [int, int, int]
) -> bool:
    return eval(f"{digits[index_1] + digits[index_2]} {eval_string}")


def verify_rest_compare(
    index: int, operator: Literal[">=", "<=", ">", "<"], *digits: [int, int, int]
) -> bool:
    return all(
        eval(f"{digits[index]} {operator} {digit}")
        for idx, digit in enumerate(digits)
        if index != idx
    )


def verify_repeat(num_repeat: int, *digits: [int, int, int]) -> bool:
    max_repeat = 1
    for num in range(1, 6):
        max_repeat = max(digits.count(num), max_repeat)
    return max_repeat == num_repeat


def verify_sequence(len_sequence: int, *digits: [int, int, int]) -> bool:
    return (
        max(
            1 + (digits[1] == digits[0] + 1) + (digits[2] == digits[1] + 1),
            1 + (digits[0] == digits[1] + 1) + (digits[1] == digits[2] + 1),
        )
        == len_sequence
    )


def verify_order(
    order_type: Literal["ASCENDING", "DESCENDING", "NEITHER"], *digits: [int, int, int]
) -> bool:
    return (
        "ASCENDING"
        if digits[0] < digits[1] < digits[2]
        else ("DESCENDING" if digits[0] > digits[1] > digits[2] else "NEITHER")
    ) == order_type


def verify(law: int, proposal: int) -> bool:
    law_type, *rest_args = LAW_DICT[law]
    return VERIFIER_FN_GENERATOR_DICT[law_type](
        *rest_args, *[int(digit) for digit in str(proposal)]
    )


class LawType(StrEnum):
    SINGLE_COMPARE = auto()
    SINGLE_PARITY = auto()
    COUNT = auto()
    SUM = auto()
    TWIN = auto()
    ASCENDING = auto()
    PARITY_COUNT = auto()
    TWO_COMPARE = auto()
    TWO_SUM = auto()
    REST_COMPARE = auto()
    REPEAT = auto()
    SEQUENCE = auto()
    ORDER = auto()


VERIFIER_FN_GENERATOR_DICT: dict[LawType, Callable[[...], bool]] = {
    LawType.SINGLE_COMPARE: verify_single_compare,
    LawType.SINGLE_PARITY: verify_single_parity,
    LawType.COUNT: verify_count,
    LawType.SUM: verify_sum,
    LawType.TWIN: verify_twin,
    LawType.ASCENDING: verify_ascending,
    LawType.PARITY_COUNT: verify_parity_count,
    LawType.TWO_COMPARE: verify_two_compare,
    LawType.TWO_SUM: verify_two_sum,
    LawType.REST_COMPARE: verify_rest_compare,
    LawType.REPEAT: verify_repeat,
    LawType.SEQUENCE: verify_sequence,
    LawType.ORDER: verify_order,
}

LAW_DICT: dict[int, (LawType, ...)] = {
    1: (LawType.SINGLE_COMPARE, 0, 1, "=="),
    3: (LawType.SINGLE_COMPARE, 0, 3, "=="),
    4: (LawType.SINGLE_COMPARE, 0, 4, "=="),
    5: (LawType.SINGLE_COMPARE, 0, 5, "=="),
    6: (LawType.SINGLE_COMPARE, 0, 1, "=="),
    8: (LawType.SINGLE_COMPARE, 0, 3, "=="),
    9: (LawType.SINGLE_COMPARE, 0, 4, "=="),
    10: (LawType.SINGLE_COMPARE, 0, 5, "=="),
    11: (LawType.SINGLE_COMPARE, 0, 1, "=="),
    13: (LawType.SINGLE_COMPARE, 0, 3, "=="),
    14: (LawType.SINGLE_COMPARE, 0, 4, "=="),
    15: (LawType.SINGLE_COMPARE, 0, 5, "=="),
    16: (LawType.SINGLE_COMPARE, 0, 1, ">"),
    18: (LawType.SINGLE_COMPARE, 0, 3, ">"),
    19: (LawType.SINGLE_COMPARE, 1, 1, ">"),
    21: (LawType.SINGLE_COMPARE, 1, 3, ">"),
    22: (LawType.SINGLE_COMPARE, 2, 1, ">"),
    24: (LawType.SINGLE_COMPARE, 2, 3, ">"),
    25: (LawType.SINGLE_COMPARE, 0, 3, "<"),
    26: (LawType.SINGLE_COMPARE, 0, 4, "<"),
    28: (LawType.SINGLE_COMPARE, 1, 3, "<"),
    29: (LawType.SINGLE_COMPARE, 1, 4, "<"),
    31: (LawType.SINGLE_COMPARE, 2, 3, "<"),
    32: (LawType.SINGLE_COMPARE, 2, 4, "<"),
    34: (LawType.SINGLE_PARITY, 0, True),
    35: (LawType.SINGLE_PARITY, 1, True),
    36: (LawType.SINGLE_PARITY, 2, True),
    37: (LawType.SINGLE_PARITY, 0, False),
    38: (LawType.SINGLE_PARITY, 1, False),
    39: (LawType.SINGLE_PARITY, 2, False),
    40: (LawType.COUNT, 1, 0),
    41: (LawType.COUNT, 1, 1),
    42: (LawType.COUNT, 1, 2),
    46: (LawType.COUNT, 3, 0),
    47: (LawType.COUNT, 3, 1),
    48: (LawType.COUNT, 3, 2),
    49: (LawType.COUNT, 4, 0),
    50: (LawType.COUNT, 4, 1),
    51: (LawType.COUNT, 4, 2),
    55: (LawType.SUM, "% 2 == 0"),
    56: (LawType.SUM, "% 2 != 0"),
    57: (LawType.SUM, "% 3 == 0"),
    58: (LawType.SUM, "% 4 == 0"),
    59: (LawType.SUM, "% 5 == 0"),
    60: (LawType.SUM, "== 6"),
    67: (LawType.SUM, "> 6"),
    74: (LawType.SUM, "< 6"),
    81: (LawType.TWIN, False),
    82: (LawType.TWIN, True),
    83: (LawType.ASCENDING, 1),
    84: (LawType.ASCENDING, 2),
    85: (LawType.PARITY_COUNT, "== 0"),
    86: (LawType.PARITY_COUNT, "== 1"),
    87: (LawType.PARITY_COUNT, "== 2"),
    88: (LawType.PARITY_COUNT, "== 3"),
    89: (LawType.TWO_COMPARE, 0, 1, "=="),
    90: (LawType.TWO_COMPARE, 0, 2, "=="),
    91: (LawType.TWO_COMPARE, 1, 2, "=="),
    92: (LawType.TWO_COMPARE, 0, 1, ">"),
    93: (LawType.TWO_COMPARE, 0, 2, ">"),
    94: (LawType.TWO_COMPARE, 1, 0, ">"),
    95: (LawType.TWO_COMPARE, 1, 2, ">"),
    96: (LawType.TWO_COMPARE, 2, 0, ">"),
    97: (LawType.TWO_COMPARE, 2, 1, ">"),
    98: (LawType.TWO_SUM, 0, 1, "== 4"),
    100: (LawType.TWO_SUM, 0, 1, "== 6"),
    103: (LawType.TWO_SUM, 0, 2, "== 4"),
    105: (LawType.TWO_SUM, 0, 2, "== 6"),
    108: (LawType.TWO_SUM, 1, 2, "== 4"),
    110: (LawType.TWO_SUM, 1, 2, "== 6"),
    113: (LawType.REST_COMPARE, 0, ">"),
    114: (LawType.REST_COMPARE, 1, ">"),
    115: (LawType.REST_COMPARE, 2, ">"),
    116: (LawType.REST_COMPARE, 0, "<"),
    117: (LawType.REST_COMPARE, 1, "<"),
    118: (LawType.REST_COMPARE, 2, "<"),
    119: (LawType.REPEAT, 3),
    120: (LawType.REPEAT, 2),
    121: (LawType.REPEAT, 1),
    122: (LawType.SEQUENCE, 1),
    123: (LawType.SEQUENCE, 2),
    124: (LawType.SEQUENCE, 3),
    125: (LawType.REST_COMPARE, 0, ">="),
    126: (LawType.REST_COMPARE, 1, ">="),
    127: (LawType.REST_COMPARE, 2, ">="),
    128: (LawType.REST_COMPARE, 0, "<="),
    129: (LawType.REST_COMPARE, 1, "<="),
    130: (LawType.REST_COMPARE, 2, "<="),
    131: (LawType.PARITY_COUNT, ">= 2"),
    132: (LawType.PARITY_COUNT, "<= 1"),
    133: (LawType.ORDER, "ASCENDING"),
    134: (LawType.ORDER, "DESCENDING"),
    135: (LawType.ORDER, "NEITHER"),
    136: (LawType.TWO_SUM, 0, 1, "> 6"),
    137: (LawType.TWO_SUM, 0, 1, "< 6"),
    138: (LawType.SINGLE_COMPARE, 1, 4, ">"),
    139: (LawType.TWO_COMPARE, 0, 1, "<"),
    140: (LawType.TWO_COMPARE, 0, 2, "<"),
    141: (LawType.TWO_COMPARE, 1, 2, "<"),
    142: (LawType.SINGLE_COMPARE, 0, 4, ">"),
    143: (LawType.SINGLE_COMPARE, 2, 4, ">"),
    144: (LawType.TWO_COMPARE, 2, 1, "<"),
    145: (LawType.TWO_COMPARE, 2, 1, "=="),
}
