from lanQ_rule.common_rule import *
from lanQ_rule.model_rule import *
from lanQ_rule.prompt_rule import *

# 有效性
QUALITY_SIGNAL_EFFECTIVENESS = 'QUALITY_SIGNAL_EFFECTIVENESS'
# 完整性
QUALITY_SIGNAL_COMPLETENESS = 'QUALITY_SIGNAL_COMPLETENESS'
# 格式
QUALITY_SIGNAL_UNDERSTANDABILITY = 'QUALITY_SIGNAL_UNDERSTANDABILITY'
# 重复
QUALITY_SIGNAL_SIMILARITY = 'QUALITY_SIGNAL_SIMILARITY'
# 流畅性
QUALITY_SIGNAL_FLUENCY = 'QUALITY_SIGNAL_FLUENCY'
# 相关性
QUALITY_SIGNAL_RELEVANCE = 'QUALITY_SIGNAL_RELEVANCE'
# 安全性
QUALITY_SIGNAL_SECURITY = 'QUALITY_SIGNAL_SECURITY'

QUALITY_MAP = {
    QUALITY_SIGNAL_EFFECTIVENESS: [
        common_chaos_en,
        common_chaos_symbol,
        common_chaos_zh,
        common_content_null,
        common_invalid_web,
        common_language_mixed,
        common_url_only,
        prompt_chinese_produce_english,
        prompt_english_produce_chinese,
    ],
    QUALITY_SIGNAL_COMPLETENESS: [
        common_bracket_unmatch,
        common_colon_end,
    ],
    QUALITY_SIGNAL_UNDERSTANDABILITY: [
        common_check_photo,
        common_ellipsis_ratio,
        common_enter_more,
        common_enter_ratio_more,
        common_space_more,
        common_emoj_characters,
        common_html_entity,
        common_img_html_tag,
        common_invisible_char,
        common_joint_special_symbol,
        common_special_character,
        common_special_mark,
        common_unconverted_symbol,
    ],
    QUALITY_SIGNAL_SIMILARITY: [
        common_doc_repeat,
        common_underscore_length,
    ],
    QUALITY_SIGNAL_FLUENCY: [
        common_anti_crawler_zh,
        common_no_punc,
        common_word_stuck,
    ],
    QUALITY_SIGNAL_RELEVANCE: [
        model_advertisement,
        model_watermark,
    ],
    QUALITY_SIGNAL_SECURITY: [
        common_license_key,
    ],
}
