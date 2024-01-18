from typing import Optional, List

import fastapi
from fastapi import Depends

from models.location import Location
from models.reports import Report, ReportSubmittal
from models.validation_error import ValidationError
from services import weather_service, report_service

router = fastapi.APIRouter()


@router.get('/api/weather/{city}')
async def weather(loc: Location = Depends(),
                  units: Optional[str] = 'metric'):
    try:
        return await weather_service.get_report(loc.city, loc.country, units)
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)


@router.get('/api/reports', name='all_reports',response_model=List[Report])
def report_get() -> List[Report]:
    return report_service.get_report()


@router.post('/api/reports', name='all_reports',status_code=201,response_model=Report)
def reports_post(report_submittal: ReportSubmittal) -> object:
    d = report_submittal.description
    loc = report_submittal.location
    return report_service.add_report(d, loc)
