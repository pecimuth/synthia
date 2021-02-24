from sqlalchemy import Column, Integer, ForeignKey, Index
from core.model import base


class ColumnConstraint(base):
    __tablename__ = 'columnconstraint'

    id = Column(Integer, primary_key=True)
    column_id = Column(Integer, ForeignKey('metacolumn.id', ondelete='CASCADE'))
    constraint_id = Column(Integer, ForeignKey('metaconstraint.id', ondelete='CASCADE'))

    __table_args__ = (
        Index('ix_cc_column_constraint', column_id, constraint_id, unique=True),
        Index('ix_cc_constraint_column', constraint_id, column_id)
    )
