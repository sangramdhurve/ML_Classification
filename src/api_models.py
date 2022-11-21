from typing import Union
from config.common_config import options
from pydantic import BaseModel, validator


class ScoringRequestData(BaseModel):
    total_visits: int
    total_time_spent_on_website: int
    page_views_per_visit: int
    lead_source: Union[str, None]
    last_activity: Union[str, None]
    specialization: Union[str, None]
    search: Union[str, None]
    newspaper: Union[str, None]
    last_notable_activity: Union[str, None]

    @validator("total_visits", "total_time_spent_on_website", "page_views_per_visit")
    def must_be_positive(cls, request):
        if request < 0:
            raise ValueError("total_visits", "total_time_spent_on_website", "page_views_per_visit must be positive")

        return request

    @validator("lead_source", "last_activity", "specialization", "search", "newspaper", "last_notable_activity")
    def must_be_valid_value(cls, value, values, config, field):

        valid_field_values = set(options["categorical_cols_and_all_unique_values"][field.name])
        if value is not None and value not in valid_field_values:
            raise ValueError(f"valid values for {field.name} are {valid_field_values}")

        return value


