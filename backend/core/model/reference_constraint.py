from sqlalchemy import Column, ForeignKey, Integer, Index, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref

from core.model import base


class ReferenceConstraint(base):
    __tablename__ = 'referenceconstraint'

    column_id = Column(Integer, ForeignKey('metacolumn.id'))
    constraint_id = Column(Integer, ForeignKey('metaconstraint.id'))
    index = Column(Integer)

    column = relationship('MetaColumn',
                          backref=backref('reference_constraint_pairs', cascade='all, delete-orphan'))
    constraint = relationship('MetaConstraint',
                              backref=backref('reference_constraint_pairs', cascade='all, delete-orphan'))

    __table_args__ = (
        PrimaryKeyConstraint(column_id, constraint_id, name='pk_rc_column_constraint'),
        Index('ix_rc_constraint_column', constraint_id, column_id)
    )
