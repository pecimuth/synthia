from sqlalchemy import Column, Integer, String, ForeignKey, Index
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

    table_id = Column(Integer, ForeignKey('metatable.id'))
    table = relationship('MetaTable', back_populates='constraints')

    constraint_type = Column(String)  # PRIMARY | FOREIGN | UNIQUE | CHECK
    constrained_columns = relationship(
        'MetaColumn',
        secondary=ColumnConstraint.__table__,
        order_by=ColumnConstraint.__table__.c.id,
        back_populates='constraints',
        passive_deletes=True
    )
    referenced_columns = relationship(
        'MetaColumn',
        secondary=ReferenceConstraint.__table__,
        order_by=ReferenceConstraint.__table__.c.id,
        passive_deletes=True
    )
    check_expression = Column(String, nullable=True)

    __table_args__ = (
        Index('ix_metaconstraint_table_name', table_id, name, unique=True),
    )

    def __repr__(self):
        return '<MetaConstraint(id={},name={},table_id={})>'.format(
            self.id,
            self.name,
            self.table.id
        )
