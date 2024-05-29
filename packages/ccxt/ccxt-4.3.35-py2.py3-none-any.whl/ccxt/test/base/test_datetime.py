import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------

import ccxt  # noqa: F402
from ccxt.base.decimal_to_precision import ROUND_UP, ROUND_DOWN  # noqa F401

# ----------------------------------------------------------------------------

# @ts-nocheck

exchange = ccxt.Exchange({
    'id': 'regirock',
})

# ----------------------------------------------------------------------------

assert exchange.iso8601(514862627000) == '1986-04-26T01:23:47.000Z'
assert exchange.iso8601(514862627559) == '1986-04-26T01:23:47.559Z'
assert exchange.iso8601(514862627062) == '1986-04-26T01:23:47.062Z'

assert exchange.iso8601(0) == '1970-01-01T00:00:00.000Z'

assert exchange.iso8601(-1) is None
assert exchange.iso8601() is None
assert exchange.iso8601(None) is None
assert exchange.iso8601('') is None
assert exchange.iso8601('a') is None
assert exchange.iso8601({}) is None

# ----------------------------------------------------------------------------

assert exchange.parse8601('1986-04-26T01:23:47.000Z') == 514862627000
assert exchange.parse8601('1986-04-26T01:23:47.559Z') == 514862627559
assert exchange.parse8601('1986-04-26T01:23:47.062Z') == 514862627062

assert exchange.parse8601('1986-04-26T01:23:47.06Z') == 514862627060
assert exchange.parse8601('1986-04-26T01:23:47.6Z') == 514862627600

assert exchange.parse8601('1977-13-13T00:00:00.000Z') is None
assert exchange.parse8601('1986-04-26T25:71:47.000Z') is None

assert exchange.parse8601('3333') is None
assert exchange.parse8601('Sr90') is None
assert exchange.parse8601('') is None
assert exchange.parse8601() is None
assert exchange.parse8601(None) is None
assert exchange.parse8601({}) is None
assert exchange.parse8601(33) is None

# ----------------------------------------------------------------------------

assert exchange.parse_date('1986-04-26 00:00:00') == 514857600000
assert exchange.parse_date('1986-04-26T01:23:47.000Z') == 514862627000
assert exchange.parse_date('1986-13-13 00:00:00') is None
# GMT formats
assert exchange.parse_date('Mon, 29 Apr 2024 14:00:17 GMT') == 1714399217000
assert exchange.parse_date('Mon, 29 Apr 2024 14:09:17 GMT') == 1714399757000
assert exchange.parse_date('Sun, 29 Dec 2024 01:01:10 GMT') == 1735434070000
assert exchange.parse_date('Sun, 29 Dec 2024 02:11:10 GMT') == 1735438270000
assert exchange.parse_date('Sun, 08 Dec 2024 02:03:04 GMT') == 1733623384000


assert exchange.roundTimeframe('5m', exchange.parse8601('2019-08-12 13:22:08'), ROUND_DOWN) == exchange.parse8601('2019-08-12 13:20:00')
assert exchange.roundTimeframe('10m', exchange.parse8601('2019-08-12 13:22:08'), ROUND_DOWN) == exchange.parse8601('2019-08-12 13:20:00')
assert exchange.roundTimeframe('30m', exchange.parse8601('2019-08-12 13:22:08'), ROUND_DOWN) == exchange.parse8601('2019-08-12 13:00:00')
assert exchange.roundTimeframe('1d', exchange.parse8601('2019-08-12 13:22:08'), ROUND_DOWN) == exchange.parse8601('2019-08-12 00:00:00')

assert exchange.roundTimeframe('5m', exchange.parse8601('2019-08-12 13:22:08'), ROUND_UP) == exchange.parse8601('2019-08-12 13:25:00')
assert exchange.roundTimeframe('10m', exchange.parse8601('2019-08-12 13:22:08'), ROUND_UP) == exchange.parse8601('2019-08-12 13:30:00')
assert exchange.roundTimeframe('30m', exchange.parse8601('2019-08-12 13:22:08'), ROUND_UP) == exchange.parse8601('2019-08-12 13:30:00')
assert exchange.roundTimeframe('1h', exchange.parse8601('2019-08-12 13:22:08'), ROUND_UP) == exchange.parse8601('2019-08-12 14:00:00')
assert exchange.roundTimeframe('1d', exchange.parse8601('2019-08-12 13:22:08'), ROUND_UP) == exchange.parse8601('2019-08-13 00:00:00')

# todo:
# $self->assertSame(null, Exchange::iso8601(null))
# $self->assertSame(null, Exchange::iso8601(False))
# $self->assertSame(null, Exchange::iso8601([]))
# $self->assertSame(null, Exchange::iso8601('abracadabra'))
# $self->assertSame(null, Exchange::iso8601('1.2'))
# $self->assertSame(null, Exchange::iso8601(-1))
# $self->assertSame(null, Exchange::iso8601('-1'))
# $self->assertSame('1970-01-01T00:00:00.000+00:00', Exchange::iso8601(0))
# $self->assertSame('1970-01-01T00:00:00.000+00:00', Exchange::iso8601('0'))
# $self->assertSame('1986-04-25T21:23:47.000+00:00', Exchange::iso8601(514848227000))
# $self->assertSame('1986-04-25T21:23:47.000+00:00', Exchange::iso8601('514848227000'))

# $self->assertSame(null, Exchange::parse_date(null))
# $self->assertSame(null, Exchange::parse_date(0))
# $self->assertSame(null, Exchange::parse_date('0'))
# $self->assertSame(null, Exchange::parse_date('+1 day'))
# $self->assertSame(null, Exchange::parse_date('1986-04-25T21:23:47+00:00 + 1 week'))
# $self->assertSame(null, Exchange::parse_date('1 february'))
# $self->assertSame(null, Exchange::parse_date('1986-04-26'))
# $self->assertSame(0, Exchange::parse_date('1970-01-01T00:00:00.000+00:00'))
# $self->assertSame(514848227000, Exchange::parse_date('1986-04-25T21:23:47+00:00'))
# $self->assertSame(514848227000, Exchange::parse_date('1986-04-26T01:23:47+04:00'))
# $self->assertSame(514848227000, Exchange::parse_date('25 Apr 1986 21:23:47 GMT'))
# $self->assertSame(514862627000, Exchange::parse_date('1986-04-26T01:23:47.000Z'))
# $self->assertSame(514862627123, Exchange::parse_date('1986-04-26T01:23:47.123Z'))
