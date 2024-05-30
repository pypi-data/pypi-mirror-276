import datetime
from collections import defaultdict
from functools import lru_cache

from database_mysql_local.generic_crud_ml import GenericCRUDML
from logger_local.MetaLogger import MetaLogger

try:
    from .constants import LOGGER_CRITERIA_CODE_OBJECT, PEOPLE_ENTITY_TYPE_ID
except ImportError:  # needed for the CLI
    from constants import LOGGER_CRITERIA_CODE_OBJECT, PEOPLE_ENTITY_TYPE_ID

cache = {}

class Criterion:
    """Criterion class"""

    # TODO Why you changed main_entity_type_id to entity_type_id? - We might have multiple entity_type_ids, one of them will probably be the main_entity_type_id
    # TODO Shall we change is_test_data default to false everywhere?
    def __init__(self, *, entity_type_id: int = None, name: str = None, min_age: float = None,
                 max_age: float = None, group_list_id: int = None, min_number_of_kids: int = None,
                 max_number_of_kids: int = None, min_kids_age: float = None, max_kids_age: float = None,
                 gender_list_id: int = None, min_height: int = None, max_height: int = None,
                 partner_experience_level: int = None, number_of_partners: int = None,
                 location_id: int = None, location_list_id: int = None, coordinate: str = None,
                 radius: int = None, radius_measure: str = None, radius_km: int = None,
                 job_group_list_id: int = None, job_location_list_id: int = None,
                 vacancy_list_id: int = None, workplace_profile_list_id: int = None,
                 start_date_type_id: int = None, job_types_id: int = None, visibility_id: int = None,
                 where_sql: str = None,
                 is_test_data: bool = None, internet_domain_id: int = None,
                 internet_domain_list_id: int = None, organization_name: str = None, group_id: int = None,
                 profile_list_id: int = None, international_code: int = None, **kwargs) -> None:
        """Initialize a Criterion object."""
        for key, value in locals().items():
            if key not in ["self", "kwargs", "__class__"]:
                setattr(self, key, value)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        """Convert the Criterion object to a dictionary."""
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def __eq__(self, other: 'Criterion') -> bool:
        """Check if two Criterion objects are equal."""
        return self.to_dict() == other.to_dict()

