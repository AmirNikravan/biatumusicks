from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import uuid
from tinydb import TinyDB, Query

# Initialize the database
db = TinyDB('db.json')
Text = Query()

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
    text = update.message.text
    unique_id = str(uuid.uuid4())
    db.insert({'id': unique_id, 'text': text})
    link = f'https://t.me/{context.bot.username}?start={unique_id}'
    await update.message.reply_text(f'Here is your link: {link}')

def main():
    app = ApplicationBuilder().token("7356594695:AAHkmaSEnbn_LPRAWf3xW7sl4HAg33ddxoQ").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == '__main__':
    main()
