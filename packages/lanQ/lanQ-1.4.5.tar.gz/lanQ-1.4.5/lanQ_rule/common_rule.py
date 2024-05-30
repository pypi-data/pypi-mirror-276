import os
import sys
import jieba
import langid
import textstat
from hanziconv import HanziConv

sys.path.append(os.path.dirname(__file__))

import lanQ_rule.config.customize as cm
from lanQ_rule.base_func.base import *

def common_anti_crawler_zh(content: str) -> dict:
    """from lvkai"""
    res = {'error_status': False, 'error_reason': ''}
    line_num = 50
    content_lines = [l.strip() for l in content.split("\n") if len(l.strip())]
    max_jieba_ratio = 0
    for line in content_lines:
        line = get_real_text(line)
        char_num = len(line)
        word_num = 0
        if len(line) > line_num:
            seg_list = jieba.cut(line, cut_all=True)
            for word in seg_list:
                if len(word) == 1:
                    word_num += 1
            max_jieba_ratio = max(max_jieba_ratio, word_num / char_num)
    if max_jieba_ratio > cm.common_anti_crawler_zh['threshold']:
        res["error_status"] = True
        res["error_reason"] = "包含反爬文本"
    return res

def common_bracket_unmatch(content: str) -> dict:
    """check whether bracket matches"""
    res = {'error_status': False, 'error_reason': ''}
    bracket_types = [("[", "]"), ("{", "}"), ("【", "】"), ("《", "》")]
    for open_bracket, close_bracket in bracket_types:
        if content.count(open_bracket) != content.count(close_bracket):
            res["error_status"] = True
            res["error_reason"] = "括号数量不一致"
    return res

def common_chaos_en(content: str) -> dict:
    """check whether content has English messy code"""
    res = {'error_status': False, 'error_reason': ''}
    af_en = delete_punc_en(content)
    af_ch = delte_punc_ch(af_en)
    str_len = len(af_ch)
    language = langid.classify(content)[0]
    if language == "en":
        seg_len = len(list(jieba.cut(af_ch)))
        if str_len == 0 or seg_len == 0 or get_tokens(content, language) < 50:
            return res
        if str_len / seg_len > 1.2:
            return res
        else:
            res["error_status"] = True
            res["error_reason"] = '英文乱码'
            return res
    else:
        return res

def common_chaos_symbol(content: str) -> dict:
    """check whether content has a lot of meaningless words"""
    res = {'error_status': False, 'error_reason': ''}
    pattern = r'[0-9a-zA-Z\u4e00-\u9fa5]'
    s = re.sub(pattern, '', content)
    str_len = len(content)
    symbol_len = len(s)
    if str_len == 0 or symbol_len == 0:
        return res
    if symbol_len / str_len > 0.5:
        res["error_status"] = True
        res['error_reason'] = '大量非正文内容'
    return res

def common_chaos_zh(content: str) -> dict:
    """check whether content has Chinese messy code"""
    res = {'error_status': False, 'error_reason': ''}
    lan = langid.classify(content)[0]
    if lan != 'zh':
        return res
    s = normalize(content)
    pattern = r'[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ\n\s]'
    s = re.sub(pattern, '', s)
    s_simplified = HanziConv.toSimplified(s)
    str_len = len(s)
    seg_len = len(list(jieba.cut(s_simplified)))
    num_bytes = len(content.encode('utf-8'))
    tokens_len = int(num_bytes * 0.248)
    if str_len == 0 or seg_len == 0 or tokens_len < 50:
        return res
    if str_len / seg_len <= 1.1:
        res["error_status"] = True
        res['error_reason'] = '中文乱码'
    return res

def common_check_photo(content: str) -> dict:
    """check whether content has photo"""
    res = {'error_status': False, 'error_reason': ''}
    pattern = '!\[\]\(http[s]?://.*?jpeg "\n"\)'
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res['error_reason'] = matches
    return res

def common_colon_end(content: str) -> dict:
    """check whether the last char is ':'"""
    res = {'error_status': False, 'error_reason': ''}
    if len(content) <= 0:
        return res
    if content[-1] == ':':
        res['error_status'] = True
        res['error_reason'] = '冒号结尾'
    return res

def common_content_null(content: str) -> dict:
    """check whether content is null"""
    res = {'error_status': False, 'error_reason': ''}
    count = len(content.strip())
    if count == 0:
        res["error_status"] = True
        res['error_reason'] = '内容为空'
    return res

