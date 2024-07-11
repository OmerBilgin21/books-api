from typing import Any, ClassVar

from bson import ObjectId
from pydantic import BaseModel

from .oid import Oid


class MongoBase(BaseModel):
	class Config:
		"""Add an encoder to pytantic's base model"""

		json_encoders: ClassVar[dict] = {
			ObjectId: lambda obj_id: str(obj_id),
		}


class Out(MongoBase):
	id: Oid

	def __init__(self: Any, **data: Any) -> None:
		"""Convert the key for id and cast it to string.

		Args:
			self (Any): The instance of the class.
			data (Any): A dictionary containing the data
				to be assigned to the instance.
		"""
		if "_id" in data:
			data["id"] = str(data["_id"])
			del data["_id"]
		super().__init__(**data)
