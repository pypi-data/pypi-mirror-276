from typing import Dict

from database_mysql_local.generic_crud_ml import GenericCRUDML
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger

from .constants import REACTION_LOCAL_PYTHON_LOGGER_CODE


class ReactionsTypesLocal(GenericCRUDML, metaclass=MetaLogger, object=REACTION_LOCAL_PYTHON_LOGGER_CODE):
    """Reaction: the person's reaction to a service or a product (for example a post).
    Reaction Type: Manage reaction types"""
    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name="reaction_type", default_ml_table_name="reaction_type_ml_table",
                         default_view_with_deleted_and_test_data="reaction_type_ml_with_deleted_and_test_data_view",
                         is_test_data=is_test_data)

    def insert(self, *, reaction_type_dict: Dict[str, any] = None, reaction_type_ml_dict: Dict[str, any], lang_code: LangCode) -> (int, int):  # noqa
        reaction_type_dict = reaction_type_dict or {}
        reaction_type_id, reaction_type_ml_id = super().add_value(
            data_dict=reaction_type_dict, data_ml_dict=reaction_type_ml_dict, lang_code=lang_code)
        return reaction_type_id, reaction_type_ml_id

    def update(self, *, reaction_type_id: int, reaction_type_ml_id: int, lang_code: LangCode,
               reaction_type_dict: Dict[str, any] = None, reaction_type_ml_dict: Dict[str, any]) -> None:
        reaction_type_dict = reaction_type_dict or {}
        super().update_value_by_id(data_dict=reaction_type_dict, data_ml_dict=reaction_type_ml_dict,
                                   table_id=reaction_type_id, ml_table_id=reaction_type_ml_id, lang_code=lang_code)

    def select_multi_dict_by_reaction_type_id(self, reaction_type_id: int, lang_code: LangCode = None) -> list:
        reaction_type_dict = self.get_values_dict_list(table_id=reaction_type_id, lang_code=lang_code)
        return reaction_type_dict

    def select_one_dict_by_reaction_type_id(self, reaction_type_id: int, lang_code: LangCode = None) -> Dict[str, any]:
        reaction_type_dict = self.get_values_dict(table_id=reaction_type_id, lang_code=lang_code)
        return reaction_type_dict

    def delete_by_reaction_type_id(self, reaction_type_id: int) -> int:
        deleted_rows = super().delete_by_column_and_value(column_value=reaction_type_id)
        return deleted_rows

    def delete_by_reaction_type_title(self, reaction_type_title: str, lang_code: LangCode) -> int:
        deleted_rows = super().delete_by_name(name=reaction_type_title, lang_code=lang_code)
        return deleted_rows
