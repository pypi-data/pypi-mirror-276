from pydatagenerator.data.impl.dataset_handler_factory import DatasetHandlerFactory

def test_random_categorical_dataset():
    categories = ['red', 'green', 'blue']
    handler = DatasetHandlerFactory().get_dataset_handler({
        'type': 'type.random-categorical-dataset',
        'name': 'colors',
        'categories': categories
    })

    value = handler.handle()
    assert value in categories

    value = handler.handle()
    assert value in categories
