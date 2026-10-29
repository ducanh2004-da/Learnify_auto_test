from pydantic import BaseModel
from typing import List, Optional, Dict, Any
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    message: str
    success: bool

class GraphQLError(BaseModel):
    message: str
    locations: Optional[List[Dict[str, int]]] = None
    path: Optional[List[str]] = None

class GraphQLResponse(BaseModel):
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[GraphQLError]] = None

class RegisterResponse(BaseModel):
    message: str
    success: bool