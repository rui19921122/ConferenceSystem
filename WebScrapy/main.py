from bs4 import BeautifulSoup
import requests

url = r'http://10.128.20.124/'
session = requests.session()
response = session.get(url)
soup = BeautifulSoup(response.text, )
viewstate = soup.find(id='__VIEWSTATE')
eventvalidation = soup.find(id='__EVENTVALIDATION')
data = {
    "__EVENTVALIDATION": eventvalidation['value'],
    "__VIEWSTATE": viewstate['value'],
    "tbLoginName": '章胜',
    'tbPWD': '123456',
    'btnLogin.x': 101,
    'btnLogin.y': 19
}
ss = session.post(url + 'Login.aspx?ReturnUrl=%2f', data=data)
print(ss.status_code)
print(ss.text)
