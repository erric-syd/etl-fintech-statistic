from task.pipeline.shared import Processor


def main():
    filepath_dts = "./asset/sheet_16.csv"
    Processor().do(
        filepath_dts=filepath_dts,
        validation_query=validation_query(),
        table_name="trx",
    )


def validation_query():
    return """
        WITH __dts_1 AS (
          SELECT
            a.id,
            a."period",
            a.cumulative_total,
            --   a.prev_value,
            a.cumulative_total > a.prev_value AS validation_check
          FROM
            df a
        )
        SELECT
          *
        FROM
          __dts_1
    """


if __name__ == "__main__":
    main()
