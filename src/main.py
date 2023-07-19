import odos

if __name__ == "__main__":
    odos.csv_read()
    text = odos.print_loc()
    odos.chat_message("독촉", text)
