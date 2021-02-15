import requests
import hashlib
import getpass
import colorama


def get_hashed_password(user_password):
    """
    :param str user_password: takes in user's password
    :return:  returns a hashed version of user's password
    """
    hashed_password = hashlib.sha1(user_password.encode('utf-8')).hexdigest().upper()
    return hashed_password


def get_api_response(hashed_password):
    """
    :param str hashed_password:  takes in hashed string
    :return: returns a Response object of all the passwords that have been breached in the past, which have the same initial five characters as hashed_password
    """
    api_url = "https://api.pwnedpasswords.com/range/" + hashed_password
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f'there was an error requesting, response.status_code is {response.status_code}')
    return response


def number_of_times_breached(user_password):
    """
    :param str user_password: user entered password
    :rtype: int
    :return: number of times their password was breached
    """
    hashed_sha1_password = get_hashed_password(user_password)
    first_five_chars, remaining_chars = hashed_sha1_password[:5], hashed_sha1_password[5:]
    response_from_api = get_api_response(first_five_chars)
    response_breach_list = response_from_api.text.splitlines()
    breach_generator_obj = (each_line.split(":") for each_line in
                            response_breach_list)  # object in the form of (breached_hashcode, breached_count)
    for breached_str, breached_count in breach_generator_obj:
        if breached_str == remaining_chars:
            return breached_count
    return 0


def get_user_input():
    """
        asks for user for input and informs the user about their password's strength.
        Once the user is done, it asks the user if they would like to check another password
    """
    ask_user = True
    try_another = True
    while ask_user:
        colorama.init(convert=True, autoreset=True)
        password = getpass.getpass("Please type in your password: ")
        if not password:
            continue
        breached_count = number_of_times_breached(password)
        if breached_count == 0:
            print(f"{colorama.Fore.GREEN}Your password is safe! :)")
        else:
            print(
                f"{colorama.Fore.RED}Your password was breached {breached_count} times in the past :(  Consider changing it!")

        while try_another:
            user_answer = input("Do you want to try another password? Y/N? ").lower()
            if user_answer == 'n':
                try_another = False
                print("Goodbye!")
                exit(0)
            elif user_answer == 'y':
                break
            else:
                try_another = True


if __name__ == "__main__":
    get_user_input()
