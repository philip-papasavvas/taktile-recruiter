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
from typing import List, Tuple

# third party imports
import pandas as pd
import numpy as np

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
        ) -> Tuple[bool, float]:
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

    total_delinq_30d = sum(customer_data_dct['delinquencies30Days'].values())
    result = True if total_delinq_30d > 0 else False

    return result, total_delinq_30d


def is_under_18_years(
        customer_identity_data_dct: dict
        ) -> Tuple[bool, int]:
    """
    Function to return if customer (on today's date) is less than 18 years

    Args:
        customer_identity_data_dct: Customer identity data dictionary containing the key 'date_of_birth'

    Returns:
        bool: Flag to show if customer is younger than 18 years old
        int: Customer age
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

    return result, int(age_today_in_years)


def has_failed_credit_score(
        customer_data_risk_model_dct: dict,
        threshold_score_for_pass: int = 500
        ) -> Tuple[bool, float]:
    """
    Helper function to convert specified column into float data type

    Args:
        customer_data_risk_model_dct (dict): Customer data dictionary containing the keys 'delinquencies30Days'
        threshold_score_for_pass (int): Threshold score for pass on credit score

    Returns:
        bool: Flag for if pass on credit score
        float: Customer credit score value
    """
    credit_score_value = float(customer_data_risk_model_dct[0]['credit_score'])

    result = True if credit_score_value < threshold_score_for_pass else False

    return result, credit_score_value


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
        customer_internal_risk_score: Risk score for customer
    """

    customer_internal_risk_score = float(customer_data_dct['NB36_risk_score'])

    result = True if customer_internal_risk_score < threshold_risk_score else False

    return result, customer_internal_risk_score


def return_knockout_result(
        customer_data_dct: dict
        ) -> Tuple[str, dict]:
    """
    Helper function to return the knockout result as a consequence of if the other
    tests have passed/failed. One True result, meaning they have failed will return a knockout result
    of FAIL.

    Args:
         customer_data_dct: must contain the key 'flag_checks' with dictionary of key, value pairs
         for keys ['has_delinquency_last_30_days', 'is_under_18', 'is_credit_score_fail', 'is_internal_risk_score_fail']

    Returns:
         str: Knockout outcome, one of 'ACCEPT' or 'REJECT'
         dict: Returning the input customer_data_dct, with the knockout result filled in
    """
    flag_check_failure = [i for i, x in enumerate(customer_data_dct['flag_checks'].values()) if x]
    if len(flag_check_failure) > 0:
        customer_data_dct['knockout_result'] = 'REJECT'
        for fail_num in flag_check_failure:
            print(
                f"Check for: {list(customer_data_dct['flag_checks'])[fail_num]} FAILED. "
                f"Value was {list(customer_data_dct['check_outcome'].values())[fail_num]}"
                )
    else:
        customer_data_dct['knockout_result'] = 'ACCEPT'

    if customer_data_dct['knockout_result'] == 'REJECT':
        print(f"Customer ID: {customer_data_dct['application_id']} has FAILED the checks.")

    return customer_data_dct['knockout_result'], customer_data_dct


