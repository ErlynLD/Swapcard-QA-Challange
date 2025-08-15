# Swapcard-QA-Challange

### This solution was implemented using Python virtual environments; you should have python and pip installed, then you should follow next steps:  

1. pip install pipenv
2. python -m venv .venv
3.  .\.venv\Scripts\activate
4. pipenv install selenium
5. pipenv install webdriver-manager
6. pipenv install pytest-html


## Important Notes

1. This test uses Google page, so you might expect some executions to be interrupted by the CAPTCHA prevention... 
2. The Shopping section might not be available in some countries, so it's recommended to have an active VPN pointing to an IP in the United States
3. Reports are done using Pytest-html, please open the report.html at the end of your execution

## Parametrization was included
This was done in the python way using metafunc.fixturenames
The parameterized data is read from /data/test_data.json


## How to run: 

Once you have your pipenv / virtual environment active and dependencies installed, you can execute the tests with next command: 

```
pipenv run python -m pytest --html=report.html --self-contained-html

