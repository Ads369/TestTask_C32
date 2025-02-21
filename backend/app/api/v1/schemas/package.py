from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveFloat


class PackageType(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class PackageBase(BaseModel):
    name: str = Field(..., max_length=255)
    weight: PositiveFloat
    type_id: int
    content_cost: PositiveFloat = Field(gt=0)


class PackageCreate(PackageBase):
    user_session: Optional[str] = None


class PackageUpdate(PackageBase):
    delivery_cost: Optional[PositiveFloat] = None


class PackageOut(BaseModel):
    id: int
    # type: PackageType

    model_config = ConfigDict(from_attributes=True)
