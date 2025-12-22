import numpy as np
import pandas as pd

############################### RULE 19 ###############################
RULE19_FEATURES_NEEDED = [
    "S_ADJECTIVE_AFTER_NOUN",
    "S_DEMONSTRATIVE_WORD_BEFORE_NOUN",
    "S_DEMONSTRATIVE_WORD_AFTER_NOUN",
    "S_NUMERAL_BEFORE_NOUN",
    "S_NUMERAL_AFTER_NOUN"
]

def evaluate_rule19_row(row: pd.Series):
    """
    Greenberg-style rule:
    If the descriptive adjective follows the noun,
    then the demonstrative and the numeral likewise follow.

    Returns:
      1  → follows rule
      0  → violates rule
      np.nan insufficient / not testable
    """

    # Antecedent: adjective after noun
    if row.get("S_ADJECTIVE_AFTER_NOUN", 0) != 1:
        return np.nan

    # Demonstrative position
    dem_before = (row.get("S_DEMONSTRATIVE_WORD_BEFORE_NOUN", np.nan) == 1)
    dem_after  = (row.get("S_DEMONSTRATIVE_WORD_AFTER_NOUN", np.nan) == 1)

    # Numeral position
    num_before = (row.get("S_NUMERAL_BEFORE_NOUN", np.nan) == 1)
    num_after  = (row.get("S_NUMERAL_AFTER_NOUN", np.nan) == 1)

    # If we cannot observe either position for dem or num → not testable
    if (
        (not dem_before and not dem_after and
         (pd.isna(row.get("S_DEMONSTRATIVE_WORD_BEFORE_NOUN")) or
          pd.isna(row.get("S_DEMONSTRATIVE_WORD_AFTER_NOUN"))))
        or
        (not num_before and not num_after and
         (pd.isna(row.get("S_NUMERAL_BEFORE_NOUN")) or
          pd.isna(row.get("S_NUMERAL_AFTER_NOUN"))))
    ):
        return np.nan

    # Violation conditions:
    # adjective after noun, but demonstrative or numeral is before noun
    # and not also attested after noun (exclude mixed orders)
    violates_dem = dem_before and not dem_after
    violates_num = num_before and not num_after

    violates = violates_dem or violates_num
    return 0 if violates else 1

############################### RULE 20 ###############################
RULE20_FEATURES_NEEDED = [
    "S_ADJECTIVE_BEFORE_NOUN",
    "S_DEMONSTRATIVE_WORD_BEFORE_NOUN",
    "S_NUMERAL_BEFORE_NOUN",
    "S_POSSESSOR_BEFORE_NOUN",
    "S_POSSESSOR_AFTER_NOUN",
    ]

def evaluate_rule20_row(row: pd.Series):
    """
    Rule 20 (your operationalization):
      If ANY modifier is before noun (Adj/Dem/Num), then possessor/genitive is before noun.
    Violation = (modifier before) AND (possessor after) AND (not also possessor before)

    Returns:
      1 follows rule
      0 violates rule
      np.nan insufficient / not testable
    """

    # Antecedent: any modifier before noun
    mod_before = (
        (row.get("S_ADJECTIVE_BEFORE_NOUN", 0) == 1) or
        (row.get("S_DEMONSTRATIVE_WORD_BEFORE_NOUN", 0) == 1) or
        (row.get("S_NUMERAL_BEFORE_NOUN", 0) == 1)
    )

    # Implicational rule: if antecedent not true, we treat as "not testable"
    if not mod_before:
        return np.nan

    gen_before = (row.get("S_POSSESSOR_BEFORE_NOUN", np.nan) == 1)
    gen_after  = (row.get("S_POSSESSOR_AFTER_NOUN", np.nan) == 1)

    # If neither is observed and values are missing, can't evaluate
    before_val = row.get("S_POSSESSOR_BEFORE_NOUN", np.nan)
    after_val  = row.get("S_POSSESSOR_AFTER_NOUN", np.nan)

    if (not gen_before) and (not gen_after) and (pd.isna(before_val) or pd.isna(after_val)):
        return np.nan

    violates = gen_after and (not gen_before)
    return 0 if violates else 1

############################### RULE 21 ###############################
RULE21_FEATURES_NEEDED = [
    "S_ADJECTIVE_AFTER_NOUN",
    "S_DEMONSTRATIVE_WORD_AFTER_NOUN",
    "S_NUMERAL_AFTER_NOUN",
    "S_POSSESSOR_BEFORE_NOUN",
    "S_POSSESSOR_AFTER_NOUN"
]

def evaluate_rule21_row(row: pd.Series):
    """
    Greenberg Rule 21 (operationalization):

    If ANY modifier follows the noun (Adj/Dem/Num),
    then the possessor/genitive also follows the noun.

    Violation = (modifier after noun)
                AND (possessor before noun)
                AND (not also possessor after noun)

    Returns:
      1  follows rule
      0  violates rule
      np.nan  not testable / insufficient data
    """

    # Antecedent: any modifier after noun
    mod_after = (
        (row.get("S_ADJECTIVE_AFTER_NOUN", 0) == 1) or
        (row.get("S_DEMONSTRATIVE_WORD_AFTER_NOUN", 0) == 1) or
        (row.get("S_NUMERAL_AFTER_NOUN", 0) == 1)
    )

    # Implicational rule: not testable if antecedent is false
    if not mod_after:
        return np.nan

    gen_before = (row.get("S_POSSESSOR_BEFORE_NOUN", np.nan) == 1)
    gen_after  = (row.get("S_POSSESSOR_AFTER_NOUN", np.nan) == 1)

    before_val = row.get("S_POSSESSOR_BEFORE_NOUN", np.nan)
    after_val  = row.get("S_POSSESSOR_AFTER_NOUN", np.nan)

    # If genitive position is completely unknown, not testable
    if (not gen_before) and (not gen_after) and (
        pd.isna(before_val) or pd.isna(after_val)
    ):
        return np.nan

    violates = gen_before and (not gen_after)
    return 0 if violates else 1


