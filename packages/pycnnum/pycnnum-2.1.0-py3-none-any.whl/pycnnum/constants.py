# pylint: disable=line-too-long
"""Chinese character constants"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CNConstant:
    """Chinese number constant"""

    SIMPLIFIED_LOWER: str
    """lower case simplified string"""

    TRADITIONAL_LOWER: Optional[str] = None
    """lower case traditional string. Defaults to simplified string"""

    SIMPLIFIED_UPPER: Optional[str] = None
    """upper case simplified string. Defaults to lower case traditional string"""

    TRADITIONAL_UPPER: Optional[str] = None
    """upper case traditional string. Defaults to lower case traditional string"""

    def __post_init__(self) -> None:
        """Post initialization"""
        self.TRADITIONAL_LOWER = self.TRADITIONAL_LOWER or self.SIMPLIFIED_LOWER
        self.SIMPLIFIED_UPPER = self.SIMPLIFIED_UPPER or self.TRADITIONAL_LOWER
        self.TRADITIONAL_UPPER = self.TRADITIONAL_UPPER or self.TRADITIONAL_LOWER

    def __getitem__(self, key: int) -> str:
        """Get item by index"""
        if self.TRADITIONAL_LOWER is None:
            raise ValueError("TRADITIONAL_LOWER is not set")
        if self.SIMPLIFIED_UPPER is None:
            raise ValueError("SIMPLIFIED_UPPER is not set")
        if self.TRADITIONAL_UPPER is None:
            raise ValueError("TRADITIONAL_UPPER is not set")
        return "".join(
            (
                self.SIMPLIFIED_LOWER[key],
                self.TRADITIONAL_LOWER[key],
                self.SIMPLIFIED_UPPER[key],
                self.TRADITIONAL_UPPER[key],
            )
        )

    def __iter__(self):
        """Iterate over the constant"""
        for i in range(len(self.SIMPLIFIED_LOWER)):
            yield self[i]


DIGITS = CNConstant("零一二三四五六七八九", "零壹贰叁肆伍陆柒捌玖")
"""Chinese number digits

- Simplified: `"零一二三四五六七八九"`
- Traditional: `"零壹贰叁肆伍陆柒捌玖"`
- Upper simplified: `"零一二三四五六七八九"`
- Upper traditional: `"零壹贰叁肆伍陆柒捌玖"`
"""


UNITS = CNConstant("十百千万亿兆京垓秭穰沟涧正载", "拾佰仟萬億兆京垓秭穰溝澗正載")
r"""Chinese number units

For $i \in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]$:

| NumberingType | value              |
|---------------|--------------------|
| `LOW`         | $10^{8 + i}$       |
| `MID`         | $10^{8 + i*4}$     |
| `HIGH`        | $10^{8 + 2^{i+3}}$ |

---

| type  |  亿     | 兆      | 京      | 垓       | 秭       | 穰       | 沟       | 涧        | 正        | 载         |
|-------| --------|---------|---------|---------|----------|----------|----------|-----------|-----------|-----------|
|`LOW`  | $10^{8}$|$10^{9}$ |$10^{10}$|$10^{11}$|$10^{12}$ |$10^{13}$ |$10^{14}$ |$10^{15}$  |$10^{16}$  |$10^{17}$  |
|`MID`  | $10^{8}$|$10^{12}$|$10^{16}$|$10^{20}$|$10^{24}$ |$10^{28}$ |$10^{32}$ |$10^{36}$  |$10^{40}$  |$10^{44}$  |
|`HIGH` | $10^{8}$|$10^{16}$|$10^{32}$|$10^{64}$|$10^{128}$|$10^{256}$|$10^{512}$|$10^{1024}$|$10^{2048}$|$10^{4096}$|

---

Example:

- "一兆" is ` 1 000 000 000` in `LOW` numbering type
- "一兆" is ` 1 000 000 000 000` in `MID` numbering type
- "一兆" is `10 000 000 000 000 000` in `HIGH` numbering type
"""


__all__ = [
    "DIGITS",
    "UNITS",
]
