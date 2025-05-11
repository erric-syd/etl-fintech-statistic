from tools import DatabaseTools as db_t


def main():
    views_name = "ticket_size"

    q = f"""
        DROP VIEW IF EXISTS {views_name};
        CREATE VIEW {views_name} AS 
        WITH __dts AS (
          SELECT
            a."period",
            -- a.cumulative_total * 1000000000 AS funding_amount,
            -- b.cumulative_total AS total_account,
            round(
              (
                a.cumulative_total * 1000000000 / b.cumulative_total
              ) :: numeric
            ) AS ticket_size
          FROM
            npp a FULL
            JOIN trx b ON b."period" = a."period"
        )
        SELECT
          *
        FROM
          __dts;
    """
    db_t.execute_query(q)


if __name__ == "__main__":
    main()
