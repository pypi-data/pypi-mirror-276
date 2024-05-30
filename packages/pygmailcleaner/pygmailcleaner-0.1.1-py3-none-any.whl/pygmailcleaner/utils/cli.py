from abc import ABC, abstractmethod
import getpass
import re
from colorama import Fore, Style

class BaseQuestionHandler(ABC):
    """
    Abstract base class for handling questions.
    
    Attributes:
        questions (list): List of questions to be handled.
        values (list): List of responses to the questions.
    """
    def __init__(self, questions):
        """
        Initialize the question handler with a list of questions.

        Args:
            questions (list): List of questions to handle.
        """
        self.questions = questions
        self.values = []

    @abstractmethod
    def get_question_response(self):
        """
        Abstract method to get responses for the questions.
        This method should be implemented by subclasses.
        """
        pass

    @abstractmethod
    def process_response(self):
        """
        Abstract method to process the responses.
        This method should be implemented by subclasses.
        """
        pass

    def run(self):
        """
        Execute the process of getting and processing question responses.

        Returns:
            list: Processed responses to the questions.
        """
        try:
            self.get_question_response()
            self.process_response()
            return self.values
        except Exception as e:
            print(f"{Fore.RED}Error occurred: {e}{Style.RESET_ALL}")

class YesNoQuestionHandler(BaseQuestionHandler):
    """
    Handler for questions that require a yes or no response.
    
    Supports multiple questions to be passed to the `questions` attribute.
    """
    def get_question_response(self):
        """
        Get yes or no responses for the questions.
        """
        try:
            for question in self.questions:
                while True:
                    choice = input(f"{question['description']}? [{Fore.GREEN}y{Style.RESET_ALL}/{Fore.RED}n{Style.RESET_ALL}]: ").strip().lower()
                    if choice in ['y', 'n']:
                        question['response'] = choice
                        break
                    else:
                        print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n' for each option.{Style.RESET_ALL}")
        except Exception as e:
            raise ValueError(f"Error occurred while getting response: {e}")

    def process_response(self):
        """
        Process the yes or no responses and store them in the `values` attribute.
        """
        try:
            self.values = [option['response'] for option in self.questions]
        except Exception as e:
            raise ValueError(f"Error occurred while processing response: {e}")

class DateQuestionHandler(BaseQuestionHandler):
    """
    Handler for questions that require a date response.

    Only supports one question at a time.
    """
    def get_question_response(self):
        """
        Get a date response for the question.
        """
        try:
            while True:
                date_str = input(f"{self.questions} (format 'YYYY-MM-DD'): ")
                if self.validate_date_format(date_str):
                    self.values = date_str
                    break
                else:
                    print(f"{Fore.RED}Invalid date format. Please enter the date in YYYY-MM-DD format.{Style.RESET_ALL}")
        except Exception as e:
            raise ValueError(f"Error occurred while getting response: {e}")

    @staticmethod
    def validate_date_format(date_str):
        """
        Validate the format of the date string.

        Args:
            date_str (str): The date string to validate.

        Returns:
            bool: True if the date string is in the correct format, False otherwise.
        """
        try:
            pattern = r'^\d{4}-\d{2}-\d{2}$'
            return bool(re.match(pattern, date_str))
        except Exception as e:
            raise ValueError(f"Error occurred while validating date format: {e}")

    def process_response(self):
        """
        Process the date response. This method is currently a placeholder.
        """
        pass

class ValueQuestionHandler(BaseQuestionHandler):
    """
    Handler for questions that require a string response.

    Only supports one question at a time.

    Expected format for `questions` attribute:
        {
            "question": "What is your password?",
            "format": r"^.{1,30}$",
            "validation": "Must be less than 30 characters",
            "sensitive": True 
        }
    """
    def get_question_response(self):
        """
        Get a string response for the question.
        """
        try:
            while True:
                sensitive_flag = self.questions['sensitive']
                if not sensitive_flag:
                    string = input(f"{self.questions['question']}: ")
                else:
                    string = getpass.getpass(f"{self.questions['question']}: ")
                pattern = self.questions['format']
                validation = self.questions['validation']
                if self.validate_string_format(string, pattern):
                    self.values = string
                    break
                else:
                    print(f"{Fore.RED} Invalid string format: {validation}.{Style.RESET_ALL}")
        except Exception as e:
            raise ValueError(f"Error occurred while getting response: {e}")

    @staticmethod
    def validate_string_format(string, pattern):
        """
        Validate the format of the string.

        Args:
            string (str): The string to validate.
            pattern (str): The regex pattern to validate against.

        Returns:
            bool: True if the string matches the pattern, False otherwise.
        """
        try:
            return bool(re.match(pattern, string))
        except Exception as e:
            raise ValueError(f"Error occurred while validating string format: {e}")

    def process_response(self):
        """
        Process the string response. This method is currently a placeholder.
        """
        pass