import numpy as np
import pandas as pd

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



