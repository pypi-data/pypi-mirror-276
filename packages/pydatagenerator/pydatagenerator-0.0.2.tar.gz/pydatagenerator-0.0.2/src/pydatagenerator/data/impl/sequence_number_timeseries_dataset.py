import re
from datetime import datetime, timedelta
from typing import Dict, List
from pydatagenerator.data.abstract import AbstractDataSet


class SequenceNumberTimeSeriesDataset(AbstractDataSet):
    """SequenceNumberTimeSeriesDataset
    """
    type = 'type.sequence-number-timeseries-dataset'

    def required_fields(self) -> List[str]:
        """Returns the required fields for the current data set

        Returns:
            List[str]: List of required fields for the current data set
        """
        return ['start_value', 'increment_value', 'start_date', 'increment_date']

    def optional_fields(self) -> List[str]:
        """Returns the optional fields for the current data set

        Returns:
            List[str]: List of optional fields for the current data set
        """
        return ['date_format', 'floating']

    def __init__(self, dataset_info: Dict[str, object]):
        super().__init__(dataset_info)
        self.__is_floating = 'floating' in dataset_info \
            and dataset_info['floating'].lower() == 'true'
        self.__increment = float(dataset_info['increment_value']) if self.__is_floating \
            else int(dataset_info['increment_value'])
        self.__parsed_increment_date = self.timedelta_parse(self._dataset_info['increment_date'])
        start_value = dataset_info['start_value']
        increment_value = dataset_info['increment_value']

        self.__val = float(start_value) - float(increment_value) if self.__is_floating \
            else int(start_value) - int(increment_value)
        self.__date_format = dataset_info['date_format'] if 'date_format' in dataset_info \
            else '%Y-%m-%dT%H:%M:%SZ'
        self.__date = datetime.strptime(dataset_info['start_date'], self.__date_format) - self.__parsed_increment_date

    def timedelta_parse(self, timedelta_str: str) -> timedelta:
        value = re.sub(r'[^0-9:.]', "", timedelta_str)
        if not value:
            return None
        return timedelta(**{
            key: float(val) for val, key in zip(value.split(':')[::-1], ('seconds', 'minutes', 'hours', 'days'))
        })

    def handle(self) -> object:
        """Process the given dataset_info and returns a result out of it

        Returns:
            object: The result obtained after processing the dataset_info
        """
        self.__val +=  self.__increment
        self.__date += self.__parsed_increment_date
        return (self.__val, self.__date)


