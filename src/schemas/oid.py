from typing import Annotated

from bson import ObjectId as _ObjectId
from pydantic.functional_validators import AfterValidator


def check_object_id(value: str) -> str:
    """_summary_

    Args:
        value (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        str: _description_
    """
    invalid_msg = "Invalid ObjectId"
    if not _ObjectId.is_valid(value):
        raise ValueError(invalid_msg)
    return value


Oid = Annotated[str, AfterValidator(check_object_id)]
