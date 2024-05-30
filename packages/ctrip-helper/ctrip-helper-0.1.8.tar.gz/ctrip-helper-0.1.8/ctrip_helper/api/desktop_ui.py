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
import re
import time
from decimal import Decimal
from selenium import webdriver
from ctrip_helper.libs import logger
from ctrip_helper.config import url_map
from selenium.webdriver.common.keys import Keys
from ctrip_helper.libs import get_element, EnumMetaClass
from ctrip_helper.utils import is_later_than_current_time


class UILocatorRegx(EnumMetaClass):
    all_orders_select_box = {"locator": "xpath",
                             "regx": '//ul[@class="fix_myctrip_order_layer"]//div[@class="select-box"]'}
    order_id_input_box = {"locator": "xpath", "regx": '//div[@class="order_inquiry"]//input[@id="searchBookingNum"]'}
    order_query_button = {"locator": "xpath", "regx": '//div[@class="order_inquiry"]//button[@class="btn_sel"]'}
    order_status_with_list = {"locator": "xpath",
                              "regx": '//ul[@class="t_body"]//span[@class="order-price-status-title"]'}
    order_price = {"locator": "xpath", "regx": '//li[@class="item"]//div[@class="order-price-detail"]'}
    order_status_sub_title = {"locator": "xpath",
                              "regx": '//div[contains(@data-testid, "orderstatus_StatusSubTitleWrap")]'}
    order_status_booking_amount = {"locator": "xpath",
                                   "regx": '//div[@data-testid="fbu_PaymentWrapper"]//span[@data-testid="false"]'}
    order_to_payment = {"locator": "xpath", "regx": '//div[@id="button-group"]//a[@data-ubt-v="主订单支付"]'}
    order_to_cancel = {"locator": "xpath", "regx": '//div[@id="button-group"]//a[@data-ubt-v="取消订单"]'}
    order_continue_cancel = {"locator": "xpath", "regx": '//div[@class="ant-modal"]//div[@data-testid="继续取消"]'}
    order_cancel_got_it = {"locator": "xpath", "regx": '//div[@class="ant-modal"]//div[@data-testid="知道了"]'}
    order_payment_amount = {"locator": "xpath", "regx": '//div[@class="m-order-amount"]//div[@class="m-order-money"]'}
    wallet_disable = {"locator": "xpath", "regx": '//div[@class="walelt-card"]//div[@class="lin-crd-disabled"]'}
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
    is_login_button = {
        "locator": "xpath",
        "regx": '//div[@class="tl_nfes_home_header_login_wrapper_siwkn"]//button[contains(@aria-label, "我的账户")]'
    }
    is_login_span = {"locator": "xpath", "regx": '//div[@class="loginbar"]//span[@class="ctrip-username"]'}
    account_input = {"locator": "xpath",
                     "regx": '//div[@data-testid="accountPanel"]//input[@data-testid="accountNameInput"]'}
    password_input = {"locator": "xpath",
                      "regx": '//div[@data-testid="accountPanel"]//input[@data-testid="passwordInput"]'}
    service_agreement = {"locator": "xpath",
                         "regx": '//div[@data-testid="agreementList"]//label[@for="checkboxAgreementInput"]'}
    login_button = {"locator": "xpath", "regx": '//div[@data-testid="accountPanel"]//input[@data-testid="loginButton"]'}
    slider_verify = {"locator": "xpath", "regx": '//div[@data-testid="captcha"]/div'}


