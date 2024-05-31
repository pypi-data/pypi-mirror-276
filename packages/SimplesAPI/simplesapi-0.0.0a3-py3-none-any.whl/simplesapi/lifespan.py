from contextlib import asynccontextmanager
from simplesapi.app import SimplesAPI

database = None

@asynccontextmanager
async def lifespan(app: SimplesAPI):
    database = {}
    yield
