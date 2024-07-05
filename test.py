from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import uuid
from tinydb import TinyDB, Query

# Initialize the database
db = TinyDB('db.json')
Text = Query()

# Table for users
user_db = db.table('users')
User = Query()

# Replace with your admin user IDs
ADMIN_USER_IDS = {6792857415, 987654321}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    # Save user information to the database
    if not user_db.contains(User.id == user_id):
        user_db.insert({'id': user_id, 'username': username, 'first_name': first_name, 'last_name': last_name})

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
    keyboard = [
        [InlineKeyboardButton("مشاهده یوزر ها", callback_data='glass_button_users')],
        [InlineKeyboardButton("Glass Button 2", callback_data='glass_button_2')],
        [InlineKeyboardButton("Glass Button 3", callback_data='glass_button_3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome to your dashboard!', reply_markup=reply_markup)

# Define individual button click handlers
async def handle_glass_button_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # Retrieve all users from the user database
    users = user_db.all()
    
    if users:
        user_info = "\n".join([f"ID: {user['id']}, Username: @{user['username']}, Name: {user.get('first_name', '')} {user.get('last_name', '')}" for user in users])
        message_text = f"List of all users:\n{user_info}"
    else:
        message_text = "No users found."
    
    await query.edit_message_text(text=message_text)

async def handle_glass_button_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="You pressed Glass Button 2!")

async def handle_glass_button_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="You pressed Glass Button 3!")

def main():
    app = ApplicationBuilder().token("7356594695:AAHkmaSEnbn_LPRAWf3xW7sl4HAg33ddxoQ").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", show_dashboard))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Add individual handlers for each button click
    app.add_handler(CallbackQueryHandler(handle_glass_button_users, pattern='^glass_button_users$'))
    app.add_handler(CallbackQueryHandler(handle_glass_button_2, pattern='^glass_button_2$'))
    app.add_handler(CallbackQueryHandler(handle_glass_button_3, pattern='^glass_button_3$'))

    app.run_polling()

if __name__ == '__main__':
    main()