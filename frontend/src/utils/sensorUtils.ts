import { config } from '../config/config';

export type SensorStatus = 'normal' | 'warning' | 'critical';

export const getTemperatureStatus = (temperature: number): SensorStatus => {
    const { critical, warning } = config.thresholds.temperature;
    if (temperature < critical.min || temperature > critical.max) return 'critical';
    if (temperature < warning.min || temperature > warning.max) return 'warning';
    return 'normal';
};

export const getHumidityStatus = (humidity: number): SensorStatus => {
    const { critical, warning } = config.thresholds.humidity;
    if (humidity < critical.min || humidity > critical.max) return 'critical';
    if (humidity < warning.min || humidity > warning.max) return 'warning';
    return 'normal';
};

export const getSoilMoistureStatus = (soilMoisture: number): SensorStatus => {
    const { critical, warning } = config.thresholds.soilMoisture;
    if (soilMoisture < critical.min || soilMoisture > critical.max) return 'critical';
    if (soilMoisture < warning.min || soilMoisture > warning.max) return 'warning';
    return 'normal';
};

export const getCO2Status = (co2: number): SensorStatus => {
    const { critical, warning } = config.thresholds.co2;
    if (co2 < critical.min || co2 > critical.max) return 'critical';
    if (co2 < warning.min || co2 > warning.max) return 'warning';
    return 'normal';
};

export const getStatusColor = (status: SensorStatus): string => {
    switch (status) {
        case 'critical':
            return '#cf1322';
        case 'warning':
            return '#fa8c16';
        case 'normal':
            return '#3f8600';
        default:
            return '#3f8600';
    }
};