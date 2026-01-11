from uuid import  UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.item import Item
from app.models.user import User


from app.models.user_item import UserItem


def user_has_item(db: Session, user: User, item: Item | str) -> UUID:
    if type(item) == str:
        item = db.query(Item).filter(Item.slug == item).scalar()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    exists = (
        db.query(UserItem)
        .filter(UserItem.user_id == user.id, UserItem.item_id == item.id, UserItem.stack_size > 0)
        .scalar()
    )

    return {
        "hasItem": exists is not None
    }
