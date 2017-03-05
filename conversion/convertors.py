# -*- coding: utf-8 -*-

place_dict = {'一': '1', '二': '2', '两': '2', '三': '3', '四': '4',
              '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
paddings = {'十': 1, '百': 2, '千': 3, '万': 4, '亿': 8}


def chinese_float(input_num, input_strict):
    number_list = input_num.split('点')
    number = number_list[0]
    float_part = number_list[-1]
    if len(number_list) > 2:
        if float_part is None and input_strict:
            raise ValueError('Illegal input')
    res = ''
    for digit in float_part:
        temp = place_dict.get(digit, '');
        if temp is None or len(temp) == 0:
            if digit == '零':
                temp = '0'
            elif input_strict:
                raise ValueError('Illegal input')
        res += temp

    return '.' + res, number






def chinese2arabic(number, strict=False):
    """
    Convert chinese numbers to arabic numbers, both support tranditional
    or simplified chinese numbers, for examples:
    >>> chinese2arabic('四十二')
    42
    >>> chinese2arabic('五百二十')
    520
    >>> chinese2arabic('两千零一十七')
    2017
    >>> chinese2arabic('一亿四千八百万bad零一千八百六十二')
    148001862
    >>> chinese2arabic('一亿四千八百万bad零一千八百六十二', True)
    Traceback (most recent call last):
    ...
    ValueError: Illegal input
    >>> chinese2arabic('')
    Traceback (most recent call last):
    ...
    AssertionError: Illegal input
    """
    assert number and len(number) > 0, 'Illegal input'
    number = simplify2lower(simplify(number))
    float_part = None
    if '点' in number:
        float_part, number = chinese_float(number, strict)

    number = number.replace('零', '')
    number = number.replace('〇', '')

    res = ''
    add_padding = 0
    for digit in reversed(number):
        sim = place_dict.get(digit, '')
        if not sim:
            padding = paddings.get(digit, '')

            if not padding:
                if strict:
                    raise ValueError('Illegal input')
                else:
                    continue

            if digit == '亿':
                add_padding = 0
            padding = padding + add_padding
            res = res.zfill(padding)
            if digit == '万':
                add_padding = add_padding + 4
            if digit == '亿':
                add_padding = 8
        else:
            res = sim + res
    try:
        if res[0] == '0':
            res = '1' + res
    except:
        return None
    if float_part is not None:
        return float(res + float_part)
    return int(res)


def arabic2chinese(number):
    """
    Convert arabic numbers to chinese numbers, for examples:
    >>> print(arabic2chinese(42))
    四十二
    >>> print(arabic2chinese(520))
    五百二十
    >>> print(arabic2chinese(2017))
    二千零一十七
    >>> print(arabic2chinese(148001862))
    一亿四千八百万一千八百六十二
    """
    yis = []
    number = str(number)
    for i in range(len(number), 0, -8):
        yi = number[max(0, i - 8):i]
        yi = yi.zfill(8)
        lwan = yi[0:4]
        rwan = yi[4:8]
        if lwan == '0000':
            yis.insert(0, convert4places(rwan))
        else:
            lwan = convert4places(lwan)
            rwan = convert4places(rwan)
            yis.insert(0, '万'.join([lwan, rwan]))
    res = '亿'.join(yis)
    return res.lstrip('零')


def convert4places(number):
    """
    Convert arabic numbers under 1000 to chinese numbers, for examples:
    >>> print(convert4places(42))
    零四十二
    >>> print(convert4places(520))
    零五百二十
    >>> print(convert4places(2017))
    二千零一十七
    >>> print(convert4places(1))
    零一
    """
    place_dicts = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九', '0': '零'}
    number = str(number)
    number = number.zfill(4)
    assert number
    last_place = number[-1]
    suffix = ''
    if last_place != '0':
        suffix = place_dicts.get(last_place)
    number = number[:-1]
    number = convert_places('十百千', number[::-1], place_dicts) + suffix
    number = number.replace('零零零零', '零')
    number = number.replace('零零零', '零')
    number = number.replace('零零', '零')

    return number.rstrip('零')


def convert_places(chinese, arabic, place_dicts):
    res = ""
    for ar, cn in zip(arabic, chinese):
        if ar == '0':
            # res = place_dicts.get(ar) + res
            res = '零' + res
        else:
            place = place_dicts.get(ar)
            res = place + cn + res
    return res.replace('\\xa0', '')


def simplify2lower(number):
    """
    Convert uppercase chinese number to lowercase chinese number,
    for examples:
    >>> simplify2lower('壹')
    '一'
    >>> simplify2lower('壹亿肆仟捌佰万零壹仟捌佰陆拾贰')
    '一亿四千八百万零一千八百六十二'
    """

    intab = '壹贰叁肆伍陆柒捌玖拾佰仟點'
    intab = [ord(c) for c in intab]
    outab = '一二三四五六七八九十百千点'
    trantab = dict(zip(intab, outab))

    return number.translate(trantab)


def simplify(number):
    """
    Convert traditional chinese uppercase number
    to simplied chinese uppercase number,
    for examples:
    >>> simplify('貳')
    '贰'

    """

    intab = '貳參陸萬億'
    intab = [ord(c) for c in intab]
    outab = '贰叁陆萬億'

    trantab = dict(zip(intab, outab))

    return number.translate(trantab)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
