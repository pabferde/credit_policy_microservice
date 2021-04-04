""" Credit policies """

def check_policies(json_data):
    is_accepted = True
    rejection_message = []
    
    active_policy_list = [
        check_customer_income,
        check_customer_debt,
        check_payment_remarks_12m,
        check_payment_remarks,
        check_customer_age,
                  ]

    for policy in active_policy_list:
        rejected = policy(json_data)
        if rejected[0]:
            is_accepted = False
            rejection_message.append(rejected[1])
    return is_accepted,rejection_message

def check_single_policy(rejection_condition, rejection_message):
    message = ''
    if rejection_condition:
        message = rejection_message
    return rejection_condition, message

## List of credit policies ##

# Income checks
def check_customer_income(json_data):
    rejection_condition = json_data['customer_income'] < 500 # in EUR
    rejection_message = 'LOW_INCOME'
    return check_single_policy(rejection_condition,rejection_message)

# Debt checks
def check_customer_debt(json_data):
    rejection_condition = json_data['customer_debt'] > 0.5*json_data['customer_income']
    rejection_message = 'HIGH_DEBT_FOR_INCOME'
    return check_single_policy(rejection_condition,rejection_message)

# Payment remarks checks
def check_payment_remarks_12m(json_data):
    rejection_condition = json_data['payment_remarks_12m'] > 0
    rejection_message = 'PAYMENT_REMARKS_12M'
    return check_single_policy(rejection_condition, rejection_message)

def check_payment_remarks(json_data):
    rejection_condition = json_data['payment_remarks'] > 1
    rejection_message = 'PAYMENT_REMARKS'
    return check_single_policy(rejection_condition, rejection_message)

# Age checks
def check_customer_age(json_data):
    rejection_condition = json_data['customer_age'] < 18
    rejection_message = 'UNDERAGE'
    return check_single_policy(rejection_condition, rejection_message)


