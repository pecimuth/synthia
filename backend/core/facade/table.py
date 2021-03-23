from sqlalchemy.orm import Session

from core.model.meta_column import MetaColumn
from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.model.project import Project
from core.model.user import User


class TableFacade:
    """Provide CRUD operations related to MetaTable."""

    def __init__(self, db_session: Session, user: User):
        self._db_session = db_session
        self._user = user

    def find_meta_table(self, meta_table_id: int) -> MetaTable:
        """Find and return a meta table by ID. Check that it belongs
        to the logged in user.
        """
        return self._db_session.query(MetaTable).\
            join(MetaTable.project).\
            filter(
                MetaTable.id == meta_table_id,
                Project.user_id == self._user.id
            ).\
            one()

    def delete(self, meta_table: MetaTable):
        """Delete a meta table and the constraints referencing it.

        The columns, constraints, and generators are deleted by the database.
        """
        referencing_constraints =\
            self._db_session.query(MetaConstraint.id).\
            join(MetaConstraint.referenced_columns).\
            filter(MetaColumn.table == meta_table)
        self._db_session.query(MetaConstraint).\
            filter(
                MetaConstraint.id.in_(referencing_constraints.subquery())
            ).\
            delete(synchronize_session=False)
        self._db_session.delete(meta_table)
