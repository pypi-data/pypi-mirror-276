from typing import Dict
from pydatagenerator.data.abstract import AbstractDataSet

class SequenceCategoricalDataSet(AbstractDataSet):
    """SequenceCategoricalDataSet
    """
    type = 'type.sequence-categorical-dataset'

    def __init__(self, dataset_info: Dict[str, object]):
        super().__init__(dataset_info)
        is_floating = 'floating' in dataset_info \
            and dataset_info['floating'].lower() == 'true'
        self.__start = float(dataset_info['start']) if is_floating \
              else int(dataset_info['start'])
        self.__increment = float(dataset_info['increment']) if is_floating \
              else int(dataset_info['increment'])
        self.__pos = self.__start - self.__increment
        self.__categories = self.dataset_info['categories']

    def required_fields(self):
        """Returns the required fields for the current data set

        Returns:
            List[str]: List of required fields for the current data set
        """
        return ['categories','start','increment']

    def optional_fields(self):
        """Returns the optional fields for the current data set

        Returns:
            List[str]: List of optional fields for the current data set
        """
        return ['floating']

    def handle(self) -> object:
        """Process the given dataset_info and returns a result out of it

        Returns:
            object: The result obtained after processing the dataset_info
        """
        self.__pos += self.__increment
        self.__pos %= len(self.__categories)
        return self.__categories[self.__pos]
        
