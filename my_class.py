from collections import UserDict
from datetime import datetime, date
from adjust_for_weekend import adjust_for_weekend, date_to_string

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:  # Проверка, что значение не пустое
            raise ValueError("Name cannot be empty")
        super().__init__(value)  # Вызов конструктора родительского класса Field
                
class Phone(Field):
    def __init__(self, value):
        if len(str(value)) != 10:  #валідація номеру
          raise ValueError("The number is not valid. Should be 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
    def __str__(self):
        return self.value.strftime('%d.%m.%Y')

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if not isinstance(phone, Phone):
            phone = Phone(phone)
            self.phones.append(phone.value)

    def add_birthday(self, birthday):
        if not isinstance(birthday, Birthday):
            birthday = Birthday(birthday)
        if birthday:
            self.birthday = birthday.value
        return self.birthday
    
    def remove_phone(self, phone):
        if not isinstance(phone, Phone):
            phone = Phone(phone)
        if phone.value in self.phones:
            self.phones.remove(phone.value)
            return self.phones
        raise ValueError("Dont have this phone on the list")
    
    def edit_phone(self, phone, new_phone):
        if not isinstance(phone, Phone):
            phone = Phone(phone)
        if not isinstance(new_phone, Phone):
            new_phone = Phone(new_phone)
        if not phone.value in self.phones:
            raise ValueError("Dont have this phone on the list. Cant be changed")
        index = self.phones.index(phone.value)
        self.phones[index] = new_phone.value

    def find_phone(self, phone_number):
        if not isinstance(phone_number, Phone):
            phone_number = Phone(phone_number)
        for phone in self.phones:
            if phone == phone_number.value:
                return phone_number
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}"
    

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Value must be a Record instance")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)
    

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
        else:
            return "The name is not found"
        
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        for user in self.data.values():
            if user.birthday != None:
                birthday_realy = datetime.strptime(user.birthday, "%d.%m.%Y").date()
                birthday_this_year = birthday_realy.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                if 0 <= (birthday_this_year - today).days <= days:
                    congratulation_date_str = date_to_string(adjust_for_weekend(birthday_this_year))
                    upcoming_birthdays.append({"name": user.name.value, "congratulation_date": congratulation_date_str})
                    
        return upcoming_birthdays

        
    def __str__(self):
        result = f"------------My Phonebook------------\n"
        for i in self.data:
            message = f"Contact name: {i}, phones: {self.data[i].phones}\n"
            result = result + message
        return result + f"-------------------------------------"
