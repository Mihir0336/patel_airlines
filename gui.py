import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont

BG_COLOR = "#f0f4f8"
HEADER_BG = "#1976d2"
HEADER_FG = "#fff"
BTN_BG = "#2196f3"
BTN_FG = "#fff"
ENTRY_BG = "#fff"
ENTRY_FG = "#222"
FRAME_BG = "#e3eaf2"

class AirTicketBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patel's Airline Reservation System")
        self.root.geometry("480x500")
        self.root.configure(bg=BG_COLOR)
        self.header_font = tkfont.Font(family="Arial", size=16, weight="bold")
        self.label_font = tkfont.Font(family="Arial", size=11)
        self.button_font = tkfont.Font(family="Arial", size=11, weight="bold")
        self.create_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_header(self, text):
        header = tk.Label(self.root, text=text, font=self.header_font, bg=HEADER_BG, fg=HEADER_FG, pady=16)
        header.pack(fill='x')

    def create_main_menu(self):
        self.clear_window()
        self.create_header("Welcome to Patel's Airline Reservation System")
        menu_frame = tk.Frame(self.root, bg=FRAME_BG, bd=2, relief=tk.RIDGE)
        menu_frame.pack(pady=40, padx=40, fill='both', expand=True)
        btn_opts = {'font': self.button_font, 'bg': BTN_BG, 'fg': BTN_FG, 'activebackground': HEADER_BG, 'activeforeground': HEADER_FG, 'bd': 0, 'height': 2, 'width': 28, 'cursor': 'hand2'}
        tk.Button(menu_frame, text="Book a Flight", command=self.book_flight_form, **btn_opts).pack(pady=18)
        tk.Button(menu_frame, text="Cancel a Flight", command=self.cancel_flight_form, **btn_opts).pack(pady=18)
        tk.Button(menu_frame, text="View Reservations", command=self.view_reservations_form, **btn_opts).pack(pady=18)
        tk.Button(menu_frame, text="Exit", command=self.root.quit, **btn_opts).pack(pady=18)

    def book_flight_form(self):
        self.clear_window()
        self.create_header("Book a Flight")
        form_frame = tk.Frame(self.root, bg=FRAME_BG, bd=2, relief=tk.RIDGE)
        form_frame.pack(pady=30, padx=40, fill='both', expand=True)
        labels = ["Name", "From (departure city)", "To (destination city)", "Travel date (DD-MM-YYYY)", "Contact number", "Email address"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label+':', font=self.label_font, bg=FRAME_BG, anchor='w').grid(row=i, column=0, sticky='w', pady=8, padx=10)
            entry = tk.Entry(form_frame, width=28, font=self.label_font, bg=ENTRY_BG, fg=ENTRY_FG, relief=tk.GROOVE, bd=2)
            entry.grid(row=i, column=1, pady=8, padx=10)
            self.entries[label] = entry
        btn_opts = {'font': self.button_font, 'bg': BTN_BG, 'fg': BTN_FG, 'activebackground': HEADER_BG, 'activeforeground': HEADER_FG, 'bd': 0, 'height': 2, 'width': 18, 'cursor': 'hand2'}
        tk.Button(form_frame, text="Book Flight", command=self.handle_booking, **btn_opts).grid(row=len(labels), column=0, pady=18, padx=10)
        tk.Button(form_frame, text="Back", command=self.create_main_menu, **btn_opts).grid(row=len(labels), column=1, pady=18, padx=10)

    def handle_booking(self):
        name = self.entries["Name"].get().strip()
        from_city = self.entries["From (departure city)"].get().strip()
        to_city = self.entries["To (destination city)"].get().strip()
        date = self.entries["Travel date (DD-MM-YYYY)"].get().strip()
        contact = self.entries["Contact number"].get().strip()
        email = self.entries["Email address"].get().strip()
        if not name or not from_city or not to_city or not date or not contact or not email:
            messagebox.showerror("Error", "All fields are required.")
            return
        if not self.validate_date(date):
            messagebox.showerror("Error", "Invalid date format. Please use DD-MM-YYYY.")
            return
        if not self.validate_phone(contact):
            messagebox.showerror("Error", "Contact number must be 10 digits.")
            return
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return
        import random
        price = random.randint(2500, 10000)
        if not messagebox.askyesno("Confirm Booking", f"Ticket price from {from_city} to {to_city} on {date}: ₹{price}\n\nDo you want to confirm your booking?"):
            return
        reservations = self.load_data()
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
        self.save_data(reservations)
        self.show_boarding_pass(reservation)
        self.create_main_menu()

    def cancel_flight_form(self):
        self.clear_window()
        self.create_header("Cancel a Flight")
        form_frame = tk.Frame(self.root, bg=FRAME_BG, bd=2, relief=tk.RIDGE)
        form_frame.pack(pady=60, padx=40, fill='both', expand=True)
        tk.Label(form_frame, text="Name:", font=self.label_font, bg=FRAME_BG, anchor='w').grid(row=0, column=0, pady=12, padx=10, sticky='w')
        self.cancel_name_entry = tk.Entry(form_frame, width=28, font=self.label_font, bg=ENTRY_BG, fg=ENTRY_FG, relief=tk.GROOVE, bd=2)
        self.cancel_name_entry.grid(row=0, column=1, pady=12, padx=10)
        tk.Label(form_frame, text="Reservation ID:", font=self.label_font, bg=FRAME_BG, anchor='w').grid(row=1, column=0, pady=12, padx=10, sticky='w')
        self.cancel_id_entry = tk.Entry(form_frame, width=28, font=self.label_font, bg=ENTRY_BG, fg=ENTRY_FG, relief=tk.GROOVE, bd=2)
        self.cancel_id_entry.grid(row=1, column=1, pady=12, padx=10)
        btn_opts = {'font': self.button_font, 'bg': BTN_BG, 'fg': BTN_FG, 'activebackground': HEADER_BG, 'activeforeground': HEADER_FG, 'bd': 0, 'height': 2, 'width': 18, 'cursor': 'hand2'}
        tk.Button(form_frame, text="Cancel Flight", command=self.handle_cancel, **btn_opts).grid(row=2, column=0, pady=18, padx=10)
        tk.Button(form_frame, text="Back", command=self.create_main_menu, **btn_opts).grid(row=2, column=1, pady=18, padx=10)

    def handle_cancel(self):
        name = self.cancel_name_entry.get().strip()
        reservation_id = self.cancel_id_entry.get().strip()
        if not name or not reservation_id:
            messagebox.showerror("Error", "Both fields are required.")
            return
        try:
            reservation_id = int(reservation_id)
        except ValueError:
            messagebox.showerror("Error", "Reservation ID must be a number.")
            return
        reservations = self.load_data()
        updated_reservations = [r for r in reservations if not (r['id'] == reservation_id and r['name'].lower() == name.lower())]
        if len(updated_reservations) < len(reservations):
            self.save_data(updated_reservations)
            messagebox.showinfo("Success", "Flight canceled successfully!")
        else:
            messagebox.showerror("Error", "No matching reservation found.")
        self.create_main_menu()

    def view_reservations_form(self):
        self.clear_window()
        self.create_header("View Reservations")
        form_frame = tk.Frame(self.root, bg=FRAME_BG, bd=2, relief=tk.RIDGE)
        form_frame.pack(pady=60, padx=40, fill='both', expand=True)
        tk.Label(form_frame, text="Name:", font=self.label_font, bg=FRAME_BG, anchor='w').grid(row=0, column=0, pady=12, padx=10, sticky='w')
        self.view_name_entry = tk.Entry(form_frame, width=28, font=self.label_font, bg=ENTRY_BG, fg=ENTRY_FG, relief=tk.GROOVE, bd=2)
        self.view_name_entry.grid(row=0, column=1, pady=12, padx=10)
        tk.Label(form_frame, text="Contact number:", font=self.label_font, bg=FRAME_BG, anchor='w').grid(row=1, column=0, pady=12, padx=10, sticky='w')
        self.view_contact_entry = tk.Entry(form_frame, width=28, font=self.label_font, bg=ENTRY_BG, fg=ENTRY_FG, relief=tk.GROOVE, bd=2)
        self.view_contact_entry.grid(row=1, column=1, pady=12, padx=10)
        btn_opts = {'font': self.button_font, 'bg': BTN_BG, 'fg': BTN_FG, 'activebackground': HEADER_BG, 'activeforeground': HEADER_FG, 'bd': 0, 'height': 2, 'width': 18, 'cursor': 'hand2'}
        tk.Button(form_frame, text="View Reservations", command=self.handle_view_reservations, **btn_opts).grid(row=2, column=0, pady=18, padx=10)
        tk.Button(form_frame, text="Back", command=self.create_main_menu, **btn_opts).grid(row=2, column=1, pady=18, padx=10)

    def handle_view_reservations(self):
        name = self.view_name_entry.get().strip()
        contact = self.view_contact_entry.get().strip()
        if not name or not contact:
            messagebox.showerror("Error", "Both fields are required.")
            return
        if not self.validate_phone(contact):
            messagebox.showerror("Error", "Contact number must be 10 digits.")
            return
        reservations = self.load_data()
        user_reservations = [r for r in reservations if r['name'].lower() == name.lower() and r['contact'] == contact]
        if user_reservations:
            msg = f"✈️  Found {len(user_reservations)} reservation(s):\n\n"
            for reservation in user_reservations:
                msg += self.format_boarding_pass(reservation) + "\n\n"
            self.show_scrollable_message("Your Reservations", msg)
        else:
            messagebox.showerror("Error", "No reservations found for the given details.")
        # self.create_main_menu()  # Removed to keep results window open

    def format_boarding_pass(self, reservation):
        return (
            f"================== ✈️  BOARDING PASS ==================\n"
            f"🧾 Reservation ID (PNR):  {reservation['id']}\n"
            f"👤 Passenger Name       :  {reservation['name']}\n"
            f"📍 From                 :  {reservation['from']}\n"
            f"📍 To                   :  {reservation['to']}\n"
            f"📅 Travel Date          :  {reservation['date']}\n"
            f"📞 Contact              :  {reservation['contact']}\n"
            f"📧 Email                :  {reservation['email']}\n"
            f"💵 Ticket Price         :  ₹{reservation['price']}\n"
            f"======================================================"
        )

    def show_scrollable_message(self, title, message):
        top = tk.Toplevel(self.root)
        top.title(title)
        text = tk.Text(top, wrap='word', width=70, height=20, font=self.label_font, bg=BG_COLOR, fg=ENTRY_FG)
        text.insert('1.0', message)
        text.config(state='disabled')
        text.pack(expand=True, fill='both')
        tk.Button(top, text="Close", command=top.destroy, font=self.button_font, bg=BTN_BG, fg=BTN_FG, activebackground=HEADER_BG, activeforeground=HEADER_FG, bd=0, height=2, width=12, cursor='hand2').pack(pady=5)

    def show_boarding_pass(self, reservation):
        msg = (
            f"================== ✈️  BOARDING PASS ==================\n"
            f"         🛫 Patel's Airline Reservation System\n"
            f"------------------------------------------------------\n"
            f"🧾 Reservation ID (PNR):  {reservation['id']}\n"
            f"👤 Passenger Name       :  {reservation['name']}\n"
            f"📍 From                 :  {reservation['from']}\n"
            f"📍 To                   :  {reservation['to']}\n"
            f"📅 Travel Date          :  {reservation['date']}\n"
            f"📞 Contact              :  {reservation['contact']}\n"
            f"📧 Email                :  {reservation['email']}\n"
            f"💵 Ticket Price         :  ₹{reservation['price']}\n"
            f"======================================================"
        )
        messagebox.showinfo("Boarding Pass", msg)

    # --- Data and validation helpers ---
    def load_data(self):
        import json, os
        DATA_FILE = 'reservations.json'
        if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
            with open(DATA_FILE, 'w') as f:
                json.dump([], f)
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def save_data(self, data):
        import json
        with open('reservations.json', 'w') as f:
            json.dump(data, f, indent=4)

    def validate_date(self, date_str):
        from datetime import datetime
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    def validate_email(self, email):
        import re
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10

if __name__ == "__main__":
    root = tk.Tk()
    app = AirTicketBookingApp(root)
    root.mainloop() 