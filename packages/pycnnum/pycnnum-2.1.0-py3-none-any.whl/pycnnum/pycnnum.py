# pylint: disable=line-too-long
"""Chinese number <=> int/float conversion """

from __future__ import annotations

import copy
import re
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from math import log2
from typing import Callable, List, Optional, Tuple, Union

from .constants import DIGITS, UNITS


class NumberingType(Enum):
    r"""Numbering system types: LOW, MID, HIGH

    Chinese numbering types:

    For $i \in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]$:


    - `LOW`  : $10^{8 + i}$
    - `MID`  : $10^{8 + i*4}$
    - `HIGH` : $10^{2^{i+3}}$

    ---

    | type  |  亿     | 兆      | 京      | 垓       | 秭       | 穰       | 沟       | 涧        | 正        | 载         |
    |-------| --------|---------|---------|---------|----------|----------|----------|-----------|-----------|-----------|
    |`low`  | $10^{8}$|$10^{9}$ |$10^{10}$|$10^{11}$|$10^{12}$ |$10^{13}$ |$10^{14}$ |$10^{15}$  |$10^{16}$  |$10^{17}$  |
    |`mid`  | $10^{8}$|$10^{12}$|$10^{16}$|$10^{20}$|$10^{24}$ |$10^{28}$ |$10^{32}$ |$10^{36}$  |$10^{40}$  |$10^{44}$  |
    |`high` | $10^{8}$|$10^{16}$|$10^{32}$|$10^{64}$|$10^{128}$|$10^{256}$|$10^{512}$|$10^{1024}$|$10^{2048}$|$10^{4096}$|
    """

    LOW = "low"
    """
        | type  |  亿     | 兆      | 京      | 垓       | 秭       | 穰       | 沟       | 涧        | 正        | 载         |
        |-------| --------|---------|---------|---------|----------|----------|----------|-----------|-----------|-----------|
        |`low`  | $10^{8}$|$10^{9}$ |$10^{10}$|$10^{11}$|$10^{12}$ |$10^{13}$ |$10^{14}$ |$10^{15}$  |$10^{16}$  |$10^{17}$  |
    """

    MID = "mid"
    """
        | type  |  亿     | 兆      | 京      | 垓       | 秭       | 穰       | 沟       | 涧        | 正        | 载         |
        |-------| --------|---------|---------|---------|----------|----------|----------|-----------|-----------|-----------|
        |`mid`  | $10^{8}$|$10^{12}$|$10^{16}$|$10^{20}$|$10^{24}$ |$10^{28}$ |$10^{32}$ |$10^{36}$  |$10^{40}$  |$10^{44}$  |
    """

    HIGH = "high"
    """
        | type  |  亿     | 兆      | 京      | 垓       | 秭       | 穰       | 沟       | 涧        | 正        | 载         |
        |-------| --------|---------|---------|---------|----------|----------|----------|-----------|-----------|-----------|
        |`high` | $10^{8}$|$10^{16}$|$10^{32}$|$10^{64}$|$10^{128}$|$10^{256}$|$10^{512}$|$10^{1024}$|$10^{2048}$|$10^{4096}$|
    """

    @property
    def powers(self) -> List[int]:
        """Powers of units for each numbering type"""
        return {
            NumberingType.LOW: [8 + i for i in range(10)],
            NumberingType.MID: [8 + 4 * i for i in range(10)],
            NumberingType.HIGH: [2 ** (i + 3) for i in range(10)],
        }[self]


