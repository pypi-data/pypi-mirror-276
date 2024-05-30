from hestia_earth.schema import TermTermType
from hestia_earth.utils.tools import flatten

from hestia_earth.validation.utils import (
    _filter_list_errors, update_error_path
)


def validate_has_animals(cycle: dict):
    has_liveAnimal = any(
        p for p in cycle.get('products', []) if p.get('term', {}).get('termType') == TermTermType.LIVEANIMAL.value
    )
    has_animals = len(cycle.get('animals', [])) > 0
    return not has_liveAnimal or has_animals or {
        'level': 'warning',
        'dataPath': '',
        'message': 'should specify the herd composition'
    }


def validate_duplicated_feed_inputs(cycle: dict):
    feed_input_ids = [i.get('term', {}).get('@id') for i in cycle.get('inputs', []) if i.get('isAnimalFeed', False)]

    def validate_animal_input(values: tuple):
        index, input = values
        term = input.get('term', {})
        term_id = term.get('@id')
        return term_id not in feed_input_ids or {
            'level': 'error',
            'dataPath': f".inputs[{index}]",
            'message': 'must not add the feed input to the Cycle as well',
            'params': {
                'term': term
            }
        }

    def validate_animal(values: tuple):
        index, blank_node = values
        errors = list(map(validate_animal_input, enumerate(blank_node.get('inputs', []))))
        return _filter_list_errors(
            [update_error_path(error, 'animals', index) for error in errors if error is not True]
        )

    blank_nodes = enumerate(cycle.get('animals', []))
    return _filter_list_errors(flatten(map(validate_animal, blank_nodes)))
