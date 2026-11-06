# Resort Room Booking Management

A Python console program that helps resort staff manage rooms and customer bookings. Group project for PFP191 (Programming Fundamentals with Python) at FPT University, Fall 2026.

## Features

- Add, update, delete and display rooms
- Add and update bookings (a room can belong to only one booking)
- Show the bookings that check in today
- Sort bookings by total amount
- Show the total booking amount of each room
- Save all data to text files and load it again when the program starts
- Check every input (ID, phone number, dates, prices) and handle errors without crashing

## Tech

Python 3 · OOP (5 classes, encapsulation with `@property`) · File I/O · Exception handling

## Project structure

```
src/
├── main.py              # Main menu and program entry
├── models/              # Room, Booking (data classes)
├── services/            # RoomManager, BookingManager (business logic)
├── utils/               # FileHandler (read/write files), validators (input checks)
├── rooms.txt            # Data file used by the program
├── bookings.txt
└── sample_data/         # Clean copy of the sample data
```

## How to run

```bash
cd src
python main.py
```

Requires Python 3.8+. No extra packages are needed.
To reset the data, copy the files in `sample_data/` back into `src/`.

## Testing

The team tested the program with 53 test cases. Testing found 10 bugs, and all of them were fixed.

## Team

Group project with 4 members. **My part (Du Ngoc Anh):**
- Today's check-in list, sorting bookings by total, total amount per room
- The main menu and program entry (`main.py`)
- Fixed one bug found during testing
