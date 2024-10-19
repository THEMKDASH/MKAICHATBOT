import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set your Hugging Face API token
api_token = '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'
headers = {
    'Authorization': f'Bearer {api_token}'
}

# Function to send questions to Hugging Face API and get an answer
def ask_hugging_face(question):
    model = 'gpt2'  # Change this to your desired model
    data = {
        'inputs': question
    }
    response = requests.post(f'https://api-inference.huggingface.co/models/{model}', headers=headers, json=data)
    
    if response.status_code == 200:
        # Extract the generated text from the response
        generated_text = response.json()[0]['generated_text']  # Access the first result
        return generated_text
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function that runs when someone sends a message to the bot
def handle_message(update, context):
    user_message = update.message.text  # Get the user's message
    bot_response = ask_hugging_face(user_message)  # Ask the Hugging Face API
    update.message.reply_text(bot_response)  # Send back the response

# Start command, sent when a user types /start
def start(update, context):
    update.message.reply_text('Hello! Ask me anything.')

# Set up the bot
def main():
    updater = Updater('7565429497:AAGZMrzmELwUb4Nv1aC1vaJQH01SCJFxln8', use_context=True)
    dp = updater.dispatcher

    # Respond to /start command
    dp.add_handler(CommandHandler("start", start))

    # Respond to any text message
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()