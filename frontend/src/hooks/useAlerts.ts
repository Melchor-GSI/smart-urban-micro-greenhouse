import { useCallback, useEffect, useState } from 'react';
import { config } from '../config/config';
import type { Alert, AlertStatus } from '../types/alertsData';

export const useAlerts = (status?: AlertStatus) => {
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchAlerts = useCallback(async () => {
        setLoading(true);
        setError(null);

        try {
            const url = new URL(`${config.api.baseUrl}/api/events`);
            if (status) {
                url.searchParams.append('status', status);
            }

            const response = await fetch(url.toString());

            if (!response.ok) {
                // If the endpoint doesn't exist, return empty array instead of error
                if (response.status === 404) {
                    console.warn('Events endpoint not found, using empty alerts array');
                    setAlerts([]);
                    return;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const payload = await response.json();
            const data = payload.data
            console.log('API Response:', data); // Debug log

            // Handle different possible response formats
            let alertsArray: Alert[] = [];
            if (Array.isArray(data)) {
                alertsArray = data;
            } else if (data.alerts && Array.isArray(data.alerts)) {
                alertsArray = data.alerts;
            } else if (data.events && Array.isArray(data.events)) {
                alertsArray = data.events;
            }

            setAlerts(alertsArray);
        } catch (err) {
            // Handle network errors gracefully
            if (err instanceof TypeError && err.message.includes('fetch')) {
                console.warn('Server not reachable, using empty alerts array');
                setAlerts([]);
                setError('Server not reachable. Alerts will be available when the server is running.');
            } else {
                setError(err instanceof Error ? err.message : 'Failed to fetch alerts');
                console.error('Error fetching alerts:', err);
            }
        } finally {
            setLoading(false);
        }
    }, [status]);

    useEffect(() => {
        fetchAlerts();
    }, [fetchAlerts]);

    const acknowledgeAlert = async (alertId: string) => {
        try {
            const response = await fetch(`${config.api.baseUrl}${config.api.endpoints.events}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: alertId, status: 'acknowledged' }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Refresh alerts after acknowledgment
            await fetchAlerts();
        } catch (err) {
            console.error('Error acknowledging alert:', err);
            throw err;
        }
    };

    return {
        alerts,
        loading,
        error,
        refetch: fetchAlerts,
        acknowledgeAlert,
    };
};