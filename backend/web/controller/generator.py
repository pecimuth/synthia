import functools

from flasgger import swag_from
from flask import Blueprint, request
from sqlalchemy.orm.exc import NoResultFound

from core.facade.generator import GeneratorFacade
from core.model.generator_setting import GeneratorSetting
from core.service.column_generator.base import RegisteredGenerator
from core.service.column_generator.setting_facade import GeneratorSettingFacade
from core.service.output_driver.file_driver.facade import FileOutputDriverFacade
from web.controller.auth import login_required
from web.controller.util import TOKEN_SECURITY, BAD_REQUEST_SCHEMA, bad_request, \
    GENERATOR_SETTING_NOT_FOUND, OK_REQUEST_SCHEMA, ok_request, validate_json, \
    patch_all_from_json, error_into_message
from web.service.database import get_db_session
from web.service.injector import inject, get_injector
from web.view.generator import GeneratorListView, GeneratorSettingWrite, GeneratorSettingView, GeneratorSettingCreate, \
    OutputFileDriverListView

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
    generators = RegisteredGenerator.__subclasses__()
    return GeneratorListView().dump({'items': generators})


@generator.route('/output-file-drivers')
@swag_from({
    'tags': ['Generator'],
    'responses': {
        200: {
            'description': 'List of output file drivers',
            'schema': OutputFileDriverListView
        }
    }
})
def get_output_file_drivers():
    output = {
        'items': FileOutputDriverFacade.get_driver_list()
    }
    return OutputFileDriverListView().dump(output)


def with_generator_setting_by_id(view):
    """Decorator for handlers accepting generator setting ID in path.

    Fetches the generator setting by ID and calls the handler
    with the generator setting instance instead of the ID.
    """
    @functools.wraps(view)
    def wrapped_view(id: int):
        facade = inject(GeneratorFacade)
        try:
            generator_setting = facade.find_setting(id)
        except NoResultFound:
            return bad_request(GENERATOR_SETTING_NOT_FOUND)
        return view(generator_setting)
    return wrapped_view


@generator.route('/generator-setting', methods=('POST',))
@login_required
@validate_json(GeneratorSettingCreate)
@error_into_message
@swag_from({
    'tags': ['Generator'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'generator_setting',
            'in': 'body',
            'description': 'Generator setting content',
            'required': True,
            'schema': GeneratorSettingCreate
        }
    ],
    'responses': {
        200: {
            'description': 'Created generator setting',
            'schema': GeneratorSettingView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def create_generator_setting():
    facade = inject(GeneratorFacade)
    generator_setting = facade.create_generator_setting(
        request.json['table_id'],
        request.json.get('column_id'),
        request.json['name'],
        request.json['params'],
        request.json['null_frequency']
    )
    get_db_session().commit()
    return GeneratorSettingView().dump(generator_setting)


@generator.route('/generator-setting/<id>', methods=('PATCH',))
@login_required
@with_generator_setting_by_id
@validate_json(GeneratorSettingWrite)
@error_into_message
@swag_from({
    'tags': ['Generator'],
    'security': TOKEN_SECURITY,
    'description': 'Patch a generator setting and optionally estimate its parameters.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Generator setting ID',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'generator_setting',
            'in': 'body',
            'description': 'Generator setting content',
            'required': True,
            'schema': GeneratorSettingWrite
        }
    ],
    'responses': {
        200: {
            'description': 'Patched generator setting',
            'schema': GeneratorSettingView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def patch_generator_setting(generator_setting: GeneratorSetting):
    patch_all_from_json(generator_setting, ['name', 'params', 'null_frequency'])
    estimate_params = request.json.get('estimate_params')
    facade = GeneratorSettingFacade(generator_setting)

    if estimate_params:
        facade.maybe_estimate_params(get_injector())
    else:
        gen_instance = facade.make_generator_instance()
        gen_instance.save_params()

    db_session = get_db_session()
    db_session.commit()
    return GeneratorSettingView().dump(generator_setting)


@generator.route('/generator-setting/<id>', methods=('DELETE',))
@login_required
@with_generator_setting_by_id
@swag_from({
    'tags': ['Generator'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Generator setting ID to be deleted',
            'required': True,
            'type': 'integer'
        },
    ],
    'responses': {
        200: OK_REQUEST_SCHEMA,
        400: BAD_REQUEST_SCHEMA
    }
})
def delete_generator_setting(generator_setting: GeneratorSetting):
    db_session = get_db_session()
    db_session.delete(generator_setting)
    db_session.commit()
    return ok_request('Deleted the generator setting')
