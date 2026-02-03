import os
import sqlite3
from datetime import time

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ================= TOKEN =================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN not found! Render Environment me TOKEN add karo")

# ================= DATABASE =================

conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    premium INTEGER
)
""")
conn.commit()


def add_user(uid):
    cur.execute("INSERT OR IGNORE INTO users VALUES (?,0)", (uid,))
    conn.commit()


def is_premium(uid):
    cur.execute("SELECT premium FROM users WHERE id=?", (uid,))
    r = cur.fetchone()
    return r and r[0] == 1


def make_premium(uid):
    cur.execute("UPDATE users SET premium=1 WHERE id=?", (uid,))
    conn.commit()


# ================= COMMANDS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    add_user(uid)

    await update.message.reply_text(
        "👋 Welcome NTPC Guru Bot\n\n"
        "/quiz\n"
        "/notes\n"
        "/premium\n"
        "/pay"
    )


# ---------- QUIZ ----------
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if not is_premium(uid):
        await update.message.reply_text("❌ Premium only quiz\nUse /pay")
        return

    await update.message.reply_text(
        "📘 Daily Quiz\n\n"
        "भारत का संविधान कब लागू हुआ?\n"
        "A) 1947\nB) 1950\nC) 1949\n\n"
        "✅ Answer: 26 Jan 1950"
    )


# ---------- NOTES ----------
async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if not is_premium(uid):
        await update.message.reply_text("❌ Premium users only\nUse /pay")
        return

    await update.message.reply_document(open("notes.pdf", "rb"))


# ---------- PAYMENT ----------
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💳 Premium ₹49/month\n"
        "UPI: yourupi@upi\n"
        "Screenshot admin ko bhejo"
    )


# ---------- PREMIUM INFO ----------
async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⭐ Premium Benefits:\n"
        "✔ All quizzes\n"
        "✔ PDFs\n"
        "✔ Mock tests\n"
    )


# ---------- ADMIN ----------
ADMIN_ID = 123456789   # 👉 apna telegram id daalo


async def addpremium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /addpremium user_id")
        return

    uid = int(context.args[0])
    make_premium(uid)

    await update.message.reply_text("✅ User premium added")


# ================= AUTO JOBS =================

async def daily_quiz(context: ContextTypes.DEFAULT_TYPE):
    cur.execute("SELECT id FROM users WHERE premium=1")

    for (uid,) in cur.fetchall():
        try:
            await context.bot.send_message(uid, "🔥 Daily Quiz time! Type /quiz")
        except:
            pass


async def ads(context: ContextTypes.DEFAULT_TYPE):
    cur.execute("SELECT id FROM users")

    for (uid,) in cur.fetchall():
        try:
            await context.bot.send_message(uid, "📢 Sponsor: Testbook Mock Test App")
        except:
            pass


# ================= MAIN (ONLY ONCE) =================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CommandHandler("notes", notes))
app.add_handler(CommandHandler("premium", premium))
app.add_handler(CommandHandler("pay", pay))
app.add_handler(CommandHandler("addpremium", addpremium))

jobq = app.job_queue
jobq.run_daily(daily_quiz, time(hour=7, minute=0))
jobq.run_daily(ads, time(hour=18, minute=0))

print("Bot running...")

app.run_polling()        await update.message.reply_text("Usage: /addpremium user_id")
        return

    uid = int(context.args[0])
    make_premium(uid)
    await update.message.reply_text("User premium added ✅")


# ================= AUTO MESSAGES =================

async def daily_quiz(context: ContextTypes.DEFAULT_TYPE):
    cur.execute("SELECT id FROM users WHERE premium=1")
    for (uid,) in cur.fetchall():
        try:
            await context.bot.send_message(uid, "🔥 Daily Quiz time! Type /quiz")
        except:
            pass


async def ads(context: ContextTypes.DEFAULT_TYPE):
    cur.execute("SELECT id FROM users")
    for (uid,) in cur.fetchall():
        try:
            await context.bot.send_message(uid, "📢 Sponsor: Testbook Mock Test App")
        except:
            pass


# ================= MAIN =================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CommandHandler("notes", notes))
app.add_handler(CommandHandler("premium", premium))
app.add_handler(CommandHandler("pay", pay))
app.add_handler(CommandHandler("addpremium", addpremium))

# Scheduler
jobq = app.job_queue
jobq.run_daily(daily_quiz, time(hour=7, minute=0))
jobq.run_daily(ads, time(hour=18, minute=0))

print("✅ Bot running...")
app.run_polling()app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CommandHandler("notes", notes))
app.add_handler(CommandHandler("premium", premium))
app.add_handler(CommandHandler("pay", pay))
app.add_handler(CommandHandler("addpremium", addpremium))

# Scheduler
jobq = app.job_queue
jobq.run_daily(daily_quiz, time(hour=7, minute=0))
jobq.run_daily(ads, time(hour=18, minute=0))

print("Bot running...")
app.run_polling()
# ---------------- MAIN ----------------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CommandHandler("notes", notes))
app.add_handler(CommandHandler("premium", premium))
app.add_handler(CommandHandler("pay", pay))
app.add_handler(CommandHandler("addpremium", addpremium))

jobq = app.job_queue
jobq.run_daily(daily_quiz, time(hour=7, minute=0))
jobq.run_daily(ads, time(hour=18, minute=0))

print("Bot running...")

app.run_polling()
