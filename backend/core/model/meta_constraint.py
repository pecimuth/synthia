from sqlalchemy import Column, Integer, String, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship

from core.model import base
from core.model.column_constraint import ColumnConstraint
from core.model.reference_constraint import ReferenceConstraint


class MetaConstraint(base):
    PRIMARY = 'primary'
    FOREIGN = 'foreign'
    UNIQUE = 'unique'
    CHECK = 'check'

    __tablename__ = 'metaconstraint'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)

    table_id = Column(Integer, ForeignKey('metatable.id', ondelete='CASCADE'))
    table = relationship('MetaTable', back_populates='constraints')

    constraint_type = Column(String)  # PRIMARY | FOREIGN | UNIQUE | CHECK
    constrained_columns = relationship(
        'MetaColumn',
        secondary=ColumnConstraint.__table__,
        order_by=ColumnConstraint.__table__.c.column_order,
        back_populates='constraints'
    )
    referenced_columns = relationship(
        'MetaColumn',
        secondary=ReferenceConstraint.__table__,
        order_by=ReferenceConstraint.__table__.c.column_order
    )
    check_expression = Column(String, nullable=True)

    __table_args__ = (
        Index('ix_metaconstraint_table_name', table_id, name, unique=True),
    )
