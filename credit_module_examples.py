"""
This script loads the credit module inside policies and runs a few examples.
"""

from policies.credit import check_policies
from policies import run as msv

_default_request_accept = dict(
        customer_income=500,
        customer_debt=100,
        payment_remarks_12m=0,
        payment_remarks=1,
        customer_age=22,
                             )

def base_request(**kwargs):
    base_request = _default_request_accept.copy()
    for key in kwargs:
        base_request[key] = kwargs[key]
    return base_request

def show_examples_from_module(interactive_session=True):

    def check_request(data):
        print('    Checking the request: {')
        print('        '+'\n        '.join('{}: {}'.format(*variable) for variable in [(key, data[key]) for key in data]))
        print('    }\n')
        check = check_policies(data)
        print('    Raw output from "check_request" function: {}'.format(check))
        if not check[0]:
            print('    Status of the request: REJECT')
            print('    Reasons: {}'.format(check[1]))
        if check[0]:
            print('    Status of the request: ACCEPT')
        print('----')
        
    def print_section(message):
        print('\n\n'+message+'\n'+'-'*len(message)+'\n')

    print_section("Let's show some examples loading the credit.py module")
    print('    An example of a POST request is \n        {}\n'.format(_default_request_accept))
    if interactive_session: input("    Press Enter to continue...")
    
    # Showing an accepted request
    print_section("Showing an accepted request")
    check_request(base_request())
    if interactive_session: input("    Press Enter to continue...")

    # Showing some single-reason rejected requests
    print_section('Showing some single-reason rejected requests')
    check_request(base_request(customer_income=400))
    check_request(base_request(customer_income=700,customer_debt=600))
    check_request(base_request(customer_age=17))
    if interactive_session: input("    Press Enter to continue...")

    # Showing a multiple-reason rejected request
    print_section("Showing some multiple-reason rejected requests")
    check_request(base_request(payment_remarks=2,customer_debt=600))
    if interactive_session: input("    Press Enter to continue...")
    print('')
    
def show_examples_from_app(interactive_session=True):
    
    def show_response(this_request):
        with msv.app.test_request_context('/', method='POST', json=this_request):
            print(msv.run())
    
    def check_request(data):
        print('Checking the request: {')
        print('    '+'\n    '.join('{}: {}'.format(*variable) for variable in [(key, data[key]) for key in data]))
        print('}\n')
        print('Response obtained:\n')
        show_response(data)
        print('----')

    def print_section(message):
        print('\n\n'+message+'\n'+'-'*len(message)+'\n')
    
    print_section("Let's show some examples loading the app")
    print('    An example of a POST request is \n        {}\n'.format(_default_request_accept))
    if interactive_session: input("    Press Enter to continue...")

    # Showing an accepted request
    print_section('Showing an accepted request')
    check_request(base_request())
    if interactive_session: input("    Press Enter to continue...")
    
    # Showing some single-reason rejected requests
    print_section('Showing some single-reason rejected requests')
    check_request(base_request(customer_income=400))
    check_request(base_request(customer_income=700,customer_debt=600))
    check_request(base_request(customer_age=17))
    if interactive_session: input("    Press Enter to continue...")

    # Showing a multiple-reason rejected request
    print_section('Showing some multiple-reason rejected requests')
    check_request(base_request(payment_remarks=2,customer_debt=600))
    if interactive_session: input("    Press Enter to continue...")
    print('')

if __name__ == '__main__':
    print('\nThis script will show a few examples of responses according to credit policies.\n')
    show_examples_from_module(interactive_session=True)    
    show_examples_from_app(interactive_session=True)
    print('End of script.\n')
