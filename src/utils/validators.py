import math
import re
from datetime import datetime


def parse_room_id(text):
    try:
        value = int(text)
    except ValueError:
        return None
    if value <= 0:
        return None
    return value


def is_valid_text(text):
    return text.strip() != "" and "|" not in text


def parse_price(text):
    try:
        value = float(text)
    except ValueError:
        return None
    if not math.isfinite(value) or value <= 0:
        return None
    return value


def is_valid_phone(text):
    return re.fullmatch(r"0[0-9]{9}", text) is not None


def parse_date(text):
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def parse_room_list(text):
    room_ids = []
    for item in text.split(","):
        room_id = parse_room_id(item.strip())
        if room_id is None:
            return None
        room_ids.append(room_id)
    return room_ids


def has_duplicates(items):
    return len(set(items)) != len(items)
