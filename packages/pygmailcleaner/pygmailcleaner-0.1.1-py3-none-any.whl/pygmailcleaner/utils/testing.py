import getpass
import re
from colorama import Fore, Style

question_user = {
            "question": "What is your gmail address?",
            "format": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "validation": "Must be a valid email address",
            "sensitive": False
        }

question_pw = {
            "question": "What is your password? (must be an app password if using 2FA)",
            "format": r"^.{1,30}$",
            "validation": "Must be less than 30 characters",
            "sensitive": True
        }

def validate_string_format(string, pattern):
    try:
        return bool(re.match(pattern, string))
    except Exception as e:
        raise ValueError(f"Error occurred while validating string format: {e}")
    
def get_question_response(questions):
    try:
        while True:
            sensitive_flag = questions['sensitive']
            if not sensitive_flag:
                string = input(f"{questions['question']}: ")
            else:
                string = getpass.getpass(f"{questions['question']}: ")
            
            pattern = questions['format']
            validation = questions['validation']
            if validate_string_format(string, pattern):
                values = string
                break
            else:
                print(f"{Fore.RED} Invalid string format: {validation}.{Style.RESET_ALL}")
    except Exception as e:
        raise ValueError(f"Error occurred while getting response: {e}")

if __name__ == "__main__":
    try:
        user = get_question_response(question_user)
        pw = get_question_response(question_pw)
        print(f"User: {user} PW: {pw}")
    except Exception as e:
        print(f"Error occurred: {e}")    