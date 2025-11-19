import { message } from 'antd';
import { useCallback, useEffect, useRef, useState } from 'react';
import { config } from '../config/config';
import type { Alert, AlertStatus } from '../types/alertsData';

export const useAlerts = (status?: AlertStatus, enablePolling: boolean = false) => {
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [lastFetch, setLastFetch] = useState<Date | null>(null);
    const previousAlertsRef = useRef<Alert[]>([]);

    const fetchAlerts = useCallback(async (silent: boolean = false) => {
        if (!silent) {
            setLoading(true);
        }
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
                    setLastFetch(new Date());
                    return;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const payload = await response.json();
            const data = payload.data;
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

            // Check for new alerts and show notifications
            if (enablePolling && previousAlertsRef.current.length > 0) {
                const previousActiveAlerts = previousAlertsRef.current.filter(
                    alert => alert.status === 'active'
                );
                const newActiveAlerts = alertsArray.filter(
                    alert => alert.status === 'active' &&
                        !previousActiveAlerts.some(prev => prev.id === alert.id)
                );

                // Show notification for new alerts
                if (newActiveAlerts.length > 0) {
                    newActiveAlerts.forEach(alert => {
                        const urgencyEmoji = alert.urgency === 'high' ? '🚨' :
                            alert.urgency === 'medium' ? '⚠️' : 'ℹ️';
                        const variableEmoji = alert.variable === 'temperature' ? '🌡️' :
                            alert.variable === 'humidity' ? '💧' :
                                alert.variable === 'soil_moisture' ? '🌱' : '💨';

                        message.warning({
                            content: `${urgencyEmoji} ${variableEmoji} New ${alert.urgency} alert: ${alert.sensor} - ${alert.variable}`,
                            duration: 8, // Show for 8 seconds
                            key: alert.id, // Prevent duplicate notifications
                        });
                    });
                }
            }

            // Update previous alerts reference
            previousAlertsRef.current = alertsArray;

            setAlerts(alertsArray);
            setLastFetch(new Date());
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
            if (!silent) {
                setLoading(false);
            }
        }
    }, [status, enablePolling]);

    useEffect(() => {
        // Initial fetch
        fetchAlerts();

        // Setup polling if enabled
        let intervalId: number | undefined;
        if (enablePolling) {
            intervalId = window.setInterval(() => {
                fetchAlerts(true); // Silent fetch for background updates
            }, 2000); // Poll every 2 seconds for faster alert detection
        }

        return () => {
            if (intervalId) {
                window.clearInterval(intervalId);
            }
        };
    }, [fetchAlerts, enablePolling]);

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
        lastFetch,
        refetch: () => fetchAlerts(false), // Force visible loading state
        acknowledgeAlert,
    };
};
