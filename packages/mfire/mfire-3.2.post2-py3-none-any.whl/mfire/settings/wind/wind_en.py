from mfire.text.wind.const import ERROR_CASE
from mfire.text.wind.reducers.gust_summary_builder.gust_enum import GustCase
from mfire.text.wind.reducers.wind_summary_builder.helpers.wind_enum import WindCase

TEMPLATE_B1_1: str = (
    "{{ wd_periods[0]['wd']|safe }} wind , "
    "{{ wf_periods[0]['interval'][0] }} at "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)

TEMPLATE_B1_2: str = (
    "{{ wd_periods[0]['wd']|safe }} wind moving "
    "{{ wd_periods[1]['wd'] }} {{ wd_periods[1]['begin_time']|safe }}, "
    "{{ wf_periods[0]['interval'][0] }} to {{ wf_periods[0]['interval'][1] }}"
    " {{ units }}."
)

TEMPLATE_B1_3: str = (
    "{{ wd_periods[0]['wd']|safe }} wind , "
    "{{ wf_periods[0]['interval'][0] }} at "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}, "
    "{{ var_marker }} {{ wf_periods[1]['interval'][0] }} to "
    "{{ wf_periods[1]['interval'][1] }} {{ units }} "
    "{{ wf_periods[1]['begin_time']|safe }}."
)

TEMPLATE_B1_4: str = (
    "{{ wd_periods[0]['wd']|safe }} wind  "
    "orienting {{ wd_periods[1]['wd'] }}, "
    "{{ wf_periods[0]['interval'][0] }} at "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}, "
    "{{ var_marker }} {{ wf_periods[1]['interval'][0] }} to "
    "{{ wf_periods[1]['interval'][1] }} {{ units }} "
    "{{ wf_periods[1]['begin_time']|safe }}."
)

TEMPLATE_B1_5: str = (
    "{{ wd_periods[0]['wd']|safe }} wind , "
    "{{ wf_periods[0]['interval'][0] }} at "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}, "
    "{{ var_marker }} {{ wf_periods[1]['interval'][0] }} to "
    "{{ wf_periods[1]['interval'][1] }} {{ units }} } "
    "with orientation {{ wd_periods[1]['wd']|safe }}"
    " {{ wf_periods[1]['begin_time']|safe }}."
)

TEMPLATE_B1_6: str = (
    "{{ wd_periods[0]['wd']|safe }} wind , "
    "between {{ wf_periods[0]['interval'][0] }} and "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)

TEMPLATE_B1_7: str = (
    "{{ wd_periods[0]['wd']|safe }} wind  "
    "orienting {{ wd_periods[1]['wd']|safe }} "
    "{{ wd_periods[1]['begin_time']|safe }}, between "
    "{{ wf_periods[0]['interval'][0] }} "
    "and {{ wf_periods[0]['interval'][1] }} {{ units }}."
)
TEMPLATE_B1_8: str = (
    "Wind from {{ wf_periods[0]['interval'][0] }} to "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)

TEMPLATE_B1_9: str = (
    "Wind from {{ wf_periods[0]['interval'][0] }} to {{ wf_periods[0]['interval'][1] }}"
    " {{ units }}, {{ var_marker }} {{ wf_periods[1]['interval'][0] }} to "
    "{{ wf_periods[1]['interval'][1] }} {{ units }} "
    "{{ wf_periods[1]['begin_time']|safe }}."
)

TEMPLATE_B1_10: str = (
    "Wind between {{ wf_periods[0]['interval'][0] }} and "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)

TEMPLATE_B2_1: str = (
    "{{ wd_periods[0]['wd']|safe }} wind , "
    "{{ wf_periods[0]['interval'][0] }} to {{ wf_periods[0]['interval'][1] }}"
    " {{ units }}, {{ wf_periods[0]['time_desc']|safe }} as well as "
    "{{ wf_periods[1]['time_desc']|safe }}."
)

TEMPLATE_B2_2: str = (
    "{{ wd_periods[0]['wd']|safe }} "
    "{{ wd_periods[0]['begin_time']|safe }} moving towards "
    "{{ wd_periods[1]['wd']|safe }} "
    "{{ wd_periods[1]['begin_time']|safe }} "
    "wind {{ wf_periods[0]['interval'][0] }} at "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)

