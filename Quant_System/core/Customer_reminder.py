from datetime import datetime
from core.email_sender import Email

tmp_if_send_email = True  # 预留的 boll 值

if tmp_if_send_email:
    Email().send_email("交易提醒",
                       "尊敬的用户：\n    您的自选股票已达到交易条件，请及时进行处理。\n交易软件\n{}年{}月{}日"
                       .format(datetime.now().year, datetime.now().month, datetime.now().day))
