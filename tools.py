# Packages
from datetime import datetime
import os
import pandas as pd
import time
import pytz
import sqlalchemy as sa


class DatetimeTools:
    """Datetime

    datetime.now() # Local indonesia timezone UTC+7
    datetime.now(pytz.utc) # Universal timezone UTC+0
    """

    @staticmethod
    def get_current_datetime_asia_jkt():
        """GMT +7"""
        return datetime.now(pytz.timezone("Asia/Jakarta")).replace(tzinfo=None)


class EventTools:
    """Event"""

    @classmethod
    def show_msg(cls, desc):
        time.sleep(2)

        dt = DatetimeTools.get_current_datetime_asia_jkt().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{desc}; {dt}\n")

    @classmethod
    def show_msg_done(cls, desc):
        """Show message action done"""
        time.sleep(2)

        dt = DatetimeTools.get_current_datetime_asia_jkt().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Done: {desc}; {dt}")


class DatabaseTools:

    @staticmethod
    def load_to_database(df, tbn):
        df.to_sql(
            name=tbn,
            con=os.environ["DB_URL_PSQL"],
            if_exists="replace",
            index=False,
        )

    @staticmethod
    def execute_query(q):
        engine = sa.create_engine(os.environ["DB_URL_PSQL"])
        with engine.connect() as con:
            con.execute(sa.text(q))
            con.commit()

    @classmethod
    def drop_all_views(cls):
        """Using cascade to forcefully drop all views"""
        q = f"""
            DO $$ 
            DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT table_name FROM information_schema.views WHERE table_schema = current_schema()) 
                LOOP
                    EXECUTE 'DROP VIEW IF EXISTS ' || quote_ident(r.table_name) || ' CASCADE';
                END LOOP;
            END $$;
        """
        cls.execute_query(q)

        EventTools.show_msg_done(f"Drop All Views")
