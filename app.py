from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection function
def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="trolly"
        )
        return db
    except mysql.connector.Error as err:
        print("❌ Database connection error:", err)
        return None

@app.route('/')
def home():
    return render_template('index.html')  # Loads registration form

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    city = request.form.get('city')
    pincode = request.form.get('pincode')

    if not all([name, phone, address, city, pincode]):
        return jsonify({'status': 'error', 'message': 'Please fill all fields'})

    db = get_db_connection()
    if db is None:
        return jsonify({'status': 'error', 'message': 'Database connection failed!'})

    cursor = None  # ✅ Prevents UnboundLocalError

    try:
        cursor = db.cursor()

        # Check if phone number already exists
        cursor.execute("SELECT * FROM Customer WHERE customer_phone = %s", (phone,))
        existing_customer = cursor.fetchone()

        if existing_customer:
            return jsonify({'status': 'error', 'message': 'You are already registered!'})

        # Insert new customer
        cursor.execute("""
            INSERT INTO Customer (customer_name, customer_phone, customer_address, customer_city, customer_pincode)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, phone, address, city, pincode))
        db.commit()

        return jsonify({'status': 'success', 'message': 'Registration successful!'})

    except mysql.connector.Error as err:
        print("❌ Database Error:", err)
        return jsonify({'status': 'error', 'message': f'Database error: {err}'})
    
    finally:
        if cursor:  
            cursor.close()
        if db:
            db.close()

if __name__ == '__main__':
    app.run(debug=True)
