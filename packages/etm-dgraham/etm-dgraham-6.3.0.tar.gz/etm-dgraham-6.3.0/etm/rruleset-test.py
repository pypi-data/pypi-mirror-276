from datetime import datetime
from dateutil.rrule import rrule, rruleset, DAILY
from dateutil.tz import gettz

def is_naive(dt):
    return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None

# Define the timezone (replace 'America/New_York' with your specific timezone)
pacific = gettz('US/Pacific')
mountain = gettz('America/Denver')
central = gettz('US/Central')
eastern = gettz('America/New_York')
local = gettz()
utc = gettz('UTC')
naive = None

tz = eastern
# Define the start date
start_date = datetime(2024, 10, 28, 13, 30, tzinfo=tz)  # 0:30 on Mon Oct 28, 2024

# Create a recurrence rule for daily events
rule1 = rrule(freq=DAILY, dtstart=start_date, count=14)

# Create another recurrence rule for specific days (e.g., every 2 days)
rule2 = rrule(freq=DAILY, dtstart=start_date, interval=2, count=7)

# Create an rruleset
rules = rruleset()

# Add the rules to the rruleset
rules.rrule(rule1)
rules.rrule(rule2)

# Add a specific date to include
rules.rdate(datetime(2024, 11, 4, 13, 45, tzinfo=tz))

# Add a specific date to exclude
rules.exdate(datetime(2024, 11, 4, 13, 30, tzinfo=tz))

# Generate the occurrences of the event
occurrences = list(rules)

# Print the occurrences
for occurrence in occurrences:
    print(occurrence.strftime("%a %Y-%m-%d %H:%M %Z %z"))
