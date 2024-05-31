import re
import string


L10N_BR_LOWER = ["da", "de", "do"]


def normalize_place_name(value: str) -> str:
    """normalize_place_name Simplistic, prone to fail, name normalization

    @TODO allow localization

    Args:
        value (str): input term

    Returns:
        str: result term
    """
    if not value or not isinstance(value, str):
        return value

    term = string.capwords(value.strip())
    term2 = re.sub("\s\s+", " ", term)

    # @TODO deal with Do Da De

    return term2
