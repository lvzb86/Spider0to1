import requests
import json
from lxml import etree


def get_info_list(url):
    href = etree.HTML(requests.get(url).content).xpath('//*[@id="content"]//tr/td[2]/a/@href')
    school_list = []
    for school_url in href:
        school_name = school_url.split('/')[-1]
        response = requests.get('http://www.qianmu.org/' + school_name).content
        tr_list = etree.HTML(response).xpath('//*[@class="infobox"]//tr')
        address = ""
        info_dict = {"学校名称": school_name}
        for i in range(len(tr_list)):
            key = ''.join(tr_list[i].xpath('./td[1]/p/text()'))
            value = ''.join(tr_list[i].xpath('./td[2]/p/text()'))
            if key in ["本科生人数", "研究生人数", "师生比", "国际学生比例", "网址"] and value != "":
                info_dict[key] = value
            elif key in ["国家", "州省", "城市"]:
                address.join(value)
        if address != "":
            info_dict["地址"] = address
        print(info_dict)
        if len(info_dict) != 1:
            school_list.append(info_dict)
    with open('2018US-NEWS.json', 'w') as f:
        json.dump(school_list, f)


if __name__ == '__main__':
    get_info_list("http://www.qianmu.org/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D")
