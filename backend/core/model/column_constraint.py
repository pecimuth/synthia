from sqlalchemy import PrimaryKeyConstraint, Column, Integer, ForeignKey
from core.model import base


class ColumnConstraint(base):
    __tablename__ = 'columnconstraint'

    column_id = Column(Integer, ForeignKey('metacolumn.id', ondelete='CASCADE'))
    constraint_id = Column(Integer, ForeignKey('metaconstraint.id', ondelete='CASCADE'))
    column_order = Column(Integer, autoincrement=True)

    __table_args__ = (
        PrimaryKeyConstraint(column_id, constraint_id),
    )
