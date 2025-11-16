import { useEffect, useState } from 'react';
import { config } from '../config/config';
import type { SensorsData } from '../types/sensorsData';

// Build the full API endpoint URL
const API_ENDPOINT = `${config.api.baseUrl}${config.api.endpoints.sensors}`;

export const useSensorData = () => {
    const [currentData, setCurrentData] = useState<SensorsData | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

    const fetchSensorData = async () => {
        try {
            const response = await fetch(API_ENDPOINT);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const body = await response.json();
            const data: SensorsData = body.data as SensorsData;
            setCurrentData(data);
            setLastUpdated(new Date());
            setError(null);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to fetch sensor data');
            console.error('Error fetching sensor data:', err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        // Initial fetch
        fetchSensorData();

        // Set up interval to fetch data every 0.5 seconds using config
        const interval = setInterval(fetchSensorData, config.api.fetchInterval);

        // Cleanup interval on component unmount
        return () => clearInterval(interval);
    }, []);

    return {
        currentData,
        isLoading,
        error,
        lastUpdated,
        refetch: fetchSensorData
    };
};