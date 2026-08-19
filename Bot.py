import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream.input_audio_stream import InputAudioStream
import yt_dlp

# Heroku Config Vars se values lena
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Bot client setup
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call = PyTgCalls(app)

# YouTube audio extract function
def get_audio_url(url):
    ydl_opts = {'format': 'bestaudio'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url']

# Play command
@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        await message.reply("Usage: /play <YouTube URL>")
        return
    url = message.command[1]
    audio_url = get_audio_url(url)
    await call.join_group_call(
        message.chat.id,
        InputStream(
            InputAudioStream(audio_url)
        )
    )
    await message.reply(f"🎶 Now playing: {url}")

# Stop command
@app.on_message(filters.command("stop"))
async def stop(_, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("⏹️ Music stopped.")

# Start bot
app.start()
call.start()
idle()
