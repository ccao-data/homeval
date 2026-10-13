"""Constants that are shared between scripts in this module"""

# It's helpful to factor these tables out into shared constants because we often
# need to switch to dev tables for testing
HOMEVAL_ASSESSMENT_CARD_TABLE = (
    "z_ci_edit_assets_for_2026_comps_refresh_pinval.assessment_card"
)
HOMEVAL_COMP_TABLE = "z_ci_edit_assets_for_2026_comps_refresh_pinval.comp"
HOMEVAL_DATA_DICT_TABLE = "pinval.vars_dict"
