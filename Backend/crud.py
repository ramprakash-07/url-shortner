import keygenerator
import database,models
from fastapi import HTTPException
from sqlalchemy.orm import Session

def validate(url):
    return bool(url)

def checkcollision(db: Session, key):
    return db.query(models.URL).filter(models.URL.Key == key).first() is not None

def create(db:Session,url,key):
    url = str(url)
    if validate(url):
        if key is not None:
            if checkcollision(db, key):
                raise HTTPException(status_code=409, detail="Already exists")

        if key==None:
            secretkey=keygenerator.generate_short_key(url)
        else:
            secretkey=key

        dburl=models.URL(Value=url,Key=secretkey)
        db.add(dburl)
        db.commit()
        db.refresh(dburl)
        return dburl


def listurls(db:Session):
    return db.query(models.URL).all()


def crud_del_url(db: Session, db_url):
    db.delete(db_url)
    db.commit()
    return {"message": "URL deleted"}
