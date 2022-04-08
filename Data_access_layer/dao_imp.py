from Data_access_layer.connection_obj import connection
from Data_access_layer.dao_interface import ReimbursementInterface
from custom_exceptions.failed_transaction import FailedTransaction
from data_entity_class.row_entity import RowEntity


class DAOImp(ReimbursementInterface):

    def trunc_table(self, sql_query) -> bool:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        connection.commit()
        return True

    def select_all(self, sql_query) -> []:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        new_record_tuple_list = cursor.fetchall()
        if cursor.rowcount < 1:
            connection.rollback()
            raise FailedTransaction("Bad table data?")
        else:
            connection.commit()
            column_names = [desc[0] for desc in cursor.description]
            if len(new_record_tuple_list) != 0:
                row_list = []
                for record in new_record_tuple_list:
                    mapping = {}
                    for i in range(len(column_names)):
                        mapping.update({column_names[i]: record[i]})
                    new_record = RowEntity(mapping)
                    row_list.append(new_record)
                return row_list
            else:
                raise FailedTransaction("something else")

    def select_record(self, sql_query) -> RowEntity:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        new_record_tuple_list = cursor.fetchall()
        if cursor.rowcount < 1:
            connection.rollback()
            raise FailedTransaction("Username is incorrect!")
        else:
            connection.commit()
            column_names = [desc[0] for desc in cursor.description]
            mapping = {}
            if len(new_record_tuple_list) != 0:
                for record in new_record_tuple_list:
                    for i in range(len(column_names)):
                        mapping.update({column_names[i]: record[i]})
                    new_record = RowEntity(mapping)
                return new_record
            else:
                raise FailedTransaction("Record may have been created, but no results were returned.")

    def create_reimbursement_request(self, sql_query: str) -> RowEntity:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        if cursor.rowcount < 1:
            connection.rollback()
            raise FailedTransaction("No record was created, transaction rolled back.")
        else:
            connection.commit()
            new_record_tuple_list = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            mapping = {}
            if len(new_record_tuple_list) != 0:
                for record in new_record_tuple_list:
                    for i in range(len(column_names)):
                        mapping.update({column_names[i]: record[i]})
                    new_record = RowEntity(mapping)
                return new_record
            else:
                raise FailedTransaction("Record may have been created, but no results were returned.")

    def cancel_reimbursement_request(self, sql_query: str) -> bool:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        if cursor.rowcount < 1:
            connection.rollback()
            raise FailedTransaction("No record was deleted, transaction rolled back.")
        else:
            connection.commit()
            return True

    def select_total_amount_requested(self, sql_query: str) -> float:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        if cursor.rowcount < 1:
            connection.rollback()
            raise FailedTransaction("No record was viewed, transaction rolled back.")
        else:
            connection.commit()
            total = cursor.fetchone()[0]
            return total

