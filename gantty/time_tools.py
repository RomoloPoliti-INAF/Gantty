# Copyright (C) 2025  Romolo Politi
import re
from datetime import timedelta, datetime



def string_to_timedelta(time_str: str) -> timedelta:

    pattern = r"(?:(\d+)y)?(?:(\d+)M)?(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?"
    match = re.match(pattern, time_str.strip())

    if match:
        years = int(match.group(1)) if match.group(1) else 0
        months = int(match.group(2)) if match.group(2) else 0
        days = int(match.group(3)) if match.group(3) else 0
        hours = int(match.group(4)) if match.group(4) else 0
        minutes = int(match.group(5)) if match.group(5) else 0
        seconds = int(match.group(6)) if match.group(6) else 0

        # Gestione di anni e mesi (non direttamente supportati da timedelta)
        delta = timedelta(days=days, hours=hours,
                          minutes=minutes, seconds=seconds)
        # Approssimazione: 1 anno = 365 giorni
        delta += timedelta(days=years * 365)
        # Approssimazione: 1 mese = 30 giorni
        delta += timedelta(days=months * 30)

        return delta
    else:
        return None  # La stringa non corrisponde al formato


def stopCal(start: datetime, durate: str):
    delta=string_to_timedelta(durate)
    # print(delta)
    return start + delta


def day_length(start: datetime, end: datetime) -> int:
    return (end - start).days
