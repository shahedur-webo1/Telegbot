# Install necessary packages
# pip install pyTelegramBotAPI Flask

import telebot
from flask import Flask, request

app = Flask(name)
TOKEN = "7182878685:AAEFlDxQWXqp3b1KfPW8qWGRMfe6FLp-5Jg"
API_KEY = "YOUR_WEBSITE_API_KEY"  # Replace with your website API key
bot = telebot.TeleBot(7182878685:AAEFlDxQWXqp3b1KfPW8qWGRMfe6FLp-5Jg)

# Temporary data storage (replace with a database in a production environment)
users = {}

# Define conversation states
SIGN_UP, LOGIN, PAY_NOW, GET_IP_NOW = range(4)

# Handlers for commands
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to the Proxy IP Selling Bot! Please use /SIGN_UP to get started.")

@bot.message_handler(commands=['SIGN_UP'])
def sign_up(message):
    bot.reply_to(message, "Please enter your desired username:")
    bot.register_next_step_handler(message, save_username)

def save_username(message):
    user_id = message.from_user.id
    username = message.text

    users[user_id] = {"username": username}
    bot.reply_to(message, f"Username set to {username}. Now, please use /LOGIN.")
    bot.register_next_step_handler(message, login)

@bot.message_handler(commands=['LOGIN'])
def login(message):
    bot.reply_to(message, "Please enter your username to log in:")
    bot.register_next_step_handler(message, check_login)

def check_login(message):
    user_id = message.from_user.id
    username = message.text

    if user_id in users and users[user_id]["username"] == username:
        bot.reply_to(message, "Login successful!")
    else:
        bot.reply_to(message, "Invalid username. Please use /LOGIN again.")

@bot.message_handler(commands=['PAY_NOW'])
def pay_now(message):
    bot.reply_to(message, "Choose a payment method:",
                 reply_markup=telebot.types.ReplyKeyboardMarkup([['Bkash', 'Nagad', 'Rocket']],
                                                               one_time_keyboard=True))
    bot.register_next_step_handler(message, handle_payment)

def handle_payment(message):
    user_id = message.from_user.id
    payment_method = message.text

    # Handle payment logic here (e.g., integrate with payment gateway)
    # Save payment information to users[user_id] if payment is successful

    bot.reply_to(message, "Payment successful! You can now use /GET_IP_NOW.")

@bot.message_handler(commands=['GET_IP_NOW'])
def get_ip_now(message):
    user_id = message.from_user.id

    # Check if the user is registered and has paid
    if user_id in users and "payment_info" in users[user_id]:
        # Call your website API to get a proxy IP
        proxy_ip = get_proxy_ip_from_website_api()

        bot.reply_to(message, f"Your proxy IP: {proxy_ip}")
    else:
        bot.reply_to(message, "You need to complete the payment first. Please use /PAY_NOW.")

# Flask route to receive payment webhook
@app.route('/payment_webhook', methods=['POST'])
def payment_webhook():
    # Handle payment webhook logic here
    return 'OK'

if name == 'main':
    # Start the Flask app in a separate thread
    import threading
    threading.Thread(target=app.run, kwargs={'debug': True, 'port': 5000}).start()

    # Start the Telegram bot
    bot.polling(none_stop=True)
