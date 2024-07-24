# 2FA (Two-Factor Authentication) Demonstration Project

## Overview

This project demonstrates a basic implementation of Two-Factor Authentication (2FA) using Python. It showcases the process of generating and validating One-Time Passwords (OTPs) using a QR code scanned by an authenticator app. The project includes features like secret key encryption, QR code generation, OTP validation, and handling of failed attempts with a blocking mechanism.

## Features

- OTP Generation and Validation
- QR Code Generation for OTP Provisioning
- Secret Key Encryption using AES
- Handling Multiple Failed OTP Attempts
- Secret Key Regeneration for Enhanced Security

## Getting Started

### Prerequisites

Ensure you have the following libraries installed:

bash
pip install -r requirements.txt


### Installation

1. **Clone the repository:**

bash
git clone https://github.com/yourusername/2fa-demo.git
cd 2fa-demo


2. **Install the required packages:**

bash
pip install -r requirements.txt


# Usage

1. **Run the script:**

bash
python your_script_name.py


2. **Interaction:**
    - The script will generate and display a QR code. Scan this QR code with an authenticator app.
    - Enter the OTP generated by the app when prompted by the script.
    - If the OTP is valid, a "Login successful!" message will appear, and the script will terminate.
    - If the OTP is invalid, you will be prompted to enter the OTP again until you get it right or the regeneration time elapses.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please contact prepprepcall911@gmail.com.
