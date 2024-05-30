# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-helper
# FileName:     libs.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/05/26
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import time
import logging
import typing as t
from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException

logger = logging.getLogger("root")


class EnumMetaClass(Enum):

    @classmethod
    def values(cls) -> list:
        return [x.value for x in cls]

    @classmethod
    def keys(cls) -> list:
        return [x.name for x in cls]

    @classmethod
    def get(cls, key: str) -> t.Any:
        if key.upper() in cls.keys():
            return getattr(cls, key.upper()).value
        elif key.lower() in cls.keys():
            return getattr(cls, key.lower()).value
        else:
            return None

    @classmethod
    def items(cls) -> t.List:
        return [(x.name, x.value) for x in cls]


class Locator(EnumMetaClass):
    id = By.ID
    name = By.NAME
    xpath = By.XPATH
    tag_name = By.TAG_NAME
    link_text = By.LINK_TEXT
    class_name = By.CLASS_NAME
    css_selector = By.CSS_SELECTOR
    partial_link_text = By.PARTIAL_LINK_TEXT


def is_exist_element(driver: webdriver, locator: str, regx: str, loop: int, sleep: float,
                     is_ignore: bool = True, is_log_output: bool = True) -> bool:
    is_exist = False
    for i in range(loop):
        try:
            # 根据实际情况定位按钮元素
            element = driver.find_element(Locator.get(locator), regx)
            if element:
                is_exist = True
                break
        except (NoSuchElementException,):
            if is_log_output is True:
                logger.error("Element Not Found")
            if is_ignore is False:
                raise NoSuchElementException()
        except (TimeoutException,):
            if is_log_output is True:
                logger.error("Element found timeout")
            if is_ignore is False:
                raise TimeoutException()
            pass
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，判断元素是否存在失败".format(locator, regx)
            e_slice = str(e).split("Message:")
            if e_slice[0]:
                err_str = err_str + "，error: {}".format(e_slice[0])
            if is_log_output is True:
                logger.error(err_str)
            if is_ignore is False:
                raise OverflowError("Element found failed, reason: {}".format(err_str))
        if sleep > 0:
            time.sleep(sleep)
    return is_exist


def get_element(driver: webdriver, locator: str, regx: str, loop: int, sleep: float, **kwargs) -> WebElement:
    element = None
    is_ignore = kwargs.get("is_ignore", True)
    is_log_output = kwargs.get("is_log_output", True)
    for i in range(loop):
        try:
            # 根据实际情况定位按钮元素
            element = driver.find_element(Locator.get(locator), regx)
            if element:
                return element
        except (NoSuchElementException,):
            if is_log_output is True:
                logger.error("Element Not Found")
            if is_ignore is False:
                raise NoSuchElementException()
        except (TimeoutException,):
            if is_log_output is True:
                logger.error("Element found timeout")
            if is_ignore is False:
                raise TimeoutException()
            pass
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，获取元素失败".format(locator, regx)
            e_slice = str(e).split("Message:")
            if e_slice[0]:
                err_str = err_str + "，error: {}".format(e_slice[0])
            if is_log_output is True:
                logger.error(err_str)
            if is_ignore is False:
                raise OverflowError("Element found failed, reason: {}".format(err_str))
        if sleep > 0:
            time.sleep(sleep)
    return element