TEMPLATE_B2_3: str = (
    "{{ wd_periods[0]['wd']|safe }} "
    "{{ wd_periods[0]['time_desc']|safe }} "
    "wind {{ wf_periods[0]['interval'][0] }} at {{ wf_periods[0]['interval'][1] }}"
    " {{ units }}."
)

TEMPLATE_B2_4: str = (
    "{{ wf_periods[0]['time_desc']|safe }} "
    "{{ wd_periods[0]['wd']|safe }}"
    " then {{ wd_periods[1]['wd'] }}, and {{ wf_periods[1]['time_desc']|safe }} "
    "{{ wd_periods[2]['wd']|safe }} "
    "wind {{ wf_periods[0]['interval'][0] }} at "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)
TEMPLATE_B2_5: str = (
    "{{ wf_periods[0]['time_desc']|safe }} "
    "{{ wd_periods[0]['wd']|safe }}, and "
    "{{ wf_periods[1]['time_desc']|safe }} "
    "{{ wd_periods[1]['wd']|safe }} then "
    "{{ wd_periods[2]['wd'] }} } "
    "wind {{ wf_periods[0]['interval'][0] }} at "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)

TEMPLATE_B2_6: str = (
    "{{ wf_periods[0]['time_desc']|safe }}"
    "{{ wd_periods[0]['wd']||safe }} "
    "then {{ wd_periods[1]['wd'] }}, and "
    "{{ wf_periods[1]['time_desc']|safe }} "
    "{{ wd_periods[2]['wd']|safe }} "
    "then {{ wd_periods[3]['wd'] }}} "
    "wind {{ wf_periods[0]['interval'][0] }} at "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)

TEMPLATE_B2_7: str = (
    "{{ wd_periods[0]['wd']|safe }} wind , "
    "{{ wf_periods[0]['interval'][0] }} to {{ wf_periods[0]['interval'][1] }}"
    " {{ units }} {{ wf_periods[0]['time_desc']|safe }}, "
    "{{ wf_periods[1]['interval'][0] }} to {{ wf_periods[1]['interval'][1] }}"
    " {{ units }} {{ wf_periods[1]['time_desc']|safe }}."
)

TEMPLATE_B2_8: str = (
    "{{ wd_periods[0]['wd']|safe }} wind , "
    "{{ wf_periods[0]['interval'][0] }} to {{ wf_periods[0]['interval'][1] }} "
    " {{ units }} {{ wf_periods[0]['time_desc']|safe }}, then "
    "{{ wf_periods[1]['interval'][0] }} to {{ wf_periods[1]['interval'][1] }} "
    " {{ units }} with orientation {{ wd_periods[1]['wd']|safe }} "
    "{{ wf_periods[1]['time_desc']|safe }}."
)

TEMPLATE_B2_9: str = (
    "{{ wd_periods[0]['wd']|safe }} wind  moving "
    "{{ wd_periods[-1]['wd'] }}, {{ wf_periods[0]['interval'][0] }} to "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}, "
    "{{ wf_periods[0]['time_desc']|safe }}, "
    "{{ wf_periods[1]['interval'][0] }} to {{ wf_periods[1]['interval'][1] }}"
    " {{ units }} {{ wf_periods[1]['time_desc']|safe }}."
)

TEMPLATE_B2_10: str = (
    "{{ wd_periods[0]['wd']|safe }} wind , between "
    "{{ wf_periods[0]['interval'][0] }} and "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)
TEMPLATE_B2_11: str = (
    "{{ wd_periods[0]['wd']|safe }} wind  "
    "{{ wd_periods[0]['begin_time']|safe }} moving towards "
    "{{ wd_periods[1]['wd']|safe }} "
    "{{ wd_periods[-1]['begin_time']|safe }}, between "
    "{{ wf_periods[0]['interval'][0] }} and "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)

TEMPLATE_B2_12: str = (
    "{{ wd_periods[0]['wd']|safe }} wind  "
    "{{ wd_periods[0]['time_desc']|safe }}, between "
    "{{ wf_periods[0]['interval'][0] }} and"
    " {{ wf_periods[0]['interval'][1] }} {{ units }}."
)

