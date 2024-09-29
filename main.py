from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    # Maintenance message
    update.message.reply_text("🚧 Bot is down for maintenance. Stay connected!")

    # Prepare inline buttons for channel and support chat
    keyboard = [
        [
            InlineKeyboardButton("Join Channel", url="https://t.me/alcyonebots"),
            InlineKeyboardButton("Join Support", url="https://t.me/alcyone_support")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the inline buttons
    update.message.reply_text("Please check out our channels for updates!", reply_markup=reply_markup)

def main() -> None:
    updater = Updater("7488772903:AAGP-ZvbH7K2XzYG9vv-jIsA12iRxTeya3U")

    # Add command handler
    updater.dispatcher.add_handler(CommandHandler("start", start))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
