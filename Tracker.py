import datetime
import json
import os

START_TIME = "data/start_time.json"
MONTHLY_WEEKLY_TOTAL = "data/monthly_weekly_total.json"
DATE_TIME = "data/date_time.json"
DATA_DIR = "data"

def main():
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR)
        except OSError as e:
            print(f"ERROR: Cannot makedir {DATA_DIR}: {e}")
            return

    now = datetime.datetime.now()
    current_year, current_week, current_weekday = now.isocalendar()
    current_month = now.month

    monthly_total = 0
    weekly_total = 0
    stored_year = current_year
    stored_month = current_month
    stored_week = current_week

    if os.path.exists(MONTHLY_WEEKLY_TOTAL):
        try:
            with open(MONTHLY_WEEKLY_TOTAL, "r") as f:
                data = json.load(f)
                monthly_total = data.get("monthly_total", 0)
                weekly_total = data.get("weekly_total", 0)
                stored_year = data.get("year", current_year)
                stored_week = data.get("week", current_week)
                stored_month = data.get("month", current_month)
        except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
            print(f"ERROR: Failed to load monthly/weekly total data: {e}")

    # Check if the current week/month/year is different from the stored
    if current_week != stored_week:
        weekly_total = 0
        stored_week = current_week

    if current_month != stored_month:
        monthly_total = 0
        stored_month = current_month

    if current_year != stored_year:
        stored_year = current_year

    # If the start time exists, stop the timer
    if os.path.exists(START_TIME):
        try:
            with open(START_TIME, "r") as f:
                start_data = json.load(f)
                start_time = datetime.datetime.fromisoformat(start_data["start_time"])

            duration = now - start_time
            duration_seconds = duration.total_seconds()

            weekly_total += duration_seconds
            monthly_total += duration_seconds

            # Update daily time
            try:
                date_durations = []

                current_day = start_time.date()
                end_day = now.date()
                delta = datetime.timedelta(days=1)

                while current_day <= end_day:
                    next_day = current_day + delta
                    start_of_day = datetime.datetime.combine(current_day, datetime.time.min)
                    end_of_day = datetime.datetime.combine(current_day, datetime.time.max)

                    day_start = max(start_time, start_of_day)
                    day_end = min(now, end_of_day)
                    day_duration = (day_end - day_start).total_seconds()

                    if day_duration > 0:
                        date_str = current_day.strftime("%Y-%m-%d")
                        date_durations.append((date_str, day_duration))

                    current_day = next_day

                date_data = []
                if os.path.exists(DATE_TIME):
                    try:
                        with open(DATE_TIME, "r") as f:
                            date_data = json.load(f)
                    except:
                        pass

                date_dict = {}
                for entry in date_data:
                    date = entry["date"]
                    sec = entry["sec"]
                    date_dict[date] = date_dict.get(date, 0) + sec

                for date_str, duration_sec in date_durations:
                    date_dict[date_str] = date_dict.get(date_str, 0) + duration_sec

                new_date_data = [{"date": date, "sec": sec} for date, sec in date_dict.items()]
                new_date_data.sort(key=lambda x:x["date"])

                with open(DATE_TIME, "w") as f:
                    json.dump(new_date_data, f, indent=2)

            except:
                pass

            try:
                os.remove(START_TIME)
            except OSError as e:
                print(f"ERROR: Failed to remove {START_TIME}: {e}")

            # Update monthly/weekly time
            with open(MONTHLY_WEEKLY_TOTAL, "w") as f:
                json.dump({
                    "monthly_total": monthly_total,
                    "weekly_total": weekly_total,
                    "year": stored_year,
                    "week": stored_week,
                    "month": stored_month
                }, f, indent=2)

            hours, remainder = divmod(duration_seconds, 3600)
            minutes = remainder // 60
            weekly_hours, weekly_remainder = divmod(weekly_total, 3600)
            weekly_minutes = weekly_remainder // 60
            monthly_hours, monthly_remainder = divmod(monthly_total, 3600)
            monthly_minutes = monthly_remainder // 60

            print_message(hours, minutes, weekly_hours, weekly_minutes, monthly_hours, monthly_minutes, mode="end")

        except:
            print("ERROR: Failed in reading start time")
            os.remove(START_TIME)

    # If the start time doesn't exist, start the timer
    else:
        with open(START_TIME, "w") as f:
            json.dump({"start_time": now.isoformat()}, f, indent=2)

        weekly_hours, weekly_remainder = divmod(weekly_total, 3600)
        weekly_minutes = weekly_remainder // 60
        monthly_hours, monthly_remainder = divmod(monthly_total, 3600)
        monthly_minutes = monthly_remainder // 60

        print_message(weekly_hours=weekly_hours, weekly_minutes=weekly_minutes,
                      monthly_hours=monthly_hours, monthly_minutes=monthly_minutes, now=now, mode="start")

# Print statistics
def print_message(hours=None, minutes=None, weekly_hours=None, weekly_minutes=None, monthly_hours=None, monthly_minutes=None, now=None, mode=None):
    message_parts = []
    if mode == "end":
        message_parts.append("---End Recording---")
        if hours is not None and minutes is not None:
            message_parts.append(f"This Time: {int(hours)} hours {int(minutes)} minutes")
        message_parts.append("-------------------")
    else:
        message_parts.append("---Start Recording---")
        if now is not None:
            message_parts.append(f"{now.strftime('%Y-%m-%d %H:%M:%S')}")
        message_parts.append("-------------------")

    if weekly_hours is not None and weekly_minutes is not None:
        message_parts.append(f"Weekly Total: {int(weekly_hours)} hours {int(weekly_minutes)} minutes")

    if monthly_hours is not None and monthly_minutes is not None:
        message_parts.append(f"Monthly Total: {int(monthly_hours)} hours {int(monthly_minutes)} minutes")

    message = "\n".join(message_parts)

    lines = message.splitlines()
    max_length = max(len(line) for line in lines)
    width = max_length + 4

    borderchar = "#"
    border = borderchar * (width + 1)

    print(border)

    # Centering the message
    for line in lines:
        padding = (width - len(line)) // 2
        centered_line = borderchar + " " * padding + line + " " * (width - len(line) - padding -1) + borderchar
        print(centered_line)

    print(border)



if __name__ == "__main__":
    main()

