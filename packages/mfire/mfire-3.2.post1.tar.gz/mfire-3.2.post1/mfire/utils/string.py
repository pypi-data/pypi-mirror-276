from __future__ import annotations

import re
import unicodedata
from typing import List, Optional, Tuple, Union

from mfire.settings.settings import Settings

_ = Settings().translate


def get_synonym(word: str) -> str:
    """
    Returns a random synonym of the given word.

    Args:
        word (str): The word for which a synonym is desired.

    Returns:
        str: A random synonym of the given word.
    """
    iter_synonyms = next(
        (seq for seq in Settings().template("synonyms") if word in seq), (word,)
    )
    return Settings().random_choice(iter_synonyms)


def match_text(text1: str, text2: str) -> bool:
    """
    Checks if a text matches a given template by comparing them after replacing
    synonyms.

    Args:
        text1 (str): The text to compare with the template.
        text2 (str): The template with tags between '<...>'.

    Returns:
        bool: True if the text matches the template, False otherwise.
    """
    ntext1, ntext2 = text1, text2
    for seq in Settings().template("synonyms"):
        tag = f"<{seq[0]}>"
        for word in seq:
            ntext1 = ntext1.replace(word, tag)
            ntext2 = ntext2.replace(word, tag)
    return ntext1 == ntext2


def decapitalize(string: str) -> str:
    """
    Decapitalizes only the first letter of a string.

    Args:
        string (str): The input string.

    Returns:
        str: The decapitalized string.
    """
    return string[:1].lower() + string[1:]


def capitalize(string: str) -> str:
    """
    Capitalizes only the first letter of a string.

    Args:
        string (str): The input string.

    Returns:
        str: The capitalized string.
    """
    return string[:1].upper() + string[1:]


def strip_string(string: str, chars: Optional[list[str]] = None) -> str:
    """Strip a string except an optional list of characters.

    Args:
        string (str): The input string.
        chars (Optional[list[str]]): A list of characters to not strip.

    Returns:
        str: The cleaned string.

    """
    if chars is None:
        chars = []

    s_string: str = string.strip()

    for c in chars:
        if c.strip != "":  # Check if c is removed by the str.strip
            continue
        if string.startswith(c):
            s_string = c + s_string
        if string.endswith(c):
            s_string = s_string + c

    return s_string


def capitalize_all(string: str) -> str:
    """
    Capitalizes all sentences in a string.

    Args:
        string (str): The input string.

    Returns:
        str: The string with all sentences capitalized.
    """
    string = string.strip() + " "

    # Get all sentences by splitting first by the ". " delimiter and then capitalize
    # those. Do the with the ".\n" delimiter.
    for delimiter, last_punctuation in [(". ", ". "), (".\n", "")]:
        f: filter = filter(None, string.split(delimiter))
        all_strings: list[str] = [capitalize(strip_string(s, ["\n"])) for s in f]
        string = concatenate_string(
            all_strings,
            delimiter=delimiter,
            last_delimiter=delimiter,
            last_punctuation=last_punctuation,
        )

    return string


def concatenate_string(
    iterator: Union[List[str], iter],
    delimiter: str = ", ",
    last_delimiter: str = f" {_('et')} ",
    last_punctuation: str = "",
) -> str:
    """
    Concatenates a list of strings with specified delimiters.

    Args:
        iterator (Union[List[str], iter]): The list or iterator of strings to
        concatenate.
        delimiter (str, optional): The delimiter between strings. Defaults to ", ".
        last_delimiter (str, optional): The delimiter before the last string. Defaults
            to " et ".
        last_punctuation (str, optional): The punctuation to add at the end. Defaults
            to "".

    Returns:
        str: The concatenated string.
    """
    list_it = [it for it in iterator if it]
    if not list_it:
        return ""

    return (
        delimiter.join(list_it[:-1]) + last_delimiter + list_it[-1]
        if len(list_it) > 1
        else f"{list_it[0]}"
    ) + last_punctuation


def clean_text(text: str) -> str:
    """
    Cleans text according to the language specified in Settings.language.

    Args:
        text: The text to clean.

    Returns:
        The cleaned text.
    """
    # make some basic cleans
    text = text.strip()
    text = re.sub(r"\s\n", "\n", text)  # Replaces " \n" with "\n"
    text = re.sub(r"\.[ ]*\.", ".", text)  # Replaces ".." or ".   ." with "."
    text = re.sub(r"\,[ ]*\.", ".", text)  # Replaces ",." or ",   ." with "."

    funcs = {
        "fr": clean_french_text,
        "en": clean_english_text,
        "es": clean_spanish_text,
    }
    text = funcs[Settings().language](text)

    text = re.sub(r"\.[ ]*\.", ".", text)  # Replaces ".." or ".   ." with "."
    text = re.sub(r"\,[ ]*\.", ".", text)  # Replaces ",." or ",   ." with "."
    text = re.sub("[ ]+ ", " ", text)
    text = re.sub("[ ]+", " ", text)
    return capitalize_all(text).strip()


