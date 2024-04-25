import requests as req
URL = "http://httpbin.org/get"
resp = req.get(URL)
print(resp.status_code)
print(resp.text)
print(resp.url)
#pcap lib를 사용하면, wifi 로그를 캡쳐할 수 있다.

payload = {'key1':'value1', 'key2':'value2'}
resp = req.get(URL, params = payload)
print(resp.url)
print(resp.text)
