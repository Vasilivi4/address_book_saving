import pickle


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return self.value


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        if not self.value.isdigit() or len(self.value) != 10:
            raise ValueError("Номер телефону повинен містити 10 цифр")


class Record:
    def __init__(self, name):
        self.name = name.value
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if old_phone not in [p.value for p in self.phones]:
            raise ValueError("Номер телефону для редагування не існує")

        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p


class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.contacts, file)

    def load_from_file(self, filename):
        try:
            with open(filename, "rb") as file:
                self.contacts = pickle.load(file)
        except FileNotFoundError:
            self.contacts = []

    def search_contacts(self, query):
        results = []
        for contact in self.contacts:
            if (
                isinstance(
                    contact.name, str
                )  # Проверяем, является ли значение имени строкой
                and query.lower() in contact.name.lower()
            ) or any(query in phone.value for phone in contact.phones):
                results.append(contact)
        return results


def main():
    address_book = AddressBook()
    address_book.load_from_file("address_book.pkl")

    while True:
        print("\nMenu:")
        print("1. Add contact")
        print("2. Search contacts")
        print("3. Save and Exit")
        choice = input("Select option: ")

        if choice == "1":
            name_value = input("Enter a name for the contact: ")
            phone_value = input("Enter phone number for contact: ")
            name = Name(name_value)
            new_contact = Record(name)
            new_contact.add_phone(phone_value)  # Добавляем номер телефона отдельно
            address_book.add_contact(new_contact)
            print("Contact added!")

        if choice == "2":
            query = input("Enter a search term to search: ")
            results = address_book.search_contacts(
                query.lower()
            )  # Преобразуем запрос к нижнему регистру
            if results:
                print("Search results:")
                for contact in results:
                    print(
                        f"Name: {contact.name}, Phone: {contact.phones[0].value}"
                    )  # Используем первый номер телефона
            else:
                print("Contact not found.")

        elif choice == "3":
            address_book.save_to_file("address_book.pkl")
            print("Data is saved. Goodbye!")
            break


if __name__ == "__main__":
    main()