# region char classes
@dataclass
class CNChar:
    """Base Chinese char class.

    Each object has simplified and traditional strings.
    When converted to string, it will shows the simplified string or traditional string or space `' '`.

    Example:
    ```python

    >>> negative = CNChar(simplified="负", traditional="負")
    >>> negative.simplified
    '负'
    >>> negative.traditional
    '負'
    >>> negative.upper_simplified
    '负'
    >>> negative.upper_traditional
    '負'

    ```
    """

    simplified: Optional[str] = None
    """Simplified Chinese character"""

    traditional: Optional[str] = None
    """Traditional Chinese character"""

    upper_simplified: Optional[str] = None
    """Capitalized character in simplified Chinese. Defaults to `None` means same as `self.simplified`."""

    upper_traditional: Optional[str] = None
    """Capitalized character in traditional Chinese. Defaults to `None` means same as `self.traditional`."""

    @property
    def all_forms(self) -> str:
        """All forms of the character"""
        return "".join(v for v in self.__dict__.values() if isinstance(v, str))

    def __post_init__(self):
        """Post initialization"""
        self.simplified = self.simplified or ""
        self.traditional = self.traditional or self.simplified
        self.upper_simplified = self.upper_simplified or self.simplified
        self.upper_traditional = self.upper_traditional or self.traditional

    def __str__(self) -> str:
        return self.simplified if self.simplified else f"Empty {self.__class__.__name__}"

    def __repr__(self) -> str:
        return str(self)


@dataclass
class CNUnit(CNChar):
    """Chinese number unit class

    Each of it is an `CNChar` with additional upper type strings.

    Example:
    ```python

    >>> wan = CNUnit(*"万萬萬萬", power=4)
    >>> wan
    10^4

    ```
    """

    power: int = 0
    r"""The power of this unit, e.g. `power` = 4 for `'万'` ( \(10^4\) )"""

    def __str__(self) -> str:
        return f"10^{self.power}"

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def create(cls, power: int, numbering_type: NumberingType = NumberingType.MID) -> CNUnit:
        """Create one unit character based on power value from constants

        - `SMALLER_CHINESE_NUMBERING_UNITS_SIMPLIFIED`
        - `SMALLER_CHINESE_NUMBERING_UNITS_TRADITIONAL`
        - `LARGER_CHINESE_NUMBERING_UNITS_SIMPLIFIED`
        - `LARGER_CHINESE_NUMBERING_UNITS_TRADITIONAL`

        Example:
        ```python

        >>> CNUnit.create(power=8, numbering_type=NumberingType.LOW).simplified
        '亿'
        >>> CNUnit.create(power=12, numbering_type=NumberingType.LOW).simplified
        '秭'
        >>> CNUnit.create(power=12, numbering_type=NumberingType.HIGH).simplified
        Traceback (most recent call last):
        ...
        ValueError: power = 12 is invalid for numbering_type = <NumberingType.HIGH: 'high'>

        ```

        Args:
            power (int): Unit power, starting from 1.
            numbering_type (NumberingType, optional): Numbering type. Defaults to `NumberingType.MID`.

        Raises:
            ValueError: Raised when invalid `numbering_type` is provided

        Returns:
            CNUnit: Created unit object
        """
        assert power > 0, "Power should be greater than 0."

        if power < 5:
            return cls(*UNITS[power - 1], power=power)  # type: ignore[misc]

        i = float(power - 8)
        if numbering_type == NumberingType.LOW:
            pass
        elif numbering_type == NumberingType.MID:
            i = i / 4
        elif numbering_type == NumberingType.HIGH:
            i = log2(power) - 3
        else:
            raise ValueError(f"Numbering type should be in {NumberingType} but {numbering_type} is provided.")

        i = int(i) if i.is_integer() else -1

        if i < 0:
            raise ValueError(f"{power = } is invalid for {numbering_type = }")

        return cls(*UNITS[i + 4], power=power)  # type: ignore[misc]


@dataclass
class CNDigit(CNChar):
    """Chinese number digit class

    Example:
    ```python

    >>> CNDigit(*"三叁叁叁", int_value=3)
    3

    ```
    """

    int_value: int = 0
    """Integer value of the digit, 0 to 9. Defaults to 0."""

    alt_s: Optional[str] = None
    """Alternative simplified character, e.g. '两' for 2. Defaults to `None`.
    """

    alt_t: Optional[str] = None
    """Alternative traditional character, e.g. '俩' for 2. Defaults to `None`.
    """

    def __str__(self):
        return str(self.int_value)

    def __repr__(self):
        return str(self)


