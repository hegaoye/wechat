# coding=utf-8
# 全局唯一标识
import os
import xml.etree.ElementTree as ET

from src.base.log4py import logger
from src.service.node import Node

unique_id = 1


def list_attr_value(abs_path, attr, value):
    """
    根据属性和值特性来查询具体的数据
    :param abs_path: xml绝对位置
    :param attr: 搜索属性
    :param value: 属性可能的值，用的是包含查询
    :return: list
    """
    logger.debug("解析xml文件: " + abs_path)
    logger.debug("获取属性: " + attr)
    logger.debug("获取属性-值匹配: " + value)
    attr_list = []
    root = ET.parse(abs_path).getroot()
    search_data_from_xml(root, attr_list, attr, value)
    logger.debug("解析数据: " + str(attr_list))
    return attr_list


def search_data_from_xml(root_node, attr_list, attr, value):
    """
    遍历所有的节点并查询到指定的属性
    :param root_node: 入口节点
    :param attr_list: 遍历集合
    """
    # 获取所有text有数据的node节点
    if str(root_node.tag).__eq__("node") and str(root_node.attrib[attr]).find(value) >= 0:
        data = {
            "index": root_node.attrib["index"],
            "text": root_node.attrib["text"],
            "bounds": root_node.attrib["bounds"],
            "desc": root_node.attrib["content-desc"],
            "package": root_node.attrib["package"],
            "class": root_node.attrib["class"]
        }
        attr_list.append(data)

    # 遍历node子节点
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        search_data_from_xml(child, attr_list, attr, value)
    return


def get_data(root_node, result_list, attr="text"):
    """
    遍历所有的节点
    :param root_node: 入口节点
    :param result_list: 遍历集合
    """
    global unique_id
    # 获取所有text有数据的node节点
    if str(root_node.tag).__eq__("node") and str(root_node.attrib[attr]).__len__() > 0:
        data = {
            "index": root_node.attrib["index"],
            "text": root_node.attrib["text"],
            "bounds": root_node.attrib["bounds"],
            "desc": root_node.attrib["content-desc"],
            "package": root_node.attrib["package"],
            "class": root_node.attrib["class"]
        }
        result_list.append(data)
        unique_id += 1

    # 遍历node子节点
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        get_data(child, result_list)
    return


def load_xml(abs_path, attr="text"):
    """
    入口
    :param file_name: 文件绝对位置
    :return: list
    """
    logger.debug("解析xml文件: " + abs_path)
    logger.debug("获取属性: " + attr)
    result_list = []
    utf8_parser = ET.XMLParser(encoding='utf-8')
    root = ET.parse(abs_path, parser=utf8_parser).getroot()
    get_data(root, result_list, attr)
    logger.debug("解析数据：" + str(result_list))
    return result_list


if __name__ == '__main__':
    abs_path = '/home/scrapy_pay_client/my.xml'
    result_list = load_xml(abs_path)

    node = Node()
    for x in result_list:
        # print(x)
        node.to_obj(x)
        if node.text.__eq__("支付宝通知"):
            print(node.get_bounds()[0])
            print(node.get_bounds()[1])

    list_attr = list_attr_value(abs_path, "resource-id", "com.alipay.android.phone.wealth.home:id/tab_description")
    for attr in list_attr:
        print(attr)
    # list = os.popen("adb devices")
    # for i in list:
    #     screen_str = str(i).replace("\n", "")
    #     if screen_str.find("device") >= 0:
    #         screen_str = screen_str.replace("Override size: ", "").replace("x", ",")
    #         print(screen_str)
