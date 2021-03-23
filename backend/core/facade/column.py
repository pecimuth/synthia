from sqlalchemy import or_
from sqlalchemy.orm import Session

from core.model.meta_column import MetaColumn
from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.model.project import Project
from core.model.user import User


class ColumnFacade:
    """Provide CRUD operations related to MetaColumn."""

    def __init__(self, db_session: Session, user: User):
        self._db_session = db_session
        self._user = user

    def find_column(self, meta_column_id: int) -> MetaColumn:
        """Find and return meta column, searched by ID.

        We need to check that it belongs to the logged in user.
        """
        return self._db_session.\
            query(MetaColumn).\
            join(MetaColumn.table).\
            join(MetaTable.project).\
            join(Project.user).\
            filter(
                MetaColumn.id == meta_column_id,
                Project.user == self._user
            ).\
            one()

    def find_column_in_table(self, meta_table: MetaTable, meta_column_id: int) -> MetaColumn:
        """Find and return meta column, constrained by ID and its parent table."""
        return self._db_session.query(MetaColumn).\
            join(MetaTable.project).\
            filter(
                MetaColumn.id == meta_column_id,
                MetaColumn.table == meta_table
            ).\
            one()

    def delete(self, meta_column: MetaColumn):
        """Delete the MetaColumn. Related constraints (constraining or referencing)
        the column are found and deleted, too."""
        column_constraints = \
            self._db_session.query(MetaConstraint.id).\
            join(MetaConstraint.constrained_columns).\
            filter(MetaColumn.id == meta_column.id)

        referencing_constraints = \
            self._db_session.query(MetaConstraint.id).\
            join(MetaConstraint.referenced_columns).\
            filter(MetaColumn.id == meta_column.id)

        self._db_session.query(MetaConstraint).\
            filter(
                or_(
                    MetaConstraint.id.in_(referencing_constraints.subquery()),
                    MetaConstraint.id.in_(column_constraints.subquery())
                )
            ).\
            delete(synchronize_session=False)
        self._db_session.delete(meta_column)
