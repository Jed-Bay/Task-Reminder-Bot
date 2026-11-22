# Household Task Reminder

Sends each housemate a WhatsApp message every morning at 06:00 (EAT) telling them
their assigned task for the day. The schedule is a 21-day rotation read from `horaire.csv`
and it restarts automatically after day 21.

## How it works
- `horaire.csv`: who does what on each day of the rotation
- `rappel.py`: computes the cycle day, builds the message, sends it via [CallMeBot](https://www.callmebot.com/)
- GitHub Actions runs the script daily (free, no server needed)
- Phone numbers and API keys live in a GitHub Secret (`CONTACTS_JSON`), never in the code

## Setup
1. Each person activates CallMeBot for their own WhatsApp number and gets an API key
2. Add a repository secret named `CONTACTS_JSON`:
   ```json
   {"Name1":{"phone":"+000000000000","apikey":"XXXXXXX"},"Name2":{"phone":"+000000000000","apikey":"XXXXXXX"}}
   ```
3. Adjust `START_DATE` in `config.py` (day 1 of the rotation)

## Local preview
```bash
export CONTACTS_JSON='{"Name1":{"phone":"+1","apikey":"0"}}'
python3 rappel.py --test --date 2026-05-02
```
