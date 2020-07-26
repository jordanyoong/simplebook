import requests
import json
from datetime import datetime
from scheduler import book_timeslot
import re 
import telegramcalendar

from config import TELEGRAM_SEND_MESSAGE_URL, TOKEN

class TelegramBot:

    def __init__(self):
        """"
        Initializes an instance of the TelegramBot class.

        Attributes:
            chat_id:str: Chat ID of Telegram chat, used to identify which conversation outgoing messages should be send to.
            text:str: Text of Telegram chat
            first_name:str: First name of the user who sent the message
            last_name:str: Last name of the user who sent the message
        """

        self.chat_id = None
        self.text = None
        self.first_name = None
        self.last_name = None
        self.accounts = {}
        self.venues = ['Room 1', 'Room 2', 'Room 3', 'Room 4']
        self.book_date = None
        self.book_time = None


    def parse_webhook_data(self, data):
        """
        Parses Telegram JSON request from webhook and sets fields for conditional actions

        Args:
            data:str: JSON string of data
        """

        message = data['message']

        self.chat_id = message['chat']['id']
        self.incoming_message_text = message['text'].lower()
        self.first_name = message['from']['first_name']
        if 'last_name' in message['from']:
            self.last_name = message['from']['last_name']


    def action(self):
        """
        Conditional actions based on set webhook data.

        Returns:
            bool: True if the action was completed successfully else false
        """

        success = None
        msg = self.incoming_message_text


        if msg == '/start':
            text = 'Welcome to SimpleBook_Bot!\nI can help you book an venue.\
            \n\nYou can control me using these commands:\n\
            /start-to start chatting with the bot\n\
            /book-to make a booking\n\
            /cancel-to stop chatting with the bot.\n\
            For more information please contact simplebook@gmail.com'

            if self.last_name == None:
                self.outgoing_message_text = "Hello {}! ".format(self.first_name) + text
            else :
                self.outgoing_message_text = "Hello {} {}! ".format(self.first_name, self.last_name) + text
        elif msg == '/book':
            self.outgoing_message_text = "Please enter a date in this format: YYYY-MM-DD"
            
        elif msg == '/cancel':
            self.outgoing_message_text = "See you again!"

        else:
            try:
                datetime.strptime(msg, '%Y-%m-%d')
                self.outgoing_message_text = 'Please enter a start time in the format: HH-MM'
            except:
                try:
                    datetime.strptime(msg, '%H:%M')
                    self.outgoing_message_text = 'Start time: ' + msg + ' Please enter an end time in the format: HH-MM'
                except:
                    self.outgoing_message_text = 'Invalid format, please try again'
                    return False
            
        success = self.send_message()
        return success


    def send_message(self):
        """
        Sends message to Telegram servers.
        """

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False
    

    @staticmethod
    def init_webhook(url):
        """
        Initializes the webhook

        Args:
            url:str: Provides the telegram server with a endpoint for webhook data
        """

        requests.get(url)

    

    def book_time(time):
        print("hello worlds")

