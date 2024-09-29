import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import youtube_dl
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a folder for downloads if it doesn't exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')

def start(update: Update, context: CallbackContext) -> None:
    bot_username = context.bot.get_me().username  # Get the bot's username
    
    keyboard = [
        [
            InlineKeyboardButton("Join Channel", url="https://t.me/alcyonebots"),
            InlineKeyboardButton("Join Support", url="https://t.me/alcyone_support")
        ],
        [
            InlineKeyboardButton("Add me to your groups +", url=f"https://t.me/{bot_username}?startgroup=true")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    image_url = "https://i.imghippo.com/files/OTItE1727595318.jpg"
    
    # Send the image with the caption
    update.message.reply_photo(
        photo=image_url,
        caption=(
            "𝗛𝗶 𝘁𝗵𝗲𝗿𝗲 👋🏻\n"
            "Welcome to 𝗩𝗶𝗱𝗲𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿 𝗕𝗼𝘁 𝗯𝘆 𝗔𝗹𝗰𝘆𝗼𝗻𝗲, your go-to bot for downloading high-quality content from all the top social platforms!! 🎬\n"
            "𝗛𝗼𝘄 𝗱𝗼𝗲𝘀 𝗶𝘁 𝘄𝗼𝗿𝗸?\n"
            "◎ Start a chat with @AlcDownloaderBot and send /start\n"
            "◎ In group send /start and then send the link of the video while replying me!!\n\n"
            "Join our channel and support group to use the bot\n\n"
            "Let's Get Started 👾"
        ),
        reply_markup=reply_markup
    )

def download_video(url: str, update: Update) -> str:
    options = {
        'format': 'best',
        'outtmpl': os.path.join('downloads', '%(title)s.%(ext)s'),  # Save with title
        'cookiefile': 'cookies.txt',  # Use cookies from the specified file
        'quiet': False,
        'progress_hooks': [progress_hook],
    }

    def progress_hook(d):
        if d['status'] == 'downloading':
            total_size = d.get('total_bytes', 0)
            downloaded_size = d.get('downloaded_bytes', 0)
            progress = downloaded_size / total_size * 100 if total_size > 0 else 0
            logger.info(f'Download progress: {progress:.2f}%')
    
    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])
        return os.path.join('downloads', f"{ydl.extract_info(url, download=False)['title']}.mp4")
    except Exception as e:
        logger.error(f"Error while downloading: {str(e)}")
        raise e

def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text.startswith("https://") or text.startswith("http://"):
        try:
            video_path = download_video(text, update)
            update.message.reply_video(video=open(video_path, 'rb'))
            os.remove(video_path)  # Clean up by removing the file after sending
        except Exception as e:
            update.message.reply_text(f"Error downloading video: {str(e)}")
    else:
        update.message.reply_text("Please send a valid video URL.")

def main() -> None:
    updater = Updater("7488772903:AAGP-ZvbH7K2XzYG9vv-jIsA12iRxTeya3U")

    # Add command handlers
    updater.dispatcher.add_handler(CommandHandler("start", start))
    
    # Add message handler for group chat
    updater.dispatcher.add_handler(MessageHandler(Filters.reply & Filters.text, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
