from easydict import EasyDict


regex_rules = EasyDict(
    {
        "Email": "[\w\.\-]+@[\w]+\.com|[\w\.\-]+@[\w]+\.co.kr",
        "PhoneNumber": "010[\s\.\-]?\d{3,4}[\s\.\-]?\d{4}",
        "Data_Units": "기가|G|GB|기가바이트|메가|메가바이트|M|MB",
        "Data_Numbers": "[일이삼사오육칠팔구십백천]+|[0-9]{1,4}"
    }
)

