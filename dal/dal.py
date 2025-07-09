from datetime import datetime

import pandas as pd
import pytz

from sqlalchemy import and_, create_engine, Column, Integer, String, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine("sqlite:///thanksCrowd.db", echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Entry(Base):
    __tablename__ = "entries"

    ticker = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=lambda: datetime.now(pytz.timezone('US/Eastern')))
    total_count = Column(Integer, nullable=False)
    positive_count = Column(Integer, nullable=False)

    __table_args__ = (PrimaryKeyConstraint("ticker", "date"),)

Base.metadata.create_all(bind=engine)

class Database:
    def __init__(self):
        self.session = Session()

    def clean(self) -> bool:
        today = datetime.now(pytz.timezone('US/Eastern')).replace(hour=0, minute=0, second=0, microsecond=0)


        try:
            oldest_date = self.session.query(Entry).order_by(Entry.date).first().date

            # Fetch all previous Entries with date < today
            entries = self.session.query(Entry).filter(Entry.date < today).all()

            for entry in entries:
                # Get the earliest entry for that ticker
                earliest_entry = (
                    self.session.query(Entry)
                    .filter(Entry.ticker == entry.ticker)
                    .order_by(Entry.date)
                    .first()
                )

                if earliest_entry and earliest_entry.date != oldest_date:
                    entry.date = oldest_date
                elif earliest_entry and earliest_entry.date != entry.date:
                    # Add that entry's value to the earliest entry for that ticker
                    earliest_entry.total_count += entry.total_count
                    earliest_entry.positive_count += entry.positive_count

                    # Delete that entry
                    self.session.delete(entry)

            self.session.commit()
            return True
        
        except SQLAlchemyError as e:
            print(f"error occurred while cleaning db: {e}")
            return False
        finally:
            self.session.close()


    def increment(self, ticker: str, timestamp: float, isPositive: bool) -> None:
        timestamp = datetime.fromtimestamp(timestamp, pytz.timezone('US/Eastern')).replace(hour=0, minute=0, second=0, microsecond=0)
        
        try:
            existing_entry = self.session.query(Entry).filter(Entry.ticker == ticker).filter(Entry.date == timestamp).first()
            if existing_entry is not None:
                existing_entry.total_count += 1
                if isPositive:
                    existing_entry.positive_count += 1

            else:
                new_entry = Entry(
                    ticker=ticker,
                    date=timestamp,
                    total_count=1,
                    positive_count=1 if isPositive else 0
                )
                self.session.add(new_entry)

            self.session.commit()
        
        except SQLAlchemyError as e:
            print(f"error while incrementing {ticker} in db: {e}")
        
        finally:
            self.session.close()

    def get_top_ticker_df(self, days: int) -> pd.DataFrame:
        try:
            # Get data
            cutoff_date = pd.Timestamp.now().normalize() - pd.Timedelta(days=days)
            data = self.session.query(Entry).filter(
                and_(
                    Entry.date >= cutoff_date
                )
            ).all()
            if not data:
                return None
            
            # Create dataframe
            df = pd.DataFrame([{
                "ticker": entry.ticker,
                "date": entry.date,
                "total_count": entry.total_count,
                "positive_count": entry.positive_count
            } for entry in data])

        except SQLAlchemyError as e:
            print(f"error while getting top tickers from db: {e}")
            return None
        finally:
            self.session.close()    
            
        return df

        
