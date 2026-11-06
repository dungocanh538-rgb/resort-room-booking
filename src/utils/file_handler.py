import os
import shutil

from models.booking import Booking
from models.room import Room
from utils.validators import (has_duplicates, is_valid_phone, is_valid_text,
                              parse_date, parse_price, parse_room_id,
                              parse_room_list)


class FileHandler:
    def __init__(self, rooms_file, bookings_file):
        self._rooms_file = rooms_file
        self._bookings_file = bookings_file

    @property
    def rooms_file(self):
        return self._rooms_file

    @property
    def bookings_file(self):
        return self._bookings_file

    # Algorithm 10: Save data to file
    def save_data(self, rooms, bookings):
        try:
            with open(self._rooms_file, "w", encoding="utf-8") as file:
                for room in rooms:
                    file.write(self._room_to_line(room) + "\n")
            with open(self._bookings_file, "w", encoding="utf-8") as file:
                for booking in bookings:
                    file.write(self._booking_to_line(booking) + "\n")
        except OSError:
            return False
        return True

    @staticmethod
    def _room_to_line(room):
        return f"{room.room_id}|{room.room_name}|{room.type}|{room.status}|{room.price}"

    @staticmethod
    def _booking_to_line(booking):
        rooms = ",".join(str(room_id) for room_id in booking.room_list)
        return (f"{booking.booking_id}|{booking.booking_date}|{booking.customer}|"
                f"{booking.customer_phone}|{rooms}|{booking.total}|"
                f"{booking.check_in}|{booking.check_out}")

    # Algorithm 11: Load data from file
    def load_data(self, file_name, room_list=None):
        name = os.path.basename(file_name)
        is_rooms_file = (file_name == self._rooms_file)
        data_list = []
        skipped = 0
        try:
            with open(file_name, "r", encoding="utf-8-sig") as file:
                for line_number, line in enumerate(file, start=1):
                    if line.strip() == "":
                        continue
                    fields = line.rstrip("\n").split("|")
                    try:
                        if is_rooms_file:
                            obj = self._line_to_room(fields, data_list)
                        else:
                            obj = self._line_to_booking(fields, data_list, room_list)
                    except (ValueError, IndexError):
                        print(f"{name} line {line_number}: Skip the invalid line.")
                        skipped += 1
                        continue
                    data_list.append(obj)
        except FileNotFoundError:
            print(f"{name}: File not found. Start with an empty list.")
        except PermissionError:
            print(f"{name}: No permission to read the file.")
            return None
        except (UnicodeDecodeError, OSError):
            print(f"{name}: Cannot read the file (not UTF-8 text or not a file).")
            return None
        if skipped > 0:
            print(f"Warning: {skipped} invalid line(s) in {name} were skipped. "
                  "They will be removed from the file at the next save.")
            try:
                shutil.copyfile(file_name, file_name + ".bak")
                print(f"A backup copy was saved as {name}.bak")
            except OSError:
                print("Cannot create the backup copy.")
        return data_list

    @staticmethod
    def _line_to_room(fields, loaded_rooms):
        if len(fields) != 5:
            raise ValueError("a room line must have 5 fields")
        room_id = parse_room_id(fields[0])
        if room_id is None or any(r.room_id == room_id for r in loaded_rooms):
            raise ValueError("invalid or duplicate room_id")
        room_name, room_type = fields[1], fields[2]
        if not is_valid_text(room_name) or not is_valid_text(room_type):
            raise ValueError("empty room_name or type")
        if fields[3] not in ("True", "False"):
            raise ValueError("status must be True or False")
        status = (fields[3] == "True")
        price = parse_price(fields[4])
        if price is None:
            raise ValueError("invalid price")
        return Room(room_id, room_name, room_type, price, status)

    @staticmethod
    def _line_to_booking(fields, loaded_bookings, room_list):
        if len(fields) != 8:
            raise ValueError("a booking line must have 8 fields")
        booking_id = fields[0]
        if (not is_valid_text(booking_id)
                or any(b.booking_id == booking_id for b in loaded_bookings)):
            raise ValueError("invalid or duplicate booking_id")
        booking_date = parse_date(fields[1])
        customer = fields[2]
        customer_phone = fields[3]
        check_in = parse_date(fields[6])
        check_out = parse_date(fields[7])
        if not is_valid_text(customer) or not is_valid_phone(customer_phone):
            raise ValueError("invalid customer or phone")
        if booking_date is None or check_in is None or check_out is None or check_out <= check_in:
            raise ValueError("invalid dates")
        total = parse_price(fields[5])
        if total is None:
            raise ValueError("total must be a number greater than 0")
        rooms_in_booking = parse_room_list(fields[4])
        existing_ids = [room.room_id for room in room_list]
        if (rooms_in_booking is None or has_duplicates(rooms_in_booking)
                or not all(room_id in existing_ids for room_id in rooms_in_booking)):
            raise ValueError("invalid room_list")
        if any(room_id in b.room_list for b in loaded_bookings for room_id in rooms_in_booking):
            raise ValueError("a room is already used by another booking")
        return Booking(booking_id, booking_date, customer, customer_phone,
                       rooms_in_booking, total, check_in, check_out)
