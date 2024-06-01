from datetime import datetime
from pydatagenerator.data.impl.dataset_handler_factory import DatasetHandlerFactory

def test_sequence_number_timeseries_dataset_with_default_date_format():
    start_date_str = '2024-05-25T14:09:03Z'
    handler = DatasetHandlerFactory().get_dataset_handler({
        'type': 'type.sequence-number-timeseries-dataset',
        'name': 'stockprice',
        'start_value': 0,
        'increment_value': 1,
        'start_date': start_date_str,
        'increment_date': '01:05:30:20'
    })

    value1 = handler.handle()
    assert isinstance(value1[0], int)
    assert isinstance(value1[1], datetime)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%SZ')
    assert value1[1] >= start_date

    value2 = handler.handle()
    assert isinstance(value2[0], int)
    assert isinstance(value2[1], datetime)
    assert value2[1] >= start_date
    assert value2[1] >= value1[1]

