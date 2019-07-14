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
    abs_path = '/home/scrapy_pay_client/bill.xml'
    result_list = load_xml(abs_path)
    print(result_list[3][1], result_list[4][1], result_list[5][1], result_list[8][1], result_list[9][1],
          result_list[11][1])
    income_list = list()
    for x in result_list:
        # print(x)
        data = {
        }
        if str(x[1]).find("收钱码收款") >= 0:
            index = result_list.index(x)
            for i in range(5):
                if i == 0:
                    data["user"] = result_list[index + i][1]
                elif i == 1:
                    data["money"] = result_list[index + i][1]
                    data["click_x_y"] = result_list[index + i][2]
                elif i == 2:
                    data["goods"] = result_list[index + i][1]
                elif i == 3:
                    data["today"] = result_list[index + i][1]
                elif i == 4:
                    data["time"] = result_list[index + i][1]
                print(data)
            income_list.append(data)

    print(income_list)
