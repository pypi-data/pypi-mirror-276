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
from utils import get_current_datetime_int_str, join_path, get_image_dir, get_log_dir
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException

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


class Locator(Enum):
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
    locator = getattr(getattr(Locator, locator, object), "value", "")
    for i in range(loop):
        try:
            # 根据实际情况定位按钮元素
            element = driver.find_element(locator, regx)
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
    locator = getattr(getattr(Locator, locator, object), "value", "")
    for i in range(loop):
        try:
            # 根据实际情况定位按钮元素
            element = driver.find_element(locator, regx)
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


def click(element: WebElement, loop: int, sleep: float, **kwargs) -> bool:
    is_ignore = kwargs.get("is_ignore", True)
    is_log_output = kwargs.get("is_log_output", True)
    for _ in range(loop):
        try:
            element.click()
            return True
        except (ElementNotInteractableException,):
            if is_log_output is True:
                logger.error("Waiting for element to become interactive")
            if is_ignore is False:
                raise RuntimeError("Waiting for element to become interactive")
        except Exception as e:
            e_slice = str(e).split("Message:")
            if is_log_output is True:
                logger.error(e_slice[0])
            if is_ignore is False:
                raise OverflowError("Element click failed, reason: {}".format(e_slice[0]))
        if sleep > 0:
            time.sleep(sleep)
    return False


def send_keys(element: WebElement, value: str, loop: int, sleep: float, **kwargs) -> bool:
    is_ignore = kwargs.get("is_ignore", True)
    is_log_output = kwargs.get("is_log_output", True)
    for _ in range(loop):
        try:
            element.send_keys(value)
            return True
        except (ElementNotInteractableException,):
            if is_log_output is True:
                logger.error("Waiting for element to become interactive")
            if is_ignore is False:
                raise RuntimeError("Waiting for element to become interactive")
        except Exception as e:
            e_slice = str(e).split("Message:")
            if is_log_output is True:
                logger.error(e_slice[0])
            if is_ignore is False:
                raise OverflowError("Element click failed, reason: {}".format(e_slice[0]))
        if sleep > 0:
            time.sleep(sleep)
    return False


def switch_to_window(driver: webdriver, origin_windows: list, loop: int, sleep: float) -> bool:
    for i in range(loop):
        # 获取所有的窗口句柄
        all_windows = driver.window_handles
        diff = set(all_windows).difference(set(origin_windows))
        if len(diff) > 0:
            new_window = diff.pop()
            driver.switch_to.window(new_window)
            return True
        if sleep > 0:
            time.sleep(sleep)
    return False


def is_switch_latest_page(driver: webdriver, latest_page: str, loop: int = 1, sleep: float = 0) -> tuple:
    current_url = ""
    for _ in range(loop):
        current_url = driver.current_url
        if current_url.startswith(latest_page) is True:
            return True, current_url
        if sleep > 0:
            time.sleep(sleep)
    return False, current_url


def get_screenshot(driver: webdriver, file_name: str = None, **kwargs) -> tuple:
    """获取当前截屏"""
    is_ignore = kwargs.get("is_ignore", True)
    is_log_output = kwargs.get("is_log_output", True)
    screenshot_file_name, screenshot_file_suffix = None, None
    try:
        if file_name is None:
            screenshot_file_suffix = get_current_datetime_int_str()
            iname_file_name = "screenshot_{}.png".format(screenshot_file_suffix)
        else:
            iname_file_name = file_name
        image_path = get_image_dir()
        screenshot_file_name = join_path([image_path, iname_file_name])
        driver.save_screenshot(screenshot_file_name)
    except Exception as e:
        err_str = "获取当前页面截屏失败"
        e_slice = str(e).split("Message:")
        if len(e_slice) > 0:
            err_str = err_str + "，原因：{}".format(e_slice[0])
        if is_log_output is True:
            logger.error(err_str)
        if is_ignore is False:
            raise OverflowError(err_str)
    return screenshot_file_name, screenshot_file_suffix


def exception_html_save_to_txt(driver: webdriver, file_name: str = None, **kwargs):
    is_ignore = kwargs.get("is_ignore", True)
    is_log_output = kwargs.get("is_log_output", True)
    try:
        if file_name is None:
            exception_file_suffix = get_current_datetime_int_str()
            exception_file_name = "exception_{}.html".format(exception_file_suffix)
        else:
            exception_file_name = file_name
        log_path = get_log_dir()
        exception_file_path = join_path([log_path, exception_file_name])
        with open(exception_file_path, "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as e:
        err_str = "页面异常内容保存至文本文件出错"
        e_slice = str(e).split("Message:")
        if len(e_slice) > 0:
            err_str = err_str + "，原因：{}".format(e_slice[0])
        if is_log_output is True:
            logger.error(err_str)
        if is_ignore is False:
            raise OverflowError(err_str)
