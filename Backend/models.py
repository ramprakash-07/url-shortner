from sqlalchemy import Integer,Boolean,Column,String
from database import Base


class URL(Base):
    __tablename__="urls"

    id=Column(Integer, primary_key=True)
    Key= Column(String,unique=True,index=True)
    Value=Column(String,index=True)
    isactive=Column(Boolean,default=True)
    exptime=Column(String,default="00:30")
    clicks=Column(Integer,default=0)
