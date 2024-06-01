
from datetime import datetime, timedelta;

now = datetime.now();

def CalculateTime(start: datetime):
    return datetime.now() - start;

def TimeToString(time: datetime) -> str:
    seconds = time.total_seconds();
    minutes = seconds // 60;
    hours = minutes // 60;
    days = hours // 24;
    return f"{round(days)} Days = {round(hours)} Hours = {round(minutes)} Minutes = {round(seconds, 2)} Seconds";

def AddTime(Hours: int) -> str:
    return (datetime.now() + timedelta(hours=Hours)).strftime('%d-%m-%Y_%H:%M:%S');