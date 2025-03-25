from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Endpoint untuk mengambil data cuaca
@app.route('/weather', methods=['GET'])
def get_weather():
    # Mendapatkan parameter 'city' dari query string, default 'Jakarta' jika tidak ada
    city = request.args.get('city', default='Jakarta', type=str)
    
    # API Key Anda dari OpenWeatherMap
    api_key = 'd873c1de1011d2d719388e34de8fc4dd'  # Gantilah dengan API key yang benar
    
    # Membuat URL untuk mengakses API dengan HTTPS
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    print(f"Request URL: {url}")  # Debugging: Menampilkan URL yang digunakan untuk permintaan
    try:
        # Mengirim permintaan ke API OpenWeatherMap
        response = requests.get(url, headers={"User-Agent": "WeatherApp"})  # Menambahkan User-Agent header
        
        # Memeriksa apakah response status code menunjukkan kesalahan (misalnya 4xx atau 5xx)
        response.raise_for_status()  # Akan melempar HTTPError jika status code bukan 200
        
        # Menampilkan status code dan respons dari API (untuk debugging)
        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Content: {response.text}")
        
        # Mengonversi respons JSON menjadi data Python
        data = response.json()

        # Jika status code dari API adalah 200, kita ekstrak data cuaca
        if data['cod'] == 200:
            # Mengonversi temperatur dari Kelvin ke Celsius
            temperature_celsius = data['main']['temp'] - 273.15  # Konversi ke Celsius
            
            weather_info = {
                'city': city,
                'temperature': round(temperature_celsius, 2),  # Membulatkan ke dua angka desimal
                'description': data['weather'][0]['description']
            }
            return jsonify(weather_info), 200
        else:
            # Menangani kasus jika 'cod' bukan 200, seperti kota tidak ditemukan
            return jsonify({'error': 'City not found or invalid'}), 404
            
    except requests.exceptions.HTTPError as http_err:
        # Menangani kesalahan HTTP (misalnya 404, 401)
        print(f"HTTP error occurred: {http_err}")  # Debugging
        return jsonify({'error': f'HTTP error: {http_err}'}), 400
    except requests.exceptions.RequestException as err:
        # Menangani kesalahan umum lainnya, misalnya masalah jaringan
        print(f"Error: {err}")  # Debugging
        return jsonify({'error': f'Request error: {err}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
