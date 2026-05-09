import discord
from discord.ext import commands
import random
import asyncio
import json
import os

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =============
# BOT READY
# =============
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# =============
# HELLO COMMAND
# =============
@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I'm your JEE Assistant Bot 🚀")

# =============
# MOTIVATION COMMAND
# =============
@bot.command()
async def motivate(ctx):
    quotes = [
        "Success comes from consistency 📚",
        "Small progress every day adds up 🔥",
        "Discipline beats motivation 💪",
        "Focus on your goals, not distractions 🎯",
        "JEE is hard, but you are harder 😎"
    ]

    await ctx.send(random.choice(quotes))

# =============
# STUDY TIP COMMAND
# =============
@bot.command()
async def studytip(ctx):
    tips = [
        "Use the Pomodoro technique: 25 min study + 5 min break ⏳",
        "Revise formulas daily 🧠",
        "Practice PYQs regularly 📘",
        "Avoid multitasking while studying 🚫",
        "Consistency matters more than intensity 🔥"
    ]

    await ctx.send(random.choice(tips))

# =============
# FORMULA COMMAND
# =============
@bot.command()
async def formula(ctx, subject=None):

    formulas = {
        "physics": "Force = Mass × Acceleration (F = ma)",
        "chemistry": "Mole = Given Mass / Molar Mass",
        "math": "Quadratic Formula: x = (-b ± √(b²-4ac)) / 2a"
    }

    if subject is None:
        await ctx.send("Usage: !formula physics/chemistry/math")
    else:
        subject = subject.lower()

        if subject in formulas:
            await ctx.send(formulas[subject])
        else:
            await ctx.send("Subject not found ❌")

# =============
# TIMER COMMAND
# =============
@bot.command()
async def timer(ctx, minutes: float):

    await ctx.send(f"⏳ Timer started for {minutes} minutes!")

    await asyncio.sleep(minutes * 60)

    await ctx.send(f"✅ Time's up! Great job studying 🔥")

# =============
# TASK STORAGE
# =============
# =============
# LOAD TASKS
# =============

TASKS_FILE = "tasks.json"

if os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "r") as f:
        tasks = json.load(f)
else:
    tasks = []

# =============
# SAVE TASKS FUNCTION
# =============

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)

# =============
# ADD TASK
# =============
@bot.command()
async def addtask(ctx, *, task=None):

    if task is None:
        await ctx.send("⚠️ Please enter a task.")
        return

    tasks.append(task)

    save_tasks()

    await ctx.send(f"✅ Task added: {task}")@bot.command()
async def addtask(ctx, *, task=None):

    if task is None:
        await ctx.send("⚠️ Please enter a task.")
        return

    tasks.append(task)

    save_tasks()

    await ctx.send(f"✅ Task added: {task}")

# =============
# SHOW TASKS
# =============
@bot.command()
async def taskslist(ctx):

    if len(tasks) == 0:
        await ctx.send("📭 No tasks available.")
        return

    message = "📚 Your Tasks:\n"

    for i, task in enumerate(tasks):
        message += f"{i+1}. {task}\n"

    await ctx.send(message)

# =============
# REMOVE TASK
# =============
@bot.command()
async def removetask(ctx, task_number: int):

    if task_number <= 0 or task_number > len(tasks):
        await ctx.send("❌ Invalid task number.")
        return

    removed = tasks.pop(task_number - 1)

    save_tasks()

    await ctx.send(f"🗑️ Removed task: {removed}")

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Missing required argument.")

    else:
        print(error)

# =============
# NOTES SYSTEM
# =============

@bot.command()
async def notes(ctx, subject=None, chapter=None):

    if subject is None or chapter is None:
        await ctx.send("Usage: !notes physics ch1")
        return

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    filename = os.path.join(
        BASE_DIR,
        "notes",
        f"{subject.lower()}_{chapter.lower()}.txt"
    )

    await ctx.send(f"📂 Searching: {filename}")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        if len(content) > 1900:
            await ctx.send("📄 Notes too long. Sending file...")
            await ctx.send(file=discord.File(filename))
        else:
            await ctx.send(f"```{content}```")

    except FileNotFoundError:
        await ctx.send("❌ Notes file not found.")

# =============
# RUN BOT
# =============
bot.run(TOKEN)