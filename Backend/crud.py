import keygenerator
import database,models
from sqlalchemy.orm import Session

def validate(url):
    return bool(url)

def create(db:Session,url,key):
    if validate(url):
        
        secretkey=keygenerator.generate_short_key(6) if key==None else key
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
