import odos

if __name__ == "__main__":
    odos.read_and_write_csv()
    text = odos.print_result()
    # odos.chat_message("독촉", text)
    odos.chat_message("odos", text)
