import logging
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.error import BadRequest
import random

# Bot token and channel username (replace with your details)
BOT_TOKEN = "7993719241:AAE6ItGn4ciaJv8c_Hjwlt01lTqhuqj9j8Q"
CHANNEL_USERNAME = "@testifychannelbot"

# Initialize bot
bot = Bot(token=BOT_TOKEN)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Predefined list of items (url and image pairs)
ITEMS = [
    {"url": "https://xpshort.com/XOVwc", "image": "https://ibb.co/rb0dHzC"},
    {"url": "https://xpshort.com/ZEq6U7", "image": "https://ibb.co/G9w84Sq"},
    {"url": "https://xpshort.com/7Sk6", "image": "https://ibb.co/0CsV3JQ"},
    {"url": "https://xpshort.com/3YozfHw", "image": "https://ibb.co/CpybSMk"},
    {"url": "https://xpshort.com/Fc1B", "image": "https://ibb.co/7NGTRnb"},
    {"url": "https://xpshort.com/KocqkUY", "image": "https://ibb.co/hMWnPWf"},
    {"url": "https://xpshort.com/2Xsk", "image": "https://ibb.co/DbxHSWh"},
    {"url": "https://xpshort.com/oRUh", "image": "https://ibb.co/KsJwPwf"},
    {"url": "https://xpshort.com/E9uC", "image": "https://ibb.co/9tLFYCJ"},
    {"url": "https://xpshort.com/Zufbw", "image": "https://ibb.co/ThNxxwH"},
    {"url": "https://xpshort.com/x4fy33", "image": "https://ibb.co/1MgD33R"},
    {"url": "https://xpshort.com/wyDYGvfa", "image": "https://ibb.co/HVx5vyK"},
    {"url": "https://xpshort.com/VXL59", "image": "https://ibb.co/H7jw0Nz"},
    {"url": "https://xpshort.com/KkGFdy", "image": "https://ibb.co/NYx3qWY"},
    {"url": "https://xpshort.com/FGffFNC", "image": "https://ibb.co/fMK7jPV"},
    {"url": "https://xpshort.com/MZMPf", "image": "https://ibb.co/3cW59W0"},
    {"url": "https://xpshort.com/T7MdpKwp", "image": "https://ibb.co/mHTqkY0"},
    {"url": "https://xpshort.com/0zqS", "image": "https://ibb.co/ch9nCSs"},
    {"url": "https://xpshort.com/mPg0lb", "image": "https://ibb.co/8949FH8"},
]

# Access denied photo URL
ACCESS_DENIED_PHOTO = "https://upload.wikimedia.org/wikipedia/en/thumb/6/68/Telegram_access_denied.jpg/800px-Telegram_access_denied.jpg?20200919053248"

# Check if the user has joined the channel
def check_channel_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Error checking membership: {e}")
        return False

# Start command
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if check_channel_membership(user_id):
        welcome_message = "Welcome to the bot! Here are the commands you can use:\n\n" \
                          "/gen - Get a random item\n" \
                          "/alive - Check if the bot is running\n" \
                          "/help - Get help\n" \
                          "/vip - Access VIP content"
        update.message.reply_text(welcome_message)
    else:
        keyboard = [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        caption = "Access Denied 🚫\n\nYou must join the channel to use the bot."
        update.message.reply_photo(photo=ACCESS_DENIED_PHOTO, caption=caption, reply_markup=reply_markup)

# Generate command
def gen(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if check_channel_membership(user_id):
        item = random.choice(ITEMS)
        try:
            caption = f"Enjoy mawa...❤️: [Click Here]({item['url']})"
            update.message.reply_photo(photo=item["image"], caption=caption, parse_mode='Markdown')
        except BadRequest as e:
            logger.error(f"Failed to send photo: {e}")
            update.message.reply_text("Oops! There was an issue with sending the photo. Please try again later.")
    else:
        keyboard = [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        caption = "Access Denied 🚫\n\nYou must join the channel to use the bot."
        update.message.reply_photo(photo=ACCESS_DENIED_PHOTO, caption=caption, reply_markup=reply_markup)

# Alive command
def alive(update: Update, context: CallbackContext):
    update.message.reply_text("The bot is alive! 😊")

# Help command
def help_command(update: Update, context: CallbackContext):
    help_message = "Here are the commands you can use:\n\n" \
                   "/gen - Get a random item\n" \
                   "/alive - Check if the bot is running\n" \
                   "/help - Get help\n" \
                   "/vip - Access VIP content"
    update.message.reply_text(help_message)

# VIP command
def vip(update: Update, context: CallbackContext):
    update.message.reply_text("VIP content coming soon! 🔥")

# Error handler
def error_handler(update: Update, context: CallbackContext):
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        update.message.reply_text("An error occurred. Please try again later.")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("gen", gen))
    dispatcher.add_handler(CommandHandler("alive", alive))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("vip", vip))

    # Register the error handler
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
