import os

from fastapi import FastAPI,HTTPException,Depends,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models ,crud
from schemas import URLBase

app=FastAPI()
frontend_url = os.getenv("FRONTEND_URL")
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
