import calendar
import os
import sys
from datetime import datetime, timedelta
from importlib.metadata import version as get_version
from typing import List, Tuple

import typer
from dateutil.relativedelta import relativedelta
from ics import Calendar, Event

help_msg: str = "Create an ical file with the shifts for the next month"
app = typer.Typer(add_completion=False, help=help_msg)


@app.command(name="version", help="Shows the current version")
def version() -> None:
    typer.echo(get_version("shifts"))


@app.command(help=help_msg)
def cmd(shifts: str):
    c = Calendar()
    year, month = next_year_month()
    try:
        clean_shifts = validate_shifts(shifts, year, month)
    except ValueError as e:
        typer.echo(f"Invalid shifts found, {str(e)}", err=True)
        sys.exit(1)

    for day, shift in enumerate(clean_shifts, start=1):
        if shift == "D":
            continue
        s = Shift(shift, year, month, day)
        c.events.add(
            Event(
                name=s.name,
                begin=datetime(
                    year, s.begin_month, s.begin_day, s.begin_hour, s.begin_minute, 0
                ),
                end=datetime(year, s.end_month, s.end_day, s.end_hour, s.end_minute, 0),
            )
        )

    schedule_file = os.getenv("SCHEDULE_FILE")
    if not schedule_file:
        schedule_file = f"schedule_{year}_{month}.ics"

    with open(schedule_file, "w") as my_file:
        my_file.writelines(c.serialize_iter())

    print(f"Calendar file '{schedule_file}' created successfully.")


def next_year_month() -> Tuple[int, int]:
    now = datetime.now()
    next_month = now + relativedelta(months=1)
    return next_month.year, next_month.month


def validate_shifts(shifts, year, month) -> List[str]:
    """
    Receives a string with the shifts and validates those, and transforms into
     a list of shifts.

    :param shifts: The string with of shifts to validate
    :param year: The year the shifts will be in
    :param month: The month the shifts will be in
    :return: A list of shifts
    """

    _, number_of_days = calendar.monthrange(year, month)
    shifts = [item.upper() for item in list(shifts) if item.strip()]  # type: ignore
    if len(shifts) != number_of_days:
        raise ValueError(f"expected {number_of_days} shifts, but got {len(shifts)}")

    return shifts


class Shift:
    def __init__(self, shift, year, month, day):
        self._shift = shift

        start_hour = {
            "M": 8,
            "T": 14,
            "N": 20,
        }
        start_minute = {
            "M": 0,
            "T": 30,
            "N": 0,
        }
        delta_end_hour = {
            "M": 6,
            "T": 6,
            "N": 12,
        }
        delta_end_minute = {
            "M": 30,
            "T": 0,
            "N": 30,
        }

        self._start = datetime(year, month, day, start_hour[shift], start_minute[shift])
        self._end = self._start + timedelta(
            hours=delta_end_hour[shift], minutes=delta_end_minute[shift]
        )

    @property
    def name(self) -> str:
        if self._shift == "N":
            return "Noite"
        if self._shift == "T":
            return "Tarde"
        return "Manhã"

    @property
    def begin_month(self) -> int:
        return self._start.month

    @property
    def begin_day(self) -> int:
        return self._start.day

    @property
    def begin_hour(self) -> int:
        return self._start.hour

    @property
    def begin_minute(self) -> int:
        return self._start.minute

    @property
    def end_month(self) -> int:
        return self._end.month

    @property
    def end_day(self) -> int:
        return self._end.day

    @property
    def end_hour(self) -> int:
        return self._end.hour

    @property
    def end_minute(self) -> int:
        return self._end.minute
