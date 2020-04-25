import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3 import disable_warnings
import time


exec_start_time = time.time()

PROTO = 'https'
HOST = 'velobike.ru'


class Session():
    ''' Class to handle session '''

    def __init__(self, username, password):
        ''' Constructor '''
        self.proto = PROTO
        self.host = HOST
        self.url = '{}://{}/'.format(self.proto, self.host)

        self.username = username
        self.password = password

        self.session = requests.Session()

    def get_request(self, url_path):
        request = self.session.get(self.url + url_path, verify=False)
        self.print_request_info(url_path, request)
        return request

    def post_request(self, url_path, payload=None, json=None):
        request = self.session.post(
            self.url + url_path, data=payload, json=json, verify=False)
        self.print_request_info(url_path, request)
        return request

    @staticmethod
    def print_request_info(url_path, request):
        print('NEW REQUEST')
        print('= Path: ' + url_path)
        print('= Request headers: ' + str(request.request.headers))
        print('= Request body: ' + str(request.request.body))
        print('= Status code: ' + str(request.status_code))

        text = str(request.text) if request.text else "—"
        if len(text) <= 500:
            print('= Text:\n' + text)

        headers = str(request.headers) if request.headers else "—"
        print('= Headers: ' + headers)

        cookies = str(request.cookies) if request.cookies else "—"
        print('= Cookies: ' + cookies)

        history = str(request.history) if request.history else "—"
        print('= History: ' + history)
        if request.history:
            for h in request.history:
                print('== History details: ' + str(h))


disable_warnings(InsecureRequestWarning)

# Start session
session = Session('0000000', '0000')

# Form Auth
login_form_url_path = '#popup2'
request = session.get_request(login_form_url_path)
cookies = request.cookies
text = request.text

# Generated inputs
token = 'csrfmiddlewaretoken'
token_input = "<input type='hidden' name='csrfmiddlewaretoken' value='"
token_value_index = text.find(token_input) + len(token_input)
token_value_end_index = text.find("'", token_value_index)
token_value = text[token_value_index:token_value_end_index]
# print('csrfmiddlewaretoken value: ' + token_value)

payload = {token: token_value,
           'login': session.username,
           'pin': session.password}

login_form_req = session.post_request('api/login/', payload)
# print('Login req text: ' + login_form_req.text)

acc_req = session.get_request('account')
# print('Account req text: ' + acc_req.text)

# Statistics
trip_url_template = 'account/history/?page={}'
start_page = 31

items = []
item_code_begin = '<li class="history-list__item" data-id="0">'
item_code_end = '</ul>'

for i in reversed(range(1, start_page + 1)):
    item_req = session.get_request(trip_url_template.format(i))

    cur_items = []
    item_index = 0
    while (item_index >= 0):
        item_index = item_req.text.find(item_code_begin, item_index + 1)
        if item_index > 0:
            item_end_index = item_req.text.find(item_code_end, item_index)
            item = item_req.text[item_index:item_end_index]
            cur_items.append(item)
    # To add in right order
    for item in reversed(cur_items):
        items.append(item)

print('Items len: {}'.format(len(items)))

with open('data.txt', 'wb') as f:
    f.write(bytearray('Velobike data\n\n', 'utf-8'))
    for item in items:
        f.write(bytearray(item, 'utf-8'))
        f.write(bytearray('\n', 'utf-8'))
        f.write(bytearray('===END===', 'utf-8'))
        f.write(bytearray('\n', 'utf-8'))

print()
print('Done! Timer={:.2f} sec'.format(time.time() - exec_start_time))
