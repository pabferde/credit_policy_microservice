# credit_policy_microservice
A Python microservice that responds to a POST request of basic customer variables.
It checks if a credit policy is accepted or rejected according to the values of the customer variables. In case of not being accepted, reasons for the rejection are given in the answer.
The project includes the microservice, a test suite for pytest and a script to run some examples.

## Install

Clone the repository
```
$ git clone https://github.com/pabferde/credit-policy-microservice.git
$ cd credit-policy-microservice
```

Install the requirements (flask for setting up the microservice, pytest for testing the code).
The recommendation is to do it after creating a virtualenv and activating it:
```
# Optional (recommended): create a virtualenv venv and activate it
$ python3 -m venv venv
$ source venv/bin/activate
# Install requirements
$ python3 -m pip install -r requirements.txt
```

## Run script with examples

To run the script, call it with python:
```
$ python3 credit_policies_examples.py
```
It will show the response of the credit policy from a) running directly the Python module policies.py, and b) passing the POST requests to the microservice.

Notice that this microservice does not accept a GET request, so opening it in http://127.0.0.1:5000 in a browser will not work.

## Test

To test that the code works, simply run pytest in the credit-policy-microservice folder:
```
$ pytest
```
