from views.view import *


def main():
    while True:
        try:
            command = input().strip()
            if command == "exit":
                break

            parsed_command = parse_input(command)

            if parsed_command is None:
                continue

            if parsed_command[0] == "create_library":
                create_library(int(parsed_command[1]))

            elif parsed_command[0] == "add_book":
                if len(parsed_command) >= 6:
                    book_id = parsed_command[1]
                    title = parsed_command[2]
                    authors = parse_commas_to_list(parsed_command[3])
                    publishers = parse_commas_to_list(parsed_command[4])
                    copies = parse_commas_to_list(parsed_command[5])

                    kwargs = {}
                    if len(parsed_command) > 6:
                        for pair in parsed_command[6:]:
                            if ':' in pair:
                                key, value = pair.split(':', 1)
                                if key and value:
                                    kwargs[key] = value
                                else:
                                    print(f"Invalid key-value pair: {pair}. Both key and value must have a value.")
                                    continue
                            else:
                                print(
                                    f"Invalid key-value pair: {pair}. Must contain a colon (':') to separate key and value.")
                                continue
                    add_book_to_library(book_id, title, authors, publishers, copies, **kwargs)
                else:
                    print_invalid_arguments_message(parsed_command, 5)

            elif parsed_command[0] == "remove_book_copy":
                if len(parsed_command) == 2:
                    remove_book_copy_from_library(parsed_command[1])
                else:
                    print_invalid_arguments_message(parsed_command, 1)

            elif parsed_command[0] == "borrow_book":
                if len(parsed_command) == 4:
                    borrow_book_from_library(parsed_command[1], parsed_command[2], parsed_command[3])
                else:
                    print_invalid_arguments_message(parsed_command, 3)

            elif parsed_command[0] == "borrow_book_copy":
                if len(parsed_command) >= 2:
                    try:
                        user_id = parsed_command[2]
                    except Exception:
                        user_id = 'user1'
                    try:
                        due_date = parsed_command[3]
                    except Exception:
                        due_date = '2020-12-31'
                    borrow_book_copy_from_library(parsed_command[1], user_id, due_date)
                else:
                    print_invalid_arguments_message(parsed_command, 1)

            elif parsed_command[0] == "return_book_copy":
                if len(parsed_command) == 2:
                    return_book_copy_to_library(parsed_command[1])
                else:
                    print_invalid_arguments_message(parsed_command, 1)

            elif parsed_command[0] == "print_borrowed":
                if len(parsed_command) == 2:
                    print_borrowed_book_copy_by_user(parsed_command[1])
                else:
                    print_invalid_arguments_message(parsed_command, 1)

            elif parsed_command[0] == "search":
                if len(parsed_command) == 3:
                    search_library_for_book_by_attribute(parsed_command[1], parsed_command[2])
                else:
                    print_invalid_arguments_message(parsed_command, 2)
            else:
                print("Invalid command was passed")

        except Exception as e:
            print(f"Error: {e}")


# Parse the input command into a list of arguments
def parse_input(command):
    parsed_command = command.split()
    if len(parsed_command) == 0:
        return None
    return parsed_command


# print error if invalid args was passed
def print_invalid_arguments_message(parse_command, expected_count):
    passed_count = len(parse_command) - 1
    print(
        "Invalid number of arguments were passed to the command. {} arguments were passed and it was expected to be {} arguments.".format(
            passed_count, expected_count))


# Parse string from input string into a list
def parse_commas_to_list(comma_separated_str):
    return comma_separated_str.split(',')


if __name__ == "__main__":
    main()
