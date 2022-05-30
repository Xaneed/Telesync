import os
import re
from pyrogram import Client
from configparser import ConfigParser

# Load config
config = ConfigParser()
config.read('config.ini')

# Setting up
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
chat_id = int(config['Telegram']['chat_id'])
path = config['App']['path']

# Create application instance
app = Client('userbot', api_id, api_hash)

async def main():
  async with app:
    async for message in app.get_chat_history(chat_id):
      if message.audio:
        ext = os.path.splitext(message.audio.file_name)
        filename = message.audio.performer + ' - ' + message.audio.title + ext[1]

        pattern = re.compile(r'[^\w\s\d.\-_()]')
        filename = re.sub(pattern, "", filename)

        filename = path + filename

        if not os.path.exists(filename):
            await app.download_media(message, filename, progress=progress, progress_args=[filename])
            print('', end='\n')

async def progress(current, total, filename):
    print('', end='\r')
    print(filename, end='  ')
    print(f"{current * 100 / total:.1f}%", end='\r')

# Run application
app.run(main())