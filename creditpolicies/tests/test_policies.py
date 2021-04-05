""" 
Test suit of policies microserver. 
    It checks that right policy messages are given.
    Tests run with pytest
"""

import pytest
from .. import run as msv
from .. import policies as pol

@pytest.fixture
def client():
    msv.app.config['TESTING'] = True
    with msv.app.test_client() as client:
        yield client

def get_credit_policy(client, **kwargs):
    return client.post('/', json=kwargs)

def base_request_accept(**kwargs):
    base_request = dict(
        customer_income=500,
        customer_debt=100,
        payment_remarks_12m=0,
        payment_remarks=1,
        customer_age=22,
                       )
    for key in kwargs:
        base_request[key] = kwargs[key]
    return base_request


# Tests on policies.py

def test_check_policies():
    d = base_request_accept
    
    # Testing ACCEPT
    t = pol.check_policies(d())
    assert t[0]
    assert [] == t[1]
    
    # Testing REJECT if any
    def base_check_reject_any(message_list,**kwargs):
        t = pol.check_policies(d(**kwargs))
        assert not t[0]
        for message in message_list:
            assert message in t[1]

    # Testing single-reason rejections
    base_check_reject_any(['LOW_INCOME'], customer_income=499)
    base_check_reject_any(['HIGH_DEBT_FOR_INCOME'], customer_income=1000, customer_debt=1000)
    base_check_reject_any(['PAYMENT_REMARKS_12M'], payment_remarks_12m=1)
    base_check_reject_any(['PAYMENT_REMARKS'], payment_remarks=2)
    base_check_reject_any(['UNDERAGE'], customer_age=17)
    # Testing multiple-reason rejections
    base_check_reject_any(['LOW_INCOME','PAYMENT_REMARKS'], customer_income=400, payment_remarks=3)
    
def test_check_single_policy():

    accept_test = pol.check_single_policy(False,'message')
    assert not accept_test[0]
    assert accept_test[1] == ''

    reject_test = pol.check_single_policy(True,'message')
    assert reject_test[0]
    assert reject_test[1] == 'message'    


# Tests on run.py

def test_credit_policy_requests(client):
        
    d = base_request_accept
    
    t = get_credit_policy(client, **d())
    assert b'ACCEPT' in t.data
    
    t = get_credit_policy(client, **d(customer_income=499))
    assert b'REJECT' in t.data
    assert b'LOW_INCOME' in t.data
    
    t = get_credit_policy(client, **d(customer_income=1000, customer_debt=1000))
    assert b'REJECT' in t.data
    assert b'HIGH_DEBT_FOR_INCOME'
    
    t = get_credit_policy(client, **d(payment_remarks_12m=1))
    assert b'REJECT' in t.data
    assert b'PAYMENT_REMARKS_12M' in t.data
    
    t = get_credit_policy(client, **d(payment_remarks=2))
    assert b'REJECT' in t.data
    assert b'PAYMENT_REMARKS' in t.data
    
    t = get_credit_policy(client, **d(customer_age=17))
    assert b'REJECT' in t.data
    assert b'UNDERAGE' in t.data


    