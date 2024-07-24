import pyotp
import qrcode
from PIL import Image

# Step 1: Generate a secret key
def generate_secret_key():
    return pyotp.random_base32()

secret_key = generate_secret_key()
print("Secret Key:", secret_key)

# Step 2: Generate a QR code from the secret key and display it
def generate_qr_code(secret):
    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri("user@example.com", issuer_name="DemoApp")
    qr = qrcode.make(otp_uri)
    qr.show()  # This will display the QR code
    print("QR code generated and displayed.")

generate_qr_code(secret_key)

# Step 3: Validate the OTP entered by the user
def validate_otp(secret, user_otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(user_otp)

# Prompt the user to enter the OTP from the authenticator app
user_otp = input("Enter the OTP: ")
if validate_otp(secret_key, user_otp):
    print("OTP is valid!")
else:
    print("Invalid OTP!")
