
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

from simplesapi import lifespan, settings
from simplesapi.auto_routing import register_routes

class SimplesConfig(BaseModel):
    verbose: Optional[bool] = Field(default=False)
    base_path: Optional[str] = Field(default="/")
    routes_path: Optional[str] = Field(default="/routes")
    redis_url: Optional[str] = Field(default=settings.SIMPLESAPI_REDIS_URL)
    redis_ssl: Optional[bool] = Field(default=settings.SIMPLESAPI_REDIS_SSL)
    database_connection_string: Optional[str] = Field(default=settings.SIMPLESAPI_DB_CONN)

class SimplesAPI(FastAPI):
    def __init__(self, simples=SimplesConfig(), **kwargs):
        self.simples = simples
        super().__init__(lifespan=lifespan, **kwargs)
        if simples.routes_path:
            register_routes(self,simples.routes_path)

        