def common_doc_repeat(content: str) -> dict:
    """check whether content repeats"""
    res = {'error_status': False, 'error_reason': ''}
    repeat_score = base_rps_frac_chars_in_dupe_ngrams(6, content)
    if repeat_score >= 80:
        res["error_status"] = True
        res['error_reason'] = '文本重复度过高： ' + str(repeat_score)
    return res

def common_ellipsis_ratio(content: str) -> dict:
    """check whether ratio of lines end with ellipsis is bigger than 75%"""
    res = {'error_status': False, 'error_reason': ''}
    lines = content.split("\n")
    non_empty_lines = 0
    ellipsis_lines = 0
    for line in lines:
        if line.strip() != "":
            non_empty_lines += 1
            if (
                line.strip().endswith("。。。")
                or line.strip().endswith("…")
                or line.strip().endswith("。。。。。。")
                or line.strip().endswith("……")
            ):
                ellipsis_lines += 1
    if non_empty_lines != 0:
        ellipsis_ratio = ellipsis_lines / non_empty_lines
        if ellipsis_ratio >0.75:
            res["error_status"] = True
            res["error_reason"] = "省略号结尾行占比超过75%"
    return res

def common_emoj_characters(content: str) -> dict:
    """check whether content contains emoji charactors"""
    res = {'error_status': False, 'error_reason': ''}
    emoj_chars_pattern = r"U\+26[0-F][0-D]|U\+273[3-4]|U\+1F[3-6][0-4][0-F]|U\+1F6[8-F][0-F]"
    matches = re.search(emoj_chars_pattern, content)
    if matches:
        res["error_status"] = True
        res["error_reason"] = "包含emoji符号"
    return res

def common_enter_more(content: str) -> dict:
    """check whether content has more than 8 continious enter"""
    res = {'error_status': False, 'error_reason': ''}
    pattern = r'\n{8,}|\r{8,}'
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res['error_reason'] = '存在连续8个回车'
    return res

def common_enter_ratio_more(content: str) -> dict:
    """check whether enter / content is more than 25%"""
    res = {'error_status': False, 'error_reason': ''}
    enter_count = content.count('\n')
    count = len(content)
    if count == 0:
        return res
    ratio = enter_count / count * 100
    if ratio >= 25:
        res["error_status"] = True
        res['error_reason'] = '回车超过正文25%'
    return res

def common_html_entity(content: str) -> dict:
    """check whether content has html entity"""
    res = {'error_status': False, 'error_reason': ''}
    entities = [
        "nbsp",
        "lt",
        "gt",
        "amp",
        "quot",
        "apos",
        "hellip",
        "ndash",
        "mdash",
        "lsquo",
        "rsquo",
        "ldquo",
        "rdquo",
    ]
    full_entities_1 = [f"&{entity}；" for entity in entities]
    full_entities_2 = [f"&{entity};" for entity in entities]
    full_entities_3 = [f"＆{entity};" for entity in entities]
    full_entities_4 = [f"＆{entity}；" for entity in entities]
    full_entities = (
        full_entities_1 + full_entities_2 + full_entities_3 + full_entities_4
    )
    # half_entity_1 = [f"{entity}；" for entity in entities]
    half_entity_2 = [f"＆{entity}" for entity in entities]
    half_entity_3 = [f"&{entity}" for entity in entities]
    # half_entity_4 = [f"{entity};" for entity in entities]
    half_entities = half_entity_2 + half_entity_3
    # maked_entities = [f"{entity}" for entity in entities]
    all_entities = full_entities + half_entities

    pattern = '|'.join(all_entities)
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res['error_reason'] = matches
    return res

def common_img_html_tag(content: str) -> dict:
    """check whether content has img or html tag"""
    res = {'error_status': False, 'error_reason': ''}
    pattern = r"(<img[^>]*>)|<p[^>]*>(.*?)<\/p>|<o:p[^>]*>(.*?)<\/o:p>"
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res['error_reason'] = matches
    return res

def common_invalid_web(content: str) -> dict:
    """check whether the content is invalid"""
    res = {'error_status': False, 'error_reason': ''}
    invalid_list = ["404 - Page not found\nThe requested page does not exist (or has been deleted).\nIf you typed a URL by hand, or used a bookmark, please double check the address that you used.\nIf you see this page, and the error persists, please contact Customer Care and provide details about the action you tried to perform."]
    for item in invalid_list:
        if item in content:
            res["error_status"] = True
            res["error_reason"] = "content内容为404"
    return res

def common_invisible_char(content: str) -> dict:
    """check whether content has invisible char"""
    res = {'error_status': False, 'error_reason': ''}
    pattern = r"[\u2000-\u200F\u202F\u205F\u3000\uFEFF\u00A0\u2060-\u206F\uFEFF\xa0]"
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res['error_reason'] = matches
    return res

