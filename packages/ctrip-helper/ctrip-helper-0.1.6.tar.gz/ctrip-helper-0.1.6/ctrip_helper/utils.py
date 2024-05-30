# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-helper
# FileName:     utils.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/05/26
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import re
import json
import random
import hashlib
import urllib.parse
from datetime import datetime, timedelta

standard_date_format = "%Y-%m-%d %H:%M:%S"


def is_later_than_current_time(time_str: str, minutes: int = 5, current_dt: str = None):
    # 将给定的时间字符串转换为 datetime 对象
    given_time = datetime.strptime(time_str, '%H:%M').time()
    if current_dt is None:
        # 获取当前日期和时间
        current_datetime = datetime.now()
    else:
        current_datetime = datetime.strptime(current_dt, standard_date_format)
    current_time = current_datetime.time()
    # 如果给定时间跨越了当前日期，则调整为明天的时间
    if given_time < current_time:
        given_date = (current_datetime + timedelta(days=1)).date()
    else:
        given_date = current_datetime.date()
    # 合并给定时间的日期和当前日期的时间
    given_datetime = datetime.combine(given_date, given_time)
    # 计算给定时间与当前时间的差值
    time_difference = given_datetime - current_datetime
    # 判断差值是否大于 多少 分钟
    return time_difference.total_seconds() > minutes * 60


def encryp_md5(data: str) -> str:
    # 创建一个 hashlib.md5 对象
    md5_hash = hashlib.md5()
    # 将输入的字符串转换为 bytes，并更新 MD5 哈希对象
    md5_hash.update(data.encode('utf-8'))
    # 获取 MD5 值的十六进制表示形式（32 位小写）
    md5_hex_digest = md5_hash.hexdigest()
    return md5_hex_digest


def covert_dict_key_to_lower(d: dict) -> dict:
    result = dict()
    for key, value in d.items():
        if isinstance(key, str):
            key_new = key.lower()
            result[key_new] = value
    return result


def get_html_title(html: str) -> str:
    # 使用正则表达式提取目标字符串
    pattern = '<title>(.*?)</title>'
    match = re.search(pattern, html)
    if match:
        title = match.group(1)
    else:
        title = "Abnormal HTML document structure"
    return title


def gen_sign(departure_city_code: str, arrival_city_code: str, departure_date: str, transaction_id: str) -> str:
    """
    sign = md5(transactionID + 起始地大写三字码+ 降落的大写三字码 + 出发时间yyyy-MM-dd)
    :param departure_city_code:
    :param arrival_city_code:
    :param departure_date:
    :param transaction_id:
    :return:
    """
    return encryp_md5(
        data="{}{}{}{}".format(transaction_id, departure_city_code, arrival_city_code, departure_date)
    )


def generate_random_ipv6():
    # 生成8个四位的16进制数，并将它们组合成IPv6地址
    ipv6 = ':'.join('{:04x}'.format(random.randint(0, 0xffff)) for _ in range(8))
    return ipv6


def generate_random_ipv6_encode() -> str:
    # 生成8个四位的16进制数，并将它们组合成IPv6地址
    seq = to_url_str(data=":")
    ipv6 = seq.join('{:04x}'.format(random.randint(0, 0xffff)) for _ in range(8))
    return ipv6


def dict_to_jsonstr(data: dict) -> str:
    # 将消息体转换为JSON字符串
    body_json = json.dumps(data, ensure_ascii=False)
    # 将JSON字符串编码为字节
    # body_bytes = body_json.encode('utf-8')
    return body_json


def get_dict_lenth(data: dict) -> int:
    # 计算字节码的字节长度
    content_length = len(dict_to_jsonstr(data=data))
    return content_length


def to_url_str(data: str) -> str:
    # 对JSON字符串进行URL编码，确保所有特殊字符被正确编码。
    encoded_data = urllib.parse.quote(data)
    return encoded_data