def clean_spanish_text(text: str) -> str:
    """Cleans up Spanish text.

    Args:
        text (str): The input text.

    Returns:
        str: The cleaned text.
    """
    return text


def clean_english_text(text: str) -> str:
    """Cleans up English text.

    Args:
        text (str): The input text.

    Returns:
        str: The cleaned text.
    """
    return text


def clean_french_text(text: str) -> str:
    """
    Cleans up French text by replacing certain patterns.

    Args:
        text (str): The input text.

    Returns:
        str: The cleaned text.
    """
    text = re.sub(r"[  ](celsius|°C)", "°C", text)

    text = re.sub(r"jusqu.à au", "jusqu'au", text)
    text = re.sub(r"jusqu.à le", "jusqu'au", text)
    text = re.sub(r"jusqu.à en", "jusqu'en", text)
    text = re.sub(r"([^\w_])dès en début", r"\1dès le début", text)
    text = re.sub(r"([^\w_])dès en première", r"\1dès la première", text)
    text = re.sub(r"([^\w_])dès en fin", r"\1dès la fin", text)
    text = re.sub(r"([^\w_])que en", r"\1qu'en", text)
    text = re.sub(r"([^\w_])de en ce", r"\1du", text)
    text = re.sub(r"([^\w_])de en début", r"\1du début", text)
    text = re.sub(r"([^\w_])de en milieu", r"\1du milieu", text)
    text = re.sub(r"([^\w_])de en fin", r"\1de la fin", text)
    text = re.sub(r"([^\w_])de en première", r"\1de la première", text)
    text = re.sub(r"([^\w_])de ([aeiouyAEIOUY])", r"\1d'\2", text)

    return text


def split_var_name(var_name: str) -> Tuple[str, Optional[int], Optional[str]]:
    """
    Splits a variable name following the pattern <prefix><accum>__<vertical_level>
    into a tuple (<prefix>, <accum>, <vertical_level>).

    Args:
        var_name (str): The variable name.

    Returns:
        Tuple[str, Optional[int], Optional[str]]: A tuple containing:
            - The prefix
            - The accumulation value (optional)
            - The vertical level (optional)
    """
    prefix, accum, vert_level = re.match(
        r"^([a-zA-Z_]+)(\d*)__(.*)$", var_name
    ).groups()

    if accum == "":
        accum = 0

    return prefix, int(accum), vert_level


class TagFormatter:
    """
    TagFormatter: Format a string containing tags of the form '[key:func]'.
    It follows the Vortex standard.
    """

    time_format: dict = {
        "fmth": "{:04d}",
        "fmthm": "{:04d}:00",
        "fmthhmm": "{:02d}:00",
        "fmtraw": "{:04d}00",
    }
    datetime_format: dict = {
        "julian": "%j",
        "ymd": "%Y%m%d",
        "yymd": "%y%m%d",
        "y": "%Y",
        "ymdh": "%Y%m%d%H",
        "yymdh": "%y%m%d%H",
        "ymdhm": "%Y%m%d%H%M",
        "ymdhms": "%Y%m%d%H%M%S",
        "mmddhh": "%m%d%H",
        "mm": "%m",
        "hm": "%H%M",
        "dd": "%d",
        "hh": "%H",
        "h": "%-H",
        "vortex": "%Y%m%dT%H%M%S",
        "stdvortex": "%Y%m%dT%H%M",
        "iso8601": "%Y-%m-%dT%H:%M:%SZ",
    }

    def format_tags(self, text: str, tags: dict = None) -> str:
        """
        Formats a string containing tags of the form '[key:func]'.

        Args:
            text (str): The text to format.
            tags (dict, optional): A dictionary of tag-value pairs. Defaults to None.

        Returns:
            str: The formatted string.
        """
        if not tags:
            return text

        for key, value in tags.items():
            # Raw key formatting
            text = text.replace("[{}]".format(key), str(value))

            # Time formatting
            if isinstance(value, int):
                for func, fmt in self.time_format.items():
                    text = text.replace("[{}:{}]".format(key, func), fmt.format(value))
            # Datetime formatting
            try:
                from mfire.utils.date import Datetime

                value_dt = Datetime(value)
                for func, fmt in self.datetime_format.items():
                    text = text.replace(
                        "[{}:{}]".format(key, func), value_dt.strftime(fmt)
                    )
            except (TypeError, ValueError):
                pass

            # Geometry formatting
            text = text.replace("[{}:area]".format(key), str(value).upper())

        return text


def is_vowel(letter: str) -> bool:
    """Indicates if the letter is a vowel"""
    if len(letter) > 1:
        raise ValueError

    return unicodedata.normalize("NFKD", letter).encode("ASCII", "ignore").decode(
        "utf-8"
    ).lower() in ["a", "e", "i", "o", "u", "y"]
