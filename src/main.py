import os

from services.booking_manager import BookingManager
from services.room_manager import RoomManager
from utils.file_handler import FileHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOMS_FILE = os.path.join(BASE_DIR, "rooms.txt")
BOOKINGS_FILE = os.path.join(BASE_DIR, "bookings.txt")


def show_menu():
    print("\n========== RESORT ROOM BOOKING MANAGEMENT ==========")
    print("1. Add room")
    print("2. Update room")
    print("3. Delete room")
    print("4. Display rooms")
    print("5. Add booking")
    print("6. Update booking")
    print("7. Display today's check-in bookings")
    print("8. Display bookings sorted by total")
    print("9. Display total amount per room")
    print("0. Exit")
    print("====================================================")


# Algorithm 12: Main menu
def main():
    file_handler = FileHandler(ROOMS_FILE, BOOKINGS_FILE)

    rooms = file_handler.load_data(ROOMS_FILE)
    bookings = None
    if rooms is not None:
        bookings = file_handler.load_data(BOOKINGS_FILE, rooms)
    if rooms is None or bookings is None:
        print("Cannot read data. The program stops.")
        return

    room_manager = RoomManager(rooms, bookings, file_handler)
    booking_manager = BookingManager(rooms, bookings, file_handler)
    fixed_count = booking_manager.sync_room_status()
    if fixed_count > 0:
        print(f"Warning: the status of {fixed_count} room(s) did not match "
              "bookings.txt and was corrected.")

    while True:
        show_menu()
        choice_text = input("Enter your choice: ")
        try:
            choice = int(choice_text)
        except ValueError:
            print("Invalid choice.")
            continue
        if choice < 0 or choice > 9:
            print("Invalid choice.")
            continue

        if choice == 0:
            print("Program ended.")
            break
        if choice == 1:
            room_manager.add_room()
        elif choice == 2:
            room_manager.update_room()
        elif choice == 3:
            room_manager.delete_room()
        elif choice == 4:
            room_manager.display_rooms()
        elif choice == 5:
            booking_manager.add_booking()
        elif choice == 6:
            booking_manager.update_booking()
        elif choice == 7:
            booking_manager.display_today_check_in()
        elif choice == 8:
            booking_manager.display_sorted_by_total()
        elif choice == 9:
            booking_manager.display_revenue_per_room()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram ended.")
