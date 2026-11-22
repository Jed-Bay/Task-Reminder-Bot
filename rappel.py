#!/usr/bin/env python3
"""Daily chore reminder sent via WhatsApp (CallMeBot).

Usage:
  python3 rappel.py                       # send today's reminders
  python3 rappel.py --test                # print messages, send nothing
  python3 rappel.py --test --date 2026-05-02   # preview a specific day
"""
import csv
import argparse
import urllib.parse
import urllib.request
from datetime import date, datetime
from zoneinfo import ZoneInfo

from config import START_DATE, CONTACTS, CSV_PATH, TIMEZONE, TASK_EMOJI

CYCLE_LENGTH = 21


def get_cycle_day(target_date):
    delta = (target_date - date.fromisoformat(START_DATE)).days
    return (delta % CYCLE_LENGTH) + 1


def get_tasks_for_day(day):
    tasks = {}
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["day"].strip() == str(day):
                tasks[row["person"].strip()] = row["task"].strip()
    return tasks


def format_message(person, task):
    emoji = TASK_EMOJI.get(task, "📋")
    if task == "Free":
        body = f"Great news: you're free today! Enjoy and rest well. {emoji}"
    else:
        body = f"Your task for today: {task} {emoji}\nDon't forget! 😊"
    return (
        f"☀️ Good morning {person}!\n"
        f"------------------\n"
        f"{body}\n"
        f"------------------\n"
        f"Have a great day! 🏠"
    )


def send_whatsapp(phone, apikey, message):
    text = urllib.parse.quote(message)
    url = (f"https://api.callmebot.com/whatsapp.php"
           f"?phone={urllib.parse.quote(phone)}&text={text}&apikey={apikey}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        # HTTP 200 alone does not prove delivery, so show CallMeBot's reply
        print(f"  HTTP {resp.status} | CallMeBot says: {body[:200].strip()!r}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--date", help="Simulate a date (YYYY-MM-DD)")
    args = parser.parse_args()

    today = (date.fromisoformat(args.date) if args.date
             else datetime.now(ZoneInfo(TIMEZONE)).date())
    cycle_day = get_cycle_day(today)
    print(f"Reminders for {today} (cycle day {cycle_day})")

    for person, task in get_tasks_for_day(cycle_day).items():
        info = CONTACTS.get(person)
        if not info:
            print(f"  No contact for {person}, skipping")
            continue
        message = format_message(person, task)
        if args.test:
            print(f"\n>>> {person}\n{message}")
            continue
        try:
            print(f"Sending to {person}...")
            send_whatsapp(info["phone"], info["apikey"], message)
        except Exception as e:
            print(f"  Error: {e}")


if __name__ == "__main__":
    main()
