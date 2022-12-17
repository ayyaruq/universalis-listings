from fastapi import APIRouter
from itertools import groupby
from uuid import uuid4

from app.models.listing.tables import Listing
from app.schemas.listing import ListingModel, ListingSummary

router = APIRouter()

# Define our groupby sort function
sort_by_item = lambda x: x['item_id']


@router.post("/listings", tags=["Internal"])
async def update_listings(listings: list[ListingsIn]):
    # Sort, and then group, by item ID
    data = sorted(listings, sort_by_item)
    buckets = groupby(data, sort_by_item)

    tx = Listing._meta.db.atomic()
    for item_id, entries in buckets:
        # For each item ID, we clear current listings
        tx.add(Listing
            .update({Band.live: False})
            .where(Listing.item_id == item_id))

        updates: list[ListingModel] = []
        for entry in entries:
            listing = ListingModel(**listing.to_dict())
            updates.append(listing)

        # insert list of new entries to DB
        tx.add(Listing.insert(updates))

    # Dispatch the transaction to commit the updates
    await tx.run()


@router.get("/listings/{item_id}", response_model=list[ListingSummary])
async def listings(item_id: int):
    ...


@router.get("/listing/{id}", response_model=ListingModel)
async def listing(id: str):
    ...


@router.delete("/listing/{id}", tags=["Internal"])
async def delete_listing(id: str):
    ...
