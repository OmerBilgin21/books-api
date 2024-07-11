from typing import Annotated, Any

from bson import ObjectId
from pydantic_core import core_schema


class _ObjectIdPydanticAnnotation:
	@classmethod
	def __get_pydantic_core_schema__(
		cls,
		_: Any,
		__: Any,
	) -> core_schema.CoreSchema:
		def validate_from_str(input_value: str) -> ObjectId:
			return ObjectId(input_value)

		return core_schema.union_schema(
			[
				core_schema.is_instance_schema(ObjectId),
				core_schema.no_info_plain_validator_function(validate_from_str),
			],
			serialization=core_schema.to_string_ser_schema(),
		)


Oid = Annotated[ObjectId, _ObjectIdPydanticAnnotation]
