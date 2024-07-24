2FA (Two-Factor Authentication) Demonstration Project
Overview
This project demonstrates a basic implementation of Two-Factor Authentication (2FA) using Python. It showcases the process of generating and validating One-Time Passwords (OTPs) using a QR code scanned by an authenticator app. The project includes features like secret key encryption, QR code generation, OTP validation, and handling of failed attempts with a blocking mechanism.

Features
OTP Generation and Validation: Generate time-based OTPs and validate them against user input.
QR Code Generation: Create QR codes for easy OTP provisioning using authenticator apps like Google Authenticator or Authy.
Secret Key Encryption: Encrypt and decrypt the secret key using AES for enhanced security.
Failed Attempts Handling: Implement a blocking mechanism to handle multiple failed OTP attempts.
Secret Key Regeneration: Regenerate the QR code and secret key after a specified time to enhance security.
Getting Started
Prerequisites
Ensure you have the following libraries installed:

bash
Copy code
pip install -r requirements.txt
Running the Script
Clone the repository:
bash
Copy code
git clone https://github.com/yourusername/2fa-demo.git
cd 2fa-demo
Run the script:
bash
Copy code
python your_script_name.py
Interaction
The script will generate and display a QR code. Scan this QR code with an authenticator app.
Enter the OTP generated by the app when prompted by the script.
If the OTP is valid, a "Login successful!" message will appear, and the script will terminate.
If the OTP is invalid, you will be prompted to enter the OTP again until you get it right or the regeneration time elapses.
Technical Details
Code Overview
Encrypting and Decrypting the Secret

Encrypting the Secret: Uses AES encryption to encrypt the base32 secret key.

python
Copy code
def encrypt_secret(secret: str) -> str:
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    encrypted_secret = cipher.encrypt(pad(secret.encode(), AES.block_size))
    return base64.b64encode(encrypted_secret).decode()
Decrypting the Secret: Decrypts the encrypted secret key using AES.

python
Copy code
def decrypt_secret(encrypted_secret: str) -> str:
    encrypted_secret_bytes = base64.b64decode(encrypted_secret)
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    decrypted_secret = unpad(cipher.decrypt(encrypted_secret_bytes), AES.block_size).decode()
    return decrypted_secret
Generating the Secret Key

Generates a new base32 secret key and encrypts it.
python
Copy code
def generate_secret_key() -> str:
    secret = pyotp.random_base32()
    return encrypt_secret(secret)
Generating the QR Code

Generates a QR code from the OTP provisioning URI and adds a message for the user to scan it with an authenticator app.
python
Copy code
def generate_qr_code(secret: str) -> Image:
    decrypted_secret = decrypt_secret(secret)
    otp_uri = pyotp.totp.TOTP(decrypted_secret).provisioning_uri("user@example.com", issuer_name="DemoApp")
    qr = qrcode.make(otp_uri)
    
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
Validating OTPs

Validates the user-provided OTP against the encrypted secret key and handles failed attempts with a blocking mechanism.
python
Copy code
def validate_otp(secret: str, user_otp: str, user_id: str) -> bool:
    current_time = time.time()
    
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
Main Program Flow

Generates the secret key and QR code, prompts for user OTP, and validates the OTP. If the OTP is valid, the script displays a success message and exits.
python
Copy code
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
        
        if time.time() - start_time >= REGEN_TIME:
            print("Regenerating QR code and secret key for enhanced security...")
            secret_key = generate_secret_key()
            qr_code = generate_qr_code(secret_key)
            qr_code.show()
            start_time = time.time()  # Reset the timer

    exit()
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any questions or suggestions, please contact [your email].

