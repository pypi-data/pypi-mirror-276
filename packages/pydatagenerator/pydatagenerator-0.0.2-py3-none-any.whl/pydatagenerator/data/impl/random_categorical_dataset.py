import random
from pydatagenerator.data.abstract import AbstractDataSet

class RandomCategoricalDataSet(AbstractDataSet):
    """RandomCategoricalDataSet
    """
    type = 'type.random-categorical-dataset'

    def required_fields(self):
        """Returns the required fields for the current data set

        Returns:
            List[str]: List of required fields for the current data set
        """
        return ['categories']

    def optional_fields(self):
        """Returns the optional fields for the current data set

        Returns:
            List[str]: List of optional fields for the current data set
        """
        return []

    def handle(self) -> object:
        """Process the given dataset_info and returns a result out of it

        Returns:
            object: The result obtained after processing the dataset_info
        """
        categories = self._dataset_info['categories']
        return categories[random.randint(0, len(categories)-1)]