# TODO: add the insert_ methods to queue
class CriteriaLocal(GenericCRUDML, metaclass=MetaLogger, object=LOGGER_CRITERIA_CODE_OBJECT):
    """CriteriaLocal class"""

    def __init__(self, is_test_data: bool = False) -> None:
        """
        Initialize the CriteriaLocal object.

        This class inherits from GenericCRUD.

        :rtype: None
        """
        super().__init__(default_schema_name="criteria",
                         default_table_name="criteria_table",
                         default_view_table_name="criteria_view",
                         default_column_name="criteria_id",
                         is_test_data=is_test_data)

    def insert(self, criterion: Criterion) -> int:  # noqa
        """
        Insert a criterion into the database.
        criterion.entity_type_id is required.

        :param criterion: The criterion to insert.
        :type criterion: Criterion
        :rtype: None
        """
        criteria_dict = criterion.to_dict()
        criterion_id = super().insert(data_dict=criteria_dict)
        return criterion_id

    def update(self, criteria_id: int, new_criterion: Criterion) -> None:
        """
        Update a criterion in the database.

        :param criteria_id: The ID of the criterion to update.
        :param new_criterion: The new criterion.
        :type criteria_id: int
        :type new_criterion: Criterion
        :rtype: None
        """
        criteria_dict = new_criterion.to_dict()
        super().update_by_column_and_value(column_value=criteria_id, data_dict=criteria_dict)

    def select_criterion_object(self, criteria_id: int) -> Criterion:
        """
        Select a criterion from the database.

        :param criteria_id: The ID of the criterion to select.
        :type criteria_id: int
        :rtype: Criterion
        """
        criterion = self.select_criterion_dict(criteria_id=criteria_id)
        criterion_object = Criterion(**criterion)
        return criterion_object

    def select_criterion_dict(self, criteria_id: int) -> dict:
        """
        Select a criterion from the database.

        :param criteria_id: The ID of the criterion to select.
        :type criteria_id: int
        :rtype: dict
        """
        criterion_dict = super().select_one_dict_by_column_and_value(column_value=criteria_id)
        return criterion_dict

    def delete(self, criteria_id: int) -> None:
        """
        Delete a criterion from the database.

        :param criteria_id: The ID of the criterion to delete.
        :type criteria_id: int
        :rtype: None
        """
        self.delete_by_column_and_value(column_value=criteria_id)

    def get_test_criteria_id(self, criterion: Criterion = None, **kwargs) -> int:
        if not criterion:
            criterion = Criterion(entity_type_id=PEOPLE_ENTITY_TYPE_ID, is_test_data=True, **kwargs)
        test_criteria_id = super().get_test_entity_id(
            entity_name="criteria", insert_function=self.insert, insert_kwargs={"criterion": criterion})
        return test_criteria_id

    def get_entity_criteria_by_criterion(self, *, criterion: Criterion, is_criteria: bool = True) -> dict:
        """Get entity details by criterion, based on entity_type_id and where_sql using entity_type_view
        For example, criterion.entity_type_id=17 will return values from people_view, as per entity_type_view"""
        where_sql = criterion.where_sql  # noqa
        entity_type_id = criterion.entity_type_id  # noqa

        # TODO: move to entity repo
        schema_key = "criteria_schema_name" if is_criteria else "schema_name"
        view_key = "criteria_view_name" if is_criteria else "view_name"
        select_clause_value = f"{schema_key}, {view_key}"
        entity = self.select_one_dict_by_column_and_value(
            schema_name="entity_type", view_table_name="entity_type_view",
            column_name="entity_type_id", column_value=entity_type_id,
            select_clause_value=select_clause_value)
        if not entity:
            raise Exception(f"entity_type_id {entity_type_id} is not supported")
        schema_name = entity[schema_key]
        view_table_name = entity[view_key]
        if not schema_name or not view_table_name:
            raise Exception(f"{schema_key} or {view_key} not found for entity_type_id {entity_type_id}.\n"
                            f"{schema_key}: {schema_name}, {view_key}: {view_table_name}")
        entity_dict = self.select_one_dict_by_where(
            schema_name=schema_name, view_table_name=view_table_name,
            where=where_sql, select_clause_value="*")
        return entity_dict

    @lru_cache
    def get_childs_criteria_set_ids_per_parent(self) -> dict[int, list[dict]]:
        select_clause_value = "parent_criteria_set_id, child_criteria_set_id, criteria_id, entity_type_id"
        all_rows = self.select_multi_dict_by_where(view_table_name="criteria_set_general_view",
                                                   select_clause_value=select_clause_value, where="TRUE")
        childs_criteria_set_ids_per_parent = {}
        for row in all_rows:
            parent_criteria_set_id = row["parent_criteria_set_id"]
            row.pop("parent_criteria_set_id")
            if parent_criteria_set_id not in childs_criteria_set_ids_per_parent:
                childs_criteria_set_ids_per_parent[parent_criteria_set_id] = []
            childs_criteria_set_ids_per_parent[parent_criteria_set_id].append(row)
        return childs_criteria_set_ids_per_parent

    def get_criterias_per_criteria_set_id(self, criteria_set_ids: list[int]) -> dict[int, list[dict]]:
        """Given (parent) criteria_set_id, find its child_criteria_set_id which now becomes parent_criteria_set_id,
            and continue recursively until all child_criteria_set_id not found in parent_criteria_set_id.
            For each such leaf, return its critiria_id and entity_type_id"""

        childs_criteria_set_ids_per_parent = self.get_childs_criteria_set_ids_per_parent()
        criterias_per_criteria_set_ids = defaultdict(list)

        def recursive_find_criteria_set(parent_criteria_set_id: int) -> None:
            if parent_criteria_set_id not in childs_criteria_set_ids_per_parent:
                # it's a child
                for childs in childs_criteria_set_ids_per_parent.values():
                    for child in childs:
                        if child["child_criteria_set_id"] == parent_criteria_set_id:
                            if not child["criteria_id"] or not child["entity_type_id"]:
                                raise Exception(f"criteria_id and entity_type_id not found for criteria_set_id "
                                                f"{parent_criteria_set_id}")
                            criterias_per_criteria_set_ids[parent_criteria_set_id].append(
                                {"criteria_id": child["criteria_id"], "entity_type_id": child["entity_type_id"]})
                            return
            for row in childs_criteria_set_ids_per_parent[parent_criteria_set_id]:
                if row["child_criteria_set_id"] in childs_criteria_set_ids_per_parent:
                    recursive_find_criteria_set(row["child_criteria_set_id"])
                elif row["criteria_id"] and row["entity_type_id"]:  # leaf
                    criterias_per_criteria_set_ids[parent_criteria_set_id].append(
                        {"criteria_id": row["criteria_id"], "entity_type_id": row["entity_type_id"]})

        for criteria_set_id in criteria_set_ids:
            recursive_find_criteria_set(criteria_set_id)
        if not criterias_per_criteria_set_ids:
            raise Exception(f"No criteria found for criteria_set_ids {criteria_set_ids}")
        return criterias_per_criteria_set_ids

    def _get_entity_where(self, *, entity_list_id: int, entity_id: int, entity_name: str,
                          column_name: str, schema_name: str = None) -> str:
        if entity_list_id and entity_id:
            self.logger.warning(f"Both {entity_name}_list_id and {entity_name}_id are provided. Ignoring the list.")

        if entity_id is not None:
            where = f" AND {column_name} = {entity_id}"
        elif entity_list_id is not None:
            entity_cache_key = (entity_name, entity_list_id)
            if entity_cache_key not in cache:
                schema_name = schema_name or entity_name
                entity_in_list = self.sql_in_list_by_entity_list_id(
                    schema_name=schema_name, entity_name=entity_name, entity_list_id=entity_list_id)
                cache[entity_cache_key] = entity_in_list
            else:
                entity_in_list = cache[entity_cache_key]

            where = f" AND {column_name} " + entity_in_list
        else:
            where = ""
        return where

    def get_where_by_criteria_dict(self, criteria_dict: dict) -> str:
        # TODO add support to user_external_id in criteria_dict
        min_age = criteria_dict.get("min_age")
        max_age = criteria_dict.get("max_age")

        # profile_id didn't receive messages from this campaign for campaign.minimal_days
        where = "TRUE "
        if min_age is not None:
            where += f" AND TIMESTAMPDIFF(YEAR, person_birthday_date, CURDATE()) >= {min_age}"
        if max_age is not None:
            where += f" AND TIMESTAMPDIFF(YEAR, person_birthday_date, CURDATE()) <= {max_age}"

        where += self._get_entity_where(
            entity_list_id=criteria_dict.get("gender_list_id"), entity_id=criteria_dict.get("gender_id"),
            entity_name="gender", column_name="gender_id")
        where += self._get_entity_where(
            entity_list_id=criteria_dict.get("location_list_id"), entity_id=criteria_dict.get("location_id"),
            entity_name="location", column_name="location_id")
        where += self._get_entity_where(
            entity_list_id=criteria_dict.get("group_list_id"), entity_id=criteria_dict.get("group_id"),
            entity_name="group", column_name="group_profile.group_id")
        where += self._get_entity_where(
            entity_list_id=criteria_dict.get("country_list_id"), entity_id=criteria_dict.get("country_id"),
            entity_name="country", column_name="country_id", schema_name="location")
        where += self._get_entity_where(
            entity_list_id=criteria_dict.get("county_list_id"), entity_id=criteria_dict.get("county_id"),
            entity_name="county", column_name="county_id", schema_name="location")
        where += self._get_entity_where(
            entity_list_id=criteria_dict.get("state_list_id"), entity_id=criteria_dict.get("state_id"),
            entity_name="state", column_name="state_id", schema_name="location")
        where += self._get_entity_where(
            entity_list_id=criteria_dict.get("city_list_id"), entity_id=criteria_dict.get("city_id"),
            entity_name="city", column_name="city_id", schema_name="location")
        where += self._get_entity_where(
            entity_list_id=criteria_dict.get("label_list_id"), entity_id=criteria_dict.get("label_id"),
            entity_name="label", column_name="label_id")
        self.logger.info(object={"criteria_dict": criteria_dict, "where": where})
        return where

    def get_profiles_ids_satisfying_criteria(self, criteria_dict: dict, append_where: str = None) -> list[int]:
        """Get a list of profile ids for the given criteria_dict
        :param criteria_dict: dictionary of criteria, each of which includes:
            min_age, max_age, gender_list_id, group_list_id
        :param append_where: additional where clause to append to the query (add parentheses if needed)"""
        function_name = "get_profiles_satisfying_criteria"
        if function_name not in cache:
            cache[function_name] = {}
        cache_key = str(criteria_dict)
        if cache_key in cache[function_name]:
            return cache[function_name][cache_key]

        where = self.get_where_by_criteria_dict(criteria_dict)
        if append_where:
            # assert all(recipient.get_profile_id() is not None for recipient in recipients)
            # profile_ids_str = ",".join(str(recipient.get_profile_id()) for recipient in recipients)
            # where += f" AND user.profile_id IN ({profile_ids_str})"
            where = f"({where}) {append_where}"
        # Old:             SELECT DISTINCT user_id,
        #                             person_id,
        #                             user_main_email_address,
        #                             user.profile_id AS profile_id,
        #                             profile_phone_full_number_normalized,
        #                             profile_preferred_lang_code
        query_for_potentials_recipients = f"""
            SELECT DISTINCT profile.profile_id AS profile_id
            FROM profile.profile_view AS profile """
        if criteria_dict.get("min_age") or criteria_dict.get("max_age"):
            query_for_potentials_recipients += """
            LEFT JOIN person_profile.person_profile_view AS person_profile
                ON person_profile.profile_id = profile.profile_id 
            LEFT JOIN person.person_general_view AS person
                ON person.person_id = profile.main_person_id """
        if criteria_dict.get("group_id") or criteria_dict.get("group_list_id"):
            query_for_potentials_recipients += """
                  LEFT JOIN group_profile.group_profile_view AS group_profile
                     on group_profile.profile_id = profile.profile_id"""
        if (criteria_dict.get("location_id") or criteria_dict.get("location_list_id")
                or criteria_dict.get("country_id") or criteria_dict.get("country_list_id")
                or criteria_dict.get("county_id") or criteria_dict.get("county_list_id")
                or criteria_dict.get("state_id") or criteria_dict.get("state_list_id")
                or criteria_dict.get("city_id") or criteria_dict.get("city_list_id")):
            if criteria_dict.get("label_id") or criteria_dict.get("label_list_id"):
                view_name = "location_profile_label_general_view"
            else:
                view_name = "location_profile_general_view"
            query_for_potentials_recipients += f"""
                  LEFT JOIN location_profile.{view_name} AS location_profile
                     on location_profile.profile_id = profile.profile_id"""

        query_for_potentials_recipients += f" WHERE {where}"
        query_for_potentials_recipients += " LIMIT 2000"
        # columns = ("user_id, person_id, user_main_email_address, profile_id,"
        #            "profile_phone_full_number_normalized, profile_preferred_lang_code")
        self.cursor.execute(query_for_potentials_recipients)
        profiles_ids = [row[0] for row in self.cursor.fetchall()]
        cache[function_name][cache_key] = profiles_ids
        return profiles_ids

    def get_criteria_set_ids_list_by_campaign_id(self, campaign_id: int) -> list[int]:
        """Given a campaign_id, find its criteria_set_ids from campaign_criteria_set_view"""
        criteria_set_ids = self.select_multi_value_by_column_and_value(
            schema_name="campaign_criteria_set", view_table_name="campaign_criteria_set_view",
            select_clause_value="criteria_set_id", column_name="campaign_id", column_value=campaign_id)
        return criteria_set_ids

    def get_profile_ids_per_criteria_and_criteria_set_id(
            self, criteria_set_ids: list[int], append_where: str = None) -> (
    dict[int, list[int]], dict[int, list[int]]):
        profile_ids_per_criteria_id = {}
        profile_ids_per_criteria_set_id = {}
        criterias_per_criteria_set_id = self.get_criterias_per_criteria_set_id(criteria_set_ids)
        for criteria_set_id, criterias in criterias_per_criteria_set_id.items():
            for criteria in criterias:
                criterion = Criterion(criteria_id=criteria["criteria_id"], entity_type_id=criteria["entity_type_id"],
                                      where_sql="criteria_id=" + str(criteria["criteria_id"]))
                entity_dict = self.get_entity_criteria_by_criterion(criterion=criterion)
                profiles_ids = self.get_profiles_ids_satisfying_criteria(
                    criteria_dict=entity_dict, append_where=append_where)
                profile_ids_per_criteria_id[criteria["criteria_id"]] = profiles_ids
                profile_ids_per_criteria_set_id[criteria_set_id] = profiles_ids
        return profile_ids_per_criteria_id, profile_ids_per_criteria_set_id

    def insert_profiles_by_campaign_id(self, campaign_id: int) -> None:
        criteria_set_ids = self.get_criteria_set_ids_list_by_campaign_id(campaign_id)
        self.insert_profiles_by_criteria_set_ids(criteria_set_ids)

    def insert_profiles_by_criteria_set_ids(self, criteria_set_ids: list[int], append_where: str = None) -> None:
        """
        1. Find all the criteria_ids and entity_type_ids from criteria_set_general_view.
        2. With the entities, get schema_name & criteria_table_name from entity_type_view.
        3. For each entity, get all the profiles that satisfy the criteria.
        4. Insert the profile_id, criteria_id, and batch_timestamp into criteria_profile_table.
        """
        profile_ids_per_criteria_id, profile_ids_per_criteria_set_id = self.get_profile_ids_per_criteria_and_criteria_set_id(
            criteria_set_ids=criteria_set_ids, append_where=append_where)
        batch_timestamp = datetime.datetime.now(datetime.UTC)  # Note: may not be the sql server time
        data_dicts_criterias = []
        data_dicts_criteria_sets = []
        for criteria_set_id, profiles_ids in profile_ids_per_criteria_set_id.items():
            for profile_id in profiles_ids:
                data_dict_criteria_set = {
                    "profile_id": profile_id,
                    "criteria_set_id": criteria_set_id,
                    "batch_timestamp": batch_timestamp
                }

                if data_dict_criteria_set not in data_dicts_criteria_sets:
                    data_dicts_criteria_sets.append(data_dict_criteria_set)

        for criteria_id, profiles_ids in profile_ids_per_criteria_id.items():
            for profile_id in profiles_ids:
                data_dict_criteria = {
                    "profile_id": profile_id,
                    "criteria_id": criteria_id,
                    "batch_timestamp": batch_timestamp
                }
                if data_dict_criteria not in data_dicts_criterias:
                    data_dicts_criterias.append(data_dict_criteria)

        # insert to criteria_profile
        inserted_rows_criteria = super().insert_many_dicts(
            schema_name="criteria_profile", table_name="criteria_profile_table", data_dicts=data_dicts_criterias)
        inserted_rows_criteria_set = super().insert_many_dicts(
            schema_name="criteria_profile", table_name="criteria_set_profile_table",
            data_dicts=data_dicts_criteria_sets)
        self.logger.debug(object=locals())

    def get_profile_ids_per_criteria_set_id(self, criteria_set_ids: list[int]) -> dict[int, list[int]]:
        """Given a set of criteria_set_ids, find the profile_ids from criteria_set_profile_table"""
        result = self.select_multi_dict_by_column_and_value(
            schema_name="criteria_profile", view_table_name="criteria_set_profile_view",
            select_clause_value="criteria_set_id, profile_id",
            column_name="criteria_set_id", column_value=criteria_set_ids)

        profile_ids_per_criteria_set_id = defaultdict(list)
        for row in result:
            profile_ids_per_criteria_set_id[row["criteria_set_id"]].append(row["profile_id"])
        return profile_ids_per_criteria_set_id

    def get_profile_ids_by_criteria_id(self, criteria_id: int) -> list[int]:
        """Given a criteria_id, find the profile_ids from criteria_profile_table"""
        profile_ids = self.select_multi_value_by_column_and_value(
            schema_name="criteria_profile", view_table_name="criteria_profile_view",
            select_clause_value="profile_id", column_name="criteria_id", column_value=criteria_id)
        return profile_ids


if __name__ == "__main__":
    # CLI
    import argparse

    parser = argparse.ArgumentParser(description="Insert profiles by criteria_set_ids or campaign_id")
    parser.add_argument("--campaign_id", type=int, required=False)
    parser.add_argument("--criteria_set_ids", type=int, nargs="+", required=False)

    args = parser.parse_args()
    print(args)
    criteria_local = CriteriaLocal()
    if args.campaign_id:
        criteria_local.insert_profiles_by_campaign_id(campaign_id=args.campaign_id)
    elif args.criteria_set_ids:
        criteria_local.insert_profiles_by_criteria_set_ids(criteria_set_ids=args.criteria_set_ids)
    else:
        parser.print_help()
