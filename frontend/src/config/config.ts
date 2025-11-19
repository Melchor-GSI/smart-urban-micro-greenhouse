// Configuration for the IoT sensor dashboard
export const config = {
    // API Configuration
    api: {
        // Change this to your actual server endpoint
        baseUrl: 'http://localhost:5001',
        endpoints: {
            sensors: '/api/readings/now',
            readings: '/api/readings/',
            events: '/api/events/',
        },
        // Data fetch interval in milliseconds (500ms = 0.5 seconds)
        fetchInterval: 1000,
    },

    // Sensor thresholds for status determination
    thresholds: {
        temperature: {
            critical: { min: 10, max: 35 },
            warning: { min: 14, max: 30 },
        },
        humidity: {
            critical: { min: 30, max: 90 },
            warning: { min: 40, max: 80 },
        },
        soilMoisture: {
            critical: { min: 20, max: 90 },
            warning: { min: 30, max: 80 },
        },
        co2: {
            critical: { min: 350, max: 2000 },
            warning: { min: 550, max: 1200 },
        },
    },
};