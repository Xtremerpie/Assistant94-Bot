import discord
from discord.ext import commands

TOKEN = "Enter_Your_Discord_Bot_Token" #|||||||||||||||||||||||||notices that user||||||||||||||||||||||||||||||||

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I'm your JEE Assistant Bot 🚀")

bot.run(TOKEN)