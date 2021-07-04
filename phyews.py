import requests
from lxml import etree


class User(object):
    __base_url = 'http://10.101.161.71/PhyEws/'
    __username = ''
    __pwd = ''
    __key_value = ''
    __login_url = 'http://10.101.161.71/PhyEws/default.aspx'
    __rq = requests.session()
    __name = ''
    __course_url = 'http://10.101.161.71/PhyEws/student/select.aspx'

    def __init__(self, username: str, pwd: str):
        self.__username = username
        self.__pwd = pwd
        
        response = self.__rq.get(url=self.__base_url)
        page = etree.HTML(response.text)
        
        self.__key_value = page.xpath('/html/body/form/input/@value')[0]

        self.__login()

    def __login(self):
        data = {
            '__VIEWSTATE': self.__key_value,
            'login1:StuLoginID': self.__username,
            'login1:StuPassword': self.__pwd,
            'login1:UserRole': 'Student',
            'login1:btnLogin.x': 23,
            'login1:btnLogin.y': 7
        }

        response = self.__rq.post(url=self.__login_url, data=data)
        page = etree.HTML(response.text.replace('&nbsp;', ''))

        self.__name = page.xpath('/html/body/table[3]//font[1]/text()')[0]

    def get_course(self):
        response = self.__rq.get(url=self.__course_url)
        page = etree.HTML(response.text.replace('&nbsp;', '').replace('\r', '').replace('\n', '').replace('\t', '').replace('下载', '').replace('新开', '').replace('实验教材', ''))
        result = page.xpath('//table[3]//tr//td//text()')
        del result[0:11]
        num = int(len(result) / 6)
        course = []
        for i in range(0, num):
            course.append({
                'num': result[i * 6],
                'name': result[i * 6 + 1],
                'week': result[i * 6 + 2],
                'time': result[i * 6 + 3],
                'place': result[i * 6 + 4],
                'grade': result[i * 6 + 5]
            })
        print(course)


if __name__ == '__main__':
    a = User('学号', '密码')
    a.get_course()
