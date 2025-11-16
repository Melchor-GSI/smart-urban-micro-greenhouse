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
            critical: { min: 18, max: 28 },
            warning: { min: 20, max: 26 },
        },
        humidity: {
            critical: { min: 40, max: 80 },
            warning: { min: 50, max: 70 },
        },
        soilMoisture: {
            critical: { min: 20, max: 80 },
            warning: { min: 30, max: 70 },
        },
        co2: {
            critical: { min: 300, max: 600 },
            warning: { min: 350, max: 550 },
        },
    },
};