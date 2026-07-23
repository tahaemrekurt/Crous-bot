import time
import requests
import os
import smtplib
from email.mime.text import MIMEText

API_URL = "https://trouverunlogement.lescrous.fr/api/fr/search/47"

PARAMS = {
    "bounds": "7.6881371_48.6461896_7.8360646_48.491861",
    "page": 1,
    "perPage": 20
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*"
}

# --- EMAIL CONFIGURATION ---
SENDER_EMAIL = "kurttahaemre@gmail.com"
SENDER_PASSWORD = "ijyq ysbl bsgy izym"  # Google'dan aldığın 16 haneli uygulama şifresini buraya yaz
RECEIVER_EMAIL = "kurttahaemre@gmail.com"

def send_alert(housing_items):
    subject = f"🏠 CROUS Alert: {len(housing_items)} Housing Available in Strasbourg!"
    body = "New CROUS housing offers found:\n\n"
    
    for item in housing_items:
        title = item.get("title", "CROUS Residence")
        price = item.get("price", "N/A")
        body += f"• {title} - {price}€\n"
    
    body += "\nDirect link: https://trouverunlogement.lescrous.fr/tools/47/search?bounds=7.6881371_48.6461896_7.8360646_48.491861&locationName=Strasbourg"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_crous():
    print("Checking CROUS Strasbourg API...")
    try:
        response = requests.get(API_URL, params=PARAMS, headers=HEADERS, timeout=10)
        data = response.json()
        
        results = data.get("results", {}).get("items", [])
        
        if results:
            print(f"🎉 FOUND {len(results)} AVAILABLE PLACES!")
            send_alert(results)
        else:
            print("No housing available right now.")
            
    except Exception as e:
        print(f"Error querying API: {e}")

if __name__ == "__main__":
    check_crous()