@dataclass
class CNMath(CNChar):
    """
    Chinese math operators

    Example:
    ```python

    >>> positive = CNMath(*"正正正正", symbol="+", expression=lambda x: +x)
    >>> positive.symbol
    '+'

    ```
    """

    symbol: str = ""
    """Mathematical symbol, e.g. '+'. Defaults to ``."""

    expression: Optional[Callable] = None
    """Mathematical expression, e.g. `lambda x: +x`. Defaults to `None`."""

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return str(self)


SymbolType = Union[CNUnit, CNDigit, CNMath]


@dataclass
class MathSymbols:
    """Math symbols used in Chinese for both traditional and simplified Chinese

    - positive = ['正', '正']
    - negative = ['负', '負']
    - point = ['点', '點']

    Used in `NumberingSystem`.

    Example:
    ```python

    >>> positive = CNMath(*"正正正正", symbol="+", expression=lambda x: +x)
    >>> negative = CNMath(*"负負负負", symbol="-", expression=lambda x: -x)
    >>> point = CNMath(*"点點点點", symbol=".", expression=lambda integer, decimal: float(str(integer) + "." + str(decimal)))
    >>> math = MathSymbols(positive, negative, point)
    >>> math.positive
    +
    >>> list(math)
    [+, -, .]
    >>> for i in math:
    ...     print(i)
    +
    -
    .

    ```
    """

    positive: CNMath
    """Positive"""

    negative: CNMath
    """Negative"""

    point: CNMath
    """Decimal point"""

    def __iter__(self):
        for v in self.__dict__.values():
            yield v


