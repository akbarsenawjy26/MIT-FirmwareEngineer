const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3000; // Port untuk server Express

// Mengatur endpoint untuk mengambil data tegangan (voltage) dari API
app.get('/api/voltage', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:5000/api/voltage');
    res.json(response.data); // Mengirim response data JSON ke client
  } catch (error) {
    console.error('Error fetching voltage data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Mengatur endpoint untuk mengambil data arus (current) dari API
app.get('/api/current', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:5000/api/current');
    res.json(response.data); // Mengirim response data JSON ke client
  } catch (error) {
    console.error('Error fetching current data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Mengatur endpoint untuk menampilkan halaman HTML
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html'); // Mengirim file HTML ke client
});

// Mulai server Express
app.listen(PORT, () => {
  console.log(`Server berjalan di http://localhost:${PORT}`);
});
