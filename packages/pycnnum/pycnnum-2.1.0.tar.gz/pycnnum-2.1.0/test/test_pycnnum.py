"""All tests"""

from collections import namedtuple

import pytest

from pycnnum import cn2num, num2cn

TestData = namedtuple(
    "TestData",
    ["cn", "num", "num_type", "alt_0", "alt_2", "num2cn"],
    defaults=["一", 0, "mid", False, False, None],
)
"""Test data for cn2num and num2cn

- cn: Chinese number, default to `"一"`
- num: Arabic number, default to `0`
- alt_0: Use alternative format zero, default to `False`
- alt_2: Use alternative format two, default to `False`
"""

test_data = [
    TestData("一", 1),  # https://github.com/zcold/pycnnum/issues/7, https://github.com/zcold/pycnnum/issues/9
    TestData("十六", 16),  # https://github.com/zcold/pycnnum/issues/2
    TestData("一百一十六", 116),  # https://github.com/zcold/pycnnum/issues/2
    TestData("一百零一", 101),  # https://github.com/zcold/pycnnum/issues/4
    TestData("一百二十三", 123),
    TestData("一千二百三十四", 1234),
    TestData("一千两百三十四", 1234, alt_2=True),
    TestData("两千四百零一", 2401, alt_2=True),  # https://github.com/zcold/pycnnum/issues/5
    TestData("二千四百零一", 2401),  # https://github.com/zcold/pycnnum/issues/5
    TestData("一万二千三百四十五", 12345),
    TestData("一百二十三万四千五百六十七", 1234567),
    TestData("一千二百三十四万五千六百七十八", 12345678),
    TestData("一亿二千三百四十五万六千七百八十九", 123456789),
    TestData("一百二十三亿四千五百六十七万八千九百零一", 12345678901),
    TestData("一千两百三十四亿五千六百七十八万九千零一", 123456789001, alt_2=True),
    TestData("点四五", 0.45, num2cn="零点四五"),  # https://github.com/zcold/pycnnum/issues/1
    TestData("零点四五", 0.45),  # https://github.com/zcold/pycnnum/issues/1
    TestData("三点四", 3.4),  # https://github.com/zcold/pycnnum/issues/1
    TestData("二千万零一百八十五", 20000185),
    TestData("两千万一百八十五", 20000185, num2cn="二千万零一百八十五"),
]
"""Test data for `pycnnum.pycnnum.cn2num` and `pycnnum.pycnnum.num2cn`"""


@pytest.mark.parametrize("td", test_data)
def test_cn2num(td: TestData) -> None:
    """Test cn2num

    - Test if `td.cn` is converted to `td.num`
    - If `td.num2cn` is not `None`, test if `td.num2cn` is converted to `td.num`

    Args:
        td (TestData): Test data
    """
    assert cn2num(td.cn, numbering_type=td.num_type) == td.num
    if td.num2cn:
        assert cn2num(td.num2cn, numbering_type=td.num_type) == td.num


@pytest.mark.parametrize("td", test_data)
def test_num2cn(td: TestData):
    """Test num2cn

    - Test if `td.num` is converted to `td.cn`
    - Test if `str(td.num)` is converted to `td.cn`

    Args:
        td (TestData): Test data
    """
    cn = td.num2cn if td.num2cn else td.cn
    assert num2cn(td.num, numbering_type=td.num_type, alt_0=td.alt_0, alt_2=td.alt_2) == cn
    assert num2cn(str(td.num), numbering_type=td.num_type, alt_0=td.alt_0, alt_2=td.alt_2) == cn
