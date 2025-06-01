const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');

// Route imports
const cameraRoutes = require('./routes/cameras');
const analyticsRoutes = require('./routes/analytics');
const customersRoutes = require('./routes/customers');
const vehiclesRoutes = require('./routes/vehicles');

dotenv.config();
const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/trinetra', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => {
    console.log('Connected to MongoDB');
}).catch((error) => {
    console.error('MongoDB connection error:', error);
});

// Routes
app.use('/api/cameras', cameraRoutes);
app.use('/api/analytics', analyticsRoutes);
app.use('/api/customers', customersRoutes);
app.use('/api/vehicles', vehiclesRoutes);

// Health check endpoint
app.get('/', (req, res) => {
    res.json({ status: 'ok', message: 'TRINETRA API is running' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
