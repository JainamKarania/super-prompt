import uuid
from typing import Annotated

from fastapi import Depends, Header


def get_owner_id(x_owner_id: Annotated[uuid.UUID, Header()]) -> str:
    """The browser's anonymous ID. A missing or malformed header is a 422."""
    return str(x_owner_id)


OwnerDep = Annotated[str, Depends(get_owner_id)]
