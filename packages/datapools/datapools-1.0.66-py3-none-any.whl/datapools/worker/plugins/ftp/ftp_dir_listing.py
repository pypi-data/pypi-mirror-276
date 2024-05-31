# taken from https://gist.github.com/robcowie/2575241

import datetime
import re
from ftplib import FTP
from ....common.logger import logger


months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def line_parser(line: str):
    """"""
    #'-rw-rw-r--  148 10006    10050     1422353 Jan 01 07:33 1231mstf.zip'
    #'-rw-rw-r--  145 10006    10050       87316 Aug 01  2009 0731m53a.zip'
    # {'a': '144', 'c': '10050', 'b': '10006', 'd': '336285', 'month': 'Jan', 'time': '08:05', 'filename': '0129m53d.zip', 'day': '30', 'permissions': '-rw-r--r--'}
    # print(f"parsing '{line}'")
    # print(line.encode("utf-8").hex())

    parts = [
        r"(?P<permissions>[-a-z]{10})",
        r"(?P<a>[0-9]*)",
        r"(?P<b>[\w]*)",
        r"(?P<c>[\w]*)",
        r"(?P<d>[0-9]*)",
        r"(?P<month>[\w]*)",
        r"(?P<day>[0-9]{2})",
        r"(?P<time>[0-9]{2}:[0-9]{2}|[0-9]{4})",
        r"(?P<filename>[\w\.\-\(\)\,\.]*)",
    ]
    patt = r"\s+".join(parts)
    # print(patt)

    matches = re.match(patt, line.strip())
    if not matches:
        raise AttributeError
    groups = matches.groupdict()

    ## Account for year vs time
    if ":" in groups["time"]:
        hour, minute = [int(i) for i in groups["time"].split(":")]
        # TODO: Is this correct? Time, so assume this year?
        year = datetime.datetime.now().year
    else:
        hour = minute = -1
        year = int(groups["time"])

    ## Get month int
    month = months[groups["month"]]
    day = int(groups["day"])

    if hour and minute:
        groups["datetime"] = datetime.datetime(day=day, month=month, year=year, hour=hour, minute=minute)
    else:
        groups["datetime"] = datetime.datetime(day=day, month=month, year=year)
    return groups


class DirectoryListing(object):
    """FTP directory listing"""

    def __init__(self):
        self.contents = []

    def __call__(self, line):
        """"""
        try:
            self.contents.append(line_parser(line))
        except AttributeError:
            logger.error(f'Failed parse dir line "{line}"')

    def __iter__(self):
        return iter(self.contents)

    def __len__(self):
        return len(self.contents)

    def by_date(self):
        """Iterate over the directory contents by modification date"""
        return iter(sorted(self.contents, key=lambda x: x["datetime"]))

    @staticmethod
    def is_dir(permissions):
        """"""
        return permissions[0:1] == "d"
