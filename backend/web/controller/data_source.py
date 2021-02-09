from flasgger import swag_from
from flask import Blueprint, g, request

from core.model.data_source import DataSource
from core.model.project import Project
from core.service.data_source import DataSourceUtil
from web.controller.auth import login_required
from web.service.database import get_db_session
from web.view import DataSourceView, MessageView, DataSourceDatabaseWrite

source = Blueprint('data_source', __name__, url_prefix='/api')


@source.route('/data-source-database', methods=('POST',))
@login_required
@swag_from({
    'tags': ['DataSource'],
    'parameters': [
        {
            'name': 'data_source_database',
            'in': 'body',
            'description': 'Database credentials',
            'required': True,
            'schema': DataSourceDatabaseWrite
        }
    ],
    'responses': {
        200: {
            'description': 'Created new database data source',
            'schema': DataSourceView
        },
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def create_data_source_database():
    db_session = get_db_session()

    validation_errors = DataSourceDatabaseWrite().validate(request.json)
    if validation_errors:
        return {
           'result': 'error',
           'message': 'Invalid input'
        }, 400

    # TODO not found error
    proj = db_session.\
        query(Project).\
        filter(
            Project.id == request.json['project_id'],
            Project.user == g.user
        ).\
        one()

    data_source = DataSource(
        project=proj,
        driver=DataSourceUtil.DRIVER_POSTGRES,
        db=request.json['db'],
        usr=request.json['usr'],
        pwd=request.json['pwd'],
        host=request.json['host'],
        port=request.json['port']
    )
    db_session.add(data_source)
    db_session.commit()
    return DataSourceView().dump(data_source)
