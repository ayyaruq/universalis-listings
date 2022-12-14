from fastapi import APIRouter
from piccolo.utils.pydantic import create_pydantic_model
from pydantic import BaseModel
from uuid import uuid4

from listings.tables import Listing

ListingModel = create_pydantic_model(Listing, nested=True)

router = APIRouter()

@router.post("/listings")
async def update_listings():


@router.get("/listings/{item_id}")
async def listings(item_id: str):


@router.get("/listing/{id}")
async def listing(id: str):

