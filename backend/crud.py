from sqlalchemy.orm import Session

from . import models, schemas


def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()


def get_account_by_email(db: Session, email: str):
    return db.query(models.Account).filter(models.Account.email == email).first()


def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()


def create_account(db: Session, account: schemas.AccountCreate):
    fake_hashed_password = account.password + "notreallyhashed"
    db_account = models.Account(email=account.email, hashed_password=fake_hashed_password)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account