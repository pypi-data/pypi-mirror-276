from contextlib import contextmanager
import csv
from datetime import datetime, timezone
from enum import Enum
import operator
import re
import sys
from typing import Any, Callable, Iterable, Iterator, Optional

import pendulum
import rich
from typing_extensions import TypeAlias


SECS_PER_HOUR = 3600
HOURS_PER_DAY = 24
DAYS_PER_WEEK = 7
SECS_PER_DAY = SECS_PER_HOUR * HOURS_PER_DAY


#########
# ENUMS #
#########

class StrEnum(str, Enum):
    """Enum class whose __str__ representation is just a plain string value.
    NOTE: this class exists in the standard library in Python >= 3.11."""

    def __str__(self) -> str:
        return self.value


class NotGivenType(Enum):
    """Sentinel class for a value of "not given," when needed to distinguish it from None."""
    NotGiven = 'NotGiven'


NotGiven = NotGivenType.NotGiven


###################
# STRING HANDLING #
###################

def to_snake_case(name: str) -> str:
    """Converts an arbitrary string to snake case."""
    name = name.replace('"', '').replace("'", '')
    return re.sub(r'[^\w]+', '_', name.strip()).lower()

def prefix_match(token: str, match: str, minlen: int = 1) -> bool:
    """Returns True if token is a prefix of match and has length at least minlen."""
    n = len(token)
    return (n >= minlen) and (match[:n] == token)

def convert_number_words_to_digits(s: str) -> str:
    """Replaces occurrences of number words like 'one', 'two', etc. to their digital equivalents."""
    words_to_numbers = {
        'zero': '0',
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
    }
    pattern = re.compile(r'\b(' + '|'.join(words_to_numbers.keys()) + r')\b')
    return re.sub(pattern, lambda x: words_to_numbers[x.group()], s)

# function which matches a queried name against an existing name
NameMatcher: TypeAlias = Callable[[str, str], bool]
exact_match: NameMatcher = operator.eq

def whitespace_insensitive_match(name1: str, name2: str) -> bool:
    """Matches two strings, leading/trailing-whitespace-insensitively."""
    return name1.strip() == name2.strip()

def case_insensitive_match(name1: str, name2: str) -> bool:
    """Matches two strings, case- and leading/trailing-whitespace-insensitively."""
    return name1.strip().casefold() == name2.strip().casefold()

def fuzzy_match(name1: str, name2: str) -> bool:
    """Matches a queried name against a stored name, case-insensitively.
    This allows the first string to be a prefix of the second, if it is at least three characters long."""
    s1 = name1.strip().casefold()
    s2 = name2.strip().casefold()
    return (s1 == s2) or ((len(s1) >= 3) and s2.startswith(s1))

def first_name_match(matcher: NameMatcher, name1: str, names2: Iterable[str]) -> Optional[str]:
    """Given a NameMatcher, query name, and an iterable of names to compare against, returns the first name that matches (if there is one), otherwise None."""
    return next((name2 for name2 in names2 if matcher(name1, name2)), None)

def parse_string_set(s: str) -> Optional[set[str]]:
    """Parses a comma-separated string into a set of strings.
    Allows for quote delimiting so that commas can be escaped.
    Strips any leading or trailing whitespace from each string."""
    return {string.strip() for string in list(csv.reader([s]))[0]} or None


############
# DATETIME #
############

def get_current_time() -> datetime:
    """Gets the current time (timezone-aware)."""
    return datetime.now(timezone.utc).astimezone()

def get_duration_between(dt1: datetime, dt2: datetime) -> float:
    """Gets the duration (in days) between two datetimes."""
    return (dt2 - dt1).total_seconds() / SECS_PER_DAY

def human_readable_duration(days: float, prefer_days: bool = False) -> str:
    """Given a duration (in days), converts it to a human-readable string.
    This goes out to minute precision only.
    If prefer_days=True, show days and not weeks."""
    if days == 0:
        return '0 seconds'
    dur = pendulum.Duration(days=days)
    s = dur.in_words()
    if prefer_days and ('week' in s):
        s = re.sub(r'\d+ weeks?( \d+ days?)?', f'{dur.days} days', s)
    # hacky way to truncate the seconds
    return re.sub(r'\s+\d+ seconds?', '', s)


#########
# STYLE #
#########

def style_str(val: Any, color: str, bold: bool = False, italic: bool = False) -> str:
    """Renders a value as a rich-formatted string with a given color, bold, and italic settings."""
    tags = [('' if bold else 'not ') + 'bold', ('' if italic else 'not ') + 'italic', color]
    tag = ' '.join(tags)
    return f'[{tag}]{val}[/]'

def err_style(obj: object) -> str:
    """Renders an error as a rich-styled string."""
    s = str(obj)
    if s:
        s = s[0].upper() + s[1:]
    return style_str(s, 'red')


##########
# ERRORS #
##########

class KanbanError(ValueError):
    """Custom error type for Kanban errors."""

class UserInputError(KanbanError):
    """Class for user input errors."""


def exit_with_error(msg: str) -> None:
    """Exits the program with the given error message."""
    rich.print(f'[bold red]{msg}[/]', file=sys.stderr)
    sys.exit(1)

@contextmanager
def handle_error(*errtypes: type[Exception], msg: Optional[str] = None) -> Iterator[None]:
    """Context manager for catching an error of a certain type (or types), optionally displaying a message, then exiting the program."""
    try:
        yield
    except errtypes as e:
        msg = str(e) if (msg is None) else msg
        exit_with_error(msg)
