import random
from datetime import datetime
from pydatagenerator.data.abstract import AbstractDataSet

class RandomNumberTimeSeriesDataset(AbstractDataSet):
    """"RandomNumberTimeSeriesDataset
    """
    type = 'type.random-number-timeseries-dataset'
    
    def required_fields(self):
        """Returns the required fields for the current data set

        Returns:
            List[str]: List of required fields for the current data set
        """
        return ['min_value', 'max_value', 'min_date', 'max_date']

    def optional_fields(self):
        """Returns the optional fields for the current data set

        Returns:
            List[str]: List of optional fields for the current data set
        """
        return ['floating', 'date_format']

    def random_date(self, start: datetime, end: datetime):
        epoch = datetime(1970, 1, 1)
        start_seconds = int((start - epoch).total_seconds())
        end_seconds = int((end - epoch).total_seconds())
        dt_seconds = random.randint(start_seconds, end_seconds)
        return datetime.fromtimestamp(dt_seconds)

    def handle(self) -> object:
        """Process the given dataset_info and returns a result out of it

        Returns:
            object: The result obtained after processing the dataset_info
        """
        is_floating = 'floating' in self._dataset_info and self._dataset_info['floating'].lower() == 'true'
        func = random.uniform if is_floating else random.randint
        value = func(int(self._dataset_info['min_value']), int(self._dataset_info['max_value']))
        # default format is iso-8601
        datetime_format = self._dataset_info['date_format'] if 'date_format' in self._dataset_info else '%Y-%m-%dT%H:%M:%SZ'
        min_date = datetime.strptime(self._dataset_info['min_date'], datetime_format)
        max_date = datetime.strptime(self._dataset_info['max_date'], datetime_format)
        date = self.random_date(min_date, max_date).strftime(datetime_format)
        datetime_value = datetime.strptime(date, datetime_format)
        return (value, datetime_value)


