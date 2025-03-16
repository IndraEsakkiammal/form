import qrcode

# Your Render-deployed URL (Replace with your actual Render URL)
render_url = "https://flask-qrcode-app.onrender.com/?ngrok-skip-browser-warning=true"

# Generate QR code
qr = qrcode.make(render_url)

# Save it as qrcode.png (consistent with app.py)
qr.save("qrcode.png")

print("✅ QR Code Generated Successfully! Saved as qrcode.png")
