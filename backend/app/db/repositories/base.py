from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

# T represents the model type (e.g., a SQLAlchemy model)
T = TypeVar("T")
# CreateSchemaType and UpdateSchemaType can represent the Pydantic schemas
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseRepository(ABC, Generic[T, CreateSchemaType, UpdateSchemaType]):
    """
    Abstract base repository defining the interface for CRUD operations.

    Concrete repository implementations must implement the following methods:
    - get: Retrieve a record by its ID.
    - list: Retrieve multiple records with optional pagination.
    - create: Create a new record using the provided input schema.
    - update: Update an existing record with the provided data.
    - delete: Delete a record by its ID.
    """

    @abstractmethod
    def get(self, id: Any) -> Optional[T]:
        """
        Retrieve a single record by its unique identifier.

        :param id: The unique identifier of the record.
        :return: The record if found, else None.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Retrieve a list of records with pagination.

        :param skip: The number of records to skip.
        :param limit: The maximum number of records to return.
        :return: A list of records.
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, obj_in: CreateSchemaType) -> T:
        """
        Create a new record based on the provided input schema.

        :param obj_in: The input data for creating the record.
        :return: The created record.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, db_obj: T, obj_in: UpdateSchemaType) -> T:
        """
        Update an existing record with the provided data.

        :param db_obj: The existing record instance.
        :param obj_in: The update data.
        :return: The updated record.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: Any) -> Optional[T]:
        """
        Delete a record by its unique identifier.

        :param id: The unique identifier of the record to delete.
        :return: The deleted record if deletion was successful, else None.
        """
        raise NotImplementedError
