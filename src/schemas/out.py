from typing import Any

from pydantic import BaseModel

from .oid import Oid


class Out(BaseModel):
    id: Oid  # noqa: A003

    def __init__(self: Any, **data: Any) -> None:
        """Initializes an instance of the class.

        Args:
            self (MongoOut): The instance of the class.
            data (dict): A dictionary containing the data
                to be assigned to the instance.
        """
        if "_id" in data:
            data["id"] = str(data["_id"])
            del data["_id"]
        self.__dict__.update(data)
