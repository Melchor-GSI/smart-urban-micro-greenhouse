
export interface SensorsData {
    timestamp: string;
    temperature: number | null;
    humidity: number | null;
    soil_moisture: number | null;
    co2: number | null;
}

// Variable types for type safety
export type VariableType = 'temperature' | 'humidity' | 'soil_moisture' | 'co2';

// Reading interface for historical data from the API
export interface Reading {
    id?: string;
    variable: VariableType;
    sensor: string;
    value: number;
    creation_date?: string;
}