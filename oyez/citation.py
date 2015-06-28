"""Manipulate citations"""
import functools
import re

from oyez import lookup

us_reports_citation_re = re.compile(r'^([0-9]{1,4})[_ ]U\.?S\.?[ _]([0-9]{1,4})')
federal_reporter_citation_re = re.compile(r'^([0-9]{1,4})[_ ]F\.?([1-9]+)d\.?[ _]([0-9]{1,4})')


@functools.total_ordering
class FederalReporterCitation:
    """Helper class to deal with ordering of Federal Reporter citations"""

    __slots__ = ('volume', 'series', 'page')

    def __init__(self, volume, series, page):
        self.volume, self.series, self.page = int(volume), int(series), int(page)

    @classmethod
    def from_str(cls, s):
        match = federal_reporter_citation_re.match(s.strip())
        if match is None:
            raise ValueError("Expected Federal Reporter citation, found: {}".format(s))
        return cls(*match.groups())

    @property
    def year(self):
        return lookup.federal_reporter_citation_year_lookup[(self.series, self.volume)]

    def __repr__(self):
        return "{} F.{}d {}".format(self.volume, self.series, self.page)

    def __hash__(self):
        return hash((self.series, self.volume, self.page))

    def __eq__(self, other):
        return (self.series, self.volume, self.page) == (other.series, other.volume, other.page)

    def __lt__(self, other):
        return (self.series, self.volume, self.page) < (other.series, other.volume, other.page)


@functools.total_ordering
class USReportsCitation:
    """Helper class to deal with US Reports citations"""

    __slots__ = ('volume', 'page')

    def __init__(self, volume, page):
        self.volume, self.page = int(volume), int(page)

    @classmethod
    def from_str(cls, s):
        volume, page = (int(i) for i in us_reports_citation_re.match(s.strip()).groups())
        return cls(volume, page)

    @property
    def year(self):
        return lookup.us_reports_citation_year_lookup[self.volume]

    def __repr__(self):
        return "{} U.S. {}".format(self.volume, self.page)

    def __hash__(self):
        return hash((self.volume, self.page))

    def __eq__(self, other):
        return (self.volume, self.page) == (other.volume, other.page)

    def __lt__(self, other):
        return (self.volume, self.page) < (other.volume, other.page)
