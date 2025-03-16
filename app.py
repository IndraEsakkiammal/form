from flask import Flask, render_template, request, send_file
import mysql.connector
import qrcode

app = Flask(__name__)

# MySQL Database Configuration
db_config = {
    "host": "localhost",  
    "user": "root",       
    "password": "1234",  
    "database": "trolly"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    phone = request.form["phone"]
    address = request.form["address"]
    city = request.form["city"]
    pincode = request.form["pincode"]

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if phone number already exists
        cursor.execute("SELECT * FROM Customer WHERE customer_phone = %s", (phone,))
        existing_customer = cursor.fetchone()

        if existing_customer:
            return "<h1>⚠️ You are already registered. Thank You!</h1>"

        # Insert new customer record
        cursor.execute(
            "INSERT INTO Customer (customer_name, customer_phone, customer_address, customer_city, customer_pincode) VALUES (%s, %s, %s, %s, %s)",
            (name, phone, address, city, pincode)
        )
        conn.commit()
        return "<h1>✅ Registration Successful!</h1>"

    except mysql.connector.Error as err:
        return f"<h1>❌ Database Error: {err}</h1>"

    finally:
        cursor.close()
        conn.close()

@app.route("/qrcode")
def generate_qr():
    url = "https://yourapp.onrender.com/?ngrok-skip-browser-warning=true"
    qr = qrcode.make(url)
    qr.save("qrcode.png")  # Save QR code in the same filename
    return send_file("qrcode.png", mimetype="image/png")  # Serve the QR image dynamically

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
