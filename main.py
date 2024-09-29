import os
import logging
from pytube import YouTube
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to handle the download progress
def progress_callback(stream, chunk, bytes_remaining, update):
    total_size = stream.filesize
    downloaded = total_size - bytes_remaining
    percent = (downloaded / total_size) * 100
    
    # Send progress update to the user
    update.message.reply_text(f'Downloaded: {downloaded} of {total_size} bytes ({percent:.2f}%)')

# Function to download YouTube videos using cookies
def download_youtube_video(url: str, update: Update) -> str:
    yt = YouTube(url, on_progress_callback=lambda s, c, b: progress_callback(s, c, b, update), cookies='cookies.txt')
    stream = yt.streams.get_highest_resolution()  # Get the highest resolution stream
    output_path = 'downloads/' + stream.default_filename  # Set the output path
    
    # Start the download
    stream.download(output_path)  # Download the video
    return output_path  # Return the file path

# Function to download Instagram Reels using cookies
def download_instagram_reel(url: str, update: Update) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    
    # Use requests to get the page content
    session = requests.Session()
    session.cookies.load('cookies.txt', ignore_discard=True, ignore_expires=True)  # Load Instagram cookies
    response = session.get(url, headers=headers)
    
    # Here you need to parse the response content to get the video URL
    # This is a simplified example; you may need to adjust this based on the actual HTML structure
    if 'video_url' in response.text:
        video_url = response.text.split('video_url":"')[1].split('"')[0]
        video_path = 'downloads/reel.mp4'  # Set the output path
        
        # Download the video
        video_response = session.get(video_url)
        with open(video_path, 'wb') as video_file:
            video_file.write(video_response.content)
        return video_path
    else:
        raise Exception("Could not find the video URL in the response.")

# Start command handler
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

# Video download handler
def handle_message(update: Update, context: CallbackContext) -> None:
    # Ensure the bot only responds to its own messages
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        url = update.message.text
        try:
            update.message.reply_text("Starting download...")
            if 'youtube.com' in url or 'youtu.be' in url:
                video_path = download_youtube_video(url, update)  # Download the YouTube video
            elif 'instagram.com' in url:
                video_path = download_instagram_reel(url, update)  # Download the Instagram Reel
            else:
                update.message.reply_text("Unsupported URL. Please provide a YouTube or Instagram link.")
                return
            
            with open(video_path, 'rb') as video_file:
                update.message.reply_video(video_file, caption="Here is your video!")  # Send the video file
        except Exception as e:
            logger.error(f"Error while downloading: {str(e)}")  # Log the error
            update.message.reply_text(f"Error: {str(e)}")  # Send error message to the user
    else:
        update.message.reply_text("Please reply to my message with the YouTube or Instagram video link.")

# Error handler
def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(f"Update {update} caused error {context.error}")
    if update.effective_message:
        update.effective_message.reply_text("An unexpected error occurred. Please try again later.")

def main() -> None:
    # Create updater and dispatcher
    updater = Updater("7488772903:AAGP-ZvbH7K2XzYG9vv-jIsA12iRxTeya3U", use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Add error handler
    dp.add_error_handler(error_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    os.makedirs('downloads', exist_ok=True)  # Create downloads folder if it doesn't exist
    main()
