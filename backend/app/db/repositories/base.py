from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

# Define more specific type variables
ModelType = TypeVar("ModelType", bound=DeclarativeBase)
OutputSchemaType = TypeVar("OutputSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseReadRepository(ABC, Generic[ModelType, OutputSchemaType]):
    """
    Base Repository for read operations.

    Generic Parameters:
        ModelType: SQLAlchemy model class
        OutputSchemaType: Pydantic model for output data
    """

    @abstractmethod
    async def get(self, id: Any) -> Optional[OutputSchemaType]:
        """
        Retrieve a single record by its ID.

        Args:
            id: Primary key of the record

        Returns:
            Optional[OutputSchemaType]: The found record as a Pydantic model or None
        """
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> List[OutputSchemaType]:
        """
        Retrieve multiple records with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[OutputSchemaType]: List of records as Pydantic models
        """
        pass


class BaseWriteRepository(
    ABC, Generic[ModelType, OutputSchemaType, CreateSchemaType, UpdateSchemaType]
):
    """
    Base Repository for write operations.

    Generic Parameters:
        ModelType: SQLAlchemy model class
        OutputSchemaType: Pydantic model for output data
        CreateSchemaType: Pydantic model for creation data
        UpdateSchemaType: Pydantic model for update data
    """

    @abstractmethod
    async def create(self, obj_in: CreateSchemaType) -> OutputSchemaType:
        """
        Create a new record.

        Args:
            obj_in: Pydantic model containing the data for creation

        Returns:
            OutputSchemaType: The created record as a Pydantic model
        """
        pass

    @abstractmethod
    async def update(
        self, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> OutputSchemaType:
        """
        Update an existing record.

        Args:
            db_obj: Existing database model instance
            obj_in: Pydantic model containing the update data

        Returns:
            OutputSchemaType: The updated record as a Pydantic model
        """
        pass

    @abstractmethod
    async def delete(self, id: Any) -> Optional[OutputSchemaType]:
        """
        Delete a record by its ID.

        Args:
            id: Primary key of the record to delete

        Returns:
            Optional[OutputSchemaType]: The deleted record as a Pydantic model or None
        """
        pass


class BaseCRUDRepository(
    BaseReadRepository[ModelType, OutputSchemaType],
    BaseWriteRepository[
        ModelType, OutputSchemaType, CreateSchemaType, UpdateSchemaType
    ],
    ABC,
):
    """
    Base Repository combining both read and write operations for full CRUD functionality.

    Generic Parameters:
        ModelType: SQLAlchemy model class (must inherit from DeclarativeBase)
        OutputSchemaType: Pydantic model for output data
        CreateSchemaType: Pydantic model for creation data
        UpdateSchemaType: Pydantic model for update data

    Example:
        class UserRepository(BaseCRUDRepository[
            UserModel,           # SQLAlchemy model
            UserSchema,          # Pydantic model for output
            UserCreateSchema,    # Pydantic model for creation
            UserUpdateSchema     # Pydantic model for updates
        ]):
            pass
    """

    pass