############################### RULE 23 ###############################
RULE23_FEATURES_NEEDED = [
    "S_SVO",
    "S_VSO",
    "S_VOS",
    "S_ADJECTIVE_BEFORE_NOUN",
    "S_ADJECTIVE_AFTER_NOUN"
]

def evaluate_rule23_row(row: pd.Series):
    """
    Greenberg Rule 23:
      If the verb precedes the object (VO), the adjective likewise precedes the noun.

    Operationalization:
      Antecedent (VO):
        S_SVO == 1 OR S_VSO == 1 OR S_VOS == 1

      Violation:
        VO == True AND
        ADJECTIVE_AFTER_NOUN == 1 AND
        ADJECTIVE_BEFORE_NOUN != 1

    Returns:
      1  → follows rule
      0  → violates rule
      np.nan → not testable / insufficient data
    """

    # Antecedent: verb precedes object (VO)
    vo = (
        (row.get("S_SVO", 0) == 1) or
        (row.get("S_VSO", 0) == 1) or
        (row.get("S_VOS", 0) == 1)
    )

    # Implicational rule: if antecedent does not hold, not testable
    if not vo:
        return np.nan

    adj_before = (row.get("S_ADJECTIVE_BEFORE_NOUN", np.nan) == 1)
    adj_after  = (row.get("S_ADJECTIVE_AFTER_NOUN", np.nan) == 1)

    before_val = row.get("S_ADJECTIVE_BEFORE_NOUN", np.nan)
    after_val  = row.get("S_ADJECTIVE_AFTER_NOUN", np.nan)

    # If adjective order is completely unknown, not testable
    if (not adj_before) and (not adj_after) and (
        pd.isna(before_val) or pd.isna(after_val)
    ):
        return np.nan

    violates = adj_after and (not adj_before)
    return 0 if violates else 1

############################### RULE 24 ###############################
RULE24_FEATURES_NEEDED = [
    "S_SOV",
    "S_OSV",
    "S_OVS",
    "S_ADJECTIVE_BEFORE_NOUN",
    "S_ADJECTIVE_AFTER_NOUN"
]

def evaluate_rule24_row(row: pd.Series):
    """
    Greenberg Rule 24:
      If the verb follows the object (OV), the adjective likewise follows the noun.

    Antecedent (OV order):
      S_SOV == 1 OR S_OSV == 1 OR S_OVS == 1

    Violation:
      OV is true AND
      adjective BEFORE noun AND
      adjective is NOT also AFTER noun

    Returns:
      1  follows rule
      0  violates rule
      np.nan  not testable / insufficient data
    """

    # Antecedent: verb follows object (OV)
    is_ov = (
        (row.get("S_SOV", 0) == 1) or
        (row.get("S_OSV", 0) == 1) or
        (row.get("S_OVS", 0) == 1)
    )

    # Implicational rule → not testable if antecedent false
    if not is_ov:
        return np.nan

    adj_before = (row.get("S_ADJECTIVE_BEFORE_NOUN", np.nan) == 1)
    adj_after  = (row.get("S_ADJECTIVE_AFTER_NOUN", np.nan) == 1)

    before_val = row.get("S_ADJECTIVE_BEFORE_NOUN", np.nan)
    after_val  = row.get("S_ADJECTIVE_AFTER_NOUN", np.nan)

    # If adjective position is entirely missing, not testable
    if (not adj_before) and (not adj_after) and (pd.isna(before_val) or pd.isna(after_val)):
        return np.nan

    # Violation = adjective before noun only
    violates = adj_before and (not adj_after)

    return 0 if violates else 1

############################### RULE 41 ###############################

RULE41_FEATURES_NEEDED = [
    # verb-final orders (verb follows BOTH S and O)
    "S_SOV",
    "S_OSV",
    # case system indicators (choose the set you actually have)
    "S_CASE_MARK",
    "S_CASE_PREFIX",
    "S_CASE_SUFFIX",
    "S_CASE_PROCLITIC",
    "S_CASE_ENCLITIC"
]

import numpy as np
import pandas as pd

def evaluate_rule41_row(row: pd.Series):
    """
    Greenberg Rule 41 (operationalization):
      If dominant order is verb-final (V follows both nominal S and nominal O),
      the language almost always has a case system.

    Antecedent: verb-final = SOV or OSV (if present)
    Consequent: has_case_system = any of the case indicators == 1

    Returns:
      1 follows rule
      0 violates rule
      np.nan not testable / insufficient data
    """

    # Antecedent: verb-final
    verb_final = (
        (row.get("S_SOV", 0) == 1) or
        (row.get("S_OSV", 0) == 1)
    )

    if not verb_final:
        return np.nan

    # Consequent: has some case marking strategy
    case_features = [
        "S_CASE_MARK",
        "S_CASE_PREFIX",
        "S_CASE_SUFFIX",
        "S_CASE_PROCLITIC",
        "S_CASE_ENCLITIC"
    ]

    # If none of these columns exist / all missing, we can't evaluate
    present_vals = [row.get(c, np.nan) for c in case_features]
    if all(pd.isna(v) for v in present_vals):
        return np.nan

    has_case = any(v == 1 for v in present_vals)
    return 1 if has_case else 0


