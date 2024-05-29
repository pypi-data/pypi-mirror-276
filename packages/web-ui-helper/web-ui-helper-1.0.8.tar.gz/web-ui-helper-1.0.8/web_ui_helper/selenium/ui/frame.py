# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  web-ui-helper
# FileName:     frame.py
# Description:  页面数据框架
# Author:       GIGABYTE
# CreateDate:   2024/04/28
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import time
import typing as t
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from web_ui_helper.decorators.selenium_exception import element_find_exception
from web_ui_helper.selenium.frame.browser import get_element, js_click, scroll_element
from web_ui_helper.selenium.frame.browser import scroll_to_bottom, get_elements, execute_script, get_sub_element


class ListFrame(object):

    @classmethod
    @element_find_exception
    def get_all_elements(
            cls, driver: webdriver, url: str, locator: str, regx: str, list_key: str, timeout: int = 1
    ) -> dict:
        """
        爬取页面的主函数
        """
        # 打开网页
        driver.get(url)
        time.sleep(5)
        flag = True
        parsed_data = dict()
        while flag:
            scroll_to_bottom(driver=driver)
            elements = get_elements(driver=driver, locator=locator, regx=regx, timeout=timeout, loop=60)
            new_elements = {element.get_attribute(list_key): element for element in elements if
                            element.get_attribute(list_key) not in list(parsed_data.keys())}
            if new_elements:
                parsed_data.update(new_elements)
            else:
                flag = False
        return parsed_data

    @classmethod
    def get_all_elements_with_scroll_tile(
            cls, driver: webdriver, url: str, locator: str, regx: str, list_key: str, start_element_locator: str,
            start_element_regx: str, timeout: int = 1, max_scroll_attempts: int = 20
    ) -> dict:
        """

        :param driver:
        :param url:
        :param locator:
        :param regx:
        :param list_key:
        :param start_element_locator:
        :param start_element_regx:
        :param timeout:
        :param timeout: 每次滚动后等待页面加载的时间（秒）
        :param max_scroll_attempts: 最大滚动尝试次数
        :return:
        """
        # 打开网页
        driver.get(url)
        start_element = get_element(
            driver=driver, locator=start_element_locator, regx=start_element_regx, loop=max_scroll_attempts,
            interval=0.5
        )
        if start_element:
            is_start_element = True
        else:
            is_start_element = False
        parsed_data = dict()
        if is_start_element is True:
            # 获取当前页面高度
            last_height = execute_script(driver=driver, js_str="return document.body.scrollHeight", loop=1)
            for attempt in range(max_scroll_attempts):
                # 向下滚动一小部分距离
                execute_script(driver=driver, js_str="window.scrollBy(0, window.innerHeight * 0.75);", loop=1)
                # 等待页面加载
                time.sleep(timeout)
                # 获取新的页面高度
                new_height = execute_script(driver=driver, js_str="return document.body.scrollHeight", loop=1)
                # 如果页面高度没有变化，则说明已经加载完所有数据
                if new_height == last_height:
                    break
                else:
                    elements = get_elements(driver=driver, locator=locator, regx=regx, timeout=timeout, loop=1)
                    new_elements = {element.get_attribute(list_key): element for element in elements if
                                    element.get_attribute(list_key) not in list(parsed_data.keys())}
                    if new_elements:
                        parsed_data.update(new_elements)
                last_height = new_height
        return parsed_data

    @classmethod
    def get_list_indexes(cls, driver: webdriver, locator: str, regx: str, list_key: str, timeout: int,
                         max_scroll_attempts: int) -> list:
        list_indexes = list()
        # 获取当前页面高度
        last_height = execute_script(driver=driver, js_str="return document.body.scrollHeight", loop=1)
        for attempt in range(max_scroll_attempts):
            elements = get_elements(
                driver=driver, locator=locator, regx=regx, timeout=timeout, loop=1
            ) or list()
            for element in elements:
                index = element.get_attribute(list_key)
                list_indexes.append(index)
            # 向下滚动一小部分距离
            execute_script(driver=driver, js_str="window.scrollBy(0, window.innerHeight * 0.75);", loop=1)
            # 等待页面加载
            time.sleep(timeout)
            # 获取新的页面高度
            new_height = execute_script(driver=driver, js_str="return document.body.scrollHeight", loop=1)
            # 如果页面高度没有变化，则说明已经加载完所有数据
            if new_height == last_height:
                break
            last_height = new_height
        list_indexes = sorted(list(set(list_indexes)), key=int)
        return list_indexes

    @classmethod
    def get_all_elements_with_scroll_expand(
            cls, driver: webdriver, url: str, indexes_locator: str, indexes_regx: str, index_locator: str,
            index_regx: str, list_key: str, list_parse_func: t.Callable, start_element_locator: str,
            start_element_regx: str, expand_locator: str, expand_regx: str, more_all_locator: str, more_all_regx: str,
            area_parse_func: t.Callable, timeout: int = 1, max_scroll_attempts: int = 50
    ) -> dict:
        # 打开网页
        driver.get(url)
        start_element = get_element(
            driver=driver, locator=start_element_locator, regx=start_element_regx, loop=max_scroll_attempts,
            interval=0.5
        )
        if start_element:
            is_start_element = True
        else:
            is_start_element = False
        rows_data = list()
        all_expand_area_data = list()
        if is_start_element is True:
            indexes = cls.get_list_indexes(
                driver=driver, locator=indexes_locator, regx=indexes_regx, list_key=list_key, timeout=timeout,
                max_scroll_attempts=max_scroll_attempts
            )
            for index in indexes:
                sub_index_regx = index_regx.format(index)
                index_element = get_element(driver=driver, locator=index_locator, regx=sub_index_regx, loop=1)
                if index_element:
                    row_data = list_parse_func(element=index_element, index=index)
                    if row_data and isinstance(row_data, dict):
                        row_data["index"] = index
                        rows_data.append(row_data)
                    is_success = cls.click_expand_element(
                        driver=driver, element=index_element, locator=expand_locator, regx=expand_regx, timeout=timeout
                    )
                    if is_success is True:
                        index_element = get_element(driver=driver, locator=index_locator, regx=sub_index_regx, loop=1)
                        cls.click_more_product(
                            driver=driver, element=index_element, locator=more_all_locator, timeout=timeout,
                            regx=more_all_regx
                        )
                        index_element = get_element(
                            driver=driver, locator=index_locator, regx=sub_index_regx, loop=1
                        )
                        area_data = area_parse_func(element=index_element, index=index)
                        if area_data:
                            if isinstance(area_data, list):
                                all_expand_area_data.extend(area_data)
                            else:
                                all_expand_area_data.append(area_data)

        result = dict()
        if rows_data:
            result["rows_data"] = rows_data
        if all_expand_area_data:
            result["expand_data"] = all_expand_area_data
        return result

    @classmethod
    def click_expand_element(cls, driver: webdriver, element: WebElement, locator: str, regx: str,
                             timeout: int) -> bool:
        expand_element = get_sub_element(element=element, locator=locator, regx=regx, loop=1)
        if expand_element:
            scroll_element(driver=driver, element=expand_element, loop=1, is_log_output=False)
            js_click(driver=driver, element=expand_element, loop=1, is_log_output=False)
            time.sleep(timeout)
            return True
        else:
            return False

    @classmethod
    def click_more_product(cls, driver: webdriver, element: WebElement, locator: str, regx: str, timeout: int) -> None:
        more_product_element = get_sub_element(element=element, locator=locator, regx=regx, loop=1, is_log_output=False)
        if more_product_element:
            scroll_element(driver=driver, element=more_product_element, loop=1, is_log_output=False)
            js_click(driver=driver, element=more_product_element, loop=1, is_log_output=False)
            time.sleep(timeout)
