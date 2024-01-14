from typing import Tuple

from models.validation_error import ValidationError


def validate_units(
        city: str, country: str, units: str
) -> Tuple[str, str, str]:
    city = city.lower().strip()

    if not country:
        country = 'BGD'

    if len(country) not in (2, 3):
        error = f'Invalid country code: {country}. It must be a two or three-letter abbreviation.'
        raise ValidationError(status_code=400, error_msg=error)

    valid_units = {'standard', 'metric', 'imperial'}
    if units:
        units = units.strip().lower()
        if units not in valid_units:
            error = f"Invalid units '{units}'. It must be one of {valid_units}."
            raise ValidationError(status_code=400, error_msg=error)

    return city, country, units
