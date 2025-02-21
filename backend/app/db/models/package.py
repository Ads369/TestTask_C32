from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    weight = Column(Float())
    content_cost = Column(Float())
    delivery_cost = Column(Float(), nullable=True)

    type_id = Column(Integer, ForeignKey("package_types.id"))
    type = relationship("PackageType")

    user_session = Column(String(36), ForeignKey("user_sessions.id"))
