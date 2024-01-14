import datetime
import uuid
from typing import List

from models.location import Location
from models.reports import Report

__reports: List[Report] = []


def get_report() -> List[Report]:
    return list(__reports)


def add_report(description: str, location: Location) -> object:
    now = datetime.datetime.now()
    report = Report(id = str(uuid.uuid4()),
                    location=location,
                    description=description,
                    created_date=now)

    # Simulating saving to the DB
    __reports.append(report)
    __reports.sort(key=lambda r: r.created_date, reverse=True)
    return report
