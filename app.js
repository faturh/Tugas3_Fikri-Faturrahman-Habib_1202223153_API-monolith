const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

// API Key OpenWeatherMap Anda
const apiKey = '0376c622c914cfcea53dec537780cfc9';  // Pastikan API key ini benar dan aktif

// Endpoint untuk mengambil data cuaca
app.get('/weather', async (req, res) => {
    const city = req.query.city || 'Jakarta';  // Default city adalah Jakarta jika parameter tidak ada
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`; // units=metric untuk temperatur dalam Celsius

    console.log(`Request URL: ${url}`);  // Debugging: Menampilkan URL yang digunakan untuk permintaan
    
    try {
        // Mengirim permintaan GET ke API OpenWeatherMap
        const response = await axios.get(url);
        
        // Jika status code adalah 200, berarti permintaan berhasil
        if (response.status === 200) {
            const weatherData = {
                city: city,
                temperature: response.data.main.temp,  // Suhu dalam Celsius
                description: response.data.weather[0].description  // Deskripsi cuaca
            };
            
            console.log(weatherData);  // Debugging: Menampilkan data cuaca yang diterima
            res.json(weatherData);     // Mengirimkan data cuaca dalam format JSON ke client
        } else {
            // Jika API mengembalikan status code selain 200, misalnya 404
            console.log(`City not found or invalid API key: ${city}`);
            res.status(404).json({ error: 'City not found or invalid API key' });
        }
    } catch (error) {
        // Menangani error yang terjadi saat fetching data
        console.error(`Error fetching weather data: ${error.message}`);  // Debugging: Menampilkan error yang terjadi
        
        // Memberikan pesan error yang lebih jelas jika API key salah atau kota tidak ditemukan
        if (error.response && error.response.status === 401) {
            res.status(401).json({ error: 'Invalid API key or Unauthorized access' });
        } else {
            res.status(500).json({ error: 'Failed to fetch data' });
        }
    }
});

// Menjalankan server pada port 3000
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
