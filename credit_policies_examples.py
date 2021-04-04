"""
This script loads the credit module inside policies and runs a few examples.
"""

from creditpolicies.policies import check_policies
from creditpolicies import run as msv

class ShowExamples:

    def __init__(self, interactive_session=True):
        self._interactive_session = interactive_session
        self._default_request_accept = dict(
                customer_income=500,
                customer_debt=100,
                payment_remarks_12m=0,
                payment_remarks=1,
                customer_age=22,
                                           )

    def _base_request(self, **kwargs):
        base_request = self._default_request_accept.copy()
        for key in kwargs:
            base_request[key] = kwargs[key]
        return base_request
    
    def check_request(self, data):
        print('    Showing the following request: {')
        print('        '+'\n        '.join('{}: {}'.format(*variable) for variable in [(key, data[key]) for key in data]))
        print('    }\n')

    def _print_section(self, message):
        print('\n\n'+message+'\n'+'-'*len(message)+'\n')

    def _print_initial_message(self):
        self._print_section("Let's show some bare examples of requests")
        
    def _continue(self):
        if self._interactive_session: input("    Press Enter to continue...")

    def show(self):
        self._print_initial_message()
        print('    An example of a POST request is \n        {}\n'.format(self._default_request_accept))
        self._continue()
        
        # Showing an accepted request
        self._print_section("Showing an accepted request")
        self.check_request(self._base_request())
        self._continue()
    
        # Showing some single-reason rejected requests
        self._print_section('Showing some single-reason rejected requests')
        self.check_request(self._base_request(customer_income=400))
        self.check_request(self._base_request(customer_income=700,customer_debt=600))
        self.check_request(self._base_request(customer_age=17))
        self._continue()
    
        # Showing a multiple-reason rejected request
        self._print_section("Showing some multiple-reason rejected requests")
        self.check_request(self._base_request(payment_remarks=2,customer_debt=600))
        self._continue()
        print('')

class ShowExamplesFromModule(ShowExamples):

    def __init__(self, interactive_session=True):
        ShowExamples.__init__(self, interactive_session)

    def _print_initial_message(self):
        self._print_section("Let's show some examples loading the policies.py module")

    def check_request(self, data):
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

class ShowExamplesFromApp(ShowExamples):

    def __init__(self, interactive_session=True):
        ShowExamples.__init__(self, interactive_session)

    def _print_initial_message(self):
        self._print_section("Let's show some examples loading the app")

    def show_response(self, this_request):
        with msv.app.test_request_context('/', method='POST', json=this_request):
            print(msv.run())
    
    def check_request(self, data):
        print('    Checking the request: {')
        print('        '+'\n        '.join('{}: {}'.format(*variable) for variable in [(key, data[key]) for key in data]))
        print('    }\n')
        print('    Response obtained:\n')
        self.show_response(data)
        print('----')


if __name__ == '__main__':
    print('\nThis script will show a few examples of responses according to credit policies.\n')
    show_examples_from_module = ShowExamplesFromModule(interactive_session=True)
    show_examples_from_module.show()
    show_examples_from_app = ShowExamplesFromApp()
    show_examples_from_app.show()
    print('End of script.\n')
