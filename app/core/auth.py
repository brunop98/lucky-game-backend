from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session, joinedload

from app.core.deps import get_db
from app.core.security import ALGORITHM, SECRET_KEY
from app.db.models.user import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    user = db.query(User).options(joinedload(User.wallet)).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return user
