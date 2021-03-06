import unittest
import datetime
from geodepy.convert import (dec2hp, hp2dec, DMSAngle, DDMAngle, dec2dms,
                             dec2ddm, hp2dms, hp2ddm, yyyydoy_to_date,
                             date_to_yyyydoy)

dec_ex = 123.74875
dec_ex2 = 12.575
dec_ex3 = -12.575
dec_ex4 = 0.0525
dec_ex5 = 0.005

hp_ex = 123.44555
hp_ex2 = 12.3430
hp_ex3 = -12.3430
hp_ex4 = 0.0309
hp_ex5 = 0.0018

dms_ex = DMSAngle(123, 44, 55.5)
dms_ex2 = DMSAngle(12, 34, 30)
dms_ex3 = DMSAngle(-12, -34, -30)
dms_ex4 = DMSAngle(0, 3, 9)
dms_ex5 = DMSAngle(0, 0, 18)

ddm_ex = DDMAngle(123, 44.925)
ddm_ex2 = DDMAngle(12, 34.5)
ddm_ex3 = DDMAngle(-12, -34.5)
ddm_ex4 = DDMAngle(0, 3.15)
ddm_ex5 = DDMAngle(0, 0.3)


class TestConvert(unittest.TestCase):
    def test_dec2hp(self):
        self.assertAlmostEqual(hp_ex, dec2hp(dec_ex), 13)
        self.assertAlmostEqual(-hp_ex, dec2hp(-dec_ex), 13)

    def test_hp2dec(self):
        self.assertAlmostEqual(dec_ex, hp2dec(hp_ex), 13)
        self.assertAlmostEqual(-dec_ex, hp2dec(-hp_ex), 13)
        self.assertAlmostEqual(hp2dec(hp_ex) +
                               hp2dec(hp_ex2), dec_ex + dec_ex2, 13)

    def test_DMSAngle(self):
        # Test DMSAngle Methods
        self.assertEqual(dec_ex, dms_ex.dec())
        self.assertEqual(hp_ex, dms_ex.hp())
        self.assertEqual(hp_ex3, dms_ex3.hp())
        self.assertEqual(ddm_ex, dms_ex.ddm())
        self.assertEqual(-ddm_ex, -dms_ex.ddm())
        self.assertEqual(ddm_ex3, dms_ex3.ddm())

        # Test DMSAngle Sign Conventions
        self.assertEqual(-dec_ex, DMSAngle(-dms_ex.degree, dms_ex.minute,
                                           dms_ex.second).dec())
        self.assertEqual(dec_ex, DMSAngle(dms_ex.degree, -dms_ex.minute,
                                          -dms_ex.second).dec())
        self.assertAlmostEqual(-dec_ex4, DMSAngle(0, -dms_ex4.minute,
                                                  dms_ex4.second).dec(), 9)
        self.assertAlmostEqual(dec_ex4, DMSAngle(0, dms_ex4.minute,
                                                 dms_ex4.second).dec(), 9)
        self.assertEqual(-dec_ex5, DMSAngle(0, 0, -dms_ex5.second).dec())
        self.assertEqual(dec_ex5, DMSAngle(0, 0, dms_ex5.second).dec())
        self.assertEqual(-dms_ex3, DMSAngle(12, 34, -30))
        self.assertEqual(dms_ex.sign, 1)
        self.assertEqual(-dms_ex.sign, -1)
        self.assertEqual(dms_ex4.sign, 1)
        self.assertEqual(-dms_ex4.sign, -1)
        self.assertEqual(dms_ex5.sign, 1)
        self.assertEqual(-dms_ex5.sign, -1)
        self.assertEqual(DMSAngle(-1, 2, 3).sign, -1)
        self.assertEqual(DMSAngle(1, -2, 3).sign, 1)
        self.assertEqual(DMSAngle(1, 2, -3).sign, 1)
        self.assertEqual(DMSAngle(0, -1, 2).sign, -1)
        self.assertEqual(DMSAngle(0, 0, -3).sign, -1)
        self.assertEqual(DMSAngle(-0, 1, 2).sign, 1)
        self.assertEqual(DMSAngle(-0.0, 1, 2).sign, -1)
        self.assertEqual(repr(dms_ex), '{DMSAngle: +123d 44m 55.5s}')
        self.assertEqual(repr(dms_ex3), '{DMSAngle: -12d 34m 30s}')

        # Test DMSAngle Overloads
        self.assertEqual(dec_ex + dec_ex2, (dms_ex + dms_ex2).dec())
        self.assertEqual(dec_ex2 + dec_ex, (dms_ex2 + dms_ex).dec())
        self.assertEqual(dec_ex - dec_ex2, (dms_ex - dms_ex2).dec())
        self.assertEqual(dec_ex2 - dec_ex, (dms_ex2 - dms_ex).dec())
        self.assertEqual(dec_ex * 5, (dms_ex * 5).dec())
        self.assertEqual(5 * dec_ex, (5 * dms_ex).dec())
        self.assertEqual(dec_ex / 3, (dms_ex / 3).dec())
        self.assertEqual(abs(-dms_ex), dms_ex)
        self.assertEqual(-dms_ex2, dms_ex3)
        self.assertEqual(dms_ex2, abs(dms_ex3))
        self.assertEqual(dms_ex, ddm_ex)
        self.assertTrue(dms_ex == dms_ex)
        self.assertFalse(dms_ex == dms_ex2)
        self.assertTrue(dms_ex != dms_ex2)
        self.assertFalse(dms_ex != dms_ex)
        self.assertTrue(dms_ex > dms_ex2)
        self.assertFalse(dms_ex2 > dms_ex)
        self.assertTrue(dms_ex2 < dms_ex)
        self.assertFalse(dms_ex < dms_ex2)
        with self.assertRaises(TypeError):
            dms_ex * 'a'
        with self.assertRaises(TypeError):
            'a' * dms_ex
        with self.assertRaises(TypeError):
            dms_ex / 'a'
        with self.assertRaises(TypeError):
            dms_ex + 'a'
        with self.assertRaises(TypeError):
            'a' + dms_ex
        with self.assertRaises(TypeError):
            dms_ex - 'a'
        with self.assertRaises(TypeError):
            'a' - dms_ex

        # Test Class Interoperability
        self.assertEqual(DMSAngle(1, 2, 3) + DDMAngle(2, 3), DMSAngle(3, 5, 3))
        self.assertEqual(DMSAngle(3, 2, 0) - DDMAngle(2, 2.5),
                         DMSAngle(0, 59, 30))
        self.assertEqual(DDMAngle(2, 3) + DMSAngle(1, 2, 3), DDMAngle(3, 5.05))
        self.assertEqual(DDMAngle(3, 2) - DMSAngle(2, 2, 30),
                         DDMAngle(0, 59.5))

    def test_DDMAngle(self):
        # Test DDMAngle Methods
        self.assertEqual(dec_ex, ddm_ex.dec())
        self.assertEqual(hp_ex, ddm_ex.hp())
        self.assertEqual(dms_ex, ddm_ex.dms())
        self.assertEqual(hp_ex3, ddm_ex3.hp())

        # Test DMSAngle Sign Conventions
        self.assertEqual(-dec_ex, DDMAngle(-dms_ex.degree,
                                           ddm_ex.minute).dec())
        self.assertEqual(dec_ex, DDMAngle(dms_ex.degree, -ddm_ex.minute).dec())
        self.assertAlmostEqual(-dec_ex4, DDMAngle(0, -ddm_ex4.minute).dec(), 9)
        self.assertAlmostEqual(dec_ex4, DDMAngle(0, ddm_ex4.minute).dec(), 9)
        self.assertEqual(-ddm_ex3, DDMAngle(12, 34.5))
        self.assertEqual(ddm_ex.sign, 1)
        self.assertEqual(-ddm_ex.sign, -1)
        self.assertEqual(ddm_ex4.sign, 1)
        self.assertEqual(-ddm_ex4.sign, -1)
        self.assertEqual(ddm_ex5.sign, 1)
        self.assertEqual(-ddm_ex5.sign, -1)
        self.assertEqual(DDMAngle(-1, 2).sign, -1)
        self.assertEqual(DDMAngle(1, -2).sign, 1)
        self.assertEqual(DDMAngle(1, 2).sign, 1)
        self.assertEqual(DDMAngle(0, -1).sign, -1)
        self.assertEqual(DDMAngle(-0, 1).sign, 1)
        self.assertEqual(DDMAngle(-0.0, 1).sign, -1)
        self.assertEqual(repr(ddm_ex), '{DDMAngle: +123d 44.925m}')
        self.assertEqual(repr(ddm_ex3), '{DDMAngle: -12d 34.5m}')

        # Test DDMAngle Overloads
        self.assertEqual(dec_ex + dec_ex2, (ddm_ex + ddm_ex2).dec())
        self.assertEqual(dec_ex2 + dec_ex, (ddm_ex2 + ddm_ex).dec())
        self.assertEqual(dec_ex - dec_ex2, (ddm_ex - ddm_ex2).dec())
        self.assertEqual(dec_ex2 - dec_ex, (ddm_ex2 - ddm_ex).dec())
        self.assertEqual(dec_ex * 5, (ddm_ex * 5).dec())
        self.assertEqual(5 * dec_ex, (5 * ddm_ex).dec())
        self.assertEqual(dec_ex / 3, (ddm_ex / 3).dec())
        self.assertEqual(abs(-ddm_ex), ddm_ex)
        self.assertEqual(-ddm_ex2, ddm_ex3)
        self.assertEqual(ddm_ex2, abs(ddm_ex3))
        self.assertEqual(ddm_ex, dms_ex)
        self.assertTrue(ddm_ex == ddm_ex)
        self.assertFalse(ddm_ex == ddm_ex2)
        self.assertTrue(ddm_ex != ddm_ex2)
        self.assertFalse(ddm_ex != ddm_ex)
        self.assertTrue(ddm_ex > ddm_ex2)
        self.assertFalse(ddm_ex2 > ddm_ex)
        self.assertTrue(ddm_ex2 < ddm_ex)
        self.assertFalse(ddm_ex < ddm_ex2)
        with self.assertRaises(TypeError):
            ddm_ex * 'a'
        with self.assertRaises(TypeError):
            'a' * ddm_ex
        with self.assertRaises(TypeError):
            ddm_ex / 'a'
        with self.assertRaises(TypeError):
            ddm_ex + 'a'
        with self.assertRaises(TypeError):
            'a' + ddm_ex
        with self.assertRaises(TypeError):
            ddm_ex - 'a'
        with self.assertRaises(TypeError):
            'a' - ddm_ex

    def test_dec2dms(self):
        self.assertEqual(dms_ex, dec2dms(dec_ex))
        self.assertEqual(-dms_ex, dec2dms(-dec_ex))

    def test_dec2ddm(self):
        self.assertEqual(ddm_ex, dec2ddm(dec_ex))
        self.assertEqual(-ddm_ex, dec2ddm(-dec_ex))

    def test_hp2dms(self):
        self.assertEqual(dms_ex.degree, hp2dms(hp_ex).degree)
        self.assertEqual(dms_ex.minute, hp2dms(hp_ex).minute)
        self.assertAlmostEqual(dms_ex.second, hp2dms(hp_ex).second, 10)

        self.assertEqual(-dms_ex.sign, hp2dms(-hp_ex).sign)
        self.assertEqual(dms_ex.degree, hp2dms(-hp_ex).degree)
        self.assertEqual(dms_ex.minute, hp2dms(-hp_ex).minute)
        self.assertAlmostEqual(dms_ex.second, hp2dms(-hp_ex).second, 10)

    def test_hp2ddm(self):
        self.assertEqual(ddm_ex, hp2ddm(hp_ex))
        self.assertEqual(-ddm_ex, hp2ddm(-hp_ex))

    def test_date_to_yyyydoy(self):
        self.assertEqual(date_to_yyyydoy(datetime.date(2020, 1, 4)),
                         '2020.004')
        self.assertEqual(date_to_yyyydoy(datetime.date(2020, 10, 12)),
                         '2020.286')
        self.assertEqual(date_to_yyyydoy(datetime.date(1998, 4, 7)),
                         '1998.097')
        self.assertEqual(date_to_yyyydoy(datetime.date(2000, 11, 22)),
                         '2000.327')
        self.assertEqual(date_to_yyyydoy(datetime.date(2008, 2, 29)),
                         '2008.060')
        with self.assertRaises(AttributeError):
            date_to_yyyydoy('a')
        with self.assertRaises(AttributeError):
            date_to_yyyydoy('2020123')

    def test_yyyydoy_to_date(self):
        self.assertEqual(yyyydoy_to_date('2020.004'),
                         datetime.date(2020, 1, 4))
        self.assertEqual(yyyydoy_to_date('2020.286'),
                         datetime.date(2020, 10, 12))
        self.assertEqual(yyyydoy_to_date('1998.097'),
                         datetime.date(1998, 4, 7))
        self.assertEqual(yyyydoy_to_date('2000.327'),
                         datetime.date(2000, 11, 22))
        self.assertEqual(yyyydoy_to_date('2008.060'),
                         datetime.date(2008, 2, 29))
        self.assertEqual(yyyydoy_to_date('2020004'),
                         datetime.date(2020, 1, 4))
        self.assertEqual(yyyydoy_to_date('2020286'),
                         datetime.date(2020, 10, 12))
        self.assertEqual(yyyydoy_to_date('1998097'),
                         datetime.date(1998, 4, 7))
        self.assertEqual(yyyydoy_to_date('2000327'),
                         datetime.date(2000, 11, 22))
        self.assertEqual(yyyydoy_to_date('2008060'),
                         datetime.date(2008, 2, 29))
        with self.assertRaises(ValueError):
            yyyydoy_to_date('a')
        with self.assertRaises(ValueError):
            yyyydoy_to_date('20201234')
        with self.assertRaises(ValueError):
            yyyydoy_to_date('2020.1234')
        with self.assertRaises(ValueError):
            yyyydoy_to_date('202012')
        with self.assertRaises(ValueError):
            yyyydoy_to_date('2020.12')


if __name__ == '__main__':
    unittest.main()
