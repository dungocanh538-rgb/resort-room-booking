class Room:
    TABLE_HEADER = (f"{'room_id':<8} | {'room_name':<16} | {'type':<24} | "
                    f"{'status':<9} | {'price':>12}")

    def __init__(self, room_id, room_name, room_type, price, status=False):
        self._room_id = room_id
        self._room_name = room_name
        self._type = room_type
        self._price = price
        self._status = status

    @property
    def room_id(self):
        return self._room_id

    @property
    def room_name(self):
        return self._room_name

    @room_name.setter
    def room_name(self, value):
        self._room_name = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def status_text(self):
        return "Booked" if self._status else "Available"

    def __str__(self):
        return (f"{self._room_id:<8} | {self._room_name:<16} | {self._type:<24} | "
                f"{self.status_text:<9} | {self._price:>12,.0f}")
