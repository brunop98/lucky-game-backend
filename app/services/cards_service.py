import random
import re
from uuid import uuid4, UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.item import Item
from app.models.user import User


from app.models.card_hash import CardHash


# PROBABILITY
def get_rare_item_probability(db: Session, user: User, item_slug):
    # TODO
    return 0.5


def get_jackpot_probability(db: Session, user: User, item_slug):
    # TODO
    return 0.5


# HASH


def cancel_game_uuid(db: Session, user: User, game_uuid: UUID):
    db.query(CardHash).filter(CardHash.user_id == user.id, CardHash.id == game_uuid).update(
        {"canceled": True}
    )
    db.commit()
    return


def create_game_uuid(
    db: Session,
    user: User,
    item_slug: str | None = None,
) -> UUID:
    if item_slug is not None:
        exists = db.query(Item.slug).filter(Item.slug == item_slug).scalar()

        if exists is None:
            raise HTTPException(status_code=404, detail="Item not found")

    game_uuid = uuid4()

    db.add(
        CardHash(
            id=game_uuid,
            user_id=user.id,
            item_slug=item_slug,  # sempre string ou None
        )
    )

    db.commit()

    return game_uuid


def search_game_uuid(db: Session, user: User, item_slug):
    print("search")

    game_uuid = (
        db.query(CardHash)
        .filter(
            CardHash.user_id == user.id,
            CardHash.item_slug == item_slug,
            CardHash.used == False,
            CardHash.canceled == False,
        )
        .first()
    )
    if game_uuid:
        return game_uuid.id

    return


def get_game_uuid(
    db: Session,
    user: User,
    item_slug: str | None = None,
) -> UUID:
    print(f"item_slug: {item_slug}")
    if item_slug is None:
        return create_game_uuid(db, user)

    game_uuid = search_game_uuid(db, user, item_slug)
    if game_uuid is not None:
        return game_uuid

    return create_game_uuid(db, user, item_slug)
