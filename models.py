import typing as ty
from pydantic import BaseModel


class UserConfig(BaseModel):
    keyid: str
    secrets: ty.Dict[str, str]
