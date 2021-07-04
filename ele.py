import requests
from lxml import etree


class Elect(object):
    def __init__(self, userid: str):
        self.__request = requests.session()
        self.__url = 'http://eetec.nuc.edu.cn/syxt/login/login_login.do'
        self.__data = {
            'loginName': userid,
            'password': '111111'
        }
        self.__request.post(url=self.__url, data=self.__data)
        self.__url = 'http://eetec.nuc.edu.cn/syxt/system/che_shouyemyscore.do'
        self.__response = self.__request.get(url=self.__url)
        self.__username = etree.HTML(self.__response.text).xpath('/html/body/div[2]/table[2]/tr/td/text()[1]')[
            0].strip().replace("欢迎您：", '')

    def printGrades(self):
        for i in range(2, 12):
            self.__result = etree.HTML(self.__response.text).xpath(
                '//*[@id="me_content_right_contnent"]/table/tr[{}]/td[6]/text()'.format(str(i)))
            if len(self.__result) == 0:
                self.__result.append('暂无')
            print(etree.HTML(self.__response.text).xpath(
                '//*[@id="me_content_right_contnent"]/table/tr[{}]/td[2]/text()'.format(str(i)))[0], end=':')
            print(self.__result[0])

    def getName(self):
        return self.__username


if __name__ == '__main__':
    id = '学号'
    a = Elect(userid=id)
    print(id + a.getName())
    a.printGrades()
