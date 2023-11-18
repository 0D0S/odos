import datetime

import odos

if __name__ == "__main__":
    flag = datetime.datetime.now().hour < 6
    odos.read_and_write_csv(flag)
    if not flag:
        text = odos.print_result()
        odos.chat_message("독촉", text)
