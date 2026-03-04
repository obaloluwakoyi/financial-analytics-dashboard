# database.py
from sqlalchemy import (
    create_engine, text, Table, Column,
    String, Float, MetaData, UniqueConstraint
)
from sqlalchemy.engine import Engine
import pandas as pd

DB_URL = "sqlite:///enterprise.db"

metadata = MetaData()

invoices = Table(
    "invoices",
    metadata,
    Column("invoice", String, nullable=False),
    Column("client", String, nullable=False),
    Column("amount", Float, nullable=False),
    Column("date", String, nullable=False),
    Column("status", String, nullable=False),
    Column("source", String, nullable=False),
    UniqueConstraint("invoice", "source", name="uq_invoice_source")
)


class DatabaseError(Exception):
    pass


def get_engine(db_url: str = DB_URL) -> Engine:
    return create_engine(db_url, future=True)


def init_db(engine: Engine):
    metadata.create_all(engine)


def save_invoices(df: pd.DataFrame, engine: Engine):
    if df.empty:
        return

    required = set(c.name for c in invoices.columns)
    if not required.issubset(df.columns):
        raise DatabaseError("DataFrame schema mismatch")

    records = df.to_dict(orient="records")

    stmt = text("""
        INSERT OR IGNORE INTO invoices
        (invoice, client, amount, date, status, source)
        VALUES (:invoice, :client, :amount, :date, :status, :source)
    """)

    try:
        with engine.begin() as conn:
            conn.execute(stmt, records)
    except Exception as e:
        raise DatabaseError("Failed to save invoices") from e


def load_invoices(engine: Engine) -> pd.DataFrame:
    try:
        with engine.connect() as conn:
            return pd.read_sql(text("SELECT * FROM invoices"), conn)
    except Exception as e:
        raise DatabaseError("Failed to load invoices") from e