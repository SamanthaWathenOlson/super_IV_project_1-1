from Data_access_layer.dao_imp import DAOImp
from custom_exceptions.failed_transaction import FailedTransaction
from data_entity_class.row_entity import RowEntity
from service_access_layer.service_access_imp import ServiceAccessIMP

test_dao = DAOImp()
test_service = ServiceAccessIMP(test_dao)

def test_sanitize_json_from_api_success():
    test_dict = {
        "tableName": "tablename",
        "tableNameId": 1
    }
    assert test_service.sanitize_json_from_api(test_dict)["table_name_id"] == 1


def test_sanitize_json_from_api_non_string_table_name():
    try:
        test_dict = {
            "tableName": 5,
            "tableNameId": 1
        }
        test_service.sanitize_json_from_api(test_dict)
        assert False
    except FailedTransaction as e:
        assert str(e) == "The field containing the table name is in the wrong format, must be a string."


def test_sanitize_json_from_api_convertible_number():
    try:
        test_dict = {
            "tableName": "5",
            "tableNameId": 1
        }
        test_service.sanitize_json_from_api(test_dict)
        assert False
    except FailedTransaction as e:
        assert str(e) == "The table name should not be a number"


def test_sanitize_json_from_api_id_field_non_number():
    try:
        test_dict = {
            "tableName": "tablename",
            "tableNameId": "one"
        }
        test_service.sanitize_json_from_api(test_dict)
        assert False
    except FailedTransaction as e:
        assert str(e) == "The input from the api is not convertible to integer for an id field."


def test_service_create_reimbursement_request_comment_less_than_100():
    try:
        test_dict = {"employee_id": 5,
                     "reason_id": 5,
                     "amount": 100,
                     "reimbursement_request_comment": "service8910service8910service8910service8910service8910service8910service8910service8910service8910service8910service8910v"}
        service_access_input = ServiceAccessIMP(test_dao)
        service_access_input.service_create_reimbursement_request(test_dict)
        assert False
    except FailedTransaction as e:
        assert str(e) == "test service reimbursement request should not exceed 100"


def test_service_create_reimbursement_request_amount_between_1_and_1000():
    try:
        test_dict = {"employee_id": 5,
                     "reason_id": 5,
                     "amount": 1000000,
                     "reimbursement_request_comment": "this is ok"}
        test_service.service_create_reimbursement_request(test_dict)
        assert False
    except FailedTransaction as e:
        assert str(e) == "reimbursement amount must be between $1 and $1000"


def test_service_create_reimbursement_request_success():

    pass


def test_service_cancel_reimbursement_request_id_is_not_a_number():
    try:
        test_dict = {
            "reimbursement_request_id": "non-numeric"
        }
        test_service.service_cancel_reimbursement_request(test_dict)
        assert False
    except FailedTransaction as e:
        assert str(e) == "Reimbursement Request ID should be numeric!"


def test_service_cancel_reimbursement_request_success():
    pass


def test_service_select_total_amount_requested_employee_id_non_numeric():
    try:
        test_dict = {"employee_id": "5",
                     "reason_id": 5,
                     "amount": 1000,
                     "reimbursement_request_comment": "this is ok"}
        test_service.service_select_total_amount_requested(test_dict)
        assert False
    except FailedTransaction as e:
        assert str(e) == "test reimbursement employee_id cannot use numeric type"


def test_service_select_total_amount_requested_employee_id_success():
    pass

