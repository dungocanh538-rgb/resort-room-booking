class Booking:
    TABLE_HEADER = (f"{'booking_id':<10} | {'booking_date':<12} | {'customer':<18} | "
                    f"{'phone':<10} | {'room_list':<14} | {'check_in':<10} | "
                    f"{'check_out':<10} | {'total':>14}")

    def __init__(self, booking_id, booking_date, customer, customer_phone,
                 room_list, total, check_in, check_out):
        self._booking_id = booking_id
        self._booking_date = booking_date
        self._customer = customer
        self._customer_phone = customer_phone
        self._room_list = list(room_list)
        self._total = total
        self._check_in = check_in
        self._check_out = check_out

    @property
    def booking_id(self):
        return self._booking_id

    @property
    def booking_date(self):
        return self._booking_date

    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, value):
        self._customer = value

    @property
    def customer_phone(self):
        return self._customer_phone

    @customer_phone.setter
    def customer_phone(self, value):
        self._customer_phone = value

    @property
    def room_list(self):
        return list(self._room_list)

    @room_list.setter
    def room_list(self, value):
        self._room_list = list(value)

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    @property
    def check_in(self):
        return self._check_in

    @check_in.setter
    def check_in(self, value):
        self._check_in = value

    @property
    def check_out(self):
        return self._check_out

    @check_out.setter
    def check_out(self, value):
        self._check_out = value

    @property
    def stay_days(self):
        return (self._check_out - self._check_in).days

    def __str__(self):
        rooms = ",".join(str(room_id) for room_id in self._room_list)
        return (f"{self._booking_id:<10} | {str(self._booking_date):<12} | "
                f"{self._customer:<18} | {self._customer_phone:<10} | {rooms:<14} | "
                f"{str(self._check_in):<10} | {str(self._check_out):<10} | "
                f"{self._total:>14,.0f}")
