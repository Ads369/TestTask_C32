from pydantic import BaseModel, ConfigDict


class PackageBase(BaseModel):
    name: str
    weight: float
    type_id: int
    content_cost: float


class PackageCreate(PackageBase):
    pass


class Package(PackageBase):
    id: int
    delivery_cost: float | None
    type_name: str

    model_config = ConfigDict(from_attributes=True)


class PackageType(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
