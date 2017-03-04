#-*- coding: utf-8 -*-

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
  number = number.replace('零', '')
  number = number.replace('〇', '')
  place_dict = {'一': '1', '二': '2', '两': '2', '三': '3', '四': '4',
   '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
  paddings = {'十': 1, '百': 2, '千': 3, '万': 4, '亿': 8}

  res = ''
  add_padding = 0
  for digit in reversed(number):
    sim = place_dict.get(digit, '')
    if not sim:
      padding = paddings.get(digit, '')
      if not padding:
        if strict: raise ValueError('Illegal input')
        else: continue

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
  return int(res)


def arabic2chinese(number):
  """
  Convert arabic numbers to chinese numbers, for examples:
  >>> arabic2chinese(42)
  四十二
  >>> arabic2chinese(520)
  五百二十
  >>> arabic2chinese(2017)
  两千零一十七
  >>> arabic2chinese(148001862)
  一亿四千八百万零一千八百六十二
  """
  pass


def simplify2lower(number):
  """
  Convert uppercase chinese number to lowercase chinese number,
  for examples:
  >>> simplify2lower('壹')
  '一'
  >>> simplify2lower('壹亿肆仟捌佰万零壹仟捌佰陆拾贰')
  '一亿四千八百万零一千八百六十二'
  """

  intab = '壹贰叁肆伍陆柒捌玖拾佰仟'
  intab = [ord(c) for c in intab]
  outab = '一二三四五六七八九十百千'
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


if __name__=='__main__':
  import doctest
  doctest.testmod()

