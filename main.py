import os
import discord
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get tokens from .env
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Set up Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Function to get Gemini's response
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini API Error: {str(e)}"

# When bot is ready
@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

# When someone sends a message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # If user asks about creator
    lower_msg = message.content.lower()
    if "who made you" in lower_msg or "who created you" in lower_msg:
        await message.channel.send(
            "🤖 I was created by **Google (Gemini AI)** and developed by **Lokesh Shadani** 🚀"
        )
        return

    # If message starts with !ask, send to Gemini
    if message.content.startswith("!ask"):
        prompt = message.content[len("!ask "):].strip()
        if not prompt:
            await message.channel.send("⚠️ Please provide a question!")
            return

        await message.channel.send("🤖 Thinking...")
        reply = get_gemini_response(prompt)
        await message.channel.send(reply)

# Run the Discord bot
client.run(DISCORD_TOKEN)
