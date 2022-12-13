from fastapi import APIRouter
from piccolo.utils.pydantic import create_pydantic_model
from pydantic import BaseModel
from uuid import uuid4

from listings.tables import Listing

ListingModel = create_pydantic_model(Listing, nested=True)

router = APIRouter()

@router.post("/")
async def create_listing():


@router.get("/")
async def listings():


@router.get("/{id}")
async def listing(id: str):
