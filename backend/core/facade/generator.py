from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from core.facade.column import ColumnFacade
from core.facade.table import TableFacade
from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.model.project import Project
from core.model.user import User
from core.service.column_generator.assignment import GeneratorAssignment
from core.service.column_generator.setting_facade import GeneratorSettingFacade
from core.service.exception import SomeError
from core.service.injector import Injector


class GeneratorFacade:
    def __init__(self,
                 db_session: Session,
                 user: User,
                 table_facade: TableFacade,
                 column_facade: ColumnFacade,
                 injector: Injector):
        self._db_session = db_session
        self._user = user
        self._table_facade = table_facade
        self._column_facade = column_facade
        self._injector = injector

    def find_setting(self, generator_setting_id: int) -> GeneratorSetting:
        return self._db_session.\
            query(GeneratorSetting).\
            join(GeneratorSetting.table).\
            join(MetaTable.project).\
            join(Project.user).\
            filter(
                GeneratorSetting.id == generator_setting_id,
                Project.user == self._user
            ).\
            one()

    def find_setting_in_table(self,
                              generator_setting_id: int,
                              meta_table: MetaTable) -> GeneratorSetting:
        return self._db_session.\
            query(GeneratorSetting).\
            filter(
                GeneratorSetting.id == generator_setting_id,
                GeneratorSetting.table == meta_table
            ).\
            one()

    def create_generator_setting(self,
                                 table_id: int,
                                 column_id: Optional[int],
                                 name: str,
                                 params: dict,
                                 null_frequency: float) -> GeneratorSetting:
        meta_column = None
        try:
            meta_table = self._table_facade.find_meta_table(table_id)
            if column_id is not None:
                meta_column = self._column_facade.find_column_in_table(
                    meta_table,
                    column_id
                )
        except NoResultFound:
            raise SomeError('Table or column not found')

        generator_setting = GeneratorSetting(
            table=meta_table,
            name=name,
            params=params,
            null_frequency=null_frequency
        )
        if meta_column is not None:
            meta_column.generator_setting = generator_setting
            facade = GeneratorSettingFacade(generator_setting)
            facade.maybe_estimate_params(self._injector)
        self._db_session.add(generator_setting)
        return generator_setting

    def update_column_generator(self, meta_column: MetaColumn, generator_setting_id: int) -> bool:
        generator_setting = self.find_setting_in_table(
            generator_setting_id,
            meta_column.table
        )

        if not GeneratorAssignment.maybe_assign(generator_setting, meta_column):
            return False

        facade = GeneratorSettingFacade(generator_setting)
        facade.maybe_estimate_params(self._injector)
        return True
