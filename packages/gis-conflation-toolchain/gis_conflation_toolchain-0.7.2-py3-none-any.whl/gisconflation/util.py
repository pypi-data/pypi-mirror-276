import re
import string

# https://pypi.org/project/Levenshtein/
# pip install levenshtein
import Levenshtein

# Record separator
DICTIONARY_SEPARATOR = "␞"


class AttributesEditor:
    """Edit attributes of a dictionary"""

    def __init__(
        self,
        rename_attr: dict = None,
        value_fixed: dict = None,
        value_name_place: list = None,
        normalize_prop: bool = True,
    ) -> None:
        self.rename_attr = rename_attr
        self.value_fixed = value_fixed
        self.value_name_place = value_name_place
        self.normalize_prop = normalize_prop

    def edit(self, item: dict) -> dict:
        result = item

        # print('teste')
        # raise NotImplementedError
        # if self.rename_attr is not None and len(self.rename_attr.keys()) > 0:
        if self.rename_attr is not None:
            for key, val in self.rename_attr.items():
                if key in result:
                    result[val] = result.pop(key)

        # if isinstance(self.value_fixed, list) and len(self.value_fixed) > 0:
        if self.value_fixed:
            for key, val in self.value_fixed.items():
                result[key] = val

        # if isinstance(self.value_name_place, list) and len(self.value_name_place) > 0:
        if self.value_name_place:
            for key in self.value_name_place:
                if key not in result:
                    continue
                _value = _zzz_format_name_place_br(result[key])
                if _value:
                    result[key] = _value
                else:
                    result[key] = ""

        if self.normalize_prop:
            prop_new = {}
            # print(result["properties"])
            for key, val in sorted(result.items()):
                if isinstance(val, str):
                    val = val.strip()
                if not val:
                    continue
                prop_new[key] = val
            result = prop_new

        return result


class DictionaryHelper:
    # @TODO impelement
    def __init__(self) -> None:
        pass