TEMPLATE_B2_13: str = (
    "{{ wf_periods[0]['time_desc']|safe }} "
    "{{ wd_periods[0]['wd']|safe }} then {{ wd_periods[1]['wd'] }}, "
    "and {{ wf_periods[1]['time_desc']|safe }} "
    "{{ wd_periods[2]['wd']|safe }}"
    "Wind between {{ wf_periods[0]['interval'][0] }} and "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)

TEMPLATE_B2_14: str = (
    "{{ wf_periods[0]['time_desc']|safe }} "
    "{{ wd_periods[0]['wd']|safe }}, and "
    "{{ wf_periods[1]['time_desc']|safe }} "
    "{{ wd_periods[1]['wd']|safe }} then {{ wd_periods[2]['wd'] }} } "
    "wind between {{ wf_periods[0]['interval'][0] }} and "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)

TEMPLATE_B2_15: str = (
    "{{ wd_periods[0]['wd']|safe }} "
    "{{ wd_periods[0]['begin_time']|safe }} moving "
    "{{ wd_periods[3]['wd'] }} {{ wd_periods[3]['begin_time']|safe }} } "
    "wind between {{ wf_periods[0]['interval'][0] }} and "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)

TEMPLATE_B2_16: str = (
    " {{ wd_periods[0]['wd']|safe }} {{ wf_periods[1]['time_desc']|safe }} } "
    "wind {{ wf_periods[0]['interval'][0] }} at {{ wf_periods[0]['interval'][1] }}"
    " {{ units }} {{ wf_periods[0]['time_desc']|safe }}, "
    "{{ wf_periods[1]['interval'][0] }} to {{ wf_periods[1]['interval'][1] }}"
    " {{ units }}."
)

TEMPLATE_B2_17: str = (
    "Wind from {{ wf_periods[0]['interval'][0] }} to {{ wf_periods[0]['interval'][1] }}"
    " {{ units }}, {{ wf_periods[0]['time_desc']|safe }} as well as "
    "{{ wf_periods[1]['time_desc']|safe }}."
)

TEMPLATE_B2_18: str = (
    "Wind from {{ wf_periods[0]['interval'][0] }} to {{ wf_periods[0]['interval'][1] }}"
    " {{ units }} {{ wf_periods[0]['time_desc']|safe }}, "
    "{{ wf_periods[1]['interval'][0] }} to {{ wf_periods[1]['interval'][1] }}"
    " {{ units }} {{ wf_periods[1]['time_desc']|safe }}."
)

TEMPLATE_B2_19: str = (
    "Wind between {{ wf_periods[0]['interval'][0] }} and "
    "{{ wf_periods[0]['interval'][1] }} {{ units }}."
)

ERROR_TEMPLATE: str = "Error generating wind summaries."


