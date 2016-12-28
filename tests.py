import unittest2 as unittest
import arrow
from datemath import dm 
from datemath import datemath

iso8601 = 'YYYY-MM-DDTHH:mm:ssZZ'
class TestDM(unittest.TestCase):
    
    def testParse(self):

        # Baisc dates
        self.assertEqual(dm('2016.01.02').format(iso8601), '2016-01-02T00:00:00-00:00')
        self.assertEqual(dm('2016-01-02').format(iso8601), '2016-01-02T00:00:00-00:00')
        self.assertEqual(dm('2016-01-02 01:00:00').format(iso8601), '2016-01-02T01:00:00-00:00')

        # Rounding Tests
        self.assertEqual(dm('2016-01-01||/d').format('YYYY-MM-DDTHH:mm:ssZZ'), '2016-01-01T00:00:00-00:00')
        self.assertEqual(dm('2014-11-18||/y').format('YYYY-MM-DDTHH:mm:ssZZ'), '2014-01-01T00:00:00-00:00')
        self.assertEqual(dm('2016-01-01 14:00:00||/w').format('YYYY-MM-DDTHH:mm:ssZZ'), '2015-12-28T00:00:00-00:00')
        self.assertEqual(dm('2014-11||/M').format('YYYY-MM-DDTHH:mm:ssZZ'), '2014-11-01T00:00:00-00:00')
        self.assertEqual(dm('2016-01-02||/M+1h+1m').format(iso8601), '2016-01-01T01:01:00-00:00')
        self.assertEqual(dm('2016-01-02||/d+1h').format(iso8601), '2016-01-02T01:00:00-00:00')
        self.assertEqual(dm('2016-01-02T14:02:00||/h').format(iso8601), '2016-01-02T14:00:00-00:00')
        self.assertEqual(dm('2016-01-02T14:02:00||/H').format(iso8601), '2016-01-02T14:00:00-00:00')

        # relitive formats
        # addition
        self.assertEqual(dm('+1s').format(iso8601), arrow.utcnow().replace(seconds=+1).format(iso8601))
        self.assertEqual(dm('+1m').format(iso8601), arrow.utcnow().replace(minutes=+1).format(iso8601))
        self.assertEqual(dm('+1h').format(iso8601), arrow.utcnow().replace(hours=+1).format(iso8601))
        self.assertEqual(dm('+1d').format(iso8601), arrow.utcnow().replace(days=+1).format(iso8601))
        self.assertEqual(dm('+1w').format(iso8601), arrow.utcnow().replace(weeks=+1).format(iso8601))
        self.assertEqual(dm('+1M').format(iso8601), arrow.utcnow().replace(months=+1).format(iso8601))
        self.assertEqual(dm('+1Y').format(iso8601), arrow.utcnow().replace(years=+1).format(iso8601))
        self.assertEqual(dm('+1y').format(iso8601), arrow.utcnow().replace(years=+1).format(iso8601))
        # subtraction
        self.assertEqual(dm('-1s').format(iso8601), arrow.utcnow().replace(seconds=-1).format(iso8601))
        self.assertEqual(dm('-1m').format(iso8601), arrow.utcnow().replace(minutes=-1).format(iso8601))
        self.assertEqual(dm('-1h').format(iso8601), arrow.utcnow().replace(hours=-1).format(iso8601))
        self.assertEqual(dm('-1d').format(iso8601), arrow.utcnow().replace(days=-1).format(iso8601))
        self.assertEqual(dm('-1w').format(iso8601), arrow.utcnow().replace(weeks=-1).format(iso8601))
        self.assertEqual(dm('-1M').format(iso8601), arrow.utcnow().replace(months=-1).format(iso8601))
        self.assertEqual(dm('-1Y').format(iso8601), arrow.utcnow().replace(years=-1).format(iso8601))
        self.assertEqual(dm('-1y').format(iso8601), arrow.utcnow().replace(years=-1).format(iso8601))
        # rounding
        self.assertEqual(dm('/s').format(iso8601), arrow.utcnow().floor('second').format(iso8601))
        self.assertEqual(dm('/m').format(iso8601), arrow.utcnow().floor('minute').format(iso8601))
        self.assertEqual(dm('/h').format(iso8601), arrow.utcnow().floor('hour').format(iso8601))
        self.assertEqual(dm('/d').format(iso8601), arrow.utcnow().floor('day').format(iso8601))
        self.assertEqual(dm('/w').format(iso8601), arrow.utcnow().floor('week').format(iso8601))
        self.assertEqual(dm('/M').format(iso8601), arrow.utcnow().floor('month').format(iso8601))
        self.assertEqual(dm('/Y').format(iso8601), arrow.utcnow().floor('year').format(iso8601))
        self.assertEqual(dm('/y').format(iso8601), arrow.utcnow().floor('year').format(iso8601))
        # complicated date math
        self.assertEqual(dm('now/d-1h').format(iso8601), arrow.utcnow().floor('day').replace(hours=-1).format(iso8601))
        self.assertEqual(dm('+1h').format(iso8601), arrow.utcnow().replace(hours=+1).format(iso8601))
        self.assertEqual(dm('/M+2d').format(iso8601), arrow.utcnow().floor('month').replace(days=+2).format(iso8601))
        self.assertEqual(dm('now/w+2d-2h').format(iso8601), arrow.utcnow().floor('week').replace(days=+2, hours=-2).format(iso8601))
        self.assertEqual(dm('now/M+1w-2h+10s').format(iso8601), arrow.utcnow().floor('month').replace(weeks=+1, hours=-2, seconds=+10).format(iso8601))
        self.assertEqual(dm('now-1d/d').format(iso8601), arrow.utcnow().replace(days=-1).floor('day').format(iso8601))
        self.assertEqual(dm('now+1d/d').format(iso8601), arrow.utcnow().replace(days=1).floor('day').format(iso8601))
        self.assertEqual(dm('now-10d/d').format(iso8601), arrow.utcnow().replace(days=-10).floor('day').format(iso8601))
        self.assertEqual(dm('now+10d/d').format(iso8601), arrow.utcnow().replace(days=10).floor('day').format(iso8601))
        

        # future
        self.assertEqual(dm('+1s').format(iso8601), arrow.utcnow().replace(seconds=+1).format(iso8601))
        self.assertEqual(dm('+1s+2m+3h').format(iso8601), arrow.utcnow().replace(seconds=+1, minutes=+2, hours=+3).format(iso8601))
        self.assertEqual(dm('+1m').format(iso8601), arrow.utcnow().replace(minutes=+1).format(iso8601))
        self.assertEqual(dm('+1m+5h').format(iso8601), arrow.utcnow().replace(minutes=+1, hours=+5).format(iso8601))
        self.assertEqual(dm('/d+1m+5h').format(iso8601), arrow.utcnow().floor('day').replace(minutes=+1, hours=+5).format(iso8601))
        self.assertEqual(dm('+1h').format(iso8601), arrow.utcnow().replace(hours=+1).format(iso8601))
        self.assertEqual(dm('+1w').format(iso8601), arrow.utcnow().replace(weeks=+1).format(iso8601))
        self.assertEqual(dm('+1w+12d').format(iso8601), arrow.utcnow().replace(weeks=+1, days=+12).format(iso8601))
        self.assertEqual(dm('+2y').format(iso8601), arrow.utcnow().replace(years=+2).format(iso8601))
        self.assertEqual(dm('+2y+22d+4h').format(iso8601), arrow.utcnow().replace(years=+2, days=+22, hours=+4).format(iso8601))
        
        # past
        self.assertEqual(dm('-3w').format(iso8601), arrow.utcnow().replace(weeks=-3).format(iso8601))
        self.assertEqual(dm('-3W').format(iso8601), arrow.utcnow().replace(weeks=-3).format(iso8601))
        self.assertEqual(dm('-3w-2d-6h').format(iso8601), arrow.utcnow().replace(weeks=-3, days=-2, hours=-6).format(iso8601))
        self.assertEqual(dm('-3w-2d-22h-36s').format(iso8601), arrow.utcnow().replace(weeks=-3, days=-2, hours=-22, seconds=-36).format(iso8601))
        self.assertEqual(dm('-6y-3w-2d-22h-36s').format(iso8601), arrow.utcnow().replace(years=-6, weeks=-3, days=-2, hours=-22, seconds=-36).format(iso8601))

       
        import datetime
        delta = datetime.timedelta(seconds=1) 
        # datetime objects
        self.assertAlmostEqual(dm('now').datetime, arrow.utcnow().datetime, delta=delta)
        self.assertAlmostEqual(dm('now+1d').datetime, arrow.utcnow().replace(days=+1).datetime, delta=delta)
        self.assertAlmostEqual(dm('/w').datetime, arrow.utcnow().floor('week').datetime, delta=delta)


        # Floats
        self.assertEqual(dm('now-2.5h').format(iso8601), arrow.utcnow().replace(hours=-2.5).format(iso8601))
        self.assertEqual(dm('now-2.5d').format(iso8601), arrow.utcnow().replace(days=-2.5).format(iso8601))


if __name__ == "__main__":
    unittest.main()
        

    
