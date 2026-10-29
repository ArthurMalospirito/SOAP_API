from pydantic import BaseModel
from typing import Optional, Any

class SuccessResponse(BaseModel):
    success: bool = True
    data: Optional[Any]=None
    message: Optional[str] = None