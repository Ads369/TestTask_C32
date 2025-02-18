from database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class PackageType(Base):
    __tablename__ = "package_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)


class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True, index=True)
    user_session = Column(String(255), index=True)
    name = Column(String(255))
    weight = Column(Float)
    type_id = Column(Integer, ForeignKey("package_types.id"))
    content_cost = Column(Float)
    delivery_cost = Column(Float, nullable=True)

    type = relationship("PackageType")
