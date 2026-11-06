from datetime import date

from models.booking import Booking
from utils.validators import (has_duplicates, is_valid_phone, is_valid_text,
                              parse_date, parse_room_list)


class BookingManager:
    def __init__(self, rooms, bookings, file_handler):
        self._rooms = rooms
        self._bookings = bookings
        self._file_handler = file_handler

    def find_booking(self, booking_id):
        for booking in self._bookings:
            if booking.booking_id == booking_id:
                return booking
        return None

    def _find_room(self, room_id):
        for room in self._rooms:
            if room.room_id == room_id:
                return room
        return None

    def _is_available(self, room_id):
        room = self._find_room(room_id)
        return room is not None and not room.status

    def sync_room_status(self):
        booked_ids = set()
        for booking in self._bookings:
            for room_id in booking.room_list:
                booked_ids.add(room_id)
        fixed_count = 0
        for room in self._rooms:
            correct_status = room.room_id in booked_ids
            if room.status != correct_status:
                room.status = correct_status
                fixed_count += 1
        return fixed_count

    def _calculate_total(self, room_list, stay_days):
        return sum(self._find_room(room_id).price for room_id in room_list) * stay_days

    def _save_and_report(self, success_message):
        if self._file_handler.save_data(self._rooms, self._bookings):
            print(success_message)
        else:
            print("Cannot save data to file.")

    @staticmethod
    def _print_booking_table(bookings):
        print(Booking.TABLE_HEADER)
        print("-" * len(Booking.TABLE_HEADER))
        for booking in bookings:
            print(booking)

    # Algorithm 5: Add a new booking
    def add_booking(self):
        if not any(not room.status for room in self._rooms):
            print("No available room.")
            return

        while True:
            booking_id = input("Enter booking_id: ").strip()
            if not is_valid_text(booking_id) or self.find_booking(booking_id) is not None:
                print("Invalid or duplicate booking_id.")
                continue
            break

        while True:
            customer = input("Enter customer: ").strip()
            if not is_valid_text(customer):
                print("Invalid customer.")
                continue
            break

        while True:
            customer_phone = input("Enter customer_phone: ").strip()
            if not is_valid_phone(customer_phone):
                print("Invalid customer_phone.")
                continue
            break

        while True:
            check_in = parse_date(input("Enter check_in (YYYY-MM-DD): ").strip())
            if check_in is None:
                print("Invalid check_in date.")
                continue
            break

        while True:
            check_out = parse_date(input("Enter check_out (YYYY-MM-DD): ").strip())
            if check_out is None or check_out <= check_in:
                print("Invalid check_out date.")
                continue
            break

        available_ids = ", ".join(str(r.room_id) for r in self._rooms if not r.status)
        while True:
            room_list = parse_room_list(input(
                f"Enter room_list (room_ids separated by commas) - available: {available_ids}: "))
            if (room_list is None or has_duplicates(room_list)
                    or not all(self._is_available(room_id) for room_id in room_list)):
                print("Invalid room list.")
                continue
            break

        booking_date = date.today()
        stay_days = (check_out - check_in).days
        total = self._calculate_total(room_list, stay_days)
        self._bookings.append(Booking(booking_id, booking_date, customer, customer_phone,
                                      room_list, total, check_in, check_out))
        for room_id in room_list:
            self._find_room(room_id).status = True
        self._save_and_report("Booking added successfully.")

    # Algorithm 6: Update booking information
    def update_booking(self):
        booking = self.find_booking(input("Enter booking_id to update: ").strip())
        if booking is None:
            print("Booking not found.")
            return

        old_rooms_text = ",".join(str(room_id) for room_id in booking.room_list)
        print("Press Enter to keep the old value.")
        while True:
            customer_input = input(f"New customer [{booking.customer}]: ").strip()
            customer = customer_input if customer_input != "" else booking.customer
            if not is_valid_text(customer):
                print("Invalid customer.")
                continue
            break

        while True:
            phone_input = input(f"New customer_phone [{booking.customer_phone}]: ").strip()
            customer_phone = phone_input if phone_input != "" else booking.customer_phone
            if not is_valid_phone(customer_phone):
                print("Invalid customer_phone.")
                continue
            break

        while True:
            check_in_input = input(f"New check_in [{booking.check_in}]: ").strip()
            check_in = parse_date(check_in_input) if check_in_input != "" else booking.check_in
            if check_in is None:
                print("Invalid check_in date.")
                continue
            break

        while True:
            check_out_input = input(f"New check_out [{booking.check_out}]: ").strip()
            check_out = parse_date(check_out_input) if check_out_input != "" else booking.check_out
            if check_out is None or check_out <= check_in:
                print("Invalid check_out date.")
                continue
            break

        while True:
            rooms_input = input(f"New room_list [{old_rooms_text}]: ").strip()
            room_list = parse_room_list(rooms_input) if rooms_input != "" else booking.room_list
            if room_list is None or has_duplicates(room_list):
                print("Invalid room list.")
                continue
            added_rooms = [room_id for room_id in room_list if room_id not in booking.room_list]
            if not all(self._is_available(room_id) for room_id in added_rooms):
                print("Invalid room list.")
                continue
            break

        removed_rooms = [room_id for room_id in booking.room_list if room_id not in room_list]
        for room_id in removed_rooms:
            self._find_room(room_id).status = False
        for room_id in added_rooms:
            self._find_room(room_id).status = True

        booking.customer = customer
        booking.customer_phone = customer_phone
        booking.check_in = check_in
        booking.check_out = check_out
        booking.room_list = room_list
        booking.total = self._calculate_total(room_list, booking.stay_days)
        self._save_and_report("Booking updated successfully.")

    # Algorithm 7: Display today's check-in bookings
    def display_today_check_in(self):
        today = date.today()
        today_list = []
        for booking in self._bookings:
            if booking.check_in == today:
                today_list.append(booking)
        if len(today_list) == 0:
            print("No check-in today.")
            return
        self._print_booking_table(today_list)

    # Algorithm 8: Display bookings sorted by total (highest first)
    def display_sorted_by_total(self):
        if len(self._bookings) == 0:
            print("No bookings found.")
            return
        sorted_list = sorted(self._bookings, key=lambda b: b.total, reverse=True)
        self._print_booking_table(sorted_list)

    # Algorithm 9: Display the total booking amount for each room
    def display_revenue_per_room(self):
        if len(self._rooms) == 0:
            print("No rooms found.")
            return
        room_prices = {room.room_id: room.price for room in self._rooms}
        revenue = {room.room_id: 0.0 for room in self._rooms}
        for booking in self._bookings:
            stay_days = (booking.check_out - booking.check_in).days
            for room_id in booking.room_list:
                revenue[room_id] += room_prices[room_id] * stay_days
        print(f"{'room_id':<8} | {'total amount':>16}")
        print("-" * 27)
        for room_id, amount in revenue.items():
            print(f"{room_id:<8} | {amount:>16,.0f}")
