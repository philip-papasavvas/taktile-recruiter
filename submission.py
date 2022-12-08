"""
Created by: Philip P
Created on: Thurs 8 Dec 2022

Taktile Neobank NB36 take home test - exploratory data analysis
Submission includes
- Jupyter notebook
- Response to Head of Credit
- Documentation with follow-up questions
"""
# built in imports
import datetime
from typing import List

# third party imports
import pandas as pd

pd.options.display.width = 1000
pd.options.display.max_columns = 10


def convert_dict_dtype_to_float(
        input_data_dict: dict,
        columns_to_convert: List[str]
        ) -> dict:
    """
    Helper function to convert specified column into float data type

    Args:
        input_data_dict: In the format provided in the sample data parsed from e-mail attachments
        columns_to_convert: A list of columns to convert to numeric type (float)

    Returns:
        dict: Same format as the input dictionary, but the specified columns
        for conversion have numeric/float data type
    """
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
      customer_data_dct (dict): Customer data dictionary containing the key 'delinquencies30Days'

    Returns:
      bool: Flag for if delinquencies in last 30 days or not
    """
    # setup error handling if it has negative delinquencies, either throw an error in the program
    # and stop immediately, or smooth this and set negative values to NaN

    result = True if sum(customer_data_dct['delinquencies30Days'].values()) > 0 else False

    return result


def is_under_18_years(
        customer_identity_data_dct: dict
        ) -> bool:
    """
    Function to return if customer (on today's date) is less than 18 years

    Args:
        customer_identity_data_dct: Customer identity data dictionary containing the key 'date_of_birth'

    Returns:
        bool: Flag to show if customer is younger than 18 years old
    """
    today_date = datetime.date.today()
    date_of_birth_dict = customer_identity_data_dct['date_of_birth']
    datetime_date_of_birth = datetime.date(
        year=date_of_birth_dict['year'],
        month=date_of_birth_dict['month'],
        day=date_of_birth_dict['day'],
        )
    # this gives a time delta in days - convert to years
    total_days_in_year = 365.25  # account for leap years
    age_today_in_years = (today_date - datetime_date_of_birth).days / total_days_in_year

    # On purpose I have not set a variable age as a parameter for the
    # function, as it's unlikely that the threshold age might be 16
    # or 21. but this could be the case and the code can be easily adapted
    result = True if age_today_in_years < 18 else False

    return result


def has_failed_credit_score(
        customer_data_risk_model_dct: dict,
        threshold_score_for_pass: int = 500
        ) -> bool:
    """
    Helper function to convert specified column into float data type

    Args:
        customer_data_risk_model_dct (dict): Customer data dictionary containing the keys 'delinquencies30Days'
        threshold_score_for_pass (int): Threshold score for pass on credit score

    Returns:
        bool: Flag for if pass on credit score
    """
    credit_score_value = float(customer_data_risk_model_dct[0]['credit_score'])

    result = True if credit_score_value < threshold_score_for_pass else False

    return result


def is_risk_score_below_threshold(
    customer_data_dct: dict,
    threshold_risk_score: float = 450
        ) -> bool:
    """
    Function to return if customer internal risk score is below threshold

    Args:
        customer_data_dct (dict): Customer data dictionary containing the key 'NB36_risk_score'
        threshold_risk_score (float): Threshold risk score below which a customer fails

    Returns:
        bool: Flag to show if customer fails internal risk score assessment
    """

    customer_internal_risk_score = float(customer_data_dct['NB36_risk_score'])

    result = True if customer_internal_risk_score < threshold_risk_score else False

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
        }

    # create a dummy for customer data
    customer_data = example_payload
    customer_data['credit_bureau_report'] = credit_bureau_report_sample_one
    # add in the flag checks as to determine the knockout result
    customer_data['flag_checks'] = customer_flag_check_results
    customer_data['knockout_result'] = None
    customer_data['limit'] = None

    # define parameters
    tradeline_columns_to_convert_to_float = [
        'amount1', 'amount2', 'balanceAmount', 'delinquencies30Days'
        ]

    # --------
    # decision flow
    # --------

    # Rule 1: IF has_delinquency_last_30_days > 0 THEN FAIL
    # -------------
    # convert the data to float to handle this flag
    customer_data['credit_bureau_report']['tradeline'] = convert_dict_dtype_to_float(
        input_data_dict=customer_data['credit_bureau_report']['tradeline'],
        columns_to_convert=tradeline_columns_to_convert_to_float
        )

    delinquency_result = has_delinquency_last_30_days(
        customer_data_dct=customer_data['credit_bureau_report']['tradeline']
        )
    customer_data['flag_checks']['has_delinquency_last_30_days'] = delinquency_result

    # Rule 2: IF age < 18 THEN FAIL
    # -------------
    customer_identity_data = customer_data['credit_bureau_report']['consumerIdentity']
    customer_age_check = is_under_18_years(customer_identity_data_dct=customer_identity_data)
    customer_data['flag_checks']['age_less_than_18'] = customer_age_check

    # Rule 3: IF credit_score < 500 THEN FAIL
    # -------------
    credit_score_result = has_failed_credit_score(
        customer_data_risk_model_dct=customer_data['credit_bureau_report']['riskModel']
        )
    customer_data['flag_checks']['credit_score_less_than_500'] = credit_score_result


    # Rule 4: IF internal_risk_score < 450 THEN FAIL
    # -------------
    risk_score_result = is_risk_score_below_threshold(
        customer_data_dct=customer_data
        )
    customer_data['flag_checks']['internal_risk_score_less_than_450'] = risk_score_result

    # Rule 5
    # -----------
    # If any of the above are False (for failed checks, then return reject), else
    def return_
