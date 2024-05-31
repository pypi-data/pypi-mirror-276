import datetime

from database_infrastructure_local.number_generator import NumberGenerator
from database_mysql_local.connector import Connector
from language_remote.lang_code import LangCode
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import Logger
from people_local.people import PeopleLocal
from user_context_remote.user_context import UserContext

from .person import Person

PERSONS_LOCAL_PYTHON_COMPONENT_ID = 169
PERSONS_LOCAL_PYTHON_COMPONENT_NAME = 'person-local-python'

person_local_python_code_logger_init_object = {
    'component_id': PERSONS_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': PERSONS_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": "jenya.b@circ.zone"
}
logger = Logger.create_logger(
    object=person_local_python_code_logger_init_object)

user_context = UserContext()


class PersonsLocal(PeopleLocal):
    """PersonsLocal class"""

    def __init__(self,
                 first_name_original: str = None,
                 last_names_original: str = None,
                 organizations_names_original: list = None,
                 email_addresses: list = None,
                 urls: list = None,
                 is_test_data: bool = False) -> None:
        PeopleLocal.__init__(self,
                             default_schema_name="person", default_table_name="person_table",
                             default_view_table_name="person_view", default_column_name='person_id',
                             first_name_original=first_name_original,
                             last_names_original=last_names_original,
                             organizations_names_original=organizations_names_original,
                             email_addresses=email_addresses,
                             urls=urls, is_test_data=is_test_data)

    def get_person_id_by_person_number(self, person_number: int) -> int or None:
        logger.start(object={'person_number': person_number})
        person_id = self.select_one_value_by_column_and_value(column_name='number',
                                                              select_clause_value='person_id',
                                                              column_value=person_number)
        logger.end(object={'person_id': person_id})
        return person_id

    def get_person_number_by_person_id(self, person_id: int) -> int:
        logger.start(object={'person_id': person_id})
        person_number = None
        fetched_result = self.select_multi_dict_by_column_and_value(select_clause_value='number',
                                                                    column_value=person_id)
        if fetched_result:
            person_number = fetched_result[0]['number']
        logger.end(object={'person_number': person_number})
        return person_number

    def get_person_id_by_email_address_str(self, email_address: str) -> int or None:
        logger.start(object={'email_address': email_address})
        person_id = None
        result = self.select_one_dict_by_column_and_value(column_name='main_email_person',
                                                          select_clause_value='person_id',
                                                          column_value=email_address)
        if result:
            person_id = result['person_id']
        logger.end(object={'person_id': person_id})
        return person_id

    def insert(self, person: Person) -> int:  # noqa
        logger.start("Insert person", object={
            "number": person.number,
            "gender_id": person.gender_id,
            "last_coordinate": person.last_coordinate,
            "location_id": person.location_id,
            'birthday_date': person.birthday_date,
            'day': person.day,
            'month': person.month,
            'year': person.year,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'nickname': person.nickname,
            'father_name': person.father_name,
            'main_email_address': person.main_email_address,
            'birthday_original': person.birthday_original,
            'is_approved': person.is_approved,
            'is_identity_confirmed': person.is_identity_confirmed,
            'birthday_timestamp': person.birthday_timestamp,
            'year_cira': person.year_cira,
            'is_first_name_approved': person.is_first_name_approved,
            'is_nickname_approved': person.is_nickname_approved,
            'last_location_id': person.last_location_id,
            'is_rip': person.is_rip,
            'name': person.name,
            'main_full_number_normalized': person.main_full_number_normalized,
            'is_test_data': person.is_test_data
        })
        # TODO: We should handle also situations when there is no person.number
        # and we need to generate it using database-with-out-orm package number_generator()

        x_coordinate, y_coordinate = float(
            person.last_coordinate.longitude), float(person.last_coordinate.latitude)
        query = (
            "INSERT INTO person_table (number, gender_id, last_coordinate, "
            "location_id, birthday_date, day, month, year, first_name, last_name, nickname, is_test_data,"
            " father_name, main_email_person, birthday_original, is_approved, is_identity_confirmed, "
            "birthday_timestamp, year_cira, is_first_name_approved, is_nickname_approved, "
            "last_location_id, is_rip, name, main_full_number_normalized, start_timestamp) "
            "VALUES (%s, %s, POINT(%s, %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)"
        )

        data = (person.number, person.gender_id, x_coordinate, y_coordinate,
                person.location_id, person.birthday_date, person.day, person.month,
                person.year, person.first_name, person.last_name, person.nickname,
                person.is_test_data, person.father_name, person.main_email_address,
                person.birthday_original, person.is_approved, person.is_identity_confirmed,
                person.birthday_timestamp, person.year_cira, person.is_first_name_approved,
                person.is_nickname_approved, person.last_location_id, person.is_rip, person.name,
                person.main_full_number_normalized)

        """person_detail = {
            "number": person.number,
            "gender_id": person.gender_id,
            "last_coordinate": person.last_coordinate,
            "location_id": person.location_id
        }"""
        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, data)
        connection.commit()
        logger.info("Person inserted successfully.")
        person_id = cursor.lastrowid()
        logger.end(f"Person added person_id= {person_id}", object={
            'person_id': person_id})
        return person_id

    @staticmethod
    def _insert_person_ml(person_id: int, first_name: str, last_name: str,
                          lang_code: LangCode = None,
                          is_first_name_approved: bool = False,
                          is_last_name_approved: bool = False) -> int:
        logger.start("Insert person", object={"person_id": person_id, "lang_code": lang_code,
                                              "first_name": first_name, "last_name": last_name})
        lang_code = lang_code or LangCode.detect_lang_code_restricted(
            text=first_name, default_lang_code=LangCode.ENGLISH)
        query = (
            f"INSERT INTO person_ml_table (person_id, lang_code, first_name, last_name, "
            f"is_first_name_approved, is_last_name_approved) "
            f"VALUES ({person_id}, '{lang_code.value}', '{first_name}', '{last_name}', '{is_first_name_approved}',"
            f" '{is_last_name_approved}')"
        )
        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query)
        connection.commit()
        logger.end("Person added", object={'person_id': person_id})
        return person_id

    def insert_if_not_exists(self, person: Person,
                             lang_code: LangCode = None) -> tuple:
        logger.start("Insert person", object={
            "gender_id": person.gender_id,
            "last_coordinate": person.last_coordinate,
            "location_id": person.location_id,
            'birthday_date': person.birthday_date,
            'day': person.day,
            'month': person.month,
            'year': person.year,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'nickname': person.nickname,
            'father_name': person.father_name,
            'main_email_address': person.main_email_address,
            'main_full_number_normalized': person.main_full_number_normalized,
            'birthday_original': person.birthday_original,
            'is_approved': person.is_approved,
            'is_identity_confirmed': person.is_identity_confirmed,
            'birthday_timestamp': person.birthday_timestamp,
            'year_cira': person.year_cira,
            'is_first_name_approved': person.is_first_name_approved,
            'is_nickname_approved': person.is_nickname_approved,
            'last_location_id': person.last_location_id,
            'is_rip': person.is_rip,
            'name': person.name,
        })
        person_id = super().select_one_value_by_column_and_value(
            view_table_name='person_view',
            select_clause_value='person_id',
            column_value=person.name,
            column_name='name'
        )
        if person_id:  # TODO: test this part
            ml_person_id = super().select_one_value_by_column_and_value(
                view_table_name='person_ml_view',
                select_clause_value='person_ml_id',
                column_value=person_id,
                column_name='person_id'
            )
            logger.end(object={"person_id": person_id, "person_ml_id": ml_person_id})
            return person_id, ml_person_id
        lang_code = lang_code or LangCode.detect_lang_code_restricted(
            text=person.first_name, default_lang_code=LangCode.ENGLISH)
        # Insert to person__table
        data_dict = {
            "gender_id": person.gender_id,
            "last_coordinate": person.last_coordinate,
            "location_id": person.location_id,
            'birthday_date': person.birthday_date,
            'day': person.day,
            'month': person.month,
            'year': person.year,
            'first_name': person.first_name,
            'name': person.name,
            'last_name': person.last_name,
            'nickname': person.nickname,
            'father_name': person.father_name,
            'main_email_person': person.main_email_address,
            'main_full_number_normalized': person.main_full_number_normalized,
            'birthday_original': person.birthday_original,
            'is_approved': person.is_approved,
            'is_identity_confirmed': person.is_identity_confirmed,
            'birthday_timestamp': person.birthday_timestamp,
            'year_cira': person.year_cira,
            'is_first_name_approved': person.is_first_name_approved,
            'is_nickname_approved': person.is_nickname_approved,
            'last_location_id': person.last_location_id,
            'is_rip': person.is_rip,
        }
        data_compare_dict = {"name": person.name,
                             "main_email_person": person.main_email_address,
                             "main_full_number_normalized": person.main_full_number_normalized}
        person_id = super().insert_if_not_exists(data_dict=data_dict, table_name='person_table',
                                                 view_table_name='person_view', data_dict_compare=data_compare_dict,
                                                 compare_with_or=True)

        # Insert to person_ml_table
        data_dict_ml = {
            "first_name": person.first_name,
            "last_name": person.last_name,
            "person_id": person_id,
            "lang_code": lang_code.value,
            "is_first_name_approved": person.is_first_name_approved,
            "is_last_name_approved": person.is_last_name_approved
        }
        data_ml_compare_dict = {"person_id": person_id, "lang_code": lang_code.value}
        person_ml_id = super().insert_if_not_exists(table_name="person_ml_table", data_dict=data_dict_ml,
                                                    view_table_name="person_ml_view", data_dict_compare=data_ml_compare_dict)
        logger.end(object={"person_id": person_id, "person_ml_id": person_ml_id})
        return person_id, person_ml_id

    @staticmethod
    def update_birthday_day(person_id: int, day: int) -> None:
        """update birthday day"""
        logger.start(f"Update birthday day by person id person_id={person_id}",
                     object={"person_id": person_id, "day": day})
        query = (
            f"UPDATE person_table SET day = {day}, "
            f"birthday_date = CONCAT(YEAR(birthday_date), '-', MONTH(birthday_date), '-', {day}) "
            f"WHERE person_id = {person_id}"
        )
        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query)
        connection.commit()
        logger.end()

    @staticmethod
    def update_birthday_month(person_id: int, month: int) -> None:
        """update birthday month"""
        logger.start(f"Update birthday month by person id person_id={person_id}",
                     object={"person_id": person_id, "month": month})
        # Connector.start_tranaction(None)
        # TODO Create and use a Python SDK create_mysql_date_str(....)
        query = f"UPDATE person_table SET `month` = {month}, " \
                f"birthday_date = CONCAT(YEAR(birthday_date), '-', {month}, '-', DAY(birthday_date)) " \
                f"WHERE person_id = {person_id}"
        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query)
        connection.commit()
        logger.end()

    @staticmethod
    def update_birthday_year(person_id: int, year: int) -> None:
        """update"""
        logger.start(f"Update birthday year by person id person_id={person_id}",
                     object={"person_id": person_id, "year": year})
        query = f"UPDATE person_table SET year = {year}, " \
                f"birthday_date = CONCAT({year}, '-', MONTH(birthday_date), '-', DAY(birthday_date)) " \
                f"WHERE person_id = {person_id}"

        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query)
        connection.commit()
        logger.end()

    def update_birthday_date(self, person_id: int, birthday_date: datetime.date) -> None:
        """update birthday date"""
        logger.start(f"Update birthday date by person id person_id={person_id}", object={
            "person_id": person_id, "birthday_date": birthday_date})
        date = str(birthday_date).split('-')
        person_json = {
            "person_id": person_id,
            "year": int(date[0]),
            "month": int(date[1]),
            "day": int(date[2]),
            "birthday_date": birthday_date
        }
        self.update_by_column_and_value(column_value=person_id, data_dict=person_json)
        logger.end()

    def update_first_name_by_profile_id(self, profile_id: int, first_name: str) -> None:
        """update first name"""
        logger.start(f"Update first name by profile id profile_id={profile_id}", object={
            "profile_id": profile_id, "first_name": first_name})
        person_json = {
            "person_id": profile_id,
            "first_name": first_name
        }
        self.update_by_column_and_value(column_value=profile_id, data_dict=person_json)
        logger.end()

    @staticmethod
    def update_person_ml_first_name_by_person_id(person_id: int, first_name: str,
                                                 lang_code: LangCode = None) -> None:
        """update ml first name"""
        logger.start(f"Update first name in ml table by person id person_id={person_id}", object={
            "person_id": person_id, "lang_code": lang_code, "first_name": first_name})
        lang_code = lang_code or LangCode.detect_lang_code_restricted(
            text=first_name, default_lang_code=LangCode.ENGLISH)
        query = "UPDATE person_ml_table SET first_name = %s, lang_code = %s where person_id = %s"
        data = (first_name, lang_code.value, person_id)
        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, data)
        connection.commit()
        logger.end()

    def update_nickname_by_person_id(self, person_id: int, nickname: str) -> None:
        """update nickname"""
        logger.start(f"Update nickname by person id person_id={person_id}", object={
            "person_id": person_id, "nickname": nickname})
        person_json = {
            "person_id": person_id,
            "nickname": nickname
        }
        self.update_by_column_and_value(column_value=person_id, data_dict=person_json)
        logger.end()

    def update_last_name_by_person_id(self, person_id: int, last_name: str) -> None:
        """update last name"""
        logger.start(f"Update last name by person id person_id={person_id}", object={
            "id": id, "last_name": last_name})
        person_json = {
            "person_id": person_id,
            "last_name": last_name
        }
        self.update_by_column_and_value(column_value=person_id, data_dict=person_json)
        logger.end()

    @staticmethod
    def update_person_ml_last_name_by_person_id(person_id: int, last_name: str,
                                                lang_code: LangCode = None) -> None:
        """update ml last name"""
        logger.start(f"Update last name in ml table by person id person_id={person_id}", object={
            "person_id": person_id, "last_name": last_name})
        # TODO: Do we really want to update lang_code here?
        lang_code = lang_code or LangCode.detect_lang_code_restricted(
            text=last_name, default_lang_code=LangCode.ENGLISH)
        query = "UPDATE person_ml_table SET last_name = %s, lang_code = %s where person_id = %s"
        data = (last_name, lang_code.value, person_id)
        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, data)
        connection.commit()

    def delete_by_person_id(self, person_id: int) -> None:
        """delete person"""
        logger.start(f"Delete person by person id person_id={person_id}",
                     object={"person_id": person_id})
        self.delete_by_column_and_value(column_value=person_id)
        logger.end(f"Person deleted person_id= {person_id}", object={
            'person_id': person_id})

    @staticmethod
    def get_test_person_number() -> int:
        person_number = NumberGenerator.get_random_number(
            schema_name='person', view_name='person_view', number_column_name='number')
        return person_number

    # TODO Shall we use ORDER BY person_id ASC LIMIT 1
    def get_test_person_id(self) -> int:
        person_number = NumberGenerator.get_random_number(
            schema_name='person', view_name='person_view', number_column_name='number')
        test_person_id = super().get_test_entity_id(
            entity_name="person", schema_name="person", view_name="person_view",
            entity_creator=Person, create_kwargs={"number": person_number, "is_test_data": True},
            insert_function=self.insert)
        return test_person_id
