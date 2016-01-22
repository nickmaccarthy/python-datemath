import unittest2 as unittest
import arrow
import datemath

iso8601 = 'YYYY-MM-DDTHH:mm:ssZZ'
class TestDM(unittest.TestCase):
    
    def testParse(self):

        # Baisc dates
        #self.assertEqual(datemath.parse('2016').format(iso8601), '2016-01-01T00:00:00-00:00')
        self.assertEqual(datemath.parse('2016-01-02').format(iso8601), '2016-01-02T00:00:00-00:00')
        self.assertEqual(datemath.parse('2016-01-02 01:00:00').format(iso8601), '2016-01-02T01:00:00-00:00')

        # Rounding Tests
        self.assertEqual(datemath.parse('2016-01-01||/d').format('YYYY-MM-DDTHH:mm:ssZZ'), '2016-01-01T00:00:00-00:00')
        self.assertEqual(datemath.parse('2014-11-18||/y').format('YYYY-MM-DDTHH:mm:ssZZ'), '2014-01-01T00:00:00-00:00')
        self.assertEqual(datemath.parse('2016-01-01 14:00:00||/w').format('YYYY-MM-DDTHH:mm:ssZZ'), '2015-12-28T00:00:00-00:00')
        self.assertEqual(datemath.parse('2014-11||/M').format('YYYY-MM-DDTHH:mm:ssZZ'), '2014-11-01T00:00:00-00:00')
        self.assertEqual(datemath.parse('2016-01-02||/M+1h+1m').format(iso8601), '2016-01-01T01:01:00-00:00')
        self.assertEqual(datemath.parse('2016-01-02||/d+1h').format(iso8601), '2016-01-02T01:00:00-00:00')
        self.assertEqual(datemath.parse('2016-01-02T14:02:00||/h').format(iso8601), '2016-01-02T14:00:00-00:00')
        self.assertEqual(datemath.parse('2016-01-02T14:02:00||/H').format(iso8601), '2016-01-02T14:00:00-00:00')

        # relitive formats
        # addition
        self.assertEqual(datemath.parse('+1s').format(iso8601), arrow.utcnow().replace(seconds=+1).format(iso8601))
        self.assertEqual(datemath.parse('+1m').format(iso8601), arrow.utcnow().replace(minutes=+1).format(iso8601))
        self.assertEqual(datemath.parse('+1h').format(iso8601), arrow.utcnow().replace(hours=+1).format(iso8601))
        self.assertEqual(datemath.parse('+1d').format(iso8601), arrow.utcnow().replace(days=+1).format(iso8601))
        self.assertEqual(datemath.parse('+1w').format(iso8601), arrow.utcnow().replace(weeks=+1).format(iso8601))
        self.assertEqual(datemath.parse('+1M').format(iso8601), arrow.utcnow().replace(months=+1).format(iso8601))
        self.assertEqual(datemath.parse('+1Y').format(iso8601), arrow.utcnow().replace(years=+1).format(iso8601))
        self.assertEqual(datemath.parse('+1y').format(iso8601), arrow.utcnow().replace(years=+1).format(iso8601))
        # subtraction
        self.assertEqual(datemath.parse('-1s').format(iso8601), arrow.utcnow().replace(seconds=-1).format(iso8601))
        self.assertEqual(datemath.parse('-1m').format(iso8601), arrow.utcnow().replace(minutes=-1).format(iso8601))
        self.assertEqual(datemath.parse('-1h').format(iso8601), arrow.utcnow().replace(hours=-1).format(iso8601))
        self.assertEqual(datemath.parse('-1d').format(iso8601), arrow.utcnow().replace(days=-1).format(iso8601))
        self.assertEqual(datemath.parse('-1w').format(iso8601), arrow.utcnow().replace(weeks=-1).format(iso8601))
        self.assertEqual(datemath.parse('-1M').format(iso8601), arrow.utcnow().replace(months=-1).format(iso8601))
        self.assertEqual(datemath.parse('-1Y').format(iso8601), arrow.utcnow().replace(years=-1).format(iso8601))
        self.assertEqual(datemath.parse('-1y').format(iso8601), arrow.utcnow().replace(years=-1).format(iso8601))
        # rounding
        self.assertEqual(datemath.parse('/s').format(iso8601), arrow.utcnow().floor('second').format(iso8601))
        self.assertEqual(datemath.parse('/m').format(iso8601), arrow.utcnow().floor('minute').format(iso8601))
        self.assertEqual(datemath.parse('/h').format(iso8601), arrow.utcnow().floor('hour').format(iso8601))
        self.assertEqual(datemath.parse('/d').format(iso8601), arrow.utcnow().floor('day').format(iso8601))
        self.assertEqual(datemath.parse('/w').format(iso8601), arrow.utcnow().floor('week').format(iso8601))
        self.assertEqual(datemath.parse('/M').format(iso8601), arrow.utcnow().floor('month').format(iso8601))
        self.assertEqual(datemath.parse('/Y').format(iso8601), arrow.utcnow().floor('year').format(iso8601))
        self.assertEqual(datemath.parse('/y').format(iso8601), arrow.utcnow().floor('year').format(iso8601))
        # complicated date math
        self.assertEqual(datemath.parse('now/d-1h').format(iso8601), arrow.utcnow().floor('day').replace(hours=-1).format(iso8601))
        self.assertEqual(datemath.parse('+1h').format(iso8601), arrow.utcnow().replace(hours=+1).format(iso8601))
        self.assertEqual(datemath.parse('/M+2d').format(iso8601), arrow.utcnow().floor('month').replace(days=+2).format(iso8601))
        self.assertEqual(datemath.parse('now/w+2d-2h').format(iso8601), arrow.utcnow().floor('week').replace(days=+2, hours=-2).format(iso8601))
        self.assertEqual(datemath.parse('now/M+1w-2h+10s').format(iso8601), arrow.utcnow().floor('month').replace(weeks=+1, hours=-2, seconds=+10).format(iso8601))
        

        # future
        self.assertEqual(datemath.parse('+1s').format(iso8601), arrow.utcnow().replace(seconds=+1).format(iso8601))
        self.assertEqual(datemath.parse('+1s+2m+3h').format(iso8601), arrow.utcnow().replace(seconds=+1, minutes=+2, hours=+3).format(iso8601))
        self.assertEqual(datemath.parse('+1m').format(iso8601), arrow.utcnow().replace(minutes=+1).format(iso8601))
        self.assertEqual(datemath.parse('+1m+5h').format(iso8601), arrow.utcnow().replace(minutes=+1, hours=+5).format(iso8601))
        self.assertEqual(datemath.parse('/d+1m+5h').format(iso8601), arrow.utcnow().floor('day').replace(minutes=+1, hours=+5).format(iso8601))
        self.assertEqual(datemath.parse('+1h').format(iso8601), arrow.utcnow().replace(hours=+1).format(iso8601))
        self.assertEqual(datemath.parse('+1w').format(iso8601), arrow.utcnow().replace(weeks=+1).format(iso8601))
        self.assertEqual(datemath.parse('+1w+12d').format(iso8601), arrow.utcnow().replace(weeks=+1, days=+12).format(iso8601))
        self.assertEqual(datemath.parse('+2y').format(iso8601), arrow.utcnow().replace(years=+2).format(iso8601))
        self.assertEqual(datemath.parse('+2y+22d+4h').format(iso8601), arrow.utcnow().replace(years=+2, days=+22, hours=+4).format(iso8601))
        
        # past
        self.assertEqual(datemath.parse('-3w').format(iso8601), arrow.utcnow().replace(weeks=-3).format(iso8601))
        self.assertEqual(datemath.parse('-3w-2d-6h').format(iso8601), arrow.utcnow().replace(weeks=-3, days=-2, hours=-6).format(iso8601))
        self.assertEqual(datemath.parse('-3w-2d-22h-36s').format(iso8601), arrow.utcnow().replace(weeks=-3, days=-2, hours=-22, seconds=-36).format(iso8601))
        self.assertEqual(datemath.parse('-6y-3w-2d-22h-36s').format(iso8601), arrow.utcnow().replace(years=-6, weeks=-3, days=-2, hours=-22, seconds=-36).format(iso8601))

       
        import datetime
        delta = datetime.timedelta(seconds=1) 
        # datetime objects
        self.assertAlmostEqual(datemath.parse('now').datetime, arrow.utcnow().datetime, delta=delta)
        self.assertAlmostEqual(datemath.parse('now+1d').datetime, arrow.utcnow().replace(days=+1).datetime, delta=delta)
        self.assertAlmostEqual(datemath.parse('/w').datetime, arrow.utcnow().floor('week').datetime, delta=delta)


if __name__ == "__main__":
    unittest.main()
        

    
