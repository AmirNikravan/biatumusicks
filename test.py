from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import uuid
from tinydb import TinyDB, Query

# Initialize the database
db = TinyDB('db.json')
Text = Query()

# Replace with your admin user IDs
ADMIN_USER_IDS = {6792857415, 987654321}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if args:  # Check if there are arguments passed with the command
        unique_id = args[0]
        result = db.search(Text.id == unique_id)
        if result:
            await update.message.reply_text(f'{result[0]["text"]}')
        else:
            await update.message.reply_text('Invalid link or text not found.')
    else:
        await update.message.reply_text('Welcome! Send me any text, and I will generate a link for you to retrieve it.')

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    # Check if the sender is an admin
    if user_id not in ADMIN_USER_IDS:
        await update.message.reply_text("Sorry, only admins can send text to this bot.")
        return
    
    # Process the text message
    text = update.message.text
    unique_id = str(uuid.uuid4())
    db.insert({'id': unique_id, 'text': text})
    link = f'https://t.me/{context.bot.username}?start={unique_id}'
    await update.message.reply_text(f'Here is your link: {link}')

async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Glass Button", callback_data='glass_button')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome to your dashboard!', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    # Always answer callback queries, even if no action is needed to acknowledge the query.
    await query.answer()

    await query.edit_message_text(text="Button pressed!")

def main():
    app = ApplicationBuilder().token("7356594695:AAHkmaSEnbn_LPRAWf3xW7sl4HAg33ddxoQ").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", show_dashboard))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == '__main__':
    main()