class NumberingSystem:
    """Numbering system class

    Example:
    ```python

    >>> system = NumberingSystem(NumberingType.MID)
    >>> system.numbering_type
    <NumberingType.MID: 'mid'>
    >>> system.digits[0]
    0
    >>> system.units[0]
    10^1
    >>> system.units[7].simplified
    '垓'
    >>> system.math.positive
    +

    ```
    """

    # region: fields
    _numbering_type: NumberingType
    """Numbering type"""

    _digits: List[CNDigit]
    """Digits"""

    _units: List[CNUnit]
    """Units"""

    _maths: MathSymbols
    """Math symbols"""

    @property
    def numbering_type(self) -> NumberingType:
        """Numbering type"""
        return self._numbering_type

    @numbering_type.setter
    def numbering_type(self, value: NumberingType):
        self._numbering_type = value
        self._units[4:] = [CNUnit.create(i, self._numbering_type) for i in self._numbering_type.powers]

    @property
    def digits(self) -> List[CNDigit]:
        """Digits"""
        result = [CNDigit(*v, int_value=i) for i, v in enumerate(DIGITS)]  # type: ignore[misc]
        result[0].alt_s, result[0].alt_t = "〇", "〇"
        result[2].alt_s, result[2].alt_t = "两", "兩"
        return result

    @property
    def units(self) -> List[CNUnit]:
        """Units"""
        return self._units

    @cached_property
    def math(self) -> MathSymbols:
        """Math symbols"""
        positive_cn = CNMath(*"正正", symbol="+", expression=lambda x: x)  # type: ignore[misc]
        negative_cn = CNMath(*"负負", symbol="-", expression=lambda x: -x)  # type: ignore[misc]
        point_cn = CNMath(*"点點", symbol=".", expression=lambda i, d: float(f"{i}.{d}"))  # type: ignore[misc]
        return MathSymbols(positive_cn, negative_cn, point_cn)

    # endregion: fields

    def __init__(self, numbering_type: NumberingType = NumberingType.MID) -> None:
        """Construction"""
        self._numbering_type = numbering_type
        self._units = [CNUnit(*UNITS[i], power=i + 1) for i in range(4)]  # type: ignore[misc]
        self._units[4:] = [CNUnit.create(i, self._numbering_type) for i in self._numbering_type.powers]

    def __getitem__(self, key: str) -> SymbolType:
        if not isinstance(key, str):
            raise ValueError(f"{key = } should be a string.")

        for c in self.units + self.digits + list(self.math):
            if key in c.all_forms:
                return c

        raise ValueError(f"{key} is not in {self.numbering_type.name} system.")

    def cn2symbols(self, cn_str: str) -> Tuple[List[SymbolType], List[SymbolType]]:
        """Chinese string to symbols

        Example:
        ```python

        >>> system = NumberingSystem(NumberingType.MID)
        >>> system.cn2symbols("一百八")
        ([1, 10^2, 8], [])
        >>> system.cn2symbols("一百八十")
        ([1, 10^2, 8, 10^1], [])
        >>> system.cn2symbols("一百八点五六七")
        ([1, 10^2, 8], [5, 6, 7])
        >>> system.cn2symbols("两千万一百八十")
        ([2, 10^7, 1, 10^2, 8, 10^1], [])
        >>> system.cn2symbols("正两千万一百八十")
        ([+, 2, 10^7, 1, 10^2, 8, 10^1], [])
        >>> system.cn2symbols("负两千万一百八十")
        ([-, 2, 10^7, 1, 10^2, 8, 10^1], [])
        >>> system.cn2symbols("点负两千万一百八十")
        Traceback (most recent call last):
        ...
        ValueError: First symbol in decimal part should not be a math symbol, - is provided.
        >>> system.cn2symbols("两千万点一百点八十")
        Traceback (most recent call last):
        ...
        ValueError: Multiple points in the number 两千万点一百点八十.
        >>> system.cn2symbols("两千万点一百點八十")
        Traceback (most recent call last):
        ...
        ValueError: Multiple points in the number 两千万点一百點八十.

        ```

        Args:
            cn_str (str): Chinese number

        Returns:
            Tuple[List[SymbolType], List[SymbolType]]: Integer symbols, decimal symbols
        """
        if cn_str == "":
            return [], []

        int_part, dec_part = cn_str, ""
        int_dec = re.split(r"\.|点|點", cn_str)
        if len(int_dec) > 2:
            raise ValueError(f"Multiple points in the number {cn_str}.")
        int_part, dec_part = int_dec if len(int_dec) == 2 else (int_dec[0], "")

        integer_value = [copy.deepcopy(self[c]) for c in int_part]

        for i, v in enumerate(integer_value):
            if not isinstance(v, CNUnit):
                continue
            if i + 1 < len(integer_value) and isinstance(integer_value[i + 1], CNUnit):
                v.power += integer_value[i + 1].power  # type: ignore[union-attr]
                integer_value[i + 1] = None  # type: ignore[union-attr]

        integer_value = [v for v in integer_value if v is not None]

        for i, v in enumerate(integer_value):
            if not isinstance(v, CNUnit):
                continue
            for u in integer_value[i + 1 :]:
                if isinstance(u, CNUnit) and u.power > v.power:
                    v.power += u.power
                    break

        decimal_value = [copy.deepcopy(self[c]) for c in dec_part]

        # if first symbol is a math symbol, e.g. '正两千万一百八十'
        if int_part and (first_symbol := [c for c in self.math if int_part[0] in c.all_forms]):
            integer_value[0] = first_symbol[0]

        # if first symbol is a math symbol, e.g. '点负两千万一百八十'
        if decimal_value and (decimal_value[0] in self.math):
            raise ValueError(
                f"First symbol in decimal part should not be a math symbol, {decimal_value[0]} is provided."
            )

        return integer_value, decimal_value

    def _refine_integer_symbols(self, integer_symbols: List[SymbolType]) -> List[SymbolType]:
        """Refine integer symbols. Do not change math symbols.

        Example:
        ```python

        >>> s = NumberingSystem(NumberingType.MID)
        >>> s._refine_integer_symbols(s.cn2symbols("十八")[0])
        [1, 10^1, 8, 10^0]
        >>> s._refine_integer_symbols(s.cn2symbols("两千万一百八十")[0])
        [2, 10^7, 1, 10^2, 8, 10^1]
        >>> s._refine_integer_symbols(s.cn2symbols("两千万零一百八十")[0])
        [2, 10^7, 1, 10^2, 8, 10^1]
        >>> s._refine_integer_symbols(s.cn2symbols("两亿六")[0])
        [2, 10^8, 6, 10^7]

        ```

        Args:
            integer_symbols (List[SymbolType]): Raw integer symbols

        Returns:
            List[SymbolType]: Refined symbols
        """
        if not integer_symbols:
            return integer_symbols

        # first symbol is unit, add 1 before it, e.g. , "十五" to "一十五"
        if isinstance(integer_symbols[0], CNUnit) and integer_symbols[0].power == 1:
            integer_symbols = [self.digits[1]] + integer_symbols

        # last symbol is digit and the second last symbol is unit
        # e.g. "十 五" to "十 五 10^0",  "二 百 五" to "二 百 五 10^1"
        if len(integer_symbols) > 1:
            if isinstance(integer_symbols[-1], CNDigit) and isinstance(integer_symbols[-2], CNUnit):
                # add a dummy unit
                integer_symbols += [CNUnit(power=integer_symbols[-2].power - 1)]

        result: List[SymbolType] = []
        unit_count = 0
        for s in integer_symbols:
            if isinstance(s, CNMath):
                # reset unit_count, e.g. "两千万" has two units
                unit_count = 0
                continue
            if isinstance(s, CNDigit):
                # reset unit_count, e.g. "两千万" has two units
                unit_count = 0
                if s.int_value > 0:
                    result.append(s)
                continue
            if not isinstance(s, CNUnit):
                raise ValueError(f"Invalid symbol {s} in {integer_symbols}.")

            # create a dummy unit
            current_unit = CNUnit("", "", "", "", s.power)
            unit_count += 1

            # store the first met unit
            if unit_count == 1:
                result.append(current_unit)
                continue

            # if there are more than one units, sum them, e.g. "两 千 万" to "两 10^7"
            result[-1].power += current_unit.power  # type: ignore[union-attr]
        if integer_symbols[0] == self.math.negative:
            result = [self.math.negative] + result
        return result

    def get_int_value(self, integer_symbols: List[SymbolType]) -> int:
        """Compute the value from symbol

        Example:
        ```python

        >>> s = NumberingSystem(NumberingType.MID)
        >>> s.get_int_value(s.cn2symbols("十八")[0])
        18
        >>> s.get_int_value(s.cn2symbols("两千万一百八十")[0])
        20000180
        >>> s.get_int_value(s.cn2symbols("两亿六")[0])
        260000000

        ```

        Args:
            integer_symbols (List[SymbolType]): Symbols, without point

        Returns:
            int: value
        """
        integer_symbols = self._refine_integer_symbols(integer_symbols)

        value = [0]
        last_power = 0
        for s in integer_symbols:
            if isinstance(s, CNDigit):
                value[-1] = s.int_value
            elif isinstance(s, CNUnit):
                value[-1] *= pow(10, s.power)
                if s.power > last_power:
                    value[:-1] = [v * pow(10, s.power) for v in value[:-1]]  # pylint: disable=no-member
                    last_power = s.power
                value.append(0)
        return sum(value)

    def int2symbols(self, int_value: Union[int, str]) -> List[SymbolType]:
        """Integer to symbols

        Example:
        ```python

        >>> s = NumberingSystem(NumberingType.MID)
        >>> s.int2symbols(18)
        [1, 10^1, 8]
        >>> s.int2symbols(20000180)
        [2, 10^3, 10^4, 0, 1, 10^2, 8, 10^1]
        >>> s.int2symbols(26)
        [2, 10^1, 6]
        >>> s.int2symbols(320)
        [3, 10^2, 2, 10^1]
        >>> s.int2symbols(220)
        [2, 10^2, 2, 10^1]
        >>> s.int2symbols("220")
        [2, 10^2, 2, 10^1]

        ```

        Args:
            int_value (Union[int, str]): Value string, e.g. "0.1", "34"

        Returns:
            List[SymbolType]: List of values
        """
        value_string = str(int_value)
        striped_string = value_string.lstrip("0")

        # record nothing if all zeros
        if not striped_string:
            return []

        # record one digits
        if len(striped_string) == 1:
            result: List[SymbolType] = [self.digits[int(striped_string)]]
            if len(value_string) != len(striped_string):
                result = [self.digits[0] for _ in range(len(value_string) - len(striped_string))] + result
            return result

        # recursively record multiple digits

        # find the unit for the first digit, e.g. 123 -> 10^2
        result_unit = next(u for u in reversed(self.units) if u.power < len(striped_string))

        # get the first part of the number, e.g. 123 -> 1
        result_string = value_string[: -result_unit.power]

        # recursively record the first part of the number, e.g. 123 -> [1, 10^2, 2, 10^1, 3]
        return self.int2symbols(result_string) + [result_unit] + self.int2symbols(striped_string[-result_unit.power :])

    def alt_two_symbols(self, integer_symbols: List[SymbolType]) -> List[SymbolType]:
        """Alternative two symbols
        e.g. "二百二" to "两百二", "二千二" to "两千二", "三亿零二万二" to "三亿零两万二

        Args:
            integer_symbols (List[SymbolType]): Symbols

        Returns:
            List[SymbolType]: Symbols
        """
        liang = self.digits[2]
        for i, v in enumerate(integer_symbols):
            if not isinstance(v, CNDigit):
                continue
            if v.int_value != 2:
                continue
            next_symbol = integer_symbols[i + 1] if i < len(integer_symbols) - 1 else None
            previous_symbol = integer_symbols[i - 1] if i > 0 else None

            # if the next symbol is not a unit, skip
            if not isinstance(next_symbol, CNUnit):
                continue

            # e.g. "一亿零二百" leading_zero = True
            leading_zero = getattr(previous_symbol, "int_value", "invalid") == 0  # False == 0 in Python

            # e.g. "二百二" to "两百二"
            previous_is_unit = isinstance(previous_symbol, CNUnit)

            if not (leading_zero or previous_is_unit or (previous_symbol is None)):
                continue

            # e.g. "二百二" to "两百二", "二千二" to "两千二"
            if next_symbol.power > 1:
                integer_symbols[i].simplified = liang.alt_s
                integer_symbols[i].traditional = liang.alt_t
                integer_symbols[i].upper_simplified = liang.alt_s
                integer_symbols[i].upper_traditional = liang.alt_t
        return integer_symbols


