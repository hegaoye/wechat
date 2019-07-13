# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET

# 全局唯一标识
unique_id = 1


def get_data(root_node, result_list):
    """
    遍历所有的节点
    :param root_node: 入口节点
    :param result_list: 遍历集合
    :return:
    """
    global unique_id
    # 获取所有text有数据的node节点
    if str(root_node.tag).__eq__("node") and str(root_node.attrib["text"]).__len__() > 0:
        temp_list = [unique_id, root_node.attrib["text"], root_node.attrib["bounds"]]
        result_list.append(temp_list)
        unique_id += 1

    # 遍历node子节点
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        get_data(child, result_list)
    return


def load_xml(abs_path):
    """
    入口
    :param file_name: 文件绝对位置
    :return:
    """
    result_list = []
    root = ET.parse(abs_path).getroot()
    get_data(root, result_list)
    return result_list


if __name__ == '__main__':
    abs_path = '/home/scrapy_pay_client/ui.xml'
    R = load_xml(abs_path)
    print(R[3][1], R[4][1], R[5][1], R[8][1], R[9][1], R[11][1])
    is_my_page = 0
    for x in R:
        if str(x[1]).__eq__("我的") or str(x[1]).__eq__("账单") or str(x[1]).__eq__("银行卡"):
            is_my_page += 1
    if is_my_page >= 2:
        print("当前页是 我的 页面")

    for x in R:
        print(x)
        # if str(x[1]).find("收钱码收款") >= 0:
        #     index = x[0]
        #     # print(x[0], x[1], x[2])
        #     print(R[index][0], R[index][1], R[index][2])
        #     print(R[index + 1][0], R[index + 1][1], R[index + 1][2])
        #     print(R[index + 2][0], R[index + 2][1], R[index + 2][2])
        #     print(R[index + 3][0], R[index + 3][1], R[index + 3][2])
        #     print(R[index + 4][0], R[index + 4][1], R[index + 4][2])