TEMPLATES_DICT_EN: dict[str, str] = {
    GustCase.CASE_1.value: "",
    GustCase.CASE_2.value: (
        "Gusts exceed {% if gust_tempos[0] %}{{ gust_tempos[0]|safe }}"
        "{% endif %} {{ force_min }} {{ units }}{% if gust_tempos[1] %} "
        "{{ gust_tempos[1]|safe }}{% endif %}. Maximum possible values between "
        "{{ gust_interval[0] }} and {{ gust_interval[1] }} {{ units }}."
    ),
    WindCase.CASE_1.value: "",
    WindCase.CASE_2.value: (
        "{% if wd_periods|length > 0 %}"
        " {{ wd_periods[0]['wd']|safe }}{% endif %}"
        " {{ wf_intensity }} wind"
        "{% if wd_periods|length == 2 %} orienting itself "
        "{{ wd_periods[1]['wd']|safe }} "
        "{{ wd_periods[1]['begin_time']|safe }}{% endif %}."
    ),
    WindCase.CASE_3_1B_1.value: TEMPLATE_B1_1,
    WindCase.CASE_3_1B_2.value: TEMPLATE_B1_2,
    WindCase.CASE_3_1B_3.value: TEMPLATE_B1_8,
    WindCase.CASE_3_1B_4.value: TEMPLATE_B1_3,
    WindCase.CASE_3_1B_5.value: TEMPLATE_B1_1,
    WindCase.CASE_3_1B_6.value: TEMPLATE_B1_4,
    WindCase.CASE_3_1B_7.value: TEMPLATE_B1_5,
    WindCase.CASE_3_1B_8.value: TEMPLATE_B1_2,
    WindCase.CASE_3_1B_9.value: TEMPLATE_B1_9,
    WindCase.CASE_3_1B_10.value: TEMPLATE_B1_8,
    WindCase.CASE_3_1B_11.value: TEMPLATE_B1_6,
    WindCase.CASE_3_1B_12.value: TEMPLATE_B1_7,
    WindCase.CASE_3_1B_13.value: TEMPLATE_B1_10,
    WindCase.CASE_3_2B_1.value: TEMPLATE_B2_1,
    WindCase.CASE_3_2B_2.value: TEMPLATE_B2_2,
    WindCase.CASE_3_2B_3.value: TEMPLATE_B2_3,
    WindCase.CASE_3_2B_4.value: TEMPLATE_B2_3,
    WindCase.CASE_3_2B_5.value: TEMPLATE_B2_4,
    WindCase.CASE_3_2B_6.value: TEMPLATE_B2_2,
    WindCase.CASE_3_2B_7.value: TEMPLATE_B2_5,
    WindCase.CASE_3_2B_8.value: TEMPLATE_B2_2,
    WindCase.CASE_3_2B_9.value: TEMPLATE_B2_6,
    WindCase.CASE_3_2B_10.value: TEMPLATE_B2_17,
    WindCase.CASE_3_2B_11.value: TEMPLATE_B2_7,
    WindCase.CASE_3_2B_12.value: TEMPLATE_B2_1,
    WindCase.CASE_3_2B_13.value: TEMPLATE_B2_8,
    WindCase.CASE_3_2B_14.value: TEMPLATE_B2_2,
    WindCase.CASE_3_2B_15.value: TEMPLATE_B2_7,
    WindCase.CASE_3_2B_16.value: TEMPLATE_B2_3,
    WindCase.CASE_3_2B_17.value: TEMPLATE_B2_16,
    WindCase.CASE_3_2B_18.value: TEMPLATE_B2_3,
    WindCase.CASE_3_2B_19.value: TEMPLATE_B2_9,
    WindCase.CASE_3_2B_20.value: TEMPLATE_B2_4,
    WindCase.CASE_3_2B_21.value: TEMPLATE_B2_9,
    WindCase.CASE_3_2B_22.value: TEMPLATE_B2_2,
    WindCase.CASE_3_2B_23.value: TEMPLATE_B2_9,
    WindCase.CASE_3_2B_24.value: TEMPLATE_B2_5,
    WindCase.CASE_3_2B_25.value: TEMPLATE_B2_9,
    WindCase.CASE_3_2B_26.value: TEMPLATE_B2_2,
    WindCase.CASE_3_2B_27.value: TEMPLATE_B2_9,
    WindCase.CASE_3_2B_28.value: TEMPLATE_B2_6,
    WindCase.CASE_3_2B_29.value: TEMPLATE_B2_18,
    WindCase.CASE_3_2B_30.value: TEMPLATE_B2_17,
    WindCase.CASE_3_2B_31.value: TEMPLATE_B2_10,
    WindCase.CASE_3_2B_32.value: TEMPLATE_B2_11,
    WindCase.CASE_3_2B_33.value: TEMPLATE_B2_12,
    WindCase.CASE_3_2B_34.value: TEMPLATE_B2_12,
    WindCase.CASE_3_2B_35.value: TEMPLATE_B2_13,
    WindCase.CASE_3_2B_36.value: TEMPLATE_B2_11,
    WindCase.CASE_3_2B_37.value: TEMPLATE_B2_14,
    WindCase.CASE_3_2B_38.value: TEMPLATE_B2_11,
    WindCase.CASE_3_2B_39.value: TEMPLATE_B2_15,
    WindCase.CASE_3_2B_40.value: TEMPLATE_B2_19,
    ERROR_CASE: ERROR_TEMPLATE,
}
