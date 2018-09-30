"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import os
import pytest

from datetime import datetime, date, timedelta
from os.path import sep

from utils import get_mandatory_env, get_optional_env, import_class_from_string, \
    csv_filepath_to_dict, csv_string_to_dict, parse_date, build_time_range, UTC, \
    datetime_to_seconds, datetime_to_milliseconds


CURRENT_DIR = os.path.dirname(__file__)
TEST_FILE = 'csv_fixture.csv'

EXPECTED_OUTPUT_FROM_CSV = [
        {'key': 'table_prefix', 'value': 'wp_', 'type': 'variable'},
        {'key': 'DB_NAME', 'value': 'wp_a0veseethknlxrhdaachaj5qgdixh', 'type': 'constant'},
        {'key': 'DB_USER', 'value': 'ogtc,62msegz2beji', 'type': 'constant'},
        {'key': 'DB_PASSWORD', 'value': 'Rfcua2LKD^vpGy@m*R*Z', 'type': 'constant'},
        {'key': 'DB_COLLATE', 'value': '', 'type': 'constant'}
    ]

TEST_VAR = "test-var"


@pytest.fixture()
def environment(request):
    """
    Load fake environment variables for every test
    """
    os.environ["TEST_VAR"] = TEST_VAR
    return os.environ


@pytest.fixture()
def delete_environment(request):
    """
        Delete all env. vars
    """
    if os.environ.get("TEST_VAR"):
        del os.environ["TEST_VAR"]


class TestEnvironment:

    def test_empty_env(self, delete_environment):
        """
            Delete all env. vars and check that module raise an exception on load
        """
        assert "foo" == get_optional_env("TEST_VAR", "foo")
        with pytest.raises(Exception):
            get_mandatory_env("TEST_VAR")

    def test_env(self, environment):
        """
            Check default values for JAHIA _USER and _HOST
        """
        assert "test-var" == get_optional_env("TEST_VAR", "foo")
        assert "test-var" == get_mandatory_env("TEST_VAR")


class TestCSV:

    def test_csv_from_filepath(self):
        file_path = os.path.join(CURRENT_DIR, TEST_FILE)
        assert csv_filepath_to_dict(file_path) == EXPECTED_OUTPUT_FROM_CSV

    def test_csv_from_string(self):
        text = """key,value,type
table_prefix,wp_,variable
DB_NAME,wp_a0veseethknlxrhdaachaj5qgdixh,constant
DB_USER,"ogtc,62msegz2beji",constant
DB_PASSWORD,Rfcua2LKD^vpGy@m*R*Z,constant
DB_COLLATE,,constant"""
        assert csv_string_to_dict(text) == EXPECTED_OUTPUT_FROM_CSV


class TestImport:

    def test_first_level_import(self):
        assert datetime == import_class_from_string(
            "datetime.datetime")

    def test_low_level_import(self):
        assert sep == import_class_from_string(
            "os.path.sep")


class TestDateParsing:

    def test_none(self):
        assert parse_date() == date.today()

    def test_none_shift(self):
        assert parse_date(shift=1) == date.today() - timedelta(days=1)

    def test_input(self):
        assert parse_date("2018-09-29") == date(2018, 9, 29)
        assert parse_date("2018-9-29") == date(2018, 9, 29)

    def test_input_shift(self):
        assert parse_date("2018-09-29", 7) == date(2018, 9, 22)


class TestTimeRange:

    EXPECTED_END_TIME = datetime(2018, 9, 29, 23, 59, 59, 999999)

    def test_default(self):
        today = date.today()
        expected_end = datetime(today.year, today.month, today.day, 23, 59, 59, 999999)
        expected_start = datetime(today.year, today.month, today.day - 1, 0, 0, 0, 0)

        assert expected_start, expected_end == build_time_range()

    def test_end_only(self):
        expected_end = self.EXPECTED_END_TIME
        expected_start = datetime(2018, 9, 22, 0, 0, 0, 0)

        assert expected_start, expected_end == build_time_range(
            to_str="2018-09-29")

    def test_end_start(self):
        expected_end = self.EXPECTED_END_TIME
        expected_start = datetime(2018, 9, 25, 0, 0, 0, 0)

        assert expected_start, expected_end == build_time_range(
            to_str="2018-09-29", from_str="2018-09-25")

    def test_end_ago(self):
        expected_end = self.EXPECTED_END_TIME
        expected_start = datetime(2018, 9, 28, 0, 0, 0, 0)

        assert expected_start, expected_end == build_time_range(
            to_str="2018-09-29", ago=1)

        assert expected_start, expected_end == build_time_range(
            to_str="2018-09-29", ago="1")

    def test_fail_on_end_start(self):
        with pytest.raises(ValueError):
            build_time_range(to_str="2018-09-29", from_str="2018-10-01")

        with pytest.raises(TypeError):
            build_time_range(to_str="2018-09-29", ago="-1")


class TestDates:

    def test_datetime_to_seconds(self):
        seconds = 1535760000
        assert seconds == datetime_to_seconds(datetime(2018, 9, 1, tzinfo=UTC))

    def test_datetime_to_milliseconds(self):
        millis = 1535796052132
        assert millis == datetime_to_milliseconds(datetime(2018, 9, 1, 10, 0, 52, 132000, tzinfo=UTC))
