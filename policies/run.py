""" Main of the policies microserver. """

from flask import Flask, request
from policies.credit import check_policies

app = Flask(__name__)

@app.route('/', methods=['POST'])
def run():
    if request.method == 'POST':
        json_data = request.get_json()
        is_accepted, rejection_list_message = check_policies(json_data)
        if is_accepted:
            return 'ACCEPT'
        else:
            return 'REJECT'+'    reasons: {}'.format(rejection_list_message)
#            return {'policy_status':'REJECT', 'reason':rejection_list_message}