def return_credit_limit(
        credit_score: float,
        internal_risk_score: float
        ) -> float:
    """
    Return credit limit according to risk bucketing logic

    Args:
        credit_score: Customer credit score
        internal_risk_score: Customer internal risk score

    Returns:
        float: credit limit
    """
    credit_score_int = int(credit_score)
    internal_risk_score_int = int(internal_risk_score)

    # not the most elegant solution - didn't leave enough time to implement pd.cut()
    limit = np.where(
        (500 <= credit_score_int < 600) & (450 <= internal_risk_score_int < 500),
        2000,
        np.where(
            (500 <= credit_score_int < 600) & (500 <= internal_risk_score_int < 600),
            2500,
            np.where(
                (500 <= credit_score_int < 600) & (600 <= internal_risk_score_int < 700),
                3000,
                np.where(
                    (600 <= credit_score_int < 700) & (450 <= internal_risk_score_int < 500),
                    2500,
                    np.where(
                        (600 <= credit_score_int < 700) & (500 <= internal_risk_score_int < 600),
                        3500,
                        np.where(
                            (600 <= credit_score_int < 700) & (600 <= internal_risk_score_int < 700),
                            4500,
                            np.where(
                                (700 <= credit_score_int < 800) & (450 <= internal_risk_score_int < 500),
                                3000,
                                np.where(
                                    (700 <= credit_score_int < 800) & (500 <= internal_risk_score_int < 600),
                                    5000,
                                    np.where(
                                        (700 <= credit_score_int < 800) & (600 <= internal_risk_score_int < 700),
                                        7000,
                                        np.where(
                                            (800 <= credit_score_int < 900) & (450 <= internal_risk_score_int < 500),
                                            3500,
                                            np.where(
                                                (800 <= credit_score_int < 900) & (500 <= internal_risk_score_int < 600),
                                                7000,
                                                np.where(
                                                    (800 <= credit_score_int < 900) & (600 <= internal_risk_score_int < 700),
                                                    10000,
                                                    np.nan
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )

    if pd.isna(limit):
        print(
            f"Internal risk score: {internal_risk_score}, credit score: {credit_score} "
            f"is out of bounds, no credit limit given"
            )

    if isinstance(limit, np.ndarray):
        limit = limit.tolist()

    return limit


def add_extra_keys_to_customer_data_dct(
        customer_data_dct: dict
        ) -> dict:
    """Helper function to add extra key, value pairs to customer data dict"""

    # create a dict for the customer flag check outcome - True/False
    customer_flag_check_outcome = {
        'has_delinquency_last_30_days': None,
        'is_under_18': None,
        'is_credit_score_fail': None,
        'is_internal_risk_score_fail': None,
        }
    # dict for the numerical values of the checks, e.g. risk score
    customer_flag_check_results = {
        'has_delinquency_last_30_days': None,
        'is_under_18': None,
        'is_credit_score_fail': None,
        'is_internal_risk_score_fail': None,
        }
    customer_data_dct['flag_checks'] = customer_flag_check_outcome
    customer_data_dct['check_outcome'] = customer_flag_check_results
    customer_data_dct['knockout_result'] = None
    customer_data_dct['limit'] = None

    return customer_data_dct


def run_customer_credit_check(
        customer_data_dict: dict
        ) -> float:
    """Function to wrap up all individual checks, including the rules defined,
    and calculate the credit limit according to the customer information

    Args:
        customer_data_dict: Must include the keys:
        ['application_id', 'credit_bureau_report', 'NB36_risk_score', 'flag_checks', 'check_outcome', 'knockout_result', 'limit']

    Returns:
        dict: Return the customer data (as part of the decision flow defined in the problem)
    """
    customer_data = customer_data_dict

    assert customer_data['credit_bureau_report'], \
        f"Credit bureau report doesn't exist, customer REJECTED, application ID:" \
        f"{customer_data['application_id']}"

    # add in the flag checks as to determine the knockout result
    customer_data = add_extra_keys_to_customer_data_dct(customer_data_dct=customer_data)

    # define parameters
    tradeline_columns_to_convert_to_float = [
        'amount1', 'amount2', 'balanceAmount', 'delinquencies30Days'
        ]

    # --------
    # decision flow
    # --------

    # Rule 1: IF has_delinquency_last_30_days > 0 THEN FAIL
    # -------------
    # convert the data to float
    customer_data['credit_bureau_report']['tradeline'] = convert_dict_dtype_to_float(
        input_data_dict=customer_data['credit_bureau_report']['tradeline'],
        columns_to_convert=tradeline_columns_to_convert_to_float
        )

    delinquency_result, num_delinq = has_delinquency_last_30_days(
        customer_data_dct=customer_data['credit_bureau_report']['tradeline']
        )
    customer_data['flag_checks']['has_delinquency_last_30_days'] = delinquency_result
    customer_data['check_outcome']['has_delinquency_last_30_days'] = num_delinq

    # Rule 2: IF age < 18 THEN FAIL
    # -------------
    customer_identity_data = customer_data['credit_bureau_report']['consumerIdentity']
    customer_age_check_result, customer_age = is_under_18_years(
        customer_identity_data_dct=customer_identity_data
        )
    customer_data['flag_checks']['is_under_18'] = customer_age_check_result
    customer_data['check_outcome']['is_under_18'] = customer_age

    # Rule 3: IF credit_score < 500 THEN FAIL
    # -------------
    credit_score_result, credit_score = has_failed_credit_score(
        customer_data_risk_model_dct=customer_data['credit_bureau_report']['riskModel']
        )
    customer_data['flag_checks']['is_credit_score_fail'] = credit_score_result
    customer_data['check_outcome']['is_credit_score_fail'] = credit_score

    # Rule 4: IF internal_risk_score < 450 THEN FAIL
    # -------------
    risk_score_result, internal_risk_score = is_risk_score_below_threshold(
        customer_data_dct=customer_data
        )
    customer_data['flag_checks']['is_internal_risk_score_fail'] = risk_score_result
    customer_data['check_outcome']['is_internal_risk_score_fail'] = internal_risk_score

    # Rule 5
    # -----------
    # If any of the above are False (for failed checks, then return reject), else
    knockout_outcome, customer_data = return_knockout_result(
        customer_data_dct=customer_data
        )

    # final logic to return credit limit
    if customer_data['knockout_result'] == 'ACCEPT':
        credit_limit = return_credit_limit(
            credit_score=customer_data['check_outcome']['is_credit_score_fail'],
            internal_risk_score=customer_data['NB36_risk_score']
            )
    else:
        print(f"Customer: {customer_data['application_id']} was REJECTED")
        credit_limit = np.nan

    customer_data['credit_limit'] = credit_limit

    return customer_data


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

    # create a dummy for customer data

    # example run - one
    customer_data_one = example_payload
    customer_data_one['credit_bureau_report'] = credit_bureau_report_sample_one

    credit_limit_one = run_customer_credit_check(
        customer_data_dict=customer_data_one
        )

    # example run - two
    customer_data_two = customer_data_one.copy()
    customer_data_two['NB36_risk_score'] = 800

    credit_limit_two = run_customer_credit_check(
        customer_data_dict=customer_data_two
        )

    # example run - three
    customer_data_three = customer_data_one.copy()
    customer_data_three['credit_bureau_report']['riskModel'][0]['credit_score'] = 200

    credit_limit_three = run_customer_credit_check(
        customer_data_dict=customer_data_three
        )
