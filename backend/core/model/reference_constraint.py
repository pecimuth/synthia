from sqlalchemy import Column, ForeignKey, Integer, Index
from core.model import base


class ReferenceConstraint(base):
    __tablename__ = 'referenceconstraint'

    id = Column(Integer, primary_key=True)
    column_id = Column(Integer, ForeignKey('metacolumn.id', ondelete='CASCADE'))
    constraint_id = Column(Integer, ForeignKey('metaconstraint.id', ondelete='CASCADE'))

    __table_args__ = (
        Index('ix_rc_column_constraint', column_id, constraint_id, unique=True),
        Index('ix_rc_constraint_column', constraint_id, column_id)
    )
