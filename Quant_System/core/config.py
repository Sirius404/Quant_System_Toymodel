# 在 config.json 中自建条目写入配置，在任何其他模块中 from config import Config，用 Config().config_name 即可获得配置值
# 例如 Config().email_host
# 注意：不支持条目的值为 object

import json


class Config:
    __conf = None

    def __new__(cls):
        if not cls.__conf:
            with open("D:\Quant_System\Json\SMTP.json") as file:
                try:
                    conf_j = json.loads(file.read())
                except:
                    raise Exception("配置文件读取错误")
                else:
                    for key in conf_j:
                        setattr(cls, key, conf_j[key])
            cls.__conf = super(Config, cls).__new__(cls)
        return cls.__conf

    def __init__(self) -> None:
        pass
