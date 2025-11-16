export type AlertVariable = "temperature" | "humidity" | "soil_moisture" | "co2";

export type AlertEventType =
    | "over_limit"
    | "under_limit"
    | "warning_bottom"
    | "warning_top"
    | "disconnected";

export type AlertUrgency = "low" | "medium" | "high";

export type AlertStatus = "active" | "acknowledged" | "resolved";

export interface Alert {
    id?: string;
    sensor: string;
    variable: AlertVariable;
    event_type: AlertEventType;
    urgency: AlertUrgency;
    status: AlertStatus;
    creation_date?: string;
}

export interface AlertsResponse {
    alerts: Alert[];
    total: number;
}