# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-helper
# FileName:     desktop_ui.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/05/29
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import time
from decimal import Decimal
from selenium import webdriver
from ctrip_helper.libs import logger
from ctrip_helper.config import url_map
from selenium.webdriver.common.keys import Keys
from ctrip_helper.libs import get_element, EnumMetaClass


class UILocatorRegx(EnumMetaClass):
    all_orders_select_box = {"locator": "xpath",
                             "regx": '//ul[@class="fix_myctrip_order_layer"]//div[@class="select-box"]'},
    order_id_input_box = {"locator": "xpath", "regx": '//div[@class="order_inquiry"]//input[@id="searchBookingNum"]'},
    order_query_button = {"locator": "xpath", "regx": '//div[@class="order_inquiry"]//button[@class="btn_sel"]'}
    order_status_with_list = {"locator": "xpath",
                              "regx": '//ul[@class="t_body"]//span[@class="order-price-status-title"]'}
    order_price = {"locator": "xpath", "regx": '//li[@class="item"]//div[@class="order-price-detail"]'}
    order_to_payment = {"locator": "xpath", "regx": '//div[@id="button-group"]//a[@data-ubt-v="主订单支付"]'}
    order_payment_amount = {"locator": "xpath", "regx": '//div[@class="m-order-amount"]//div[@class="m-order-money"]'}
    wallet_balance = {"locator": "xpath", "regx": '//div[@class="walelt-card"]//div[contains(@class, "crdlast")]'}
    use_wallet = {"locator": "xpath", "regx": '//div[@class="walelt-card"]//input[@class="am-switch-checkbox"]'}
    wallet_immediately_payment = {"locator": "xpath",
                                  "regx": '//div[@class="wallet_pay_button"]//button[@type="gradient"]'}
    use_yeepay2b_pyament = {"locator": "xpath",
                            "regx": '//div[@class="pay_way_container"]//div[contains(text(), "易宝会员支付")]'}
    yeepay2b_immediately_payment = {"locator": "xpath",
                                    "regx": '//div[@class="pay_btn_container"]//div[@class="trip-pay-btn-text"]'}
    password_pop_box = {"locator": "xpath", "regx": '//div[@class="trip-pay-drawer-header-title"]'}
    first_password_input_box = {"locator": "xpath",
                                "regx": '//div[@class="verify-password-box"]//div[@class="inputBox"]//div[1]'}
    yeepay2b_accout_input_box = {"locator": "xpath",
                                 "regx": '//div[@class="account-pay-main"]//input[@name="userAccount"]'}
    yeepay2b_password_input_box = {"locator": "xpath",
                                   "regx": '//div[@class="account-pay-main"]//input[@name="tradePassword"]'}
    yeepay2b_payment_next_button = {"locator": "xpath",
                                    "regx": '//div[@class="account-pay-main"]//button[@id="passPayButton"]'}


