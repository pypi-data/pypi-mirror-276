# lanQ v1.2

English | [简体中文](README_ZH.md)

Language quality evaluation tool.

## Run it

Clone the project into your environment.

```
git clone ssh://git@gitlab.pjlab.org.cn:1122/qa/lanq.git
```

Install the requirement packages.

```
pip install -r requirements.txt
```

Add the test data file `test_data.json` into `data/predictions` directory.  
Then execute `main.py` with parameter `-i`.

```
python main.py -i test_data.json
```

You will get the result file `data_predictions_test_data.json` in `data/results`.

If you want to test files in directory, you just need to change to file name to directory name in `data/predictions`, such as:

```
python main.py -i directory_name
```

## Data format

There are 2 data format supported.  
One is model type, contain `id`, `prompt` and `prediction` keys, as follows:  

```
{"id": "0", "prompt": "how old are you?", "prediction": "I am 8 years old."}
```

Another is data type, have `id` and `content` keys, such as:

```
{"id":"Bl1b6P41SlcCHv8gfhLy","content":"秦始皇嬴政，从此结束了贵族王侯专政的王国时代，进入了君主专制的帝国时代。"}
```

No matter what data format is, each line of data is `json` type and each data file only has one format data.   
Besides, data exits in data file with `jsonline` style, refering to `test_data1.json` or `test_data2.json`.

## Reading result

The file in `data/results` directory has format as follows:

```
{
    "score": 50.0,
    "num_good": 1,
    "num_bad": 1,
    "total": 2,
    "ERROR_RULE_COLON_END": {
        "count": 1,
        "ratio": 0.5,
        "detail": [
            {
                "id": "0",
                "error_reason": "冒号结尾"
            }
        ]
    },
}
```

key name | description
-|-
`score` | `num_good` / `total`, means the quality of data.  
`num_good` | the count of good data.  
`num_bad` | the count of bad data, which has some error.  
`total` | the count of all data.  
`ERROR_RULE_COLON_END` | the error name.  
`count` | the number of error appearance.    
`ratio` | `count` / `total`, means the ratio of error appearance.  
`detail` | the information of error.  
`id` | the data id with error.  
`error_reason` | the reason why judge the data has error. 

## How to Use

First, you should install the package.

```
pip install lanQ
```

After installing the tool in python environment, wo can import it in our project as follows.

```
from lanQ_rule import common_rule
```

At this time, we can use all functions in `common_rule.py`. The parameter `content` is must `string` type, such as:

```
common_bracket_unmatch(content)
```

We will get a result, which is a json type and has a key `error_status`.  
If `error_status` is `True`, which means content has problem, the result will have other 2 keys: `error_type` and `error_reason`, for example:  

```
{
   'error_status': True, 
   'error_type': 'ERROR_RULE_COLON_END', 
   'error_reason': '冒号结尾'
}
```

## Upload 

Update the version number in `setup.py`

```
setup(
    name="lanQ",
    version="x.y",
    ...
)
```

Make a .tar file for using in other project. 
You will get a .tar file in `lanQ/dist/`

```
python setup.py sdist
```

Upload the .tar file to Internet.

```
twine upload dist/lanQ-x.y.tar.gz
```

## Summary of Quality Functions

The Category in below table is the same name `.py` file in `lanQ/lanQ_rule/` path.  
Function's name are arranged in alphabetical order.

### Effectiveness
- Ratio of data items of null data values in the dataset.  
- Ratio of data items containing garbled characters in the dataset.

Function Name | Error Rule | Description                                             | Category 
-|-|---------------------------------------------------------|----------
common_chaos_en | ERROR_CHAOS_EN| 检查文本中是否包含英文乱码            | common   
common_chaos_symbol  |ERROR_CHAOS_SYMBOL| 检查文本内是否有大量非正文内容    | common   
common_chaos_zh | ERROR_CHAOS_ZH| 检查文本中是否包含中文乱码             | common   
common_content_null  | ERROR_CONTENT_NULL | 检查文本内容是否为空 | common   
common_invalid_web| ERROR_INVALID_WEB | 检查文本内容是否为404信息 | common
common_language_mixed| ERROR_LANGUAGE_MIXED | 检查文本内是否含中英文混杂   | common
common_url_only | ERROR_URL_ONLY| 检查文本内是否只有URL  | common
prompt_chinese_produce_english | ERROR_CHINESE_PRODUCE_ENGLISH| 检查中文promt生成英文prediction | prompt  
prompt_english_produce_chinese | ERROR_ENGLISH_PRODUCE_CHINESE| 检查英文promt生成中文prediction | prompt

### Completeness
- Ratio of data items in the dataset that contain incomplete content (such as ending with a colon).  
- Ratio of data items in the dataset where paired content does not appear in pairs (such as parentheses).

