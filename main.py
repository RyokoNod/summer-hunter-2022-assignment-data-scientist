import pandas as pd

from config import DEFAULT_TABLE, N_SIMULATIONS, N_USERS, TRAINING_INTERVAL_DAYS, logger
from organization import Organization
from sql import QueryParams, db_connection, query_db_to_df


def create_records_into_db() -> None:
    """Create database records from Hoxhunt training."""
    dummy_organization = Organization(
        n_users=N_USERS, n_simulations=N_SIMULATIONS, training_interval_days=TRAINING_INTERVAL_DAYS
    )
    logger.info("Organization created: %s", dummy_organization)
    dummy_organization.do_training()
    logger.info("Organization has now been trained in Hoxhunt!")
    result = dummy_organization.get_result()
    result.to_sql(DEFAULT_TABLE, db_connection, if_exists="replace", index=None)


def get_data_with_query() -> tuple:
    """Load records from the database into a DataFrame.

    Query to fetch the raw data if you want to inspect it:

    from config import TABLE_COLUMNS
    query_params = QueryParams(
        dimensions=["*"],
        table=DEFAULT_TABLE
    )
    query_db_to_df(query_params, result_columns=TABLE_COLUMNS)
    """
    # TODO(Task 3):
    # Write a SQL query that aggregates the simulated data to a format that you want to visualize
    # To do this, you will use a Jinja template that compiles a query from a set of given arguments
    # You are allowed to write multiple queries if you wish to visualize multiple things.
    # EXAMPLE: Get number of fails per user.
    # query_params = QueryParams(
    #     dimensions=[
    #         "user_id",
    #         "name",
    #         "type",
    #         "COUNT(CASE WHEN outcome = 'FAIL' THEN 1 END) AS fails",
    #     ],
    #     table=DEFAULT_TABLE,
    #     group_by=["user_id"],
    #     order_by=["fails DESC"],
    # )
    # query_result = query_db_to_df(query_params, result_columns=["user_id", "name", "type", "fails"])
    # The function call above will result in the following query:
    # SELECT user_id, name, type, COUNT(CASE WHEN outcome = 'FAIL' THEN 1 END) AS fails
    # FROM training_result
    # GROUP BY user_id
    # ORDER BY fails DESC
    query_params_usercnt = QueryParams(
        dimensions=[
            "user_id",
            "name",
            "COUNT(CASE WHEN outcome = 'SUCCESS' THEN 1 END) AS successes",
            "COUNT(CASE WHEN outcome = 'FAIL' THEN 1 END) AS fails",
            "COUNT(CASE WHEN outcome = 'MISS' THEN 1 END) AS misses",
        ],
        table=DEFAULT_TABLE,
        group_by=["user_id"],
        order_by=["successes DESC"],
    )
    query_result_usercnt = query_db_to_df(query_params_usercnt, result_columns=["user_id", "name", "successes", "fails", "misses"])
    query_params_datecnt = QueryParams(
        dimensions=[
            "STRFTIME('%Y-%m-%d', timestamp) AS date",
            "COUNT(CASE outcome WHEN 'SUCCESS' then 1 END) as successes",
            "COUNT(CASE outcome WHEN 'FAIL' then 1 END) as fails",
            "COUNT(CASE outcome WHEN 'MISS' then 1 END) as misses",
        ],
        table=DEFAULT_TABLE,
        group_by=["date"],
        order_by=["date ASC"],
    )
    query_result_datecnt = query_db_to_df(query_params_datecnt,
                                  result_columns=["date", "successes", "fails", "misses"])
    return query_result_usercnt, query_result_datecnt


def main() -> None:
    """Run the entire simulation application."""
    create_records_into_db()
    logger.info("Training results successfully uploaded to the database")
    aggregated_data_usercnt,  aggregated_data_datecnt = get_data_with_query()
    logger.info("Aggregated training results have been fetched from the db.")
    csv_filename_usercnt, csv_filename_datecnt = "visualize_usercounts.csv", "visualize_datecounts.csv"
    aggregated_data_usercnt.to_csv(csv_filename_usercnt, index=False)
    aggregated_data_datecnt.to_csv(csv_filename_datecnt, index=False)
    logger.info("Data ready for visualization can be found in %s, %s", csv_filename_usercnt, csv_filename_datecnt)


if __name__ == "__main__":
    main()
