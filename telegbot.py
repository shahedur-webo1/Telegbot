from flask import Flask, request
from telegram import Bot, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext, Updater

app = Flask(__name__)
TOKEN = "7023674671:AAHAqeb4AwDo3obBO96CsBxrkJ8mh_Ex82c"
WEBSITE_API_KEY = "YOUR_WEBSITE_API_KEY"

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher
 
SIGN_UP, LOGIN, PAY_NOW, GET_IP_NOW = range(4)

users = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Proxy IP Selling Bot! Please use /SIGN_UP to get started.")

def sign_up(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter your desired username:")
    return SIGN_UP

def save_username(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.text

    users[user_id] = {"username": username}
    update.message.reply_text(f"Username set to {username}. Now, please use /LOGIN.")
    return LOGIN

def login(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter your username to log in:")
    return LOGIN

def check_login(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.text

    if user_id in users and users[user_id]["username"] == username:
        update.message.reply_text("Login successful!")
        return ConversationHandler.END
    else:
        update.message.reply_text("Invalid username. Please use /LOGIN again.")
        return LOGIN

def pay_now(update: Update, context: CallbackContext):
    update.message.reply_text("Choose a payment method:",
                              reply_markup=ReplyKeyboardMarkup([['Bkash', 'Nagad', 'Rocket']],
                                                               one_time_keyboard=True))
    return PAY_NOW

def handle_payment(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    payment_method = update.message.text

    # Handle payment logic here (e.g., integrate with payment gateway)
    # Save payment information to users[user_id] if payment is successful

    users[user_id]["payment_info"] = {"method": payment_method}
    update.message.reply_text("Payment successful! You can now use /GET_IP_NOW.",
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def get_ip_now(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if user_id in users and "payment_info" in users[user_id]:
        # Call your website API to get a proxy IP
        proxy_ip = get_proxy_ip_from_website_api()

        update.message.reply_text(f"Your proxy IP: {proxy_ip}")
    else:
        update.message.reply_text("You need to complete the payment first. Please use /PAY_NOW.")

dp.add_handler(CommandHandler("start", start))
dp.add_handler(ConversationHandler(
    entry_points=[CommandHandler('SIGN_UP', sign_up)],
    states={
        SIGN_UP: [MessageHandler(Filters.text & ~Filters.command, save_username)],
        LOGIN: [CommandHandler('LOGIN', login), MessageHandler(Filters.text & ~Filters.command, check_login)],
        PAY_NOW: [CommandHandler('PAY_NOW', pay_now)],
        GET_IP_NOW: [CommandHandler('GET_IP_NOW', get_ip_now)]
    },
    fallbacks=[]
))

@app.route('/payment_webhook', methods=['POST'])
def payment_webhook():
    # Handle payment webhook logic here
    return 'OK'

if __name__ == '__main__':
    import threading
    threading.Thread(target=app.run, kwargs={'debug': True, 'port': 5000}).start()
    updater.start_polling()
    updater.idle()
