from models.room import Room
from utils.validators import is_valid_text, parse_price, parse_room_id


class RoomManager:
    def __init__(self, rooms, bookings, file_handler):
        self._rooms = rooms
        self._bookings = bookings
        self._file_handler = file_handler

    def find_room(self, room_id):
        for room in self._rooms:
            if room.room_id == room_id:
                return room
        return None

    def is_room_in_any_booking(self, room_id):
        return any(room_id in booking.room_list for booking in self._bookings)

    def _save_and_report(self, success_message):
        if self._file_handler.save_data(self._rooms, self._bookings):
            print(success_message)
        else:
            print("Cannot save data to file.")

    # Algorithm 1: Add a new room
    def add_room(self):
        while True:
            room_id = parse_room_id(input("Enter room_id: ").strip())
            if room_id is None or self.find_room(room_id) is not None:
                print("Invalid or duplicate room_id.")
                continue
            break

        while True:
            room_name = input("Enter room_name: ").strip()
            if not is_valid_text(room_name):
                print("Invalid room_name.")
                continue
            break

        while True:
            room_type = input("Enter type: ").strip()
            if not is_valid_text(room_type):
                print("Invalid type.")
                continue
            break

        while True:
            price = parse_price(input("Enter price: ").strip())
            if price is None:
                print("Invalid price.")
                continue
            break

        self._rooms.append(Room(room_id, room_name, room_type, price, False))
        self._save_and_report("Room added successfully.")

    # Algorithm 2: Update room information
    def update_room(self):
        room = self.find_room(parse_room_id(input("Enter room_id to update: ").strip()))
        if room is None:
            print("Room not found.")
            return

        print("Press Enter to keep the old value.")
        while True:
            name_input = input(f"New room_name [{room.room_name}]: ").strip()
            new_name = name_input if name_input != "" else room.room_name
            if not is_valid_text(new_name):
                print("Invalid room_name.")
                continue
            break

        while True:
            type_input = input(f"New type [{room.type}]: ").strip()
            new_type = type_input if type_input != "" else room.type
            if not is_valid_text(new_type):
                print("Invalid type.")
                continue
            break

        while True:
            price_input = input(f"New price [{room.price:.0f}]: ").strip()
            new_price = parse_price(price_input) if price_input != "" else room.price
            if new_price is None:
                print("Invalid price.")
                continue
            if new_price != room.price and self.is_room_in_any_booking(room.room_id):
                print("Cannot change the price of a booked room.")
                continue
            break

        room.room_name = new_name
        room.type = new_type
        room.price = new_price
        self._save_and_report("Room updated successfully.")

    # Algorithm 3: Delete a room
    def delete_room(self):
        room = self.find_room(parse_room_id(input("Enter room_id to delete: ").strip()))
        if room is None:
            print("Room not found.")
            return
        if self.is_room_in_any_booking(room.room_id):
            print("Cannot delete room linked to existing bookings!")
            return
        self._rooms.remove(room)
        self._save_and_report("Room deleted successfully.")

    # Algorithm 4: Display the room list
    def display_rooms(self):
        if len(self._rooms) == 0:
            print("No rooms found.")
            return
        print(Room.TABLE_HEADER)
        print("-" * len(Room.TABLE_HEADER))
        for room in self._rooms:
            print(room)