Function Name | Error Rule | Description                                             | Category 
-|-|---------------------------------------------------------|----------
common_bracket_unmatch | ERROR_BRACKET_UNMATCH| 检查开闭括号数量是否一致                        | common
common_colon_end | ERROR_RULE_COLON_END| 检查文本最后一个字符是冒号                      | common

### Understandability
- Ratio of data items in the dataset that contain errors in formatting (such as formulas, tables, markdown, etc.).  
- Ratio of data items in the dataset that contain special characters (such as high proportion of spaces, line breaks, #, invisible characters).

Function Name | Error Rule | Description                                             | Category 
-|-|---------------------------------------------------------|----------
common_check_photo | ERROR_CHECK_PHOTO| 检查是否包含图片 | common
common_ellipsis_ratio  | ERROR_ELLIPSIS_RATIO  |  检查省略号结尾行占比是否大于75% | common
common_enter_more  | ERROR_ENTER_MORE| 检查文本内是否有连续大于8个的回车 | common  
common_enter_ratio_more | ERROR_ENTER_RATIO_MORE | 检查文本内内是否有超过25%正文占比的回车 | common
common_space_more| ERROR_SPACE_MORE | 检查content内是否有连续500个以上的空格 | common
model_watermark | ERROR_WATERMARK| 检查文本内是否有水印 | model    

### Similarity
- Ratio of data items in the dataset that contain duplicate content.
- Ratio of duplicate data items in the dataset.

Function Name | Error Rule | Description                                             | Category 
-|-|---------------------------------------------------------|----------
common_doc_repeat | ERROR_DOC_REPEAT | 检查文本内是否连续重复                         | common
common_underscore_length | ERROR_UNDERSCORE_LENGTH| 检查文本内是包含长度大于15的下划线 | common

### Fluency
- Ratio of data items in the dataset that contain large blocks of text without punctuation.
- Ratio of data items in the dataset that contain anti-scraping content.

Function Name | Error Rule | Description                                             | Category 
-|-|---------------------------------------------------------|----------
common_anti_crawler_zh | ERROR_CRAWL_ANTI | 检查文本中是否包含反爬文本 |  common  
common_no_punc | ERROR_NO_PUNC | 检查文本内是否有大段无标点 | common
common_word_stuck | ERROR_WORD_STUCK| 检查文本内是否有英文单词黏连 | common

### Relevance
- Ratio of data items in the dataset that contain leading or trailing off-topic/unrelated content (such as advertisements, copyright notices, references from web pages).

Function Name | Error Rule | Description                                             | Category 
-|-|---------------------------------------------------------|----------
common_emoj_characters | ERROR_EMOJ_CHAR| 检查是否包含emoji符号 | common
common_html_entity| ERROR_HTML_ENTITY | 检查实体标记 | common 
common_img_html_tag | ERROR_IMG_HTML_TAG| 检查文本是否含有图片或html标签 | common
common_invisible_char | ERROR_INVISIBLE_CHAR| 检查文本内是否包含不可见字符 | common 
common_joint_special_symbol  | ERROR_JOINT_SPECIAL_SYMBOL| 检查是否含有多个符号拼接组成的特殊符号 | common
common_special_character | ERROR_SPECIAL_CHARACTER | 检查是否含有特殊字符，如'�'      | common  
common_special_mark | ERROR_SPECIAL_MARK | 检查是否包含特殊标记 | common 
common_unconverted_symbol| ERROR_UNCONVERTED_SYMBOL | 检查是否包含转换失败的特殊符号 | common 
model_advertisement | ERROR_ADVERTISEMENT| 检查文本内是否有广告 | model

### Security
- Ratio of data items in the dataset that contain pornography content.
- Ratio of data items in the dataset that contain toxic content.

Function Name | Error Rule | Description                                             | Category 
-|-|---------------------------------------------------------|----------
common_license_key | ERROR_LICENSE_KEY| 检查文本内是否含许可证密钥 | common

## RoadMap
 - 1.6:
   - add benchmark for rules
 - 1.5:
   - add convert for different data type
 - 1.4:
   - add config of functions

## Release Notes
 - 1.3:
   - reorganize `config.py`, let user can configure
   - add error ratio
   - `main.py` and `convert` support input directory
 - 1.2:
   - add v1.2 rules
   - update `main.py` and `config` module, use callable type to organize functions
   - add convert folder, support stringline type
   - `readme` add usage and data type
 - 1.1:
   - add `base.py` contain base functions
   - sort functions by alphabetic order
 - 1.0:   
   - add 1.0 functions
   - add common_rule module
   - add model_rule module 
   - add prompt_rule module
   - add convert function
   - add `main.py`