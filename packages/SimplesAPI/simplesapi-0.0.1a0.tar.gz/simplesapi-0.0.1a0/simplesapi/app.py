
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

from simplesapi.auto_routing import register_routes

class _Simples(BaseModel):
    verbose: bool
    base_path: Optional[str] = Field(default="/")
    redis_conn: Optional[str] = Field(default=None)
    postgres_conn: Optional[str] = Field(default=None)
    mysql_conn: Optional[str] = Field(default=None)

class SimplesAPI(FastAPI):
    def __init__(self, title="SimplesAPI", version="0.1.0", routes_path=None, base_path=None, redis_conn=None, postgres_conn=None, mysql_conn=None, verbose=False):
        super().__init__(title=title, version=version)
        self.simples = _Simples(verbose=verbose)
        if routes_path:
            register_routes(self,routes_path)

    def validate_simples(self):
        ...