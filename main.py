import os
import discord
from discord.ext import commands
from linkvertise import LinkvertiseClient
from flask import Flask
import threading
from discord.ui import Button, View

# 🔧 Minimalny serwer HTTP do zadowolenia Rendera
app = Flask('')

@app.route('/')
def home():
    return "Bot działa!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Uruchomienie serwera w osobnym wątku
threading.Thread(target=run).start()

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

class CopyButton(View):
    def __init__(self, link: str):
        super().__init__()
        self.link = link
        
        # Tworzymy przycisk
        button = Button(label="Kopiuj link", style=discord.ButtonStyle.primary, emoji="📋")
        button.callback = self.button_callback
        self.add_item(button)
    
    async def button_callback(self, interaction: discord.Interaction):
        # Ta funkcja zostanie wywołana po kliknięciu przycisku
        try:
            # Kopiujemy link do schowka użytkownika
            await interaction.response.send_message(f"Link skopiowany do schowka: `{self.link}`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Wystąpił błąd: {str(e)}", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Sprawdź, czy wiadomość jest z kanału o określonym ID
    if message.channel.id != 1359536602283770076:
        return

    if message.content.startswith("http://") or message.content.startswith("https://"):
        try:
            monetized_link = lv_client.linkvertise(LINKVERTISE_ID, message.content)
            
            # Tworzymy widok z przyciskiem
            view = CopyButton(monetized_link)
            
            # Wysyłamy wiadomość z przyciskiem
            await message.channel.send(
                f"Oto Twój link z Linkvertise: {monetized_link}", 
                view=view
            )
        except Exception as e:
            await message.channel.send(f"Wystąpił błąd: {str(e)}")

    await bot.process_commands(message)

# Start bota
bot.run(DISCORD_TOKEN)
