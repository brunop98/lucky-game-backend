from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.item import Item
from app.models.user import User


from app.models.user_item import UserItem


def user_has_item(db: Session, user: User, item: Item | str) -> bool:
    if isinstance(item, str):
        item = db.query(Item).filter(Item.slug == item).scalar()

    exists = (
        db.query(UserItem)
        .filter(
            UserItem.user_id == user.id,
            UserItem.item_id == item.id,
            UserItem.stack_size > 0
        )
        .scalar()
    )

    return exists is not None

