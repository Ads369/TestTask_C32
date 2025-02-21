from datetime import datetime
from typing import Any, Union

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str
    version: str
    uptime: float
    timestamp: datetime
    dependencies: dict[str, dict[str, Union[str, int, float]]]

    @property
    def dict_with_formats(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "version": self.version,
            "uptime": self.uptime,
            "timestamp": self.timestamp.isoformat(),
            "dependencies": self.dependencies,
        }

    # model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
