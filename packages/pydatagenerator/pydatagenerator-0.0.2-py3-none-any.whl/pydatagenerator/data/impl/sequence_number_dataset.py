from typing import Dict, List
from pydatagenerator.data.abstract import AbstractDataSet


class SequenceNumberDataSet(AbstractDataSet):
    """SequenceNumberDataSet
    """
    type = 'type.sequence-number-dataset'

    def required_fields(self) -> List[str]:
        """Returns the required fields for the current data set

        Returns:
            List[str]: List of required fields for the current data set
        """
        return ['start', 'increment']

    def optional_fields(self) -> List[str]:
        """Returns the optional fields for the current data set

        Returns:
            List[str]: List of optional fields for the current data set
        """
        return ['floating']

    def __init__(self, dataset_info: Dict[str, object]):
        super().__init__(dataset_info)
        is_floating = 'floating' in dataset_info \
            and dataset_info['floating'].lower() == 'true'
        self.__start = float(dataset_info['start']) if is_floating \
              else int(dataset_info['start'])
        self.__increment = float(dataset_info['increment']) if is_floating \
              else int(dataset_info['increment'])
        self.__val = self.__start - self.__increment

    def handle(self) -> object:
        """Process the given dataset_info and returns a result out of it

        Returns:
            object: The result obtained after processing the dataset_info
        """
        self.__val += self.__increment
        return self.__val
