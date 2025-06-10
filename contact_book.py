import os

def load_contacts():
    """Load contacts from contacts.txt file"""
    contacts = []
    try:
        if os.path.exists("contacts.txt"):
            with open("contacts.txt", "r") as file:
                for line in file:
                    if line.strip():
                        try:
                            name, phone, email = line.strip().split(",")
                            contacts.append({"name": name, "phone": phone, "email": email})
                        except ValueError:
                            print(f"Skipping malformed line: {line}")
    except Exception as e:
        print(f"Error loading contacts: {e}")
    return contacts

def save_contacts(contacts):
    """Save contacts to contacts.txt file"""
    with open("contacts.txt", "w") as file:
        for contact in contacts:
            file.write(f"{contact['name']},{contact['phone']},{contact['email']}\n")

def add_contact(contacts):
    """Add a new contact"""
    print("\nAdd New Contact")
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    
    contacts.append({"name": name, "phone": phone, "email": email})
    save_contacts(contacts)
    print(f"{name} has been added to contacts!")

def view_contacts(contacts):
    print("\nAll Contacts")
    print("-" * 30)
    if not contacts:
        print("No contacts found!")
    else:
        for i, contact in enumerate(contacts, 1):
            print(f"{i}. {contact['name']}")
            print(f"   Phone: {contact['phone']}")
            print(f"   Email: {contact['email']}")
            print("-" * 30)

def search_contact(contacts):
    """Search contacts by name"""
    print("\nSearch Contacts")
    search_term = input("Enter name to search: ").lower()
    
    found = [c for c in contacts if search_term in c["name"].lower()]
    
    if not found:
        print("No matching contacts found!")
    else:
        print(f"\nFound {len(found)} contact(s):")
        for contact in found:
            print(f"Name: {contact['name']}")
            print(f"Phone: {contact['phone']}")
            print(f"Email: {contact['email']}")
            print("-" * 30)

def update_contact(contacts):
    """Update an existing contact"""
    print("\nUpdate Contact")
    name = input("Enter the name of the contact to update: ").strip()
    for contact in contacts:
        if contact['name'].lower() == name.lower():
            print(f"Current details: {contact}")
            new_name = input("New name (leave blank to keep current): ").strip()
            new_phone = input("New phone (leave blank to keep current): ").strip()
            new_email = input("New email (leave blank to keep current): ").strip()

            if new_name:
                contact['name'] = new_name
            if new_phone:
                contact['phone'] = new_phone
            if new_email:
                contact['email'] = new_email

            save_contacts(contacts)
            print("✅ Contact updated successfully.")
            return
    print("❌ Contact not found.")

def delete_contact(contacts):
    """Delete an existing contact"""
    print("\nDelete Contact")
    name = input("Enter the name of the contact to delete: ").strip()
    for i, contact in enumerate(contacts):
        if contact['name'].lower() == name.lower():
            confirm = input(f"Are you sure you want to delete {contact['name']}? (y/n): ").strip().lower()
            if confirm == 'y':
                contacts.pop(i)
                save_contacts(contacts)
                print("🗑️ Contact deleted successfully.")
            else:
                print("❎ Deletion cancelled.")
            return
    print("❌ Contact not found.")

def main():
    """Main program loop"""
    contacts = load_contacts()
    
    while True:
        print("\nContact Book Menu")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contacts")
        print("4. Exit")
        print("5. Update Contact")
        print("6. Delete Contact")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            print("Goodbye!")
            break
        elif choice == "5":
            update_contact(contacts)
        elif choice == "6":
            delete_contact(contacts)
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