def cn2num(
    chinese_string: str,
    numbering_type: Union[str, NumberingType] = NumberingType.MID,
) -> Union[int, float]:
    """Convert Chinese number to `int` or `float` value。

    Example:
    ```python

    >>> cn2num("负零点五")
    -0.5
    >>> cn2num("一百八")
    180
    >>> cn2num("一百八十")
    180
    >>> cn2num("一百八点五六七")
    180.567
    >>> cn2num("两千万一百八十")
    20000180
    >>> cn2num("正两千万一百八十")
    20000180

    ```

    Args:
        chinese_string (str): Chinese number.
        numbering_type (Union[str, NumberingType], optional): numbering type. Defaults to `NumberingType.MID`.

    Raises:
        ValueError: Raised when a character is not in the numbering system, e.g. '你' is not a number nor a unit

    Returns:
        Union[int, float]: `int` or `float` value
    """

    numbering_type = NumberingType(numbering_type) if isinstance(numbering_type, str) else numbering_type

    system = NumberingSystem(numbering_type)
    int_part, dec_part = system.cn2symbols(chinese_string)
    int_value = system.get_int_value(int_part)

    # skip unit in decimal value
    dec_str = "".join([str(d.int_value) for d in dec_part if isinstance(d, CNDigit)])

    result = float(f"{int_value}.{dec_str}") if dec_part else int_value
    if int_part and int_part[0] == system.math.negative:
        result = -result
    return result


