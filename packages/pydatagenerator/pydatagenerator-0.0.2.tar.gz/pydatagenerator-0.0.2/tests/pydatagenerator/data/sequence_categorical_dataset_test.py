from pydatagenerator.data.impl.dataset_handler_factory import DatasetHandlerFactory


def test_sequence_categorical_dataset():
    categories = ['red', 'green', 'blue']
    handler = DatasetHandlerFactory().get_dataset_handler({
        'type': 'type.sequence-categorical-dataset',
        'name': 'colors',
        'categories': categories,
        'start': 0,
        'increment': 1
    })

    value1 = handler.handle()
    assert value1 in categories

    value2 = handler.handle()
    assert value2 in categories
    assert value1 != value2
