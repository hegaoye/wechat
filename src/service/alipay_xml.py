# -*- coding: utf-8 -*-
import xml.dom.minidom as xmldom

if __name__ == "__main__":
    domobj = xmldom.parse("/home/scrapy_pay_client/bill.xml")
    print("xmldom.parse:", type(domobj))
    elementobj = domobj.documentElement
    subElementObj = elementobj.getElementsByTagName("node")
    nodes = list()
    for i in range(len(subElementObj)):
        if (subElementObj[i].getAttribute("index") == '3'):
            sub2 = subElementObj[i].getElementsByTagName("p")
            for j in range(len(sub2)):
                if (sub2[j].getAttribute("n") == 'name'):
                    node = sub2[j].firstChild.data.replace('...', '')
                    print("{name:'", node, "',draggable: true,},")
                    nodes.append(node)

    print("nodes len:", len(nodes))
