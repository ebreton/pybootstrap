import csv
import io


def csv_stream_do_dict(stream, delimiter=','):
    """
    Transform Stream (in CSV format) into a dictionnary

    Arguments keywords:
    stream -- stream containing infos to put in dictionnary
                For stream information, have a look here: https://docs.python.org/3.5/library/io.html
    delimiter -- character to use to split infos coming from stream (CSV)

    Return: list of dictionnaries
    """
    rows = []
    reader = csv.DictReader(stream, delimiter=delimiter)
    for row in reader:
        rows.append(row)
    return rows


def csv_string_to_dict(text, delimiter=','):
    """
    Transform a string (in CSV format) into a dictionnary

    Arguments keywords:
    text -- String containing CSV information
    delimiter -- character to use to split infos coming from string (CSV)

    Return: list of dictionnaries
    """
    with io.StringIO(text) as stream:
        return csv_stream_do_dict(stream, delimiter=delimiter)


def csv_filepath_to_dict(file_path, delimiter=',', encoding="utf-8"):
    """
    Returns the rows of the given CSV file as a list of dicts

    Arguments keywords:
    file_path -- path to file containing infos (in CSV format)
    delimiter -- character to use to split infos coming from file (CSV)
    encoding -- encoding used in file 'file_path'

    Retur: list of dictionnaries
    """
    with open(file_path, 'r', encoding=encoding) as stream:
        return csv_stream_do_dict(stream, delimiter=delimiter)
