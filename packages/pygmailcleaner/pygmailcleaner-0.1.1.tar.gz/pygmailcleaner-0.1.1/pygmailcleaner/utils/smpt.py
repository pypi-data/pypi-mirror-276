import imaplib
import logging
import os
import datetime 

from ..utils import formatting

logger = logging.getLogger()

# get todays date str using datetime
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")

# standard GMAIL folders
MAIN_FOLDER = os.getenv("FOLDER_TO_DELETE_FROM", '"[Google Mail]/All Mail"')
TRASH_FOLDER = os.getenv("TRASH_FOLDER", '"[Google Mail]/Trash"')

class SMPTClient:
    def __init__(self, server, port, user, password):
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.imap = None  # Initialize imap variable
    
    def connect(self, FOLDER=MAIN_FOLDER):
        """
        Connect to a server and folder
        """
        try:
            self.imap = imaplib.IMAP4_SSL(self.server, self.port)
            self.imap.login(self.user, self.password)
            print("Connected to gmail")
            self.imap.select(FOLDER)
        except Exception as e:
            raise ConnectionError(f"Could not connect to server: {e}")
    
    def close(self,):
        """
        Close the connection
        """
        try:
            if self.imap is None:
                print("No open connection")
            else:
                self.imap.close()
                self.imap.logout()
                print("Connection closed")
        except Exception as e:
            raise RuntimeError(f"Error occurred while closing the connection: {e}")
    
    def get_msg_ids(self, method, date_until=datetime.datetime.now().strftime("%Y-%m-%d")) -> str:
        """
        Gets a list of message ids based on method and date in the format "1,2,3,4"
        """
        try:
            search = f'"{method} before:{formatting.get_unix_timestamp(date_until)}"'
            logger.debug(f"Search string: {search}")
            typ, [msg_ids] = self.imap.search(None, "X-GM-RAW", search)
            if isinstance(msg_ids, bytes):
                msg_ids = msg_ids.decode()
                msg_ids = ",".join(msg_ids.split(" "))
            return msg_ids
        except Exception as e:
            raise RuntimeError(f"Error occurred while getting message ids: {e}")
    
    def count_msgs(self, msg_ids) -> int:
        """
        Parse the string message ids split by a comma and return the number of emails
        """
        try:
            if msg_ids == "":
                return 0
            else:
                return len(msg_ids.split(","))
        except Exception as e:
            raise RuntimeError(f"Error occurred while counting messages: {e}")

    def delete_msgs(self, msg_ids):
        """
        Delete emails based on method and date
        """
        try:
            number_of_msgs = self.count_msgs(msg_ids)
            if msg_ids == "":
                print("No emails matching search criteria")
            else:
                print(f"Moving {number_of_msgs} to Trash")
                self.imap.store(msg_ids, "+X-GM-LABELS", "\\Trash")
                print("Emptying Trash")
                self.imap.select(TRASH_FOLDER)
                self.imap.store("1:*", "+FLAGS", "\\Deleted")
                self.imap.expunge()
        except Exception as e:
            raise RuntimeError(f"Error occurred while deleting messages: {e}")
