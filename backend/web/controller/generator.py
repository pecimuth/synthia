import functools

from flasgger import swag_from
from flask import Blueprint, g, request
from sqlalchemy.orm.exc import NoResultFound

from core.model.generator_setting import GeneratorSetting
from core.model.meta_table import MetaTable
from core.model.project import Project
from core.service.column_generator import make_generator_instance_for_meta_column
from core.service.column_generator.base import ColumnGeneratorBase
from web.controller.auth import login_required
from web.controller.util import TOKEN_SECURITY, BAD_REQUEST_SCHEMA, bad_request, \
    GENERATOR_SETTING_NOT_FOUND, OK_REQUEST_SCHEMA, ok_request, validate_json
from web.service.database import get_db_session
from web.view import GeneratorListView, GeneratorSettingWrite, GeneratorSettingView

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


def with_generator_setting_by_id(view):
    @functools.wraps(view)
    def wrapped_view(id: int):
        try:
            generator_setting: GeneratorSetting = get_db_session().\
                query(GeneratorSetting).\
                join(GeneratorSetting.table).\
                join(MetaTable.project).\
                join(Project.user).\
                filter(
                    GeneratorSetting.id == id,
                    Project.user == g.user
                ).\
                one()
        except NoResultFound:
            return bad_request(GENERATOR_SETTING_NOT_FOUND)
        return view(generator_setting)
    return wrapped_view


@generator.route('/generator-setting/<id>', methods=('PATCH',))
@login_required
@with_generator_setting_by_id
@validate_json(GeneratorSettingWrite)
@swag_from({
    'tags': ['Generator'],
    'security': TOKEN_SECURITY,
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
    # TODO check generator existence
    old_name = generator_setting.name
    new_name = request.json['name']
    generator_setting.name = new_name
    new_params = request.json['params']
    # TODO normalize params
    generator_setting.params = new_params
    null_frequency = request.json.get('null_frequency')
    if null_frequency is None or null_frequency < 0 or null_frequency > 1:
        null_frequency = 0
    generator_setting.null_frequency = null_frequency

    if generator_setting.columns:
        # TODO support several columns
        meta_column = generator_setting.columns[0]
        gen_instance = make_generator_instance_for_meta_column(meta_column)
        if new_name != old_name and new_params is None \
           and meta_column.data_source is not None:
            gen_instance.estimate_params()

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
