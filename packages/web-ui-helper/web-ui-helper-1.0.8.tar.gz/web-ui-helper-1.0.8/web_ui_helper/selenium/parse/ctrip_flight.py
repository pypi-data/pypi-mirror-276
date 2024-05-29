# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  web-ui-helper
# FileName:     ctrip_flight.py
# Description:  解析携程航班
# Author:       mfkifhss2023
# CreateDate:   2024/05/05
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from decimal import Decimal
from pandas import DataFrame
from selenium import webdriver
from web_ui_helper.common.metaclass import EnumMetaClass
from selenium.webdriver.remote.webelement import WebElement

from web_ui_helper.common.webdriver import Locator
from web_ui_helper.selenium.frame.browser import get_sub_element, get_sub_elements


class AirlineListUiLocator(EnumMetaClass):
    var_index = {"locator": "xpath", "regx": '//div[@index="{}"]'}
    all_index = {"locator": "xpath", "regx": "//div[@index]"}
    list_hearder = {"locator": "xpath", "regx": '//*[@class="sortbar-v2"]'}
    booking_expand = {"locator": "xpath", "regx": './/div[@class="flight-action"]/button'}
    more_product = {"locator": "xpath", "regx": './/div[contains(@class, "expand-default-collapse-price")]'}
    seat_row = {"locator": "xpath", "regx": './/div[contains(@class, "seat-row")]'}
    seat_type = {"locator": "xpath", "regx": './/div[@class="seat-type"]'}
    seat_type_special_img = {"locator": "xpath", "regx": './/img[@id]'}
    seat_info = {"locator": "xpath", "regx": './/div[@class="seat-info"]'}
    seat_info_rules_highlight = {"locator": "xpath", "regx": './/span[contains(@class, "highlight")]'}
    seat_info_voucher = {"locator": "xpath", "regx": './/div[@class="voucher"]'}
    seat_info_limit = {"locator": "xpath", "regx": './/span[@class="limit"]/div'}
    seat_info_service_package_text = {"locator": "xpath", "regx": './/span[@class="item-text"]'}
    domestic_seat_type = {"locator": "xpath", "regx": './/div[@class="domestic-seat-type"]'}
    domestic_seat_type_span_id = {"locator": "xpath", "regx": './/span[@id]'}
    seat_tags = {"locator": "xpath", "regx": './/div[@class="seat-tags"]'}
    seat_tags_id = {"locator": "xpath", "regx": './/span[@id]'}
    seat_operate = {"locator": "xpath", "regx": './/div[contains(@class, "seat-operate")]'}
    seat_operate_price = {"locator": "xpath", "regx": './/span[@class="price"]'}
    seat_operate_sub_price_item = {"locator": "xpath", "regx": './/div[contains(@class, "sub-price-item")]'}
    seat_operate_post_prefix = {"locator": "xpath", "regx": './/div[@class="post-prefix"]/span'}