class SeleniumApi(object):

    @classmethod
    def open_order_query_home_with_flight(cls, driver: webdriver, sleep: float = 0) -> None:
        driver.get(url_map.get_url('order_query_home_with_flight'))
        if sleep > 0:
            time.sleep(sleep)
        logger.info("打开机票订单查询首页")

    @classmethod
    def click_more_filter_conditions(cls, driver: webdriver, loop: int = 1, sleep: float = 0) -> bool:
        more_filter_expand = get_element(
            driver=driver, locator=UILocatorRegx.get("all_orders_select_box").get("locator"),
            regx=UILocatorRegx.get("all_orders_select_box").get("regx"), loop=loop, sleep=sleep
        )
        if more_filter_expand:
            more_filter_expand.click()
            logger.info("选择【更多筛选条件】，展开条件列表")
            return True
        else:
            return False

    @classmethod
    def enter_order_id(cls, driver: webdriver, order_id: str, loop: int = 1, sleep: float = 0) -> bool:
        input_box = get_element(
            driver=driver, locator=UILocatorRegx.order_id_input_box.get("locator"),
            regx=UILocatorRegx.order_id_input_box.get("regx"), loop=loop, sleep=sleep
        )
        if input_box:
            # 模拟键盘操作清空输入框内容
            input_box.send_keys(Keys.CONTROL + "a")  # 选中输入框中的所有内容
            input_box.send_keys(Keys.BACKSPACE)  # 删除选中的内容
            input_box.send_keys('{}'.format(order_id))
            logger.info("输入查询订单号：{}".format(order_id))
            return True
        else:
            return False

    @classmethod
    def click_order_query(cls, driver: webdriver, loop: int = 1, sleep: float = 0) -> bool:
        order_query_button = get_element(
            driver=driver, locator=UILocatorRegx.order_query_button.get("locator"),
            regx=UILocatorRegx.order_query_button.get("regx"), loop=loop, sleep=sleep
        )
        if order_query_button:
            order_query_button.click()
            logger.info("点击【查询】按钮")
            return True
        else:
            return False

    @classmethod
    def get_order_status(cls, driver: webdriver, loop: int = 1, sleep: float = 0) -> str:
        order_status = ""
        order_status_element = get_element(
            driver=driver, locator=UILocatorRegx.order_status_with_list.get("locator"),
            regx=UILocatorRegx.order_status_with_list.get("regx"), loop=loop, sleep=sleep
        )
        if order_status_element:
            order_status = order_status_element.text.strip()
            logger.info("获取订单的状态为：{}".format(order_status))
        return order_status

    @classmethod
    def click_order_price(cls, driver: webdriver, loop: int = 1, sleep: float = 0) -> bool:
        order_price_element = get_element(
            driver=driver, locator=UILocatorRegx.order_price.get("locator"),
            regx=UILocatorRegx.order_price.get("regx"), loop=loop, sleep=sleep
        )
        if order_price_element:
            order_price_element.click()
            logger.info("点击订单价格，进入订单详情界面")
            return True
        else:
            return False

    @classmethod
    def click_to_payment(cls, driver: webdriver, order_id: str, loop: int = 1, sleep: float = 0) -> bool:
        current_url = driver.current_url
        local_url = "{}?oid={}".format(url_map.get("flight_order_details"), order_id)
        if current_url.startswith(local_url) is True:
            to_payment_button = get_element(
                driver=driver, locator=UILocatorRegx.order_price.get("locator"),
                regx=UILocatorRegx.order_price.get("regx"), loop=loop, sleep=sleep
            )
            if to_payment_button:
                to_payment_button.click()
                logger.info("点击【去支付】，进入订单支付界面")
                return True
            else:
                return False
        else:
            logger.warn("当前订单详情页面: {}，不是本次要支付的订单: {} 的详情页".format(current_url, order_id))
            return False

    @classmethod
    def get_order_amount(cls, driver: webdriver, loop: int = 1, sleep: float = 0) -> Decimal:
        order_payment_amount = "0.00"
        current_url = driver.current_url
        if current_url.startswith(url_map.get("safe_payment_home")) is True:
            order_payment_amount_element = get_element(
                driver=driver, locator=UILocatorRegx.order_payment_amount.get("locator"),
                regx=UILocatorRegx.order_payment_amount.get("regx"), loop=loop, sleep=sleep
            )
            if order_payment_amount_element:
                order_payment_amount = order_payment_amount_element.text.strip()
                logger.info("获取订单的支付金额为：{}".format(order_payment_amount))
        else:
            logger.warning("当前的界面：{} 不是订单安全支付界面".format(current_url))
        return Decimal(order_payment_amount)

    @classmethod
    def get_wallet_balance(cls, driver: webdriver, loop: int = 1, sleep: float = 0) -> Decimal:
        wallet_balance = "0.00"
        wallet_balance_element = get_element(
            driver=driver, locator=UILocatorRegx.wallet_balance.get("locator"),
            regx=UILocatorRegx.wallet_balance.get("regx"), loop=loop, sleep=sleep
        )
        if wallet_balance_element:
            text = wallet_balance_element.text.strip()
            logger.info("获取账号礼品卡{}".format(text))
            wallet_balance = text.split("¥")[-1]
        return Decimal(wallet_balance)

    @classmethod
    def click_use_wallet(cls, driver: webdriver, loop: int = 1, sleep: float = 0) -> bool:
        use_wallet_switch = get_element(
            driver=driver, locator=UILocatorRegx.use_wallet.get("locator"),
            regx=UILocatorRegx.use_wallet.get("regx"), loop=loop, sleep=sleep
        )
        if use_wallet_switch:
            use_wallet_switch.click()
            logger.info("选择使用钱包支付")
            return True
        else:
            return False

    @classmethod
    def click_wallet_immediately_payment(cls, driver: webdriver, loop: int = 1, sleep: float = 0) -> bool:
        immediately_payment_button = get_element(
            driver=driver, locator=UILocatorRegx.wallet_immediately_payment.get("locator"),
            regx=UILocatorRegx.use_wallet.get("regx"), loop=loop, sleep=sleep
        )
        if immediately_payment_button:
            immediately_payment_button.click()
            logger.info("点击钱包【立即支付】")
            return True
        else:
            return False

    @classmethod
    def click_use_yeepay2b(cls, driver: webdriver, loop: int = 1, sleep: float = 0) -> bool:
        use_yeepay2b_switch = get_element(
            driver=driver, locator=UILocatorRegx.use_yeepay2b_pyament.get("locator"),
            regx=UILocatorRegx.use_yeepay2b_pyament.get("regx"), loop=loop, sleep=sleep
        )
        if use_yeepay2b_switch:
            use_yeepay2b_switch.click()
            logger.info("选择使用易宝会员支付")
            return True
        else:
            return False

    @classmethod
    def click_yeepay2b_immediately_payment(cls, driver: webdriver, loop: int = 1, sleep: float = 0) -> bool:
        immediately_payment_button = get_element(
            driver=driver, locator=UILocatorRegx.yeepay2b_immediately_payment.get("locator"),
            regx=UILocatorRegx.yeepay2b_immediately_payment.get("regx"), loop=loop, sleep=sleep
        )
        if immediately_payment_button:
            immediately_payment_button.click()
            logger.info("点击钱包【易宝支付】")
            return True
        else:
            return False

    @classmethod
    def enter_payment_password(cls, driver: webdriver, password: str, loop: int = 1, sleep: float = 0) -> bool:
        is_exist_pop_box = get_element(
            driver=driver, locator=UILocatorRegx.password_pop_box.get("locator"),
            regx=UILocatorRegx.password_pop_box.get("regx"), sleep=sleep, loop=loop
        )
        if is_exist_pop_box:
            first_password_inout_box = get_element(
                driver=driver, locator=UILocatorRegx.first_password_input_box.get("locator"),
                regx=UILocatorRegx.first_password_input_box.get("regx"), sleep=sleep, loop=loop
            )
            if first_password_inout_box:
                if not isinstance(password, str):
                    password = str(password)
                first_password_inout_box.click()
                for i in password:
                    driver.send_keys(i)
                    # 可选：添加一个短暂的延迟，模拟更接近人类的输入速度
                    time.sleep(0.5)
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def enter_yeepay2b_account(cls, driver: webdriver, account: str, loop: int = 1, sleep: float = 0) -> bool:
        current_url = driver.current_url
        if current_url.startswith(url_map.get("yeepay2b_cash_desk")) is True:
            input_box = get_element(
                driver=driver, locator=UILocatorRegx.yeepay2b_accout_input_box.get("locator"),
                regx=UILocatorRegx.yeepay2b_accout_input_box.get("regx"), loop=loop, sleep=sleep
            )
            if input_box:
                # 模拟键盘操作清空输入框内容
                input_box.send_keys(Keys.CONTROL + "a")  # 选中输入框中的所有内容
                input_box.send_keys(Keys.BACKSPACE)  # 删除选中的内容
                input_box.send_keys('{}'.format(account))
                logger.info("输入的易宝会员账号：{}".format(account))
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def enter_yeepay2b_password(cls, driver: webdriver, password: str, loop: int = 1, sleep: float = 0) -> bool:
        input_box = get_element(
            driver=driver, locator=UILocatorRegx.yeepay2b_password_input_box.get("locator"),
            regx=UILocatorRegx.yeepay2b_password_input_box.get("regx"), loop=loop, sleep=sleep
        )
        if input_box:
            # 模拟键盘操作清空输入框内容
            input_box.send_keys(Keys.CONTROL + "a")  # 选中输入框中的所有内容
            input_box.send_keys(Keys.BACKSPACE)  # 删除选中的内容
            input_box.send_keys('{}'.format(password))
            logger.info("输入的易宝会员账号密码：{}".format(password))
            return True
        else:
            return False

    @classmethod
    def click_yeepay2b_payment_next(cls, driver: webdriver, loop: int = 1, sleep: float = 0) -> bool:
        next_button = get_element(
            driver=driver, locator=UILocatorRegx.yeepay2b_payment_next_button.get("locator"),
            regx=UILocatorRegx.yeepay2b_payment_next_button.get("regx"), loop=loop, sleep=sleep
        )
        if next_button:
            next_button.click()
            logger.info("易宝支付收银台界面点击【下一步】")
            return True
        else:
            return False
