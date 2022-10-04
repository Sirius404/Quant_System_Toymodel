from datetime import datetime
from core.email_sender import Email

tmp_if_send_email = True  # 预留的 boll 值

if tmp_if_send_email:
    Email().send_email("风险控制提醒",
                       "尊敬的用户：\n    因市场剧烈波动，您的自选股票回撤比例达到您设定的上限，请及时进行处理。\n交易软件\n{}年{}月{}日"
                       .format(datetime.now().year, datetime.now().month, datetime.now().day))
