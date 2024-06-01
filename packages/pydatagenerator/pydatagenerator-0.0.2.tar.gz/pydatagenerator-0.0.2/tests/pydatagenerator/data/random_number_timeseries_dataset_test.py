from datetime import datetime
from pydatagenerator.data.impl.dataset_handler_factory import DatasetHandlerFactory


def test_generate_random_number_timeseries_data_with_default_format():
    min_timestamp_str = '2024-05-25T14:09:03Z'
    max_timestamp_str = '2024-05-30T14:09:03Z'
    handler = DatasetHandlerFactory().get_dataset_handler({
        'type': 'type.random-number-timeseries-dataset',
        'name': 'stockprice',
        'min_value': 10,
        'max_value': 100,
        'min_date': min_timestamp_str,
        'max_date': max_timestamp_str
    })

    value = handler.handle()
    assert 10 <= value[0] <= 100
    min_timestamp = datetime.strptime(min_timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
    max_timestamp = datetime.strptime(max_timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
    assert min_timestamp <= value[1] <= max_timestamp

def test_generate_random_number_timeseries_data_with_custom_format():
    min_timestamp_str = 'May 25 2024 14:09:03'
    max_timestamp_str = 'May 30 2024 14:09:03'
    date_format = '%b %d %Y %H:%M:%S'

    handler = DatasetHandlerFactory().get_dataset_handler({
        'type': 'type.random-number-timeseries-dataset',
        'name': 'stockprice',
        'min_value': 10,
        'max_value': 100,
        'min_date': min_timestamp_str,
        'max_date': max_timestamp_str,
        'date_format': date_format
    })

    value = handler.handle()
    assert 10 <= value[0] <= 100
    min_timestamp = datetime.strptime(min_timestamp_str, date_format)
    max_timestamp = datetime.strptime(max_timestamp_str, date_format)
    assert min_timestamp <= value[1] <= max_timestamp


