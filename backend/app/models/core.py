
"""Core data that exist in all Models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CoreModel(BaseModel):
    """Any common logic to be shared by all models."""

    pass


class IDModelMixin(BaseModel):
    """ID data."""

    id: int