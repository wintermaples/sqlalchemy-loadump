import enum
from sqlalchemy import Column, Double, ForeignKey
from sqlalchemy.orm import declarative_base

from sqlalchemy.types import BigInteger, Boolean, Date, DateTime, Enum
from sqlalchemy.types import Float, Integer, Interval, LargeBinary
from sqlalchemy.types import Numeric
from sqlalchemy.types import SmallInteger, String, Text, Time, Unicode, UnicodeText, Uuid
from sqlalchemy.orm import mapped_column

Base = declarative_base()


class EnumOfEnumTypeTestTable(enum.Enum):
    A = 1
    B = 2
    C = 3


class TypeTestTable(Base):
    __tablename__ = "type_test"
    id_ = Column(Integer, primary_key=True)
    big_integer = Column(BigInteger)
    boolean = Column(Boolean)
    date = Column(Date)
    date_time = Column(DateTime)
    double_ = Column(Double)
    enum = Column(Enum(EnumOfEnumTypeTestTable))
    float_ = Column(Float)
    integer = Column(Integer)
    large_binary = Column(LargeBinary)
    numeric = Column(Numeric)
    numeric_5_3 = Column(Numeric(5, 3))
    small_integer = Column(SmallInteger)
    string = Column(String)
    text = Column(Text)
    time = Column(Time)
    unicode = Column(Unicode)
    unicode_text = Column(UnicodeText)
    uuid = Column(Uuid)


class ParentTable(Base):
    __tablename__ = "parent"
    id_ = mapped_column(Integer, autoincrement=True, primary_key=True)


class ChildTable(Base):
    __tablename__ = "child"
    id_ = mapped_column(Integer, autoincrement=True, primary_key=True)
    parent_id = mapped_column(ForeignKey("parent.id_"))
