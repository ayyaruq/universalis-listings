from piccolo.table import Table
from piccolo.columns import UUID, Boolean, ForeignKey, Integer, JSONB, Timestamp, Varchar


class Character(Table):
    content_id_sha256 = Varchar(primary_key=True, length=64, unique=True)
    world_id = Integer()
    name = Varchar(length=20) # maximum length of a character name is 20 characters


class Retainer(Table):
    content_id_sha256 = Varchar(primary_key=True, length=64, null=True, unique=True)
    world_id = Integer()
    name = Varchar(length=20)


class Listing(Table):
    listing_id = UUID(primary_key=True, unique=True)
    world_id = Integer()
    item_id = Integer()
    hq = Boolean()
    on_mannequin = Boolean()
    materia = JSONB() # we do not enforce schema here
    unit_price = Integer()
    quatity = Integer()
    dye_id = Integer()
    last_review_time = Timestamp()
    last_upload_time = Timestamp()
    creator = ForeignKey(references=Character, null=True) # can be NULL for non-crafted items
    retainer = ForeignKey(references=Retainer, null=False) # retainers must exist on the market
    seller = ForeignKey(references=Character, null=False) # seller must exist for a retainer
    live = Boolean()

