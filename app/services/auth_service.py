from sqlalchemy.orm import Session
from app.models.user import User
from app.models.wallet import Wallet

INITIAL_BALANCE = 100

def get_or_create_user_with_wallet(
    db: Session,
    facebook_id: str,
    name: str
):
    user = (
        db.query(User)
        .filter(User.facebook_id == facebook_id)
        .first()
    )

    if not user:
        user = User(
            facebook_id=facebook_id,
            name=name
        )
        db.add(user)
        db.flush()  # garante user.id

        wallet = Wallet(
            user_id=user.id,
            balance=INITIAL_BALANCE
        )
        db.add(wallet)
    else:
        wallet = (
            db.query(Wallet)
            .filter(Wallet.user_id == user.id)
            .first()
        )

    db.commit()

    return user, wallet
