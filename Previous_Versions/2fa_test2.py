import pyotp
import qrcode
from PIL import Image, ImageDraw, ImageFont
import time
from collections import defaultdict

# Store the number of failed attempts and the last attempt time for each user
failed_attempts = defaultdict(int)
last_attempt_time = defaultdict(float)

# Maximum allowed attempts
MAX_ATTEMPTS = 5
# Block time in seconds
BLOCK_TIME = 60

# Step 1: Generate a secret key
def generate_secret_key():
    return pyotp.random_base32()

# Step 2: Generate a QR code from the secret key and display it
def generate_qr_code(secret):
    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri("user@example.com", issuer_name="DemoApp")
    qr = qrcode.make(otp_uri)
    
    # Add a message to the QR code
    qr_image = qr.convert("RGB")
    draw = ImageDraw.Draw(qr_image)
    try:
        # You might need to adjust the path to the font file or use a default one
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
        
    text = "Scan this QR code with a valid authenticator app."
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    width, height = qr_image.size
    # Adjust the position to move the text a bit to the left
    position = ((width - text_width) // 2, height - text_height - 10)
    draw.text(position, text, fill="black", font=font)
    
    return qr_image

# Step 3: Validate the OTP entered by the user
def validate_otp(secret, user_otp, user_id):
    current_time = time.time()
    
    # Check if the user is currently blocked
    if failed_attempts[user_id] >= MAX_ATTEMPTS:
        if current_time - last_attempt_time[user_id] < BLOCK_TIME:
            print("Too many attempts. Try again later.")
            return False
        else:
            # Reset the counter if the block time has passed
            failed_attempts[user_id] = 0
    
    totp = pyotp.TOTP(secret)
    if totp.verify(user_otp):
        # Reset the counter on successful validation
        failed_attempts[user_id] = 0
        return True
    else:
        # Increment the counter on failed validation
        failed_attempts[user_id] += 1
        last_attempt_time[user_id] = current_time
        return False

if __name__ == "__main__":
    secret_key = generate_secret_key()

    # Generate and show the QR code immediately
    qr_code = generate_qr_code(secret_key)
    qr_code.show()  # This will display the QR code with the message

    # Simulate user ID
    user_id = "user@example.com"

    while True:
        # Prompt the user to enter the OTP from the authenticator app
        user_otp = input("Enter the OTP: ")
        if validate_otp(secret_key, user_otp, user_id):
            print("OTP is valid!")
            break
        else:
            print("Invalid OTP!")
