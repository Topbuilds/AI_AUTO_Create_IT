import os
from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class SubmissionRecord(Base):
    __tablename__ = "submission_records"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    original_filename = Column(String(255), nullable=False)
    original_path = Column(String(1024), nullable=False)
    output_filename = Column(String(255), nullable=False)
    output_path = Column(String(1024), nullable=False)
    output_format = Column(String(20), nullable=False)
    status = Column(String(20), default="pending", nullable=False)


def get_database_url() -> str:
    return os.environ.get("DATABASE_URL", "sqlite:///uploads/review.db")


def init_db(db_url: str | None = None) -> None:
    url = db_url or get_database_url()
    engine = create_engine(url)
    Base.metadata.create_all(engine)


def get_session(db_url: str | None = None):
    url = db_url or get_database_url()
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    return Session()


def save_submission_record(
    db_url: str | None = None,
    *,
    original_filename: str,
    original_path: str,
    output_filename: str,
    output_path: str,
    output_format: str,
    status: str = "pending",
) -> SubmissionRecord:
    session = get_session(db_url)
    record = SubmissionRecord(
        original_filename=original_filename,
        original_path=original_path,
        output_filename=output_filename,
        output_path=output_path,
        output_format=output_format,
        status=status,
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    session.close()
    return record


def list_submission_records(db_url: str | None = None) -> List[SubmissionRecord]:
    session = get_session(db_url)
    records = session.query(SubmissionRecord).order_by(SubmissionRecord.created_at.desc()).all()
    session.close()
    return records


def update_submission_status(db_url: str | None = None, *, record_id: int, status: str) -> SubmissionRecord | None:
    session = get_session(db_url)
    record = session.query(SubmissionRecord).filter(SubmissionRecord.id == record_id).first()
    if not record:
        session.close()
        return None
    record.status = status
    session.commit()
    session.refresh(record)
    session.close()
    return record