class LevenshteinHelper:
    """LevenshteinHelper is ...
    @see https://maxbachmann.github.io/Levenshtein/levenshtein.html
    pip install levenshtein
    """

    def __init__(
        self, synonymous: dict = None, tokens: dict = None, normalize: bool = True
    ) -> None:
        self.synonymous = synonymous
        self.tokens = tokens
        self.normalize = normalize

    def _apply_synonymous(self, term: str) -> str:
        if not self.synonymous or len(self.synonymous.keys()) == 0:
            return term

        parts = term.split(" ")
        result = []
        for item in parts:
            if item in self.synonymous:
                result.append(self.synonymous[item])
            else:
                result.append(item)

        return " ".join(result)

    def _apply_internal_tokens(self, term: str) -> str:
        if not self.tokens or len(self.tokens.keys()) == 0:
            return term

        parts = term.split(" ")
        result = []
        for item in parts:
            if item in self.tokens:
                result.append(self.tokens[item])
            else:
                result.append(item)

        return " ".join(result)

    def _normalize_term(self, term: str) -> str:
        if not isinstance(term, str):
            term = str(term)
        # if term is not:
        #     return None
        term2 = term.lower()
        term3 = re.sub("\\s\\s+", " ", term2)
        term4 = self._normalize_term_acents(term3)
        term5 = self._apply_synonymous(term4)
        return term5

    def _normalize_term_acents(self, term: str) -> str:
        # Ideally, this should be better than simple replacement
        # @see https://stackoverflow.com/questions/517923
        # @see https://pypi.org/project/Unidecode/
        # pip install Unidecode
        new = term.lower()

        # Obviously incomplete
        new = re.sub(r"[àáâãäå]", "a", new)
        new = re.sub(r"[èéêë]", "e", new)
        new = re.sub(r"[ìíîï]", "i", new)
        new = re.sub(r"[òóôõö]", "o", new)
        return new

    def get_term_tokenized(self, term: str) -> str:
        """get_term_tokenized Return a term expanded and normalized
        Args:
            term (str): The input term

        Returns:
            str: the result

        >>> synonymous = {'7': "sete"}
        >>> tokens = {'avenida': "<PPREFIX>", 'rua': "<PPREFIX>"}
        >>> lh = LevenshteinHelper(synonymous=synonymous)
        >>> lh.get_term_tokenized('rua sete de setembro')
        'rua sete de setembro'
        """
        # return Levenshtein.distance("teste", "testeee")

        # if self.normalize:
        #     term = self._normalize_term(term)
        term = self._normalize_term(term)
        term2 = self._apply_synonymous(term)

        return term2

    def get_term_tokenized_internal(self, term: str) -> str:
        """get_term_tokenized Return a term expanded and normalized
        Args:
            term (str): The input term

        Returns:
            str: the result

        >>> synonymous = {'7': "sete"}
        >>> tokens = {'avenida': "<PPREFIX>", 'rua': "<PPREFIX>"}
        >>> lh = LevenshteinHelper(synonymous=synonymous)
        >>> lh.get_term_tokenized('TESTÉ')
        'teste'

        >>> lh.get_term_tokenized_internal('rua sete de setembro')
        'rua sete de setembro'
        """
        term = self._normalize_term(term)
        term2 = self._apply_synonymous(term)
        term3 = self._apply_internal_tokens(term2)

        return term3

    def distance(self, ref_term: str, alt_term: str) -> int:
        """distance

        Args:
            ref_term (str): reference term
            alt_term (str): alternative term

        Returns:
            int: distance value

        >>> synonymous = {'7': "sete"}
        >>> tokens = {'avenida': "<PPREFIX>", 'rua': "<PPREFIX>"}
        >>> lh = LevenshteinHelper(synonymous=synonymous, tokens=tokens)

        #>>> lh.distance('Rua 7 de Setembro', 'rua sete de setembro')
        #0

        >>> lh.distance('Avenida 7 de Setembro', 'rua sete de setembro')
        0
        """
        if self.normalize:
            ref_term = self.get_term_tokenized_internal(ref_term)
            alt_term = self.get_term_tokenized_internal(alt_term)

        # print(self.normalize)
        # print(ref_term)
        # print(alt_term)

        return Levenshtein.distance(ref_term, alt_term)

    def sorted(self, ref_terms: list, alt_terms: list, alt_original: list) -> list:
        # @TODO sort the alt_original by ref_terms VS alt_terms
        return alt_original

    def get_sorted_alternatives(self, ref_term: str, alt_terms: list) -> list:
        alt_terms_sorted_index = range(0, len(alt_terms))

        return alt_terms_sorted_index


# def parse_argument_values(arguments: list, delimiter: str = "||") -> dict:
def parse_argument_values(
    arguments: list, delimiter: str = "|||", delimiter2: str = "||"
) -> dict:
    if not arguments or len(arguments) == 0 or not arguments[0]:
        return None

    result = {}
    for item in arguments:
        # print('__', item, item.find(delimiter))
        if item.find(delimiter) > -1:
            _key, _val = item.split(delimiter)
            if _val.find(delimiter2) > -1:
                _val = item.split(_val)
            result[_key] = _val
        else:
            result[item] = True

    # print('__f', result)
    return result


# @TODO refactor this code and allow localization of values
def _zzz_format_name_place_br(value: str):
    if not value or not isinstance(value, str):
        return value

    term = string.capwords(value.strip())
    term2 = re.sub("\\s\\s+", " ", term)

    # @TODO deal with Do Da De

    term2 = term2.replace(" Da ", " da ")
    term2 = term2.replace(" De ", " de ")
    term2 = term2.replace(" Do ", " do ")

    return term2


def _zzz_format_phone_br(value: str):
    if not value:
        return False

    if value.startswith("+"):
        return value

    # @TODO deal with more than one number

    if value.startswith("(") and value.find(")") > -1:
        _num_com_ddd = "".join(filter(str.isdigit, value))

        _regiao = _num_com_ddd[0:2]
        _num_loc = _num_com_ddd[2:]
        _num_loc_p2 = _num_loc[-4:]
        _num_loc_p1 = _num_loc.replace(_num_loc_p2, "")
        # return "+55 " + _regiao + ' ' + _num_com_ddd[2:]
        return "+55 " + _regiao + " " + _num_loc_p1 + " " + _num_loc_p2

    # if value.isnumeric():
    #     if len(value) == 8:
    #         return re.sub(r"(\d{5})(\d{3})", r"\1-\2", value)
    return False
