from fastapi import FastAPI,HTTPException,Depends,Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from key_database import keyset
import models ,crud
from schemas import URLBase

app=FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:    
        db.close()


@app.get("/")
def root():
    return {"WElcome":"Haha "}
@app.get("/urls")
def listurls(db:Session=Depends(get_db)):
    return crud.listurls(db)

@app.post("/urls")
def addurls(data: URLBase, db: Session = Depends(get_db)):
    if data.Key in keyset:
        return HTTPException(status_code=409 ,detail="Alredy exist")
    return crud.create(db, data.Value, data.Key)
    

@app.get("/{short_key}")
def redirect_to_url(short_key: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.Key == short_key).first()

    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=db_url.Value, status_code=302)

@app.delete("/{short_key}")
def deleteurl(short_key: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.Key == short_key).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return crud.crud_del_url(db, db_url)
