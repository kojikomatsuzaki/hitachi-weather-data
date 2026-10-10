"""Strict, read-only worksheet layout detection for historical observations.

This module does not synthesize unobserved hourly measurements.
"""
from dataclasses import dataclass
from typing import Any

THREE_HOURLY = tuple(range(3, 25, 3))
HOURLY = tuple(range(1, 25))
DAYLIGHT = tuple(range(4, 21))
KNOWN_SCHEDULES = (THREE_HOURLY, HOURLY, DAYLIGHT)


@dataclass(frozen=True)
class ObservationLayout:
    header_row: int
    hours: tuple[int, ...]
    columns: tuple[int, ...]
    summary_columns: dict[str, int]


def as_hour(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)) and float(value).is_integer():
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def detect_observation_layout(sheet, *, expected_schedules=KNOWN_SCHEDULES,
                              start_row=1, end_row=None, summary_labels=()):
    """Validate an exact B-column hour sequence and adjacent summary headers.

    A matched prefix followed by an additional numeric hour is rejected, as is
    an ambiguous match. The caller must explicitly allow the expected schedule.
    """
    if end_row is None:
        end_row = min(sheet.max_row, start_row + 8)
    matches = []
    for row in range(start_row, min(sheet.max_row, end_row) + 1):
        for schedule in expected_schedules:
            observed = tuple(as_hour(sheet.cell(row, col).value)
                             for col in range(2, len(schedule) + 2))
            if observed != tuple(schedule):
                continue
            next_value = as_hour(sheet.cell(row, len(schedule) + 2).value)
            if next_value is not None and 1 <= next_value <= 24:
                raise ValueError(f"Unexpected extra hour at {sheet.title}!{row}")
            summary = {}
            for offset, label in enumerate(summary_labels, start=len(schedule) + 2):
                actual = str(sheet.cell(row, offset).value or "").strip()
                if actual != label:
                    raise ValueError(
                        f"Summary header mismatch {sheet.title}!{sheet.cell(row, offset).coordinate}: "
                        f"expected {label!r}, got {actual!r}"
                    )
                summary[label] = offset
            matches.append(ObservationLayout(
                row, tuple(schedule), tuple(range(2, len(schedule) + 2)), summary))
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one verified hour layout in {sheet.title!r}; "
            f"found {len(matches)}")
    return matches[0]


def extract_observed_cells(sheet, layout, year, month, convert):
    """Extract only scheduled hours; no cells are created for other hours."""
    import calendar
    days = calendar.monthrange(year, month)[1]
    rows = {}
    for row in range(layout.header_row + 1, sheet.max_row + 1):
        day = as_hour(sheet.cell(row, 1).value)
        if day is not None and 1 <= day <= days and day not in rows:
            rows[day] = row
            if len(rows) == days:
                break
    if len(rows) != days:
        raise ValueError(f"Expected {days} days, found {len(rows)} in {sheet.title}")
    return {(day, hour): convert(sheet.cell(row, col).value)
            for day, row in rows.items()
            for hour, col in zip(layout.hours, layout.columns)}
