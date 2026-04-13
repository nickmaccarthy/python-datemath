from __future__ import annotations

from datetime import UTC, timedelta, timezone
from datetime import datetime as pydatetime
from zoneinfo import ZoneInfo

import arrow
import pytest
from freezegun import freeze_time

from datemath import datemath, dm
from datemath.helpers import DateMathException

ISO8601 = "YYYY-MM-DDTHH:mm:ssZZ"


class TestDM:
    def test_basic(self) -> None:
        assert isinstance(datemath("now"), pydatetime)
        assert isinstance(dm("now"), arrow.Arrow)

        assert dm("2016.01.02").format(ISO8601) == "2016-01-02T00:00:00+00:00"
        assert dm("2016-01-02").format(ISO8601) == "2016-01-02T00:00:00+00:00"
        assert dm("2016-01-02 01:00:00").format(ISO8601) == "2016-01-02T01:00:00+00:00"

    def test_rounding(self) -> None:
        assert dm("2016-01-01||/d").format(ISO8601) == "2016-01-01T00:00:00+00:00"
        assert dm("2014-11-18||/y").format(ISO8601) == "2014-01-01T00:00:00+00:00"
        assert dm("2016-01-01 14:00:00||/w").format(ISO8601) == "2015-12-28T00:00:00+00:00"
        assert dm("2014-11||/M").format(ISO8601) == "2014-11-01T00:00:00+00:00"
        assert dm("2016-01-02||/M+1h+1m").format(ISO8601) == "2016-01-01T01:01:00+00:00"
        assert dm("2016-01-02||/d+1h").format(ISO8601) == "2016-01-02T01:00:00+00:00"
        assert dm("2016-01-02T14:02:00||/h").format(ISO8601) == "2016-01-02T14:00:00+00:00"
        assert dm("2016-01-02T14:02:00||/H").format(ISO8601) == "2016-01-02T14:00:00+00:00"

        assert dm("2016-01-01||/d", roundDown=False).format(ISO8601) == "2016-01-01T23:59:59+00:00"
        assert dm("2014-11-18||/y", roundDown=False).format(ISO8601) == "2014-12-31T23:59:59+00:00"

    def test_timezone(self) -> None:
        with freeze_time(datemath("now/d", tz="US/Pacific")):
            assert datemath("now/d", tz="US/Pacific") == pydatetime.now(tz=ZoneInfo("US/Pacific"))

        with freeze_time(pydatetime(2017, 9, 22, 10, 20, 0, tzinfo=ZoneInfo("US/Pacific"))):
            assert dm("2017-09-22 10:20:00", tz="US/Pacific").datetime == pydatetime.now(
                tz=ZoneInfo("US/Pacific")
            )

        with freeze_time(datemath("2016-01-01T00:00:00", tz="UTC")):
            assert dm("2016-01-01", tz="UTC") == arrow.get("2016-01-01").to("UTC")

        with freeze_time(datemath("2016-01-01", tz="US/Eastern")):
            assert dm("2016-01-01", tz="US/Eastern") == pydatetime(
                2016,
                1,
                1,
                tzinfo=ZoneInfo("US/Eastern"),
            )

        with freeze_time(datemath("2016-01-01T01:00:00", tz="US/Central")):
            assert datemath("2016-01-01T01:00:00", tz="US/Central") == pydatetime(
                2016,
                1,
                1,
                1,
                0,
                0,
                tzinfo=ZoneInfo("US/Central"),
            )

        with freeze_time(datemath("2016-01-01T02:00:00", tz="US/Eastern")):
            assert datemath("2016-01-01T02:00:00", tz="US/Eastern") == pydatetime(
                2016,
                1,
                1,
                2,
                tzinfo=ZoneInfo("US/Eastern"),
            )

        assert datemath("2016-01-01T16:20:00.5+12:00") == pydatetime(
            2016,
            1,
            1,
            16,
            20,
            0,
            500000,
            tzinfo=timezone(timedelta(hours=12)),
        )
        assert datemath("2016-01-01T16:20:00.5-05:00") == pydatetime(
            2016,
            1,
            1,
            16,
            20,
            0,
            500000,
            tzinfo=timezone(timedelta(hours=-5)),
        )
        assert datemath("2016-01-01T16:20:00.5-00:00") == pydatetime(
            2016,
            1,
            1,
            16,
            20,
            0,
            500000,
            tzinfo=UTC,
        )

        assert datemath("2016-01-01T16:20:00.5+12:00||+1d") == pydatetime(
            2016,
            1,
            2,
            16,
            20,
            0,
            500000,
            tzinfo=timezone(timedelta(hours=12)),
        )
        assert datemath("2016-01-01T16:20:00.6+12:00||+2d+1h") == pydatetime(
            2016,
            1,
            3,
            17,
            20,
            0,
            600000,
            tzinfo=timezone(timedelta(hours=12)),
        )
        assert datemath("2016-01-01T16:20:00.6+12:00||+2d+1h", tz="US/Eastern") == pydatetime(
            2016,
            1,
            3,
            17,
            20,
            0,
            600000,
            tzinfo=timezone(timedelta(hours=12)),
        )

    @freeze_time("2024-01-15T12:30:45Z")
    def test_relative_formats(self) -> None:
        now = arrow.utcnow()

        assert dm("+1s").format(ISO8601) == now.shift(seconds=1).format(ISO8601)
        assert dm("+1m").format(ISO8601) == now.shift(minutes=1).format(ISO8601)
        assert dm("+1h").format(ISO8601) == now.shift(hours=1).format(ISO8601)
        assert dm("+1d").format(ISO8601) == now.shift(days=1).format(ISO8601)
        assert dm("+1w").format(ISO8601) == now.shift(weeks=1).format(ISO8601)
        assert dm("+1M").format(ISO8601) == now.shift(months=1).format(ISO8601)
        assert dm("+1Y").format(ISO8601) == now.shift(years=1).format(ISO8601)
        assert dm("+1y").format(ISO8601) == now.shift(years=1).format(ISO8601)

        assert dm("-1s").format(ISO8601) == now.shift(seconds=-1).format(ISO8601)
        assert dm("-1m").format(ISO8601) == now.shift(minutes=-1).format(ISO8601)
        assert dm("-1h").format(ISO8601) == now.shift(hours=-1).format(ISO8601)
        assert dm("-1d").format(ISO8601) == now.shift(days=-1).format(ISO8601)
        assert dm("-1w").format(ISO8601) == now.shift(weeks=-1).format(ISO8601)
        assert dm("-1M").format(ISO8601) == now.shift(months=-1).format(ISO8601)
        assert dm("-1Y").format(ISO8601) == now.shift(years=-1).format(ISO8601)
        assert dm("-1y").format(ISO8601) == now.shift(years=-1).format(ISO8601)

        assert dm("/s").format(ISO8601) == now.floor("second").format(ISO8601)
        assert dm("/m").format(ISO8601) == now.floor("minute").format(ISO8601)
        assert dm("/h").format(ISO8601) == now.floor("hour").format(ISO8601)
        assert dm("/d").format(ISO8601) == now.floor("day").format(ISO8601)
        assert dm("/w").format(ISO8601) == now.floor("week").format(ISO8601)
        assert dm("/M").format(ISO8601) == now.floor("month").format(ISO8601)
        assert dm("/Y").format(ISO8601) == now.floor("year").format(ISO8601)
        assert dm("/y").format(ISO8601) == now.floor("year").format(ISO8601)

        assert dm("/s", roundDown=False).format(ISO8601) == now.ceil("second").format(ISO8601)
        assert dm("/m", roundDown=False).format(ISO8601) == now.ceil("minute").format(ISO8601)
        assert dm("/h", roundDown=False).format(ISO8601) == now.ceil("hour").format(ISO8601)
        assert dm("/d", roundDown=False).format(ISO8601) == now.ceil("day").format(ISO8601)
        assert dm("/w", roundDown=False).format(ISO8601) == now.ceil("week").format(ISO8601)
        assert dm("/M", roundDown=False).format(ISO8601) == now.ceil("month").format(ISO8601)
        assert dm("/Y", roundDown=False).format(ISO8601) == now.ceil("year").format(ISO8601)
        assert dm("/y", roundDown=False).format(ISO8601) == now.ceil("year").format(ISO8601)

        assert dm("2016-01-01T14:00:00||/d").format(ISO8601) == "2016-01-01T00:00:00+00:00"
        assert dm("2016-01-01T14:00:00||/d", roundDown=False).format(ISO8601) == (
            "2016-01-01T23:59:59+00:00"
        )

        assert dm("now/d-1h").format(ISO8601) == now.floor("day").shift(hours=-1).format(ISO8601)
        assert dm("+1h").format(ISO8601) == now.shift(hours=1).format(ISO8601)
        assert dm("/M+2d").format(ISO8601) == now.floor("month").shift(days=2).format(ISO8601)
        assert dm("now/w+2d-2h").format(ISO8601) == now.floor("week").shift(
            days=2,
            hours=-2,
        ).format(ISO8601)
        assert dm("now/M+1w-2h+10s").format(ISO8601) == now.floor("month").shift(
            weeks=1,
            hours=-2,
            seconds=10,
        ).format(ISO8601)
        assert dm("now-1d/d").format(ISO8601) == now.shift(days=-1).floor("day").format(ISO8601)
        assert dm("now+1d/d").format(ISO8601) == now.shift(days=1).floor("day").format(ISO8601)
        assert dm("now-10d/d").format(ISO8601) == now.shift(days=-10).floor("day").format(ISO8601)
        assert dm("now+10d/d").format(ISO8601) == now.shift(days=10).floor("day").format(ISO8601)
        assert dm("now-29d/d").format(ISO8601) == now.shift(days=-29).floor("day").format(ISO8601)

    @freeze_time("2024-01-15T12:30:45Z")
    def test_future_and_past(self) -> None:
        now = arrow.utcnow()

        assert dm("+1s").format(ISO8601) == now.shift(seconds=1).format(ISO8601)
        assert dm("+1s+2m+3h").format(ISO8601) == now.shift(
            seconds=1,
            minutes=2,
            hours=3,
        ).format(ISO8601)
        assert dm("+1m").format(ISO8601) == now.shift(minutes=1).format(ISO8601)
        assert dm("+1m+5h").format(ISO8601) == now.shift(minutes=1, hours=5).format(ISO8601)
        assert dm("/d+1m+5h").format(ISO8601) == now.floor("day").shift(
            minutes=1,
            hours=5,
        ).format(ISO8601)
        assert dm("+1h").format(ISO8601) == now.shift(hours=1).format(ISO8601)
        assert dm("+1w").format(ISO8601) == now.shift(weeks=1).format(ISO8601)
        assert dm("+1w+12d").format(ISO8601) == now.shift(weeks=1, days=12).format(ISO8601)
        assert dm("+2y").format(ISO8601) == now.shift(years=2).format(ISO8601)
        assert dm("+2y+22d+4h").format(ISO8601) == now.shift(years=2, days=22, hours=4).format(
            ISO8601
        )

        assert dm("-3w").format(ISO8601) == now.shift(weeks=-3).format(ISO8601)
        assert dm("-3W").format(ISO8601) == now.shift(weeks=-3).format(ISO8601)
        assert dm("-3w-2d-6h").format(ISO8601) == now.shift(weeks=-3, days=-2, hours=-6).format(
            ISO8601
        )
        assert dm("-3w-2d-22h-36s").format(ISO8601) == now.shift(
            weeks=-3,
            days=-2,
            hours=-22,
            seconds=-36,
        ).format(ISO8601)
        assert dm("-6y-3w-2d-22h-36s").format(ISO8601) == now.shift(
            years=-6,
            weeks=-3,
            days=-2,
            hours=-22,
            seconds=-36,
        ).format(ISO8601)

    @freeze_time("2024-01-15T12:30:45Z")
    def test_other(self) -> None:
        now = arrow.utcnow()

        assert dm("now").datetime == now.datetime
        assert dm("now+1d").datetime == now.shift(days=1).datetime
        assert dm("/w").datetime == now.floor("week").datetime

        assert dm("now-2.5h").format(ISO8601) == now.shift(hours=-2.5).format(ISO8601)
        assert dm("now-2.5d").format(ISO8601) == now.shift(days=-2.5).format(ISO8601)

        assert dm("1451610061").format(ISO8601) == "2016-01-01T01:01:01+00:00"
        assert dm(1367900664).format(ISO8601) == "2013-05-07T04:24:24+00:00"

        with pytest.raises(DateMathException, match="Unable to parse epoch timestamps in millis"):
            dm("1451610061000")

        with pytest.raises(DateMathException, match="Unable to parse epoch timestamps in millis"):
            dm(1451610061000)

        assert dm("now").datetime == now.datetime

    def test_exceptions(self) -> None:
        invalid_inputs = ["+1,", "+1.", "+1ö", "+1ä", "+1ü", "+1ß", "2", "123"]

        for value in invalid_inputs:
            with pytest.raises(DateMathException):
                dm(value)

        for value in ["2", "123"]:
            with pytest.raises(DateMathException):
                datemath(value)

        with pytest.raises(DateMathException, match="is not a valid timeunit"):
            dm("+1,")
