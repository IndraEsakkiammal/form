import qrcode

# ✅ Correct Render URL
HOME_URL = "https://form-kufc.onrender.com/"

# Generate QR Code
qr = qrcode.make(HOME_URL)

# Save QR Code
qr.save("customer_qr.png")

print("✅ QR Code generated successfully! Scan it to open the form.")
