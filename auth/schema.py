from typing import Optional
from pydantic import BaseModel #, BaseConfig

class TokenData(BaseModel):
    username: Optional[str] = None

    #class Config: 
     #   BaseConfig.arbitrary_types_allowed = True

#BaseConfig.arbitrary_types_allowed = True