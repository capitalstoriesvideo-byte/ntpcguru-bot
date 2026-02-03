import os
import sqlite3
from telegram import Update
from telegram.ext import *
from datetime import time

TOKEN = os.getenv("8524413023:AAEoJqRJKYzY68xfVbN428Nj6_HdGwCZ_uI")

# ---------------- DB ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, premium INTEGER)")
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


# ---------------- Commands ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    add_user(uid)

    await update.message.reply_text(
        "👋 Welcome NTPC Guru Bot\n\n"
        "/quiz\n/notes\n/premium\n/pay"
    )


# FREE + PREMIUM QUIZ
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if not is_premium(uid):
        await update.message.reply_text("❌ Premium only quiz\nUse /pay")
        return

    await update.message.reply_text(
        "📘 Daily Quiz\n\nभारत का संविधान कब लागू हुआ?\nA)1947\nB)1950\nC)1949\n\nAnswer: 26 Jan 1950"
    )


# PDF NOTES
async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if not is_premium(uid):
        await update.message.reply_text("❌ Premium users only\nUse /pay")
        return

    await update.message.reply_document("notes.pdf")


# PAYMENT INFO
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💳 Premium ₹49/month\nUPI: yourupi@upi\nPayment screenshot admin ko bhejo"
    )


# PREMIUM INFO
async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⭐ Premium benefits:\n✔ All quizzes\n✔ PDFs\n✔ Mock tests")


# ADMIN ADD PREMIUM
ADMIN_ID = 123456789  # ← apna telegram id

async def addpremium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    uid = int(context.args[0])
    make_premium(uid)
    await update.message.reply_text("User premium added ✅")


# ---------------- AUTO MESSAGES ----------------

async def daily_quiz(context: ContextTypes.DEFAULT_TYPE):
    cur.execute("SELECT id FROM users WHERE premium=1")
    for u in cur.fetchall():
        await context.bot.send_message(u[0], "🔥 Daily Quiz time! Type /quiz")


async def ads(context: ContextTypes.DEFAULT_TYPE):
    cur.execute("SELECT id FROM users")
    for u in cur.fetchall():
        await context.bot.send_message(u[0], "📢 Sponsor: Testbook Mock Test App")


# ---------------- MAIN ----------------

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

print("Bot running...")
app.run_polling()
