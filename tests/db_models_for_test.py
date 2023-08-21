import enum
from sqlalchemy import Column, Double
from sqlalchemy.orm import declarative_base

from sqlalchemy.types import BigInteger, Boolean, Date, DateTime, Enum
from sqlalchemy.types import Float, Integer, Interval, LargeBinary
from sqlalchemy.types import Numeric
from sqlalchemy.types import SmallInteger, String, Text, Time, Unicode, UnicodeText, Uuid


Base = declarative_base()


class EnumClass(enum.Enum):
    A = 1
    B = 2
    C = 3


class TypeTest(Base):
    __tablename__ = "type_test"
    id_ = Column(Integer, primary_key=True)
    big_integer = Column(BigInteger)
    boolean = Column(Boolean)
    date = Column(Date)
    date_time = Column(DateTime)
    double_ = Column(Double)
    enum = Column(Enum(EnumClass))
    float_ = Column(Float)
    integer = Column(Integer)
    interval = Column(Interval)
    large_binary = Column(LargeBinary)
    numeric = Column(Numeric)
    small_integer = Column(SmallInteger)
    string = Column(String)
    text = Column(Text)
    time = Column(Time)
    unicode = Column(Unicode)
    unicode_text = Column(UnicodeText)
    uuid = Column(Uuid)
