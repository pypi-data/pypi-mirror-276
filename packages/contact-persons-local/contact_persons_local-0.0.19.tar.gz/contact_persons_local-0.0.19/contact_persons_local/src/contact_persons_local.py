from contact_local.contact_local import ContactsLocal
from database_mysql_local.generic_mapping import GenericMapping
from logger_local.LoggerLocal import Logger
from person_local.persons_local import Person
from person_local.persons_local import PersonsLocal

from .contact_persons_local_constants import CONTACT_PERSONS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT

logger = Logger.create_logger(object=CONTACT_PERSONS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)

DEFAULT_SCHEMA_NAME = 'contact_person'
DEFAULT_ENTITY_NAME1 = 'contact'
DEFAULT_ENTITY_NAME2 = 'person'
DEFAULT_ID_COLUMN_NAME = 'contact_person_id'
DEFAULT_TABLE_NAME = 'contact_person_table'
DEFAULT_VIEW_TABLE_NAME = 'contact_person_view'

GENDER_ID = 8  # = Prefer not to respond


class ContactPersonsLocal(GenericMapping):
    def __init__(self, default_schema_name: str = DEFAULT_SCHEMA_NAME, default_entity_name1: str = DEFAULT_ENTITY_NAME1,
                 default_entity_name2: str = DEFAULT_ENTITY_NAME2, default_column_name: str = DEFAULT_ID_COLUMN_NAME,
                 default_table_name: str = DEFAULT_TABLE_NAME, default_view_table_name: str = DEFAULT_VIEW_TABLE_NAME,
                 is_test_data: bool = False):

        GenericMapping.__init__(self, default_schema_name=default_schema_name,
                                default_entity_name1=default_entity_name1,
                                default_entity_name2=default_entity_name2, default_column_name=default_column_name,
                                default_table_name=default_table_name, default_view_table_name=default_view_table_name,
                                is_test_data=is_test_data)
        self.persons_local = PersonsLocal(is_test_data=is_test_data)
        self.contacts_local = ContactsLocal(is_test_data=is_test_data)

    def insert_contact_and_link_to_existing_or_new_person(
            self, contact_dict: dict, contact_email_address: str, contact_normalized_phone_number: str,
            contact_id: int) -> dict:
        """
        Insert contact and link to existing or new person
        :param contact_dict: contact dict
        :param contact_id: contact id
        :param contact_email_address: contact email address
        :return: contact_person_id
        """
        logger.start(object={"contact_dict": contact_dict, "contact_email_address": contact_email_address,
                             "contact_id": contact_id})
        result_dict = {}
        # TODO: also check if contact_person_id by phone number
        person_id = self.select_one_value_by_column_and_value(select_clause_value="person_id",
                                                              column_name="contact_id",
                                                              column_value=contact_id)
        if contact_email_address and person_id is None:
            # TODO: use upsert with both email_addresses and phone_numbers
            '''
            # old code
            person_id = self.persons_local.get_person_id_by_email_address(email_address=contact_email_address)
            '''
            person_id = self.persons_local.get_people_id(people_entity_name="person",
                                                         ids_dict={"contact_id": contact_id})
        if person_id is None:
            # create new person and add it to person_table
            logger.info("person_id is None, creating new person")
            person_object = self._proccess_contact_dict_to_person_class(contact_dict=contact_dict,
                                                                        contact_email_address=contact_email_address,
                                                                        normalized_phone_number=contact_normalized_phone_number)
            result = self.persons_local.insert_if_not_exists(person=person_object)
            if result:
                person_id = result[0]

                result_dict["contact_person_id"] = self.insert_mapping(entity_name1=self.default_entity_name1,
                                                                       entity_name2=self.default_entity_name2,
                                                                       entity_id1=contact_id, entity_id2=person_id)

        else:
            result_dict["contact_person_id"] = self.insert_mapping_if_not_exists(
                entity_name1=self.default_entity_name1,
                entity_name2=self.default_entity_name2,
                entity_id1=contact_id, entity_id2=person_id,
                view_table_name=self.default_view_table_name)
        result_dict["person_id"] = person_id
        logger.end(object={"result_dict": result_dict})
        return result_dict

    def get_person_ids_by_contact_id(self, contact_id: int, limit: int = 1,
                                     order_by: str = "contact_person_id DESC") -> list:
        """
        Get person id by contact id
        :param contact_id: The contact id
        :param limit: limit
        :param order_by: order by
        :return: person id
        """
        logger.start(object={"contact_id": contact_id})
        person_ids_tuple_list = self.select_multi_tuple_by_column_and_value(select_clause_value="person_id",
                                                                            column_name="contact_id",
                                                                            column_value=contact_id,
                                                                            limit=limit,
                                                                            order_by=order_by)
        person_ids = [person_id_tuple[0] for person_id_tuple in person_ids_tuple_list]
        logger.end(object={"person_ids": person_ids})
        return person_ids

    def _proccess_contact_dict_to_person_class(self, contact_dict: dict, contact_email_address: str,
                                               normalized_phone_number) -> Person:
        """
        Process contact dict to person dict
        :param contact_dict: contact dict
        :return: person dict
        """
        logger.start(object={"contact_dict": contact_dict})
        person_object = Person(gender_id=GENDER_ID,
                               birthday_date=contact_dict['birthday'],
                               first_name=contact_dict['first_name'],
                               last_name=contact_dict['last_name'],
                               main_email_address=contact_email_address,
                               is_test_data=self.is_test_data,
                               main_full_number_normalized=normalized_phone_number,
                               )
        return person_object
