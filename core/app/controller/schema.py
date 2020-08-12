from flask import Blueprint
from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column
from app.service.database import get_db_engine

schema = Blueprint('schema', __name__, url_prefix='/api')

def repr_table(table: Table):
    return {
        'table_name': table.name,
        'columns': [repr_column(col) for col in table.c.values()]
    }

def repr_column(column: Column):
    return {
        'column_name': column.name,
        'primary_key': column.primary_key,
        'type': column.type.__visit_name__,
        'nullable': column.nullable,
        'computed': column.computed
    }

@schema.route('/schema')
def get_schema():
    meta = MetaData()
    meta.reflect(bind=get_db_engine())
    return {name: repr_table(table) for name, table in meta.tables.items()}