def common_joint_special_symbol(content: str) -> dict:
    """check if there are special symbols composed of multiple symbols spliced together"""
    res = {'error_status': False, 'error_reason': ''}
    pattern = r"&#247;|\? :"
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res["error_reason"] = "包含多个符号拼接组成的特殊符号"
    return res

def common_language_mixed(content: str) -> dict:
    """check whether content is mixed in Chinese and English"""
    res = {'error_status': False, 'error_reason': ''}
    s = normalize(content)
    en_len = len(re.findall(r'[a-zA-Z]', s))
    zh_len = len(re.findall(r'[\u4e00-\u9fa5]', s))
    count_len = len(s)
    if count_len == 0:
        return res
    if en_len / count_len >= 0.5 and zh_len / count_len >= 0.1:
        res["error_status"] = True
        res['error_reason'] = '中英文混杂'
    return res

def common_license_key(content: str) -> dict:
    """check if the content contains license key"""
    res = {'error_status': False, 'error_reason': ''}
    # 定义三个模式对应于上述的三种格式
    pattern = r"(License|破解)|" + "|".join([
    "[A-Z0-9]{47}",  # 字母数字混合
    "[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}",  # 分段的字母数字混合
    "[A-Z0-9]{4}-\d{8}-[A-Z0-9]{4}"  # 含有特定信息的许可证密钥，例如产品ID和购买日期
    ])
    match = re.search(pattern, content, re.I)  # re.I使匹配对大小写不敏感
    if match:
        res["error_status"] = True
        res["error_reason"] = "包含license key"
    return res

def common_no_punc(content: str) -> dict:
    """check whether content has paragraph without punctuations"""
    res = {'error_status': False, 'error_reason': ''}
    paragraphs = content.split('\n')
    max_word_count = 0
    for paragraph in paragraphs:
        if len(paragraph) == 0:
            continue
        sentences = re.split(r'[-–.!?,;•、。！？，；·]', paragraph)
        for sentence in sentences:
            words = sentence.split()
            word_count = len(words)
            if word_count > max_word_count:
                max_word_count = word_count
    text_stat_res = textstat.flesch_reading_ease(content)
    if int(max_word_count) > 56 and text_stat_res < 20:
        res["error_status"] = True
        res['error_reason'] = '段落无标点'
    return res

def common_space_more(content: str) -> dict:
    """check whether content has more than 500 consecutive spaces"""
    res = {'error_status': False, 'error_reason': ''}
    pattern = r' {500,}'
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res['error_reason'] = '存在连续500个空格'
    return res

def common_special_character(content: str) -> dict:
    res = {'error_status': False, 'error_reason': ''}
    pattern = r"[�□]|\{\/U\}"
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res['error_reason'] = matches
    return res

def common_special_mark(content: str) -> dict:
    """check if the content contains special mark"""
    res = {'error_status': False, 'error_reason': ''}
    pattern = r'keyboard_arrow_(left|right)'
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res["error_reason"] = "元素包含特殊标记"
    return res

def common_unconverted_symbol(content: str) -> dict:
    """check if the content contains special symbols for conversion failure"""
    res = {'error_status': False, 'error_reason': ''}
    pattern = r'u200e'
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res["error_reason"] = "包含转换失败的特殊符号"
    return res

def common_underscore_length(content: str) -> dict:
    """check whether the content contains underscores whose length is longer than 15"""
    res = {'error_status': False, 'error_reason': ''}
    max_underscore_count = 0
    for char in content:
        if char == '_':
            underscore_count += 1
            if underscore_count > max_underscore_count:
                max_underscore_count = underscore_count
        else:
            underscore_count = 0
    if max_underscore_count >= 15:
        res["error_status"] = True
        res["error_reason"] = "下划线长度大于15"
    return res

def common_url_only(content: str) -> dict:
    """check whether content is all urls"""
    res = {'error_status': False, 'error_reason': ''}
    if len(content.strip()) == 0:
        return res

    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'  # noqa
    s = re.sub(pattern, '', content)
    count = len(s.strip())
    if count == 0:
        res["error_status"] = True
        res['error_reason'] = '内容只有url'
    return res

def common_word_stuck(content: str) -> dict:
    """check whether words are stuck"""
    res = {'error_status': False, 'error_reason': ''}
    words = re.findall(r'[a-zA-Z]+', content)
    max_word_len = 0
    for word in words:
        if len(word) > max_word_len:
            max_word_len = len(word)
    if max_word_len > 45:
        res["error_status"] = True
        res['error_reason'] = '英文单词黏连'
    return res