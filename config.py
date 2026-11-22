import os
import json

# Day 1 of the 21-day cycle
START_DATE = "2026-04-12"
TIMEZONE = "Africa/Kampala"
CSV_PATH = "horaire.csv"

TASK_EMOJI = {
    "Cooking & Dishes": "🍳🍽️",
    "Cleaning":         "🧹🧺",
    "Free":             "🎉😎",
}

# Phone numbers and API keys come from a secret, never from the code
CONTACTS = json.loads(os.environ["CONTACTS_JSON"])
