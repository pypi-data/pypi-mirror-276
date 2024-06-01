from mfire.settings import Settings


def wind_template_dict() -> dict[str, str]:
    if Settings().language == "fr":
        from mfire.settings.wind.wind_fr import TEMPLATES_DICT_FR

        return TEMPLATES_DICT_FR
    elif Settings().language == "en":
        from mfire.settings.wind.wind_en import TEMPLATES_DICT_EN

        return TEMPLATES_DICT_EN
    elif Settings().language == "es":
        from mfire.settings.wind.wind_es import TEMPLATES_DICT_ES

        return TEMPLATES_DICT_ES
