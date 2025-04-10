import os
import discord
from discord.ext import commands
from linkvertise import LinkvertiseClient

# 🔧 Pobierz zmienne środowiskowe
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LINKVERTISE_ID = int(os.getenv("LINKVERTISE_ID"))  # musi być int

# Inicjalizacja klienta linkvertise
lv_client = LinkvertiseClient()

# Inicjalizacja bota
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("http://") or message.content.startswith("https://"):
        try:
            monetized_link = lv_client.linkvertise(LINKVERTISE_ID, message.content)
            await message.channel.send(f"Oto Twój link z Linkvertise: {monetized_link}")
        except Exception as e:
            await message.channel.send(f"Wystąpił błąd: {str(e)}")

    await bot.process_commands(message)

# Start bota
bot.run(DISCORD_TOKEN)