# pylint: disable-next=too-many-arguments
def num2cn(
    num: Union[int, float, str],
    numbering_type: Union[str, NumberingType] = NumberingType.MID,
    upper: bool = False,
    traditional: bool = False,
    alt_0: bool = False,
    alt_2: bool = False,
) -> str:
    """Integer or float value to Chinese string

    Example:
    ```python

    >>> num2cn(16)
    '十六'
    >>> num2cn(1)
    '一'
    >>> num2cn(116)
    '一百一十六'
    >>> num2cn(2401, alt_2=True)
    '两千四百零一'
    >>> num2cn(101)
    '一百零一'
    >>> num2cn(float("3.4"), numbering_type=NumberingType.HIGH, alt_2=True, upper=False, traditional=False)
    '三点四'
    >>> num2cn("3.4", numbering_type=NumberingType.HIGH, alt_2=True, upper=False, traditional=False)
    '三点四'
    >>> num2cn(23232.005184132423423423300, numbering_type=NumberingType.HIGH, alt_2=True, upper=False, traditional=True)
    '兩萬叁仟兩佰叁拾贰點零零伍壹捌肆壹叁贰肆贰肆'
    >>> num2cn("23232.005184132423423423300", numbering_type=NumberingType.HIGH, alt_2=True, upper=False, traditional=True)
    '兩萬叁仟兩佰叁拾贰點零零伍壹捌肆壹叁贰肆贰叁肆贰叁肆贰叁叁零零'
    >>> num2cn('023232.005184132423423423300', numbering_type=NumberingType.HIGH, alt_2=False, upper=False, traditional=False)
    '二万三千二百三十二点零零五一八四一三二四二三四二三四二三三零零'
    >>> num2cn(111180000)
    '一亿一千一百一十八万'
    >>> num2cn(1821010)
    '一百八十二万一千零一十'
    >>> num2cn(182.1)
    '一百八十二点一'
    >>> num2cn('3.4')
    '三点四'
    >>> num2cn(16)
    '十六'
    >>> num2cn(10600)
    '一万零六百'
    >>> num2cn(110)
    '一百一'
    >>> num2cn(1600)
    '一千六'

    ```

    Args:
        num (Tuple[int, float, str]): `int`, `float` or `str` value
        numbering_type (Union[str, NumberingType], optional): Numbering type. Defaults to `NumberingType.MID`.
        upper (bool, optional): Capitalized numbers. Defaults to `False`.
        traditional (bool, optional): Traditional Chinese. Defaults to `False`.
        alt_0 (bool, optional): Use alternative form of zero. Defaults to `False`.
        alt_2 (bool, optional): Use alternative form of two. Defaults to `False`.

    Returns:
        str: Chinese string
    """

    if alt_2 and upper:
        raise ValueError("alt_2 and upper cannot be True at the same time.")

    if alt_0 and upper:
        raise ValueError("alt_0 and upper cannot be True at the same time.")

    numbering_type = NumberingType(numbering_type) if isinstance(numbering_type, str) else numbering_type
    system = NumberingSystem(numbering_type)

    num_str = str(num)
    dec_string = ""

    if "." in num_str:
        dec_string = num_str.rsplit(".", 1)[-1]
        # dec_string = dec_string.rstrip("0")

    int_symbols = system.int2symbols(int(float(num)))
    dec_symbols = [system.digits[int(c)] for c in dec_string]

    # e.g. "二百二" to "两百二", "二千二" to "两千二", "三亿零二万二" to "三亿零两万二
    if alt_2:
        int_symbols = system.alt_two_symbols(int_symbols)

    # attribute name for simplified or traditional with upper case or not
    attr_name = "traditional" if traditional else "simplified"
    if upper:
        attr_name = "upper_" + attr_name

    # remove leading '一' for '十', e.g. 一十六 to 十六 in integer part
    if len(int_symbols) > 1 and (int_symbols[0] == system.digits[1]) and (getattr(int_symbols[1], "power", -1) == 1):
        int_symbols = int_symbols[1:]

    # remove trailing units, 1600 -> 一千六, 10600 -> 一萬零六百, 101600 -> 十萬一千六 in integer part
    if len(int_symbols) > 3 and isinstance(int_symbols[-1], CNUnit):
        if getattr(int_symbols[-3], "power", None) == (int_symbols[-1].power + 1):
            int_symbols = int_symbols[:-1]

    int_string = "".join(getattr(s, attr_name) for s in int_symbols)
    int_string = re.sub(r"零+", "零", int_string)  # remove multiple zeros in integer part only
    if not int_string:
        int_string = "零"

    dec_string = "".join(getattr(s, attr_name) for s in dec_symbols)

    result = int_string

    if dec_string:
        result += getattr(system.math.point, attr_name) + dec_string

    if alt_0:
        result = result.replace(getattr(system.digits[0], attr_name), str(system.digits[0].alt_s))

    return result
