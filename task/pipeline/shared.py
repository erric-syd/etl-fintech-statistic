"""Task Shared Function"""

from tools import EventTools as event_t, DatabaseTools as db_t

# Packages
import pandas as pd
import duckdb

# Display debug as numeric not scientific
pd.options.display.float_format = "{:.0f}".format


class Processor:
    """Extract data soure and load to data warehouse"""

    @classmethod
    def do(cls, filepath_dts, validation_query, table_name):
        df = DataSource(filepath_dts).do()

        # Transform, remove province & region, and Rename, double reset_index to add ID.
        df = df[df.columns[2:]].sum().reset_index().reset_index()
        df.columns = ["id", "period", "cumulative_total"]

        # Shift ID
        df["id"] = df["id"] + 1

        # Convert period into clear format and add previous value
        q = """
            WITH __dts AS (
              SELECT
                a.id,
                strftime(strptime(a."period", '%b-%y'), '%Y-%m') as period,
                round(a.cumulative_total) as cumulative_total,
                COALESCE(
                  LAG(round(a.cumulative_total), 1) OVER (
                    ORDER BY
                      a.id
                  ),
                  0
                ) AS prev_value
              FROM
                df a
              ORDER BY
                a.id
            )
            SELECT
              *
            FROM
              __dts
        """
        df = duckdb.sql(q).to_df()

        # Add validation check
        df = duckdb.sql(validation_query).to_df()

        db_t.load_to_database(df=df, tbn=table_name)

        event_t.show_msg_done(f"Process Data Source - {table_name}")


class DataSource:
    """Process Data Source"""

    def __init__(self, filepath_dts):
        self.filepath_dts = filepath_dts

    def do(self):
        # Read and set 1st row as header
        df = pd.read_csv(self.filepath_dts, header=1)

        # Normalize
        df = self.normalize_col_lokasi(df)
        df = self.drop_irrelevant_row(df)
        df = self.normalize_statistic_value(df)

        return df

    @classmethod
    def normalize_col_lokasi(cls, df):
        """Normalize column Lokasi"""

        c_region = "region"
        c_province = "province"

        # Rename
        df = df.rename(columns={df.columns[0]: c_region, df.columns[1]: c_province})

        # STRING Trim and Upper
        for col in [c_region, c_province]:
            df[col] = df[col].str.strip().str.upper()

        # Fill regions with the last valid value
        df[c_region] = df[c_region].ffill()

        return df

    @classmethod
    def drop_irrelevant_row(cls, df):
        # Get index for row = JUMLAH
        filt_row_jumlah = df["province"] == "JUMLAH"
        idx_row_jumlah = int(df[filt_row_jumlah].index[0])

        # Drop 1st row and the last irrelevant row
        df = df[1:idx_row_jumlah]

        # Remove rows with NaN in the provinces column
        df = df.dropna(subset=["province"])

        return df

    @classmethod
    def normalize_statistic_value(cls, df):
        # Numeric column except the description
        statistic_col = df.columns[2:]

        # Replace commas and convert to numeric
        for col in statistic_col:
            df[col] = df[col].str.replace(",", "").astype(float)

        # Replace NaN values with 0
        df = df.fillna(0)

        return df
