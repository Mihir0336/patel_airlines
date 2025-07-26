import re
from datetime import datetime
import random
import json
import os

DATA_FILE = 'reservations.json'

if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ✅ Validation helpers
def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10


def patelAirLines():
    print("-----------Hello, Welcome to Patel's Airline Reservation System-----------")
    print("Please choose an option:")
    print("1. Book a flight") 
    print("2. Cancel a flight")
    print("3. View reservations")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        book_flight()
    elif choice == '2':
        cancel_flight()
    elif choice == '3':
        view_reservations()
    elif choice == '4':
        print("\nThank you for using Patel's Airline Reservation System. Goodbye!")
    else:
        print("Invalid choice. Please try again.")
        patelAirLines()

def book_flight():
    print("\n-----------Booking a Flight-----------")
    name = input("Enter your name: ")
    from_city = input("From (departure city): ")
    to_city = input("To (destination city): ")

    # ✅ Validated date input
    while True:
        date = input("Enter your travel date (DD-MM-YYYY): ")
        if validate_date(date):
            break
        print("❌ Invalid date format. Please enter as DD-MM-YYYY.")

    # ✅ Validated phone number
    while True:
        contact = input("Enter your contact number: ")
        if validate_phone(contact):
            break
        print("❌ Invalid contact number. It should be 10 digits.")

    # ✅ Validated email
    while True:
        email = input("Enter your email address: ")
        if validate_email(email):
            break
        print("❌ Invalid email format. Try again.")

    # 💸 Generate and show random price
    price = random.randint(2500, 10000)
    print(f"\n💰 Ticket price from {from_city} to {to_city} on {date}: ₹{price}")

    confirm = input("Do you want to confirm your booking? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Booking cancelled by user.\n")
        return patelAirLines()

    reservations = load_data()
    reservation_id = len(reservations) + 1

    reservation = {
        "id": reservation_id,
        "name": name,
        "from": from_city,
        "to": to_city,
        "date": date,
        "contact": contact,
        "email": email,
        "price": price
    }

    reservations.append(reservation)
    save_data(reservations)

    print(f"\n✅ Flight booked successfully!")
    print_boarding_pass(reservation)
    patelAirLines()

def cancel_flight():
    print("\n-----------Canceling a Flight-----------")
    name = input("Enter your name: ")
    try:
        reservation_id = int(input("Enter your reservation ID: "))
    except ValueError:
        print("Invalid reservation ID. Must be a number.")
        return patelAirLines()

    reservations = load_data()
    updated_reservations = [r for r in reservations if not (r['id'] == reservation_id and r['name'].lower() == name.lower())]

    if len(updated_reservations) < len(reservations):
        save_data(updated_reservations)
        print("\nFlight canceled successfully!")
    else:
        print("\nNo matching reservation found.")

    print("-----------------------------------------------------------------\n")
    patelAirLines()

def view_reservations():
    print("\n-----------Viewing Reservations-----------")
    name = input("Enter your name: ")
    contact = input("Enter your contact number: ")

    reservations = load_data()
    user_reservations = [r for r in reservations if r['name'].lower() == name.lower() and r['contact'] == contact]

    if user_reservations:
        print(f"\n✈️  Found {len(user_reservations)} reservation(s):\n")
        for reservation in user_reservations:
            print_boarding_pass(reservation)
    else:
        print("❌ No reservations found for the given details.")

    print("-----------------------------------------------------------------\n")
    patelAirLines()


def print_boarding_pass(reservation):
    print("\n================== ✈️  BOARDING PASS ==================")
    print("         🛫 Patel's Airline Reservation System")
    print("------------------------------------------------------")
    print(f"🧾 Reservation ID (PNR):  {reservation['id']}")
    print(f"👤 Passenger Name       :  {reservation['name']}")
    print(f"📍 From                 :  {reservation['from']}")
    print(f"📍 To                   :  {reservation['to']}")
    print(f"📅 Travel Date          :  {reservation['date']}")
    print(f"📞 Contact              :  {reservation['contact']}")
    print(f"📧 Email                :  {reservation['email']}")
    print(f"💵 Ticket Price         :  ₹{reservation['price']}")
    print("======================================================\n")


patelAirLines()
