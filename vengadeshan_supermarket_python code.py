import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to generate the bill with GST calculations
def generate_bill(customer_name, customer_email, items, prices, quantities, gst_rates, date):
    total = 0
    gst_total = 0
    bill_lines = []

    bill_header = f"""
Vengadeshan Supermarket
123 Street, Thevaram, Theni District
Phone: +91 12345 6879

Customer Details:
Name: {customer_name}
Email: {customer_email}
Date: {date}

Itemized Bill:

{"Item":<20} {"Quantity":<10} {"Unit Price":<10} {"GST Rate":<10} {"Total Price":<10}
{'-'*70}
"""
    bill_lines.append(bill_header)

    for item, quantity, price, gst_rate in zip(items, quantities, prices, gst_rates):
        item_total = price * quantity
        gst_amount = item_total * (gst_rate / 100)
        total_price = item_total + gst_amount

        total += item_total
        gst_total += gst_amount

        line = f"{item:<20} {quantity:<10} ₹{price:<9.2f} {gst_rate:<10}% ₹{total_price:<9.2f}\n"
        bill_lines.append(line)

    grand_total = total + gst_total

    bill_footer = f"""
{'-'*70}
Subtotal: ₹{total:.2f}
Total GST: ₹{gst_total:.2f}
Total Amount Due: ₹{grand_total:.2f}

Thank you for shopping with Vengadeshan Supermarket! Your bill has been sent to your email: {customer_email}

Billing Date: {date}
"""
    bill_lines.append(bill_footer)

    bill_content = ''.join(bill_lines)
    with open("bill.txt", "w") as file:
        file.write(bill_content)

    return bill_content

# Function to send the bill via email
def send_email(to_email, subject, body):
    from_email = "vengadeshan@example.com"  # Replace with your email
    from_password = "your_password"         # Replace with your password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email} successfully.")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

# User input for customer details
customer_name = input("Enter customer name: ")
customer_email = input("Enter customer email: ")
date = input("Enter billing date (e.g., June 14, 2024): ")

# User input for items
items = []
prices = []
quantities = []
gst_rates = []

n = int(input("Enter the number of items: "))

for i in range(n):
    item = input(f"Enter item {i+1} name: ")
    quantity = int(input(f"Enter item {i+1} quantity: "))
    price = float(input(f"Enter item {i+1} unit price: "))
    gst_rate = float(input(f"Enter item {i+1} GST rate (%): "))
    items.append(item)
    quantities.append(quantity)
    prices.append(price)
    gst_rates.append(gst_rate)

bill_content = generate_bill(customer_name, customer_email, items, prices, quantities, gst_rates, date)
send_email(customer_email, "Your Supermarket Bill with GST", bill_content)
