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
    Test the count function with condition
    :param spark_test_session:
    :return:
    """
    expected_data = [(2112, 3), (2343, 2), (3981, 0)]

    expected_df = spark_test_session.createDataFrame(expected_data, ["employee_id", "total_car_owners"])
    expect_data = expected_df.count()
    assert expect_data == 3
