import odos
import datetime

if __name__ == "__main__":
    is_last_check = datetime.datetime.now().hour < 6
    odos.read_and_write_csv(is_last_check)
    if not is_last_check:
        text = odos.print_result()
        odos.chat_message("독촉", text)
