import logging
import argparse
import os
from .utils import (
    YesNoQuestionHandler,
    DateQuestionHandler,
    ValueQuestionHandler,
    SMPTClient,
    return_logo,
    METHODS,
)

logger = logging.getLogger()


def get_cumulative_search_term(methods) -> str:
    """
    Formulate the cumulative search term based on the provided methods.

    Args:
        methods (list): List of methods containing search terms and responses.

    Returns:
        str: The cumulative search term.
    """

    logger.info("Calculating cumulative search term...")
    cumulative_search_term = ""
    for method in methods:
        if method["response"] == "y":
            cumulative_search_term += method["y_search_term"] + " "
        else:
            cumulative_search_term += method["n_search_term"] + " "
    logger.info(f"Cumulative search term: {cumulative_search_term.strip()}")
    return cumulative_search_term.strip()


def get_commands_choices() -> tuple[list, str]:
    """
    Prompt the user to select the commands they would like to include.

    Returns:
        tuple: A tuple containing the list of included filters and the search string.
    """

    print("Please select the commands you would like to include:")
    questions = METHODS
    YesNoQuestionHandler(questions).run()
    included_filters = [
        method["description"] for method in questions if method.get("response") == "y"
    ]
    search_string = get_cumulative_search_term(questions)
    return included_filters, search_string


def get_general_stats(gmail: SMPTClient) -> bool:
    """
    Retrieve and display general statistics about the user's Gmail account.

    Args:
        gmail (SMPTClient): An instance of the SMPTClient class.

    Returns:
        bool: True if statistics are retrieved successfully.
    """

    logger.debug("Retrieving general statistics...")

    msg_ids = gmail.get_msg_ids("")
    total_msgs = gmail.count_msgs(msg_ids)

    print(f"Total number of messages: {total_msgs}")
    msg_ids = gmail.get_msg_ids("in:unread")
    unread_msgs = gmail.count_msgs(msg_ids)

    print(f"Unread messages: {unread_msgs}")

    return True


def get_response_summary(responses: dict) -> bool:
    """
    Display a summary of the user's responses.

    Args:
        responses (dict): Dictionary containing the user's responses.

    Returns:
        bool: True if the summary is displayed successfully.
    """

    print("\nSummary:")
    print(f"1. Search up until date: {responses.get('date_until')}")
    print(
        f"2. Delete immediately: {'Yes' if responses.get('delete_immediately') == 'y' else 'No'}"
    )
    print("3. Included filters:")
    for i in responses.get("included_filters"):
        print(f"   - {i}")

    return True


def handle_deletions(
    gmail: SMPTClient, msg_ids: str, responses: dict, search_string: str
) -> bool:
    """
    Handle the deletion of emails based on the user's responses and search string.

    Args:
        gmail (SMPTClient): An instance of the SMPTClient class.
        msg_ids (str): The message IDs to be deleted.
        responses (dict): Dictionary containing the user's responses.
        search_string (str): The search string used to filter emails.

    Returns:
        bool: True if deletions are handled successfully.
    """
    logger.info("Handling deletions...")

    print(
        f"Number of emails to be deleted using gmail filter: ({search_string}): {gmail.count_msgs(msg_ids)}"
    )
    if responses.get("delete_immediately") == "y":
        gmail.delete_msgs(msg_ids)
    else:
        logger.info("Skipping deletion")

    if responses.get("delete_immediately") == "n":
        get_continue_confirmation("Would you like to delete now")
        gmail.delete_msgs(msg_ids)
        logger.info("Deletion complete")

    return True


def get_continue_confirmation(question: str) -> str:
    """
    Prompt the user to confirm if they would like to continue.

    Args:
        question (str): The question to be asked.

    Returns:
        str: The user's response ('y' or 'n').
    """
    question = [{"description": question}]
    response = YesNoQuestionHandler(question).run()
    if response[0] == "n":
        logger.info("Exiting program")
        exit()
    else:
        return response[0]


def get_date_input() -> str:
    """
    Prompt the user to enter a date for filtering emails.

    Returns:
        str: The user's date input.
    """
    date_handler = DateQuestionHandler("What date would you like to clean up until?")
    date_handler.run()
    logger.info(f"Filter date: {date_handler.values}")
    return date_handler.values


def get_delete_input() -> str:
    """
    Prompt the user to confirm if they would like to delete emails immediately.

    Returns:
        str: The user's response ('y' or 'n').
    """
    question = [{"description": "Would you like to delete immediately"}]
    response = YesNoQuestionHandler(question).run()
    return response[0]


def get_credentials() -> dict:
    """
    Retrieve the user's Gmail credentiale to authenticate later

    Returns:
        dict: Dictionary containing the user's email and password.
    """

    logger.info("Retrieving credentials...")

    if os.getenv("GMAIL_USER") is None or os.getenv("GMAIL_PASSWORD") is None:
        question_user = {
            "question": "What is your gmail address?",
            "format": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "validation": "Must be a valid email address",
            "sensitive": False,
        }
        question_pw = {
            "question": "What is your password? (must be an app password if using 2FA)",
            "format": r"^.{1,30}$",
            "validation": "Must be less than 30 characters",
            "sensitive": True,
        }
        return {
            "email": ValueQuestionHandler(question_user).run(),
            "password": ValueQuestionHandler(question_pw).run(),
        }
    else:
        return {
            "email": os.getenv("GMAIL_USER"),
            "password": os.getenv("GMAIL_PASSWORD"),
        }


def main():
    """
    Main function to run the Gmail Cleaner CLI application.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-log",
        "--loglevel",
        default="notset",
        help="Provide logging level. Example --loglevel debug, default=notset",
    )
    args = parser.parse_args()

    if args.loglevel.lower() != "notset":
        logging.basicConfig(
            level=args.loglevel.upper(), format="%(levelname)s: %(message)s"
        )

    print(return_logo())
    print("Welcome to the Gmail Cleaner CLI")
    print("*******************************")

    creds = get_credentials()
    gmail = SMPTClient(
        server="imap.gmail.com",
        port=993,
        user=os.getenv("GMAIL_USER", creds.get("email")),
        password=os.getenv("GMAIL_PASSWORD", creds.get("password")),
    )
    gmail.connect()

    get_general_stats(gmail)

    filter_date = get_date_input()
    filters, search_string = get_commands_choices()

    responses = {
        "date_until": filter_date,
        "delete_immediately": get_delete_input(),
        "included_filters": filters,
        "search_string": search_string,
    }
    msg_ids = gmail.get_msg_ids(search_string, responses.get("date_until"))

    get_response_summary(responses)
    get_continue_confirmation("Would you like to continue")
    handle_deletions(gmail, msg_ids, responses, search_string)

    gmail.close()

    print("Thank you for using the Gmail Cleaner CLI. Goodbye!")


if __name__ == "__main__":
    main()
