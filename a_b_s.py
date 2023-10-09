import pickle


class Field:
    def __init__(self, value):
        self.value = value


class Phone(Field):
    pass


class Name(Field):
    pass


class Record:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone


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
                query.lower() in contact.name.value.lower()
                or query in contact.phone.value
            ):
                results.append(contact)
        return results


def main():
    address_book = AddressBook()
    address_book.load_from_file("address_book.pkl")

    while True:
        print("\nMenu:")
        print("1. Add contact")
        print("2. Search contacts")
        print("3. Exit")
        choice = input("Select option: ")

        if choice == "1":
            name_value = input("Enter a name for the contact: ")
            phone_value = input("Enter phone number for contact: ")
            name = Name(name_value)
            phone = Phone(phone_value)
            new_contact = Record(name, phone)
            address_book.add_contact(new_contact)
            print("Contact added!")

        elif choice == "2":
            query = input("Enter a search term to search: ")
            results = address_book.search_contacts(query)
            if results:
                print("Search results:")
                for contact in results:
                    print(f"Name: {contact.name.value}, Phone: {contact.phone.value}")
            else:
                print("Contact not found.")

        elif choice == "3":
            address_book.save_to_file("address_book.pkl")
            print("Data is saved. Goodbye!")
            break


if __name__ == "__main__":
    main()
