#-*- coding: utf-8 -*-

def chinese2arabic(number, strict=False):
  u"""
  Convert chinese numbers to arabic numbers, both support tranditional 
  or simplified chinese numbers, for examples:
  >>> chinese2arabic(u'四十二')
  42
  >>> chinese2arabic(u'五百二十')
  520
  >>> chinese2arabic(u'两千零一十七')
  2017
  >>> chinese2arabic(u'一亿四千八百万bad零一千八百六十二')
  148001862
  >>> chinese2arabic(u'一亿四千八百万bad零一千八百六十二', True)
  Traceback (most recent call last):
  ...
  ValueError: Illegal input
  >>> chinese2arabic(u'')
  Traceback (most recent call last):
  ...
  AssertionError: Illegal input
  """
  assert number and len(number) > 0, 'Illegal input'
  number = simplify2lower(simplify(number))
  number = number.replace(u'零', '')
  number = number.replace(u'〇', '')
  place_dict = {u'一': '1', u'二': '2', u'两': '2', u'三': '3', u'四': '4',
   u'五': '5', u'六': '6', u'七': '7', u'八': '8', u'九': '9'}
  paddings = {u'十': 1, u'百': 2, u'千': 3, u'万': 4, u'亿': 8}

  res = ''
  add_padding = 0
  for digit in reversed(number):
    sim = place_dict.get(digit, '')
    if not sim:
      padding = paddings.get(digit, '')
      if not padding:
        if strict: raise ValueError('Illegal input')
        else: continue

      if digit == u'亿':
        add_padding = 0
      padding = padding + add_padding
      res = res.zfill(padding)
      if digit == u'万':
        add_padding = add_padding + 4
      if digit == u'亿':
        add_padding = 8
    else:
      res = sim + res
  try:
    if res[0] == '0':
      res = '1' + res
  except:
    return None
  return int(res)

def simplify2lower(number):
  u"""
  Convert uppercase chinese number to lowercase chinese number,
  for examples:
  >>> print simplify2lower(u'壹')
  一
  >>> print simplify2lower(u'壹亿肆仟捌佰万零壹仟捌佰陆拾贰')
  一亿四千八百万零一千八百六十二
  """

  intab = u'壹贰叁肆伍陆柒捌玖拾佰仟'
  intab = [ord(c) for c in intab]
  outab = u'一二三四五六七八九十百千'
  trantab = dict(zip(intab, outab))

  return number.translate(trantab)


def simplify(number):
  u"""
  Convert traditional chinese uppercase number 
  to simplied chinese uppercase number,
  for examples:
  >>> print simplify(u'貳')
  贰

  """

  intab = u'貳參陸萬億'
  intab = [ord(c) for c in intab]
  outab = u'贰叁陆萬億'

  trantab = dict(zip(intab, outab))

  return number.translate(trantab)


if __name__=='__main__':
  import doctest
  doctest.testmod()