class SeleniumApi(object):

    @classmethod
    def is_login(cls, driver: webdriver, username: str, platform: str, loop: int = 1, sleep: float = 0,
                 **kwargs) -> bool:
        """是否已登录"""
        is_login_button = get_element(
            driver=driver, locator=UILocatorRegx.get("is_login_button").get("locator"),
            regx=UILocatorRegx.get("is_login_button").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if is_login_button:
            logger.info("{}平台用户<{}>已登录".format(platform, username))
            return True
        is_login_span = get_element(
            driver=driver, locator=UILocatorRegx.get("is_login_span").get("locator"),
            regx=UILocatorRegx.get("is_login_span").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if is_login_span:
            logger.info("{}平台用户<{}>已登录".format(platform, username))
            return True
        else:
            return False

    @classmethod
    def open_login_page(cls, driver: webdriver, sleep: float = 0) -> None:
        ctrip_login_prefix = url_map.get('ctrip_login_prefix')
        ctrip_login_suffix = url_map.get('ctrip_login_suffix')
        login_url = "{}{}".format(ctrip_login_prefix, ctrip_login_suffix)
        driver.get(login_url)
        if sleep > 0:
            time.sleep(sleep)
        logger.info("打开携程网页版登录页")

    @classmethod
    def enter_user_name(cls, driver: webdriver, username: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        input_box = get_element(
            driver=driver, locator=UILocatorRegx.get("account_input").get("locator"),
            regx=UILocatorRegx.get("account_input").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if input_box:
            # 模拟键盘操作清空输入框内容
            input_box.send_keys(Keys.CONTROL + "a")  # 选中输入框中的所有内容
            input_box.send_keys(Keys.BACKSPACE)  # 删除选中的内容
            input_box.send_keys('{}'.format(username))
            logger.info("输入登录账号：{}".format(username))
            return True
        else:
            return False

    @classmethod
    def enter_user_password(cls, driver: webdriver, password: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        input_box = get_element(
            driver=driver, locator=UILocatorRegx.get("password_input").get("locator"),
            regx=UILocatorRegx.get("password_input").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if input_box:
            # 模拟键盘操作清空输入框内容
            input_box.send_keys(Keys.CONTROL + "a")  # 选中输入框中的所有内容
            input_box.send_keys(Keys.BACKSPACE)  # 删除选中的内容
            input_box.send_keys('{}'.format(password))
            logger.info("输入登录密码：{}".format(password))
            return True
        else:
            return False

    @classmethod
    def click_service_agreement(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        checkbox = get_element(
            driver=driver, locator=UILocatorRegx.get("service_agreement").get("locator"),
            regx=UILocatorRegx.get("service_agreement").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if checkbox:
            checkbox.click()
            logger.info("选中【阅读并同意携程的服务协议和个人信息保护政策】")
            return True
        else:
            return False

    @classmethod
    def click_login(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        login_button = get_element(
            driver=driver, locator=UILocatorRegx.get("login_button").get("locator"),
            regx=UILocatorRegx.get("login_button").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if login_button:
            login_button.click()
            logger.info("点击登录页面的【登录】按钮")
            return True
        else:
            return False

    @classmethod
    def is_exist_slider_verify(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        current_url = driver.current_url
        slider_verify = get_element(
            driver=driver, locator=UILocatorRegx.get("slider_verify").get("locator"),
            regx=UILocatorRegx.get("slider_verify").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if slider_verify:
            logger.info("当前页面：{} 出现了滑块验证码".format(current_url))
            return True
        else:
            return False

    @classmethod
    def open_order_query_home_with_flight(cls, driver: webdriver, sleep: float = 0) -> None:
        driver.get(url_map.get('order_query_home_with_flight'))
        if sleep > 0:
            time.sleep(sleep)
        logger.info("打开机票订单查询首页")

    @classmethod
    def click_more_filter_conditions(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        more_filter_expand = get_element(
            driver=driver, locator=UILocatorRegx.get("all_orders_select_box").get("locator"),
            regx=UILocatorRegx.get("all_orders_select_box").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if more_filter_expand:
            more_filter_expand.click()
            logger.info("选择【更多筛选条件】，展开条件列表")
            return True
        else:
            return False

    @classmethod
    def enter_order_id(cls, driver: webdriver, order_id: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        input_box = get_element(
            driver=driver, locator=UILocatorRegx.get("order_id_input_box").get("locator"),
            regx=UILocatorRegx.get("order_id_input_box").get("regx"), loop=loop, sleep=sleep, **kwargs
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
    def click_order_query(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        order_query_button = get_element(
            driver=driver, locator=UILocatorRegx.get("order_query_button").get("locator"),
            regx=UILocatorRegx.get("order_query_button").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if order_query_button:
            order_query_button.click()
            logger.info("点击【查询】按钮")
            return True
        else:
            return False

    @classmethod
    def get_order_status(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> str:
        order_status = ""
        order_status_element = get_element(
            driver=driver, locator=UILocatorRegx.get("order_status_with_list").get("locator"),
            regx=UILocatorRegx.get("order_status_with_list").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if order_status_element:
            order_status = order_status_element.text.strip()
            logger.info("获取订单的状态为：{}".format(order_status))
        return order_status

    @classmethod
    def get_order_amonut_with_query_list(cls, driver: webdriver, order_id: str, loop: int = 1,
                                         sleep: float = 0, **kwargs) -> Decimal:
        order_amonut = "0.00"
        order_amonut_element = get_element(
            driver=driver, locator=UILocatorRegx.get("order_price").get("locator"),
            regx=UILocatorRegx.get("order_price").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if order_amonut_element:
            text = order_amonut_element.text.strip()
            logger.info("从查询列表中获取订单: {} 的金额：{}".format(order_id, text))
            order_amonut = text.split("¥")[-1]
        return Decimal(order_amonut)

    @classmethod
    def click_order_amonut_with_query_list(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        order_amonut_element = get_element(
            driver=driver, locator=UILocatorRegx.get("order_price").get("locator"),
            regx=UILocatorRegx.get("order_price").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if order_amonut_element:
            order_amonut_element.click()
            logger.info("点击订单金额，进入订单详情界面")
            return True
        else:
            return False

    @classmethod
    def click_to_payment(cls, driver: webdriver, order_id: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        current_url = driver.current_url
        local_url = "{}?oid={}".format(url_map.get("flight_order_details"), order_id)
        if current_url.startswith(local_url) is True:
            to_payment_button = get_element(
                driver=driver, locator=UILocatorRegx.get("order_price").get("locator"),
                regx=UILocatorRegx.get("order_price").get("regx"), loop=loop, sleep=sleep, **kwargs
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
    def click_order_cancel(cls, driver: webdriver, order_id: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        current_url = driver.current_url
        local_url = "{}?oid={}".format(url_map.get("flight_order_details"), order_id)
        if current_url.startswith(local_url) is True:
            order_cancel_button = get_element(
                driver=driver, locator=UILocatorRegx.get("order_to_cancel").get("locator"),
                regx=UILocatorRegx.get("order_to_cancel").get("regx"), loop=loop, sleep=sleep, **kwargs
            )
            if order_cancel_button:
                order_cancel_button.click()
                logger.info("点击【取消订单】，接下来会出现【取消提示】小弹框")
                return True
            else:
                return False
        else:
            logger.warn("当前订单详情页面: {}，不是本次要支付的订单: {} 的详情页".format(current_url, order_id))
            return False

    @classmethod
    def click_order_continue_cancel(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        continue_cance_button = get_element(
            driver=driver, locator=UILocatorRegx.get("order_continue_cancel").get("locator"),
            regx=UILocatorRegx.get("order_continue_cancel").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if continue_cance_button:
            continue_cance_button.click()
            logger.info("点击【继续取消】，接下来会出现【知道了】小弹框")
            return True
        else:
            return False

    @classmethod
    def is_order_cancel_success(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        got_it_button = get_element(
            driver=driver, locator=UILocatorRegx.get("order_cancel_got_it.value").get("locator"),
            regx=UILocatorRegx.get("order_cancel_got_it").get("regx"), sleep=sleep, loop=loop, **kwargs
        )
        if got_it_button:
            return True
        else:
            return False

    @classmethod
    def get_order_amount_with_safe_payment_home(cls, driver: webdriver, loop: int = 1, sleep: float = 0,
                                                **kwargs) -> Decimal:
        order_payment_amount = "0.00"
        current_url = driver.current_url
        if current_url.startswith(url_map.get("safe_payment_home")) is True:
            order_payment_amount_element = get_element(
                driver=driver, locator=UILocatorRegx.get("order_payment_amount").get("locator"),
                regx=UILocatorRegx.get("order_payment_amount").get("regx"), loop=loop, sleep=sleep, **kwargs
            )
            if order_payment_amount_element:
                order_payment_amount = order_payment_amount_element.text.strip()
                logger.info("获取订单的支付金额为：{}".format(order_payment_amount))
        else:
            logger.warning("当前的界面：{} 不是订单安全支付界面".format(current_url))
        return Decimal(order_payment_amount)

    @classmethod
    def is_cancel_order(cls, driver: webdriver, out_total_amount: str, amount_loss_limit: str, profit_cap: str,
                        passenger_number: int, platform: str, loop: int = 1, sleep: float = 0,
                        discount_amount: str = None, **kwargs) -> tuple:
        """在订单详情页，判断是否需要取消订单"""
        flag = False
        remark = ""
        status_sub_title_element = get_element(
            driver=driver, locator=UILocatorRegx.get("order_status_sub_title").get("locator"),
            regx=UILocatorRegx.get("order_status_sub_title").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        booking_amount_element = get_element(
            driver=driver, locator=UILocatorRegx.get("order_status_booking_amount").get("locator"),
            regx=UILocatorRegx.get("order_status_booking_amount").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if booking_amount_element:
            booking_amount_text = booking_amount_element.text.strip()
            # 使用 findall 获取所有匹配项
            amount_match = re.search(r"¥(\d+)", booking_amount_text)
            if amount_match:
                amount_str = amount_match.group(1)
                logger.warning("从{}订单获取的支付金额：{}，劲旅订单总价：{}".format(
                    platform, amount_str, out_total_amount
                ))
                # 预期订单利润
                ex_order_profit = Decimal(out_total_amount) - Decimal(amount_str)
                if discount_amount:
                    # 实际订单利润
                    ac_order_profit = ex_order_profit + Decimal(discount_amount)
                else:
                    ac_order_profit = ex_order_profit
                # 订单利润 < 0, 存在亏钱，与亏钱的下限进行比较
                if ac_order_profit < 0:
                    total = Decimal(amount_loss_limit) * passenger_number
                    if ac_order_profit + total < 0:
                        flag = True
                        remark = "订单亏钱{:.2f}太多，超过订单总下限值{}(单人下限{} * {}人)".format(
                            abs(ac_order_profit), total, amount_loss_limit, passenger_number
                        )
                        logger.warning(remark)
                        return flag, remark
                # 订单利润 >= 0, 存在毛利，与利润的上限进行比较
                else:
                    total = Decimal(profit_cap) * passenger_number
                    if ac_order_profit - total > 0:
                        flag = True
                        remark = "订单利润{:.2f}太高，超过订单总下限值{}(单人下限{} * {}人)".format(
                            ac_order_profit, total, profit_cap, passenger_number
                        )
                        logger.warning(remark)
                        return flag, remark
            else:
                remark = "从订单详情页面获取订单过期时间和订单金额有异常"
                logger.warning(remark)
        else:
            remark = "订单详情页面中未找到订单金额元素"
            logger.warning(remark)
        if status_sub_title_element:
            sub_title_text = status_sub_title_element.text.strip()
            # 使用 findall 获取所有匹配项
            time_match = re.search(r"(\d{2}:\d{2})", sub_title_text)
            if time_match:
                time_str = time_match.group(1)
                logger.info("从订单获取到的过期时间为：{}".format(time_str))
                minutes = 1
                is_later = is_later_than_current_time(time_str=time_str, minutes=minutes)
                if is_later is False:
                    flag = True
                    remark = "支付时间少于{}分钟".format(minutes)
                    logger.warning(remark)
                    return flag, remark
            else:
                remark = "从文案<{}>中没有获取订单过期时间".format(sub_title_text)
        else:
            remark = "从订单详情页面中未找到订单过期时间元素"
        logger.warning(remark)
        return flag, remark

    @classmethod
    def is_wallet_disable(cls, driver: webdriver, order_id: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        wallet_disable_element = get_element(
            driver=driver, locator=UILocatorRegx.get("wallet_disable").get("locator"),
            regx=UILocatorRegx.get("wallet_disable").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if wallet_disable_element:
            logger.warning("当前订单: {} 钱包不可用，需要切换至其他支付方式".format(order_id))
            return True
        else:
            return False

    @classmethod
    def get_wallet_balance(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> Decimal:
        wallet_balance = "0.00"
        wallet_balance_element = get_element(
            driver=driver, locator=UILocatorRegx.get("wallet_balance").get("locator"),
            regx=UILocatorRegx.get("wallet_balance").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if wallet_balance_element:
            text = wallet_balance_element.text.strip()
            logger.info("获取账号礼品卡{}".format(text))
            wallet_balance = text.split("¥")[-1]
        return Decimal(wallet_balance)

    @classmethod
    def click_use_wallet(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        use_wallet_switch = get_element(
            driver=driver, locator=UILocatorRegx.get("use_wallet").get("locator"),
            regx=UILocatorRegx.get("use_wallet").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if use_wallet_switch:
            use_wallet_switch.click()
            logger.info("选择使用钱包支付")
            return True
        else:
            return False

    @classmethod
    def click_wallet_immediately_payment(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        immediately_payment_button = get_element(
            driver=driver, locator=UILocatorRegx.get("wallet_immediately_payment").get("locator"),
            regx=UILocatorRegx.get("use_wallet").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if immediately_payment_button:
            immediately_payment_button.click()
            logger.info("点击钱包【立即支付】")
            return True
        else:
            return False

    @classmethod
    def click_use_yeepay2b(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        use_yeepay2b_switch = get_element(
            driver=driver, locator=UILocatorRegx.get("use_yeepay2b_pyament").get("locator"),
            regx=UILocatorRegx.get("use_yeepay2b_pyament").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if use_yeepay2b_switch:
            use_yeepay2b_switch.click()
            logger.info("选择使用易宝会员支付")
            return True
        else:
            return False

    @classmethod
    def click_yeepay2b_immediately_payment(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        immediately_payment_button = get_element(
            driver=driver, locator=UILocatorRegx.get("yeepay2b_immediately_payment").get("locator"),
            regx=UILocatorRegx.get("yeepay2b_immediately_payment").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if immediately_payment_button:
            immediately_payment_button.click()
            logger.info("点击【易宝支付】按钮")
            return True
        else:
            return False

    @classmethod
    def enter_payment_password(cls, driver: webdriver, password: str, loop: int = 1, sleep: float = 0,
                               **kwargs) -> bool:
        is_exist_pop_box = get_element(
            driver=driver, locator=UILocatorRegx.get("password_pop_box").get("locator"),
            regx=UILocatorRegx.get("password_pop_box").get("regx"), sleep=sleep, loop=loop, **kwargs
        )
        if is_exist_pop_box:
            first_password_inout_box = get_element(
                driver=driver, locator=UILocatorRegx.get("first_password_input_box").get("locator"),
                regx=UILocatorRegx.get("first_password_input_box").get("regx"), sleep=sleep, loop=loop, **kwargs
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
                logger.warning("查找密码输入框的第一个框失败")
                return False
        else:
            logger.warning("没有出现输入密码的弹框")
            return False

    @classmethod
    def is_wallet_payment_success(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        return True

    @classmethod
    def enter_yeepay2b_account(cls, driver: webdriver, account: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        current_url = driver.current_url
        if current_url.startswith(url_map.get("yeepay2b_cash_desk")) is True:
            input_box = get_element(
                driver=driver, locator=UILocatorRegx.get("yeepay2b_accout_input_box").get("locator"),
                regx=UILocatorRegx.get("yeepay2b_accout_input_box").get("regx"), loop=loop, sleep=sleep, **kwargs
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
    def enter_yeepay2b_password(cls, driver: webdriver, password: str, loop: int = 1, sleep: float = 0,
                                **kwargs) -> bool:
        input_box = get_element(
            driver=driver, locator=UILocatorRegx.get("yeepay2b_password_input_box").get("locator"),
            regx=UILocatorRegx.get("yeepay2b_password_input_box").get("regx"), loop=loop, sleep=sleep, **kwargs
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
    def click_yeepay2b_payment_next(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        next_button = get_element(
            driver=driver, locator=UILocatorRegx.get("yeepay2b_payment_next_button").get("locator"),
            regx=UILocatorRegx.get("yeepay2b_payment_next_button").get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if next_button:
            next_button.click()
            logger.info("易宝支付收银台界面点击【下一步】")
            return True
        else:
            return False

    @classmethod
    def is_yeepay2b_payment_success(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        return True
