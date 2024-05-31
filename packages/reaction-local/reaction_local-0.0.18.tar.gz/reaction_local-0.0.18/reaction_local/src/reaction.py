from typing import Dict

from database_mysql_local.generic_crud_ml import GenericCRUDML
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger

from .constants import REACTION_LOCAL_PYTHON_LOGGER_CODE


class ReactionsLocal(GenericCRUDML, metaclass=MetaLogger, object=REACTION_LOCAL_PYTHON_LOGGER_CODE):
    """Reaction: the person's reaction to a service or a product (for example a post).
    Reaction Type: Manage reaction types"""
    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name="reaction", default_ml_table_name="reaction_ml_table",
                         default_view_with_deleted_and_test_data="reaction_ml_with_deleted_and_test_data_view",
                         is_test_data=is_test_data)

    def insert(self, *, reaction_dict: Dict[str, any] = None, reaction_ml_dict: Dict[str, any], lang_code: LangCode) -> (int, int):  # noqa
        reaction_dict = reaction_dict or {}
        reaction_id, reaction_ml_id = super().add_value(
            data_dict=reaction_dict, data_ml_dict=reaction_ml_dict, lang_code=lang_code)
        return reaction_id, reaction_ml_id
        # Old code:
        # reaction_id = self.select_one_value_by_column_and_value(
        #     select_clause_value="reaction_id", view_table_name="reaction_ml_view",
        #     column_name="title", column_value=reaction_dict["title"])
        #
        # if not reaction_id:
        #     reaction_id = super().insert(table_name="reaction_table", data_dict={})
        #     super().insert(table_name="reaction_ml_table", data_dict={
        #         "reaction_id": reaction_id, "lang_code": lang_code.value, "title": reaction_dict["title"]})
        #
        # reaction_id = super().insert(data_dict={"value": reaction_dict["value"], "image": reaction_dict["image"],
        #                                         "reaction_id": reaction_id})
        # reaction_ml_id = super().insert(table_name="reaction_ml_table", data_dict={
        #     "reaction_id": reaction_id, "lang_code": lang_code.value, "title": reaction_dict["title"],
        #     "description": reaction_dict["description"]})
        # return reaction_id, reaction_ml_id

    def update(self, *, reaction_id: int, reaction_ml_id: int, lang_code: LangCode,
               reaction_dict: Dict[str, any] = None, reaction_ml_dict: Dict[str, any]) -> None:
        reaction_dict = reaction_dict or {}
        super().update_value_by_id(data_dict=reaction_dict, data_ml_dict=reaction_ml_dict,
                                   table_id=reaction_id, ml_table_id=reaction_ml_id, lang_code=lang_code)
        # Old code:
        # super().update_by_column_and_value(data_dict={"value": reaction_dict["value"], "image": reaction_dict["image"]},
        #                                    column_value=reaction_id)
        # super().update_by_column_and_value(table_name="reaction_ml_table", column_value=reaction_id, data_dict={
        #     "title": reaction_dict["title"], "description": reaction_dict["description"],
        #     "is_name_approved": is_name_approved, "is_description_approved": is_description_approved})

    def select_multi_dict_by_reaction_id(self, reaction_id: int, lang_code: LangCode = None) -> list:
        reaction_dict = self.get_values_dict_list(table_id=reaction_id, lang_code=lang_code)
        return reaction_dict

    def select_one_dict_by_reaction_id(self, reaction_id: int, lang_code: LangCode = None) -> Dict[str, any]:
        reaction_dict = self.get_values_dict(table_id=reaction_id, lang_code=lang_code)
        return reaction_dict

    def delete_by_reaction_id(self, reaction_id: int) -> int:
        deleted_rows = super().delete_by_column_and_value(column_value=reaction_id)
        return deleted_rows

    def delete_by_reaction_title(self, reaction_title: str, lang_code: LangCode) -> int:
        deleted_rows = super().delete_by_name(name=reaction_title, lang_code=lang_code)
        return deleted_rows

    @staticmethod  # TODO: where is used? Can we delete?
    def get_reaction_dict_from_entry(entry: Dict[str, Dict[str, any]]) -> Dict[str, any]:
        reaction_dict = {
            "value": entry["reaction"].get("value"),
            "image": entry["reaction"].get("image"),
            "title": entry["reaction"].get("title")
        }
        return reaction_dict