class DesktopFlight:

    @classmethod
    def merge_flight_airline(cls, airline: str, plane_no: str, aircraft_type: str) -> str:
        merge_slice = list()
        if airline:
            merge_slice.append(airline)
        if plane_no:
            merge_slice.append(plane_no)
        if aircraft_type:
            merge_slice.append(aircraft_type)
        return "|".join(merge_slice) if merge_slice else ""

    @classmethod
    def parse_mul_airline(cls, element: WebElement) -> list:
        plane_no_regx = "plane-No"
        mul_airline = list()
        sub_elements = get_sub_elements(element=element, locator="class_name", regx=plane_no_regx, loop=1)
        for sub_element in sub_elements:
            plane_no_item = sub_element.text.strip()
            plane_no_item = plane_no_item.replace(" ", "|")
            mul_airline.append(plane_no_item)
        return mul_airline

    @classmethod
    def parse_flight_airline(cls, element: WebElement) -> str:
        """解析航线数据，包括航司，航班，飞机型号"""
        mul_airline_regx = "mul-airline"
        segment_airline_regx = './/div[@class="airline-item"]'
        segment_airline_elements = get_sub_elements(
            element=element, locator="xpath", regx=segment_airline_regx, loop=1
        )
        mul_airline_element = get_sub_element(
            element=element, locator="class_name", regx=mul_airline_regx, loop=1, is_log_output=False
        )
        if segment_airline_elements:
            segment_airline = list()
            for segment_airline_element in segment_airline_elements:
                airline_item = cls.get_airline(element=segment_airline_element)
                plane_no_item, aircraft_type_item = cls.get_plane_no(element=segment_airline_element)
                merge_str = cls.merge_flight_airline(
                    airline=airline_item, plane_no=plane_no_item, aircraft_type=aircraft_type_item
                )
                if merge_str:
                    segment_airline.append(merge_str)
            flight_airline = ";".join(segment_airline) if segment_airline else ""
        elif mul_airline_element:
            flight_airline_slice = list()
            master_airline = mul_airline_element.text.strip()
            mul_airlines = cls.parse_mul_airline(element=element)
            if master_airline:
                master_airline = master_airline.replace(" ", "|")
                flight_airline_slice.append(master_airline)
            if mul_airlines:
                for mul_airline in mul_airlines:
                    flight_airline_slice.append(mul_airline)
            flight_airline = ";".join(flight_airline_slice) if flight_airline_slice else ""
        else:
            airline = cls.get_airline(element=element)
            plane_no, aircraft_type = cls.get_plane_no(element=element)
            flight_airline = cls.merge_flight_airline(airline=airline, plane_no=plane_no, aircraft_type=aircraft_type)
        return flight_airline

    @classmethod
    def get_airline(cls, element: WebElement) -> str:
        airline_regx = "airline-logo"
        airline_element = get_sub_element(
            element=element, locator="class_name", regx=airline_regx, loop=1
        )
        # 提取alt属性的值
        airline = airline_element.get_attribute("alt")
        return airline

    @classmethod
    def get_flight_price(cls, element: WebElement) -> tuple:
        price_regx = './/span[@class="price"]'
        price_element = get_sub_element(element=element, locator="xpath", regx=price_regx, loop=1)
        text = price_element.text.strip() if price_element else ""
        if text:
            price = Decimal(text[1:])
            unit = text[:1]
        else:
            price, unit = "", ""
        return price, unit

    @classmethod
    def get_index(cls, driver: webdriver, index: str) -> WebElement:
        index_regx = './/div[@index="{}"]'
        return driver.find_element(Locator.get("xpath"), index_regx.format(index))

    @classmethod
    def get_plane_no(cls, element: WebElement) -> tuple:
        plane_no_regx = './/div[@class="plane"]'
        plane_no_element = get_sub_element(
            element=element, locator="xpath", regx=plane_no_regx, loop=1
        )
        text = plane_no_element.text if plane_no_element else ""
        plane_no_slice = text.strip().split()
        plane_no = aircraft_type = ""
        if len(plane_no_slice) > 0:
            plane_no = plane_no_slice[0].strip()
            aircraft_type = plane_no_slice[1].strip()
        return plane_no, aircraft_type

    @classmethod
    def get_depart_time(cls, element: WebElement) -> str:
        depart_time_regx = './/div[@class="depart-box"]/div[@class="time"]'
        depart_time_element = get_sub_element(
            element=element, locator="xpath", regx=depart_time_regx, loop=1
        )
        depart_time = depart_time_element.text.strip() if depart_time_element else ""
        return depart_time

    @classmethod
    def get_depart_airport(cls, element: WebElement) -> str:
        depart_box_regx = "depart-box"
        depart_box_element = get_sub_element(element=element, locator="class_name", regx=depart_box_regx, loop=1)
        terminal_regx = "terminal"
        depart_airport_regx = '//div[@class="depart-box"]//div[@class="airport"]/span'
        depart_airport_element = get_sub_element(
            element=depart_box_element, locator="xpath", regx=depart_airport_regx, loop=1
        )
        depart_airport_list = list()
        depart_text = depart_airport_element.text.strip() if depart_airport_element else ""
        terminal_element = get_sub_element(
            element=depart_box_element, locator="class_name", regx=terminal_regx, loop=1
        )

        terminal_text = terminal_element.text.strip() if terminal_element else ""
        if depart_text:
            depart_airport_list.append(depart_text)
        if terminal_text:
            depart_airport_list.append(terminal_text)
        return " ".join(depart_airport_list) if depart_airport_list else ""

    @classmethod
    def get_arrive_time(cls, element: WebElement) -> tuple:
        arrive_time_regx = './/div[@class="arrive-box"]/div[@class="time"]'
        arrive_time_element = get_sub_element(
            element=element, locator="xpath", regx=arrive_time_regx
        )
        arrive_time_slice = arrive_time_element.text.strip().split("\n") if arrive_time_element else list()
        arrive_time = arrive_time_slice[0] if len(arrive_time_slice) > 0 else ""
        cross_days = arrive_time_slice[1] if len(arrive_time_slice) > 1 else ""
        return arrive_time, cross_days

    @classmethod
    def get_arrive_airport(cls, element: WebElement) -> str:
        arrive_box_regx = "arrive-box"
        arrive_box_element = get_sub_element(element=element, locator="class_name", regx=arrive_box_regx, loop=1)
        terminal_regx = "terminal"
        arrive_airport_regx = '//div[@class="arrive-box"]//div[@class="airport"]/span'
        arrive_airport_element = get_sub_element(
            element=element, locator="xpath", regx=arrive_airport_regx, loop=1
        )
        arrive_airport_list = list()
        arrive_text = arrive_airport_element.text.strip() if arrive_airport_element else ""
        terminal_element = get_sub_element(
            element=arrive_box_element, locator="class_name", regx=terminal_regx, loop=1
        )
        terminal_text = terminal_element.text.strip() if terminal_element else ""
        if arrive_text:
            arrive_airport_list.append(arrive_text)
        if terminal_text:
            arrive_airport_list.append(terminal_text)
        return " ".join(arrive_airport_list) if arrive_airport_list else ""

    @classmethod
    def get_transfer_duration(cls, element: WebElement) -> str:
        transfer_regx = "transfer-duration"
        transfer_element = get_sub_element(
            element=element, locator="class_name", regx=transfer_regx, loop=1, is_log_output=False
        )
        transfer_text = transfer_element.text.strip() if transfer_element else ""
        return transfer_text

    @classmethod
    def parse_airline(cls, driver: webdriver = None, index: str = None, element: WebElement = None) -> dict:
        if driver and index:
            element = cls.get_index(driver=driver, index=index)
        # print(element.get_attribute('outerHTML'))
        price, unit = cls.get_flight_price(element=element)
        airline = cls.parse_flight_airline(element=element)
        if airline.find("共享") != -1:
            is_share = True
        else:
            is_share = False
        if airline.find(";") != -1:
            is_transfer = True
        else:
            is_transfer = False
        depart_time = cls.get_depart_time(element=element)
        arrive_time, cross_days = cls.get_arrive_time(element=element)
        depart_airport = cls.get_depart_airport(element=element)
        arrive_airport = cls.get_arrive_airport(element=element)
        transfer_duration = cls.get_transfer_duration(element=element)
        airline_data = dict(
            index=index, airline=airline, arrive_time=arrive_time, cross_days=cross_days, depart_time=depart_time,
            price=price, price_uint=unit, depart_airport=depart_airport, arrive_airport=arrive_airport,
            transfer_duration=transfer_duration, is_share=is_share, is_transfer=is_transfer
        )
        if index:
            airline_data["index"] = index
        return airline_data

    @classmethod
    def parse_airlines(cls, elements_data: dict) -> DataFrame:
        columns = [
            "index", "airline", "is_share", "is_transfer", "price", "price_uint", "depart_time", "depart_airport",
            "arrive_time", "cross_days", "arrive_airport", "transfer_duration"
        ]
        df = DataFrame(columns=columns)
        for index, element in elements_data.items():
            # 逐行添加数据
            new_row = cls.parse_airline(element=element)
            new_row["index"] = index
            # 添加新行数据
            df.loc[len(df)] = new_row
        return df

    @classmethod
    def parse_expand_area(cls, element: WebElement, index: str) -> list:
        set_rows = get_sub_elements(
            element=element, locator=AirlineListUiLocator.seat_row.value.get("locator"),
            regx=AirlineListUiLocator.seat_row.value.get("regx"), loop=1, is_log_output=False
        )
        area_data = list()
        if set_rows:
            for set_row in set_rows:
                merged_dict = dict()
                seat_type = cls.parse_seat_type(element=set_row)
                seat_info = cls.parse_seat_info(element=set_row)
                seat_tags = cls.parse_seat_tags(element=set_row)
                seat_operate = cls.parse_seat_operate(element=set_row)
                domestic_seat_type = cls.parse_domestic_seat_type(element=set_row)
                if seat_type:
                    merged_dict.update(seat_type)
                if seat_info:
                    merged_dict.update(seat_info)
                if seat_tags:
                    merged_dict.update(seat_tags)
                if seat_operate:
                    merged_dict.update(seat_operate)
                if domestic_seat_type:
                    merged_dict.update(domestic_seat_type)
                if merged_dict:
                    new_merged_dict = dict(index=index)
                    new_merged_dict.update(merged_dict)
                    area_data.append(new_merged_dict)
        return area_data

    @classmethod
    def parse_seat_type(cls, element: WebElement) -> dict:
        seat_type_element = get_sub_element(
            element=element, locator=AirlineListUiLocator.seat_type.value.get("locator"),
            regx=AirlineListUiLocator.seat_type.value.get("regx"), loop=1, is_log_output=False
        )
        seat_type = dict(seat_type_special_id="", seat_type_special_src="", seat_type_special_alt="")
        if seat_type_element:
            special_img_element = get_sub_element(
                element=seat_type_element, regx=AirlineListUiLocator.seat_type_special_img.value.get("regx"),
                locator=AirlineListUiLocator.seat_type_special_img.value.get("locator"), loop=1, is_log_output=False
            )
            if special_img_element:
                special_id = special_img_element.get_attribute("id").strip()
                special_src = special_img_element.get_attribute("src").strip()
                special_alt = special_img_element.get_attribute("alt").strip()
                seat_type["seat_type_special_id"] = special_id
                seat_type["seat_type_special_src"] = special_src
                seat_type["seat_type_special_alt"] = special_alt
        return seat_type

    @classmethod
    def parse_seat_info(cls, element: WebElement) -> dict:
        seat_info_element = get_sub_element(
            element=element, locator=AirlineListUiLocator.seat_info.value.get("locator"),
            regx=AirlineListUiLocator.seat_info.value.get("regx"), loop=1, is_log_output=False
        )
        seat_info = dict(seat_info_rules="", seat_info_voucher="", seat_info_service_package="", seat_info_limit="")
        if seat_info_element:
            highlight_elements = get_sub_elements(
                element=seat_info_element, locator=AirlineListUiLocator.seat_info_rules_highlight.value.get("locator"),
                regx=AirlineListUiLocator.seat_info_rules_highlight.value.get("regx"), loop=1, is_log_output=False
            )
            voucher_element = get_sub_element(
                element=seat_info_element, locator=AirlineListUiLocator.seat_info_voucher.value.get("locator"),
                regx=AirlineListUiLocator.seat_info_voucher.value.get("regx"), loop=1, is_log_output=False
            )
            service_elements = get_sub_elements(
                element=seat_info_element,
                locator=AirlineListUiLocator.seat_info_service_package_text.value.get("locator"),
                regx=AirlineListUiLocator.seat_info_service_package_text.value.get("regx"), loop=1, is_log_output=False
            )
            limit_element = get_sub_element(
                element=seat_info_element, locator=AirlineListUiLocator.seat_info_limit.value.get("locator"),
                regx=AirlineListUiLocator.seat_info_limit.value.get("regx"), loop=1, is_log_output=False
            )
            if isinstance(highlight_elements, list):
                highlights = list()
                for highlight_element in highlight_elements:
                    highlight_text = highlight_element.text.strip()
                    if highlight_text:
                        highlights.append(highlight_text)
                highlight = "|".join(highlights) if highlights else ""
                seat_info["seat_info_rules"] = highlight
            if voucher_element:
                seat_info["seat_info_voucher"] = voucher_element.text.strip()
            if limit_element:
                seat_info["seat_info_limit"] = limit_element.text.strip()
            if isinstance(service_elements, list):
                service_packages = list()
                for service_element in service_elements:
                    service_package_text = service_element.text.strip()
                    if service_package_text:
                        service_packages.append(service_package_text)
                service_package = "|".join(service_packages) if service_packages else ""
                seat_info["seat_info_service_package"] = service_package
        return seat_info

    @classmethod
    def parse_domestic_seat_type(cls, element: WebElement) -> dict:
        domestic_seat_type_element = get_sub_element(
            element=element, locator=AirlineListUiLocator.domestic_seat_type.value.get("locator"),
            regx=AirlineListUiLocator.domestic_seat_type.value.get("regx"), loop=1, is_log_output=False
        )
        domestic_seat_type = dict(domestic_seat_type_cabin="")
        if domestic_seat_type_element:
            span_id_elements = get_sub_elements(
                element=domestic_seat_type_element,
                locator=AirlineListUiLocator.domestic_seat_type_span_id.value.get("locator"),
                regx=AirlineListUiLocator.domestic_seat_type_span_id.value.get("regx"), loop=1, is_log_output=False
            )
            if isinstance(span_id_elements, list):
                span_ids = list()
                for span_id_element in span_id_elements:
                    span_id = span_id_element.text.strip()
                    if span_id:
                        span_ids.append(span_id)
                if span_ids:
                    cabin = "|".join(span_ids)
                    domestic_seat_type["domestic_seat_type_cabin"] = cabin if cabin else ""
        return domestic_seat_type

    @classmethod
    def parse_seat_tags(cls, element: WebElement) -> dict:
        seat_tags_element = get_sub_element(
            element=element, locator=AirlineListUiLocator.seat_tags.value.get("locator"),
            regx=AirlineListUiLocator.seat_tags.value.get("regx"), loop=1, is_log_output=False
        )
        seat_tags = dict(seat_tags_ids="")
        if seat_tags_element:
            span_id_elements = get_sub_elements(
                element=seat_tags_element, locator=AirlineListUiLocator.seat_tags_id.value.get("locator"),
                regx=AirlineListUiLocator.seat_tags_id.value.get("regx"), loop=1, is_log_output=False
            )
            if isinstance(span_id_elements, list):
                span_ids = list()
                for span_id_element in span_id_elements:
                    span_id = span_id_element.text.strip()
                    if span_id:
                        span_ids.append(span_id)
                if span_ids:
                    ids = "|".join(span_ids)
                    seat_tags["seat_tags_ids"] = ids if ids else ""
        return seat_tags

    @classmethod
    def parse_seat_operate(cls, element: WebElement) -> dict:
        seat_operate_element = get_sub_element(
            element=element, locator=AirlineListUiLocator.seat_operate.value.get("locator"),
            regx=AirlineListUiLocator.seat_operate.value.get("regx"), loop=1, is_log_output=False
        )
        seat_operate = dict(
            seat_operate_price=Decimal("NaN"), seat_operate_uint="", seat_operate_highlight="",
            seat_operate_post_prefix=""
        )
        if seat_operate_element:
            prcie_element = get_sub_element(
                element=seat_operate_element, locator=AirlineListUiLocator.seat_operate_price.value.get("locator"),
                regx=AirlineListUiLocator.seat_operate_price.value.get("regx"), loop=1, is_log_output=False
            )
            high_light_element = get_sub_element(
                element=seat_operate_element,
                locator=AirlineListUiLocator.seat_operate_sub_price_item.value.get("locator"),
                regx=AirlineListUiLocator.seat_operate_sub_price_item.value.get("regx"), loop=1, is_log_output=False
            )
            post_prefix_element = get_sub_element(
                element=seat_operate_element,
                locator=AirlineListUiLocator.seat_operate_post_prefix.value.get("locator"),
                regx=AirlineListUiLocator.seat_operate_post_prefix.value.get("regx"), loop=1, is_log_output=False
            )
            if high_light_element:
                seat_operate["seat_operate_highlight"] = high_light_element.text.strip()
            if post_prefix_element:
                seat_operate["seat_operate_post_prefix"] = post_prefix_element.text.strip()
            if prcie_element:
                price_text = prcie_element.text.strip()
                if price_text:
                    # 获取剩余部分 (价格值)
                    seat_operate["seat_operate_price"] = Decimal(price_text[1:]) if len(
                        price_text) > 1 else ""
                    # 获取第一个字符 (货币符号)
                    seat_operate["seat_operate_uint"] = price_text[0] if len(
                        price_text) > 0 else ""
        return seat_operate
