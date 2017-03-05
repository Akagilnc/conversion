import os
import conversion
import unittest
import tempfile


class ConversionTestCase(unittest.TestCase):

  def setUp(self):
    self.app = conversion.app.test_client()

  def tearDown(self):
    pass

  def test_home(self):
    rv = self.app.get('/')
    assert b'home' in rv.data

  def test_c2a(self):
    rv = self.app.get('/chinese2arabic/四十二')
    assert b'42' in rv.data
    rv = self.app.get('/chinese2arabic/两千零一十七')
    assert b'2017' in rv.data
    rv = self.app.get('/chinese2arabic/一亿四千八百万bad零一千八百六十二')
    assert b'148001862' in rv.data
    rv = self.app.get('/chinese2arabic/一亿四千八百万bad零一千八百六十二?strict=True')
    assert b'Conversion failed' in rv.data
    rv = self.app.get('/chinese2arabic/两千零一十七点五零五')
    assert b'2017.505' in rv.data
    rv = self.app.get('/chinese2arabic/一亿两千零一十七点五零零五八')
    assert b'100002017.50058' in rv.data
    rv = self.app.get('/chinese2arabic/两千零一十七点五零五一九')
    assert b'2017.50519' in rv.data


if __name__=='__main__':
  unittest.main()
