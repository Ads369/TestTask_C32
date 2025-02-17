from datetime import datetime
from typing import Any, Union

from pydantic import BaseModel, ConfigDict


class HealthCheckResponse(BaseModel):
    status: str
    version: str
    uptime: float
    timestamp: datetime
    dependencies: dict[str, dict[str, Union[str, int, float]]]

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
