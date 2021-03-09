from sqlalchemy import Column, Integer, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.orm import backref, relationship

from core.model import base


class ColumnConstraint(base):
    __tablename__ = 'columnconstraint'

    column_id = Column(Integer, ForeignKey('metacolumn.id', ondelete='CASCADE'))
    constraint_id = Column(Integer, ForeignKey('metaconstraint.id', ondelete='CASCADE'))
    index = Column(Integer)

    column = relationship('MetaColumn',
                          backref=backref('column_constraint_pairs', cascade='all, delete-orphan'))
    constraint = relationship('MetaConstraint',
                              backref=backref('column_constraint_pairs', cascade='all, delete-orphan'))

    __table_args__ = (
        PrimaryKeyConstraint(column_id, constraint_id, name='pk_cc_column_constraint'),
        Index('ix_cc_constraint_column', constraint_id, column_id)
    )
