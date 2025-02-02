import os
import logging
from PIL import Image, ImageDraw
from rembg import remove
from io import BytesIO
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me an image and I will remove its background.')

# Function to handle image background removal
def remove_bg(update: Update, context: CallbackContext) -> None:
    # Get image file from the user
    file = update.message.photo[-1].get_file()
    file.download('user_image.png')
    
    # Open image and remove background
    with open('user_image.png', 'rb') as f:
        input_data = f.read()
    output_data = remove(input_data)

    # Save output image
    output_image = 'output_image.png'
    with open(output_image, 'wb') as f:
        f.write(output_data)

    # Send the processed image back to the user
    with open(output_image, 'rb') as f:
        update.message.reply_photo(photo=f)

# Erase a specific part of the image (using PIL for simple rect area)
def erase_part(update: Update, context: CallbackContext) -> None:
    image_path = 'output_image.png'  # Assuming the background removed image is saved
    image = Image.open(image_path)
    
    # Erase a part (simple example: creating a white rectangle)
    draw = ImageDraw.Draw(image)
    draw.rectangle([(50, 50), (150, 150)], fill="white")  # Erase part of image
    
    image.save('erased_image.png')

    with open('erased_image.png', 'rb') as f:
        update.message.reply_photo(photo=f)

# Restore erased part (or simple undo)
def restore_part(update: Update, context: CallbackContext) -> None:
    image_path = 'output_image.png'  # Assuming original background removed image
    image = Image.open(image_path)
    
    # Simple restore (Example: drawing a rectangle over erased part)
    draw = ImageDraw.Draw(image)
    draw.rectangle([(50, 50), (150, 150)], fill="black")  # Restore part of image
    
    image.save('restored_image.png')

    with open('restored_image.png', 'rb') as f:
        update.message.reply_photo(photo=f)

# Main function to set up the bot
def main() -> None:
    # Your Telegram Bot Token
    token = 'YOUR_BOT_TOKEN'
    
    updater = Updater(token)

    dispatcher = updater.dispatcher

    # Commands
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Message handlers
    dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, remove_bg))
    
    # Handlers for erasing and restoring parts of the image
    dispatcher.add_handler(CommandHandler("erase", erase_part))
    dispatcher.add_handler(CommandHandler("restore", restore_part))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()