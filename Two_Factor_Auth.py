import pyotp
import qrcode
from PIL import Image, ImageDraw, ImageFont
import time
from collections import defaultdict
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes

# Store the number of failed attempts and the last attempt time for each user
failed_attempts = defaultdict(int)
last_attempt_time = defaultdict(float)

# Maximum allowed attempts
MAX_ATTEMPTS = 5
# Block time in seconds
BLOCK_TIME = 30
# Regeneration time in seconds (5 minutes)
REGEN_TIME = 300

# AES key and IV (In practice, securely manage these)
aes_key = get_random_bytes(32)  # 256-bit key
aes_iv = get_random_bytes(16)   # 128-bit IV

def encrypt_secret(secret: str) -> str:
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    encrypted_secret = cipher.encrypt(pad(secret.encode(), AES.block_size))
    return base64.b64encode(encrypted_secret).decode()

def decrypt_secret(encrypted_secret: str) -> str:
    encrypted_secret_bytes = base64.b64decode(encrypted_secret)
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    decrypted_secret = unpad(cipher.decrypt(encrypted_secret_bytes), AES.block_size).decode()
    return decrypted_secret

def generate_secret_key() -> str:
    secret = pyotp.random_base32()
    return encrypt_secret(secret)

def generate_qr_code(secret: str) -> Image:
    decrypted_secret = decrypt_secret(secret)
    otp_uri = pyotp.totp.TOTP(decrypted_secret).provisioning_uri("user@example.com", issuer_name="DemoApp")
    qr = qrcode.make(otp_uri)
    
    # Add a message to the QR code
    qr_image = qr.convert("RGB")
    draw = ImageDraw.Draw(qr_image)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
        
    text = "Scan this QR code with a valid authenticator app."
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    width, height = qr_image.size
    position = ((width - text_width) // 2, height - text_height - 10)
    draw.text(position, text, fill="black", font=font)
    
    return qr_image

def validate_otp(secret: str, user_otp: str, user_id: str) -> bool:
    current_time = time.time()
    
    # Check if the user is currently blocked
    if failed_attempts[user_id] >= MAX_ATTEMPTS:
        if current_time - last_attempt_time[user_id] < BLOCK_TIME:
            print("Too many attempts. Try again later.")
            return False
        else:
            failed_attempts[user_id] = 0
    
    decrypted_secret = decrypt_secret(secret)
    totp = pyotp.TOTP(decrypted_secret)
    if totp.verify(user_otp):
        failed_attempts[user_id] = 0
        return True
    else:
        failed_attempts[user_id] += 1
        last_attempt_time[user_id] = current_time
        return False

if __name__ == "__main__":
    secret_key = generate_secret_key()
    qr_code = generate_qr_code(secret_key)
    qr_code.show()
    
    user_id = "user@example.com"
    start_time = time.time()
    
    while True:
        user_otp = input("Enter the OTP: ")
        if validate_otp(secret_key, user_otp, user_id):
            print("Login successful!")
            break
        else:
            print("Invalid OTP!")
        
        # Check if regeneration time has passed (optional)
        if time.time() - start_time >= REGEN_TIME:
            print("Regenerating QR code and secret key for enhanced security...")
            secret_key = generate_secret_key()
            qr_code = generate_qr_code(secret_key)
            qr_code.show()
            start_time = time.time()  # Reset the timer

    # Close the program after successful login
    exit()
