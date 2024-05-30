class RequestingError(Exception):
    def __init__(self, meassge: str = "cookie获取时出现错误. \n \
                              English translation: There was an error when the cookie was obtained."):
        self.message = meassge

    def __str__(self):
        return self.message


class ParseringError(Exception):
    def __init__(self, message: str = "解析文件时出错. \n \
                                    English translation: There was an error parsing the file."):
        self.message = message

    def __str__(self):
        return self.message


def rgetcookies(url: str = "https://baidu.com/s", method: str = "post") -> dict:
    import requests
    from requests.utils import dict_from_cookiejar
    from supplies.reptiles import useragents

    r = None
    parma = {"wd": "python"}

    if method == "post":
        r = requests.post(url=url, headers=useragents.chrome(), params=parma, verify=False)
    if method == "get":
        r = requests.get(url=url, headers=useragents.chrome(), params=parma, verify=False)

    r.encoding = "utf-8"

    try:
        r.raise_for_status()
        return dict_from_cookiejar(r.cookies)
    except (Exception, ):
        raise RequestingError()


def HARparser_Test(HARfile: str) -> None:
    import json

    try:
        with open(HARfile, "r") as file:
            HARdata = json.load(file)
        cookies = HARdata["log"]["entries"][0]["response"]["cookies"]
        for cookie in cookies:
            print(cookie)
    except (Exception, ):
        raise ParseringError()
