import odos

if __name__ == "__main__":
    odos.read_and_write_csv()
    text = odos.print_result()
		if input("독촉방에 올리시겠습니까?(y/n)") == "y":
	    odos.chat_message("독촉", text)
		else:
	    odos.chat_message("odos", text)
