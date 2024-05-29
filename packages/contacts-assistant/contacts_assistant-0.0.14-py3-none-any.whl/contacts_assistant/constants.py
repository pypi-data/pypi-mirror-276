"""
A module containing configuration settings for a application.

Constants:
    DATE_FORMAT (str): The format string for dates.
    CONTACTS_BOOK_FILENAME (str): The filename for the contacts book file.
    NOTEBOOK_FILENAME (str): The filename for the notebook file.
    MENU_BORDER (str): The border style for the menu.
    GREETING_BANNER (str): The text displayed as a greeting.
    INPUT_STYLE (dict): The style settings for input prompts.
"""

DATE_FORMAT = "%d.%m.%Y"
CONTACTS_BOOK_FILENAME = "./contacts_book.pkl"
NOTEBOOK_FILENAME = "./notebook.json"
MENU_BORDER = f"{'-'*116}\n"
GREETING_BANNER = """
  ___          _     _              _     _           _   
 / _ \        (_)   | |            | |   | |         | |  
/ /_\ \___ ___ _ ___| |_ __ _ _ __ | |_  | |__   ___ | |_ 
|  _  / __/ __| / __| __/ _` | '_ \| __| | '_ \ / _ \| __|
| | | \__ \__ \ \__ \ || (_| | | | | |_  | |_) | (_) | |_ 
\_| |_/___/___/_|___/\__\__,_|_| |_|\__| |_.__/ \___/ \__|
"""
INPUT_STYLE = {
    "completion-menu.completion": "bg:#008888 #ffffff",
    "completion-menu.completion.current": "bg:#00aaaa #000000",
    "scrollbar.background": "bg:#88aaaa",
    "scrollbar.button": "bg:#222222",
    "prompt": "#47C959",
    "prompt.arg.text": "#00aaaa",
}
MAX_SIMBOLS_IN_ROW = 80
