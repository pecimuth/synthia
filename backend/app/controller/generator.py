from flasgger import swag_from
from flask import Blueprint

from app.service.generator.column_generator import ColumnGeneratorBase
from app.view import GeneratorListView

generator = Blueprint('generator', __name__, url_prefix='/api')


@generator.route('/generators')
@swag_from({
    'tags': ['Generator'],
    'responses': {
        200: {
            'description': 'Returned generator list',
            'schema': GeneratorListView
        }
    }
})
def get_generators():
    generators = ColumnGeneratorBase.__subclasses__()
    return GeneratorListView().dump({'items': generators})
