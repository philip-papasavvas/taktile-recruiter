"""
Created by: Philip P
Created on: Thurs 8 Dec 2022

Taktile Neobank NB36 take home test - exploratory data analysis
Submission includes
- Jupyter notebook
- Response to Head of Credit
- Documentation with follow up questions
"""

import pandas as pd
import pprint # pretty print JSON dicts with nested dicts indented

pd.options.display.width = 1000
pd.options.display.max_columns = 10



# ----------
# sample data
# ----------
credit_bureau_report = {
    "consumerIdentity": {
      "name": [
        {
          "firstName": "LUKE",
          "middleName": "PAUL",
          "surname": "DUVERGER"
        }
      ],
      "date_of_birth": {
        "day": 23,
        "month": 11,
        "year": 1964
      }
    },
    "riskModel": [
      {
        "credit_score": "0787"
      }
    ],
    "tradeline": [
      {
        "accountType": "07",
        "amount1": "00002650",
        "amount1Qualifier": "L",
        "amount2": "00002631",
        "amount2Qualifier": "H",
        "balanceAmount": "00000000",
        "balanceDate": "06282017",
        "delinquencies30Days": "00",
        "delinquencies60Days": "00",
        "delinquencies90to180Days": "00",
        "openOrClosed": "C"
      },
      {
        "accountType": "07",
        "amount1": "00000500",
        "amount1Qualifier": "L",
        "amount2": "00000049",
        "amount2Qualifier": "H",
        "balanceDate": "09132022",
        "delinquencies30Days": "00",
        "delinquencies60Days": "00",
        "delinquencies90to180Days": "00",
        "openOrClosed": "O"
      },
      {
        "accountType": "26",
        "amount1": "00088600",
        "amount1Qualifier": "O",
        "balanceDate": "08212019",
        "delinquencies30Days": "00",
        "delinquencies60Days": "00",
        "delinquencies90to180Days": "00",
        "openOrClosed": "O"
      },
      {
        "accountType": "19",
        "amount1": "00029650",
        "amount1Qualifier": "O",
        "balanceDate": "07062019",
        "delinquencies30Days": "00",
        "delinquencies60Days": "00",
        "delinquencies90to180Days": "00",
        "openOrClosed": "O"
      }
    ]
}
credit_bureau_report2 = {
    "consumerIdentity": {
      "name": [
        {
          "firstName": "LAILA",
          "middleName": "",
          "surname": "MUELLER"
        }
      ],
      "date_of_birth": {
        "day": 23,
        "month": 11,
        "year": 1964
      }
    },
    "riskModel": [
      {
        "credit_score": "0832"
      }
    ],
    "tradeline": [
      {
        "accountType": "07",
        "amount1": "00002650",
        "amount1Qualifier": "L",
        "amount2": "00002631",
        "amount2Qualifier": "H",
        "balanceAmount": "00000000",
        "balanceDate": "06282017",
        "delinquencies30Days": "00",
        "delinquencies60Days": "00",
        "delinquencies90to180Days": "00",
        "openOrClosed": "C"
      },
      {
        "accountType": "07",
        "amount1": "00000500",
        "amount1Qualifier": "L",
        "amount2": "00000049",
        "amount2Qualifier": "H",
        "balanceDate": "09132022",
        "delinquencies30Days": "01",
        "delinquencies60Days": "00",
        "delinquencies90to180Days": "00",
        "openOrClosed": "O"
      },
      {
        "accountType": "26",
        "amount1": "00088600",
        "amount1Qualifier": "O",
        "balanceDate": "08212019",
        "delinquencies60Days": "00",
        "delinquencies90to180Days": "00",
        "openOrClosed": "O"
      },
      {
        "accountType": "19",
        "amount1": "00029650",
        "amount1Qualifier": "O",
        "balanceDate": "07062019",
        "delinquencies60Days": "00",
        "delinquencies90to180Days": "00",
        "openOrClosed": "O"
      }
    ]
}

example_payload = {
  "application_id": 123456,
  "credit_bureau_report": {},
  "NB36_risk_score": 600,
}


# view the data
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(credit_bureau_report)

customer_data = credit_bureau_report

# parse the customer data, change the dtype to float from str where appropriate

# e.g. delinquencies
pd.DataFrame(customer_data['tradeline'])

tradeline_columns_to_convert_to_float = [
  'amount1', 'amount2', 'balanceAmount', 'delinquencies30Days'
]

# ------
# Rules
# ------
# IF has_delinquency_last_30_days > 0 THEN FAIL
#
# delinquencies last 30 days is in the 'tradeline' key, within
# each different account
type(customer_data['tradeline'])
# of type list, so convert to dataframe with named columns, then filter
# by column values
customer_df_tradeline = pd.DataFrame(customer_data['tradeline'])["delinquencies30Days"]

# --------
# IF age < 18 THEN FAIL
# extract this from the ['consumerIdentity']['date_of_birth'] -
# convert to datetime, use the datetime from today
# --------

# --------
# IF credit_score < 500 THEN FAIL
# risk_model - credit score, convert str to float, and extract the value
# according to the boolean

# --------

# IF internal_risk_score < 450 THEN FAIL
# implement internal_risk_score table logic
# using the NB36_risk_score

# IF any of the rules above failed then REJECT, else ACCEPT

# use this by conversion to float type, then bool flags where False/True,
# some or conditions, then return PASS/FAIL
