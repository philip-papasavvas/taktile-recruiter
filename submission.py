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

from typing import List

pd.options.display.width = 1000
pd.options.display.max_columns = 10

# define functions

# ---------
# functions
# ---------
def convert_dict_dtype_to_float(input_data_dict: pd.DataFrame,
                                columns_to_convert: List[str]) -> dict:
  """Helper function to convert specified column into float data type"""
  out_data_df = pd.DataFrame(input_data_dict).copy()

  for col in columns_to_convert:
    out_data_df[col] = pd.to_numeric(out_data_df[col])

   out_data_dict = out_data_df.to_dict()

  return out_data_dict

def has_delinquency_last_30_days(
        customer_data_dct: dict
) -> bool:
  """
  Helper function to return if a customer has delinquencies in last 30 days
  (containing the key 'delinquencies30Days')

  Args:
      customer_data_dct (dict): Customer data dictionary containing the keys 'delinquencies30Days'

  Returns:
      bool: Flag for if delinquencies in last 30 days or not
  """
  # setup error handling if it has negative delinquencies, either throw an error in the program
  # and stop immediately, or smooth this and set negative values to NaN

  if sum(customer_data_dct['delinquencies30Days'].values()) > 0:
    result = True
  else:
    result = False

  return result


if __name__ == '__main___':

    # ----------
    # sample data
    # ----------
    credit_bureau_report_sample_one = {
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
    credit_bureau_report_sample_two = {
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

    # create a dict for the customer flag check results
    customer_flag_check_results = {
        'has_delinquency_last_30_days': None,
        'age_less_than_18': None,
        'credit_score_less_than_500': None,
        'internal_risk_score_less_than_450': None,
        'knockout_result': None,
        'limit': None
    }

    # create a dummy for customer data
    customer_data = example_payload
    customer_data['credit_bureau_report'] = credit_bureau_report_sample_one
    customer_data['flag_checks'] = customer_flag_check_results

    # define parameters
    tradeline_columns_to_convert_to_float = [
        'amount1', 'amount2', 'balanceAmount', 'delinquencies30Days'
    ]


    # --------
    # decision flow
    # --------

    # IF has_delinquency_last_30_days > 0 THEN FAIL
    customer_data['credit_bureau_report']['tradeline'] = convert_dict_dtype_to_float(
        input_data_dict=customer_data['credit_bureau_report']['tradeline'],
        columns_to_convert=tradeline_columns_to_convert_to_float
    )

    delinquency_result = has_delinquency_last_30_days(customer_data_dct=out_tradeline_dct)
