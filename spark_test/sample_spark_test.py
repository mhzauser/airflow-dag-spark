import pytest

from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark_test_session():
    return (
        SparkSession
        .builder
        .master('local[*]')
        .appName('unit-testing')
        .getOrCreate()
    )


def test_conditional_count(spark_test_session):
    """
    Test the count Of simple Df
    """
    expected_data = [(1231, 123), (123, 123), (3981, 123)]

    expected_df = spark_test_session.createDataFrame(expected_data, ["employee_id", "total_car_owners"])
    expect_data = expected_df.count()
    assert expect_data == 3
