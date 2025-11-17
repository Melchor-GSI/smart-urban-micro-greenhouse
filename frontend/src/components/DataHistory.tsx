import { Alert, Button, Card, Spin, Table, Tag, Typography } from "antd";
import { useCallback, useEffect, useState } from "react";
import { config } from "../config/config";
import type { VariableType } from "../types/sensorsData";

const { Text } = Typography;

// Define the Reading interface based on the API model
interface Reading {
  id?: string;
  variable: VariableType;
  sensor: string;
  value: number;
  creation_date?: string;
}

// API Response wrapper interface
interface ApiResponse {
  count: number;
  data: Reading[];
  status: string;
}

// Variable type mapping for display
const VARIABLE_TYPE_LABELS: Record<VariableType, string> = {
  temperature: "Temperature",
  humidity: "Humidity",
  soil_moisture: "Soil Moisture",
  co2: "CO2",
};

// Variable type colors for tags
const VARIABLE_TYPE_COLORS: Record<VariableType, string> = {
  temperature: "#ff7875",
  humidity: "#73d13d",
  soil_moisture: "#40a9ff",
  co2: "#ffb347",
};

export const DataHistory = () => {
  const [historicalData, setHistoricalData] = useState<Reading[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Build the API endpoint for readings
  const API_ENDPOINT = `${config.api.baseUrl}${config.api.endpoints.readings}`;

  const fetchHistoricalData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await fetch(API_ENDPOINT);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ApiResponse = await response.json();

      // Check if response has data property (API wrapper format)
      if (data && data.data && Array.isArray(data.data)) {
        const sorted_data = data.data.sort((a, b) => {
          const dateA = a.creation_date
            ? new Date(a.creation_date).getTime()
            : 0;
          const dateB = b.creation_date
            ? new Date(b.creation_date).getTime()
            : 0;
          return dateB - dateA; // Descending order
        });
        console.log("🚀 ~ DataHistory ~ sorted_data:", sorted_data);
        setHistoricalData(sorted_data);
      } else {
        console.warn("API response format not recognized:", data);
        setHistoricalData([]);
      }
    } catch (err) {
      console.error("Error fetching historical data:", err);
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setIsLoading(false);
    }
  }, [API_ENDPOINT]);

  useEffect(() => {
    fetchHistoricalData();
  }, [fetchHistoricalData]);

  // Format date for display
  const formatDate = (dateString?: string) => {
    if (!dateString) return "N/A";

    try {
      const date = new Date(dateString);
      return date.toLocaleString("es-ES", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
    } catch {
      return dateString;
    }
  };

  // Format value with appropriate units
  const formatValue = (value: number, variable: VariableType) => {
    switch (variable) {
      case "temperature":
        return `${value.toFixed(1)}°C`;
      case "humidity":
      case "soil_moisture":
        return `${value.toFixed(1)}%`;
      case "co2":
        return `${Math.round(value)} ppm`;
      default:
        return value.toFixed(2);
    }
  };

  // Define table columns
  const columns = [
    {
      title: "Date/time",
      dataIndex: "creation_date",
      key: "creation_date",
      render: (date: string) => (
        <Text style={{ fontSize: "12px" }}>{formatDate(date)}</Text>
      ),
      width: 150,
    },
    {
      title: "Variable",
      dataIndex: "variable",
      key: "variable",
      render: (variable: VariableType) => (
        <Tag
          color={VARIABLE_TYPE_COLORS[variable] || "default"}
          style={{ fontSize: "11px" }}
        >
          {VARIABLE_TYPE_LABELS[variable] || variable}
        </Tag>
      ),
      width: 120,
    },
    {
      title: "Sensor",
      dataIndex: "sensor",
      key: "sensor",
      render: (sensor: string) => (
        <Text style={{ fontSize: "12px", fontWeight: 500 }}>{sensor}</Text>
      ),
      width: 100,
    },
    {
      title: "Value",
      dataIndex: "value",
      key: "value",
      render: (value: number, record: Reading) => (
        <Text style={{ fontSize: "12px", fontWeight: 600 }}>
          {formatValue(value, record.variable)}
        </Text>
      ),
      width: 80,
      align: "right" as const,
    },
  ];

  // Show loading state
  if (isLoading && (!historicalData || historicalData.length === 0)) {
    return (
      <Card title="📈 Readings History" style={{ marginBottom: 24 }}>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            padding: "40px",
          }}
        >
          <Spin size="large" />
          <Text style={{ marginLeft: 16 }}>Cargando historial...</Text>
        </div>
      </Card>
    );
  }

  // Show error state
  if (error) {
    return (
      <Card title="📈 Readings History" style={{ marginBottom: 24 }}>
        <Alert
          message="Error loading data"
          description={`Failed to load historical data: ${error}`}
          type="error"
          showIcon
        />
      </Card>
    );
  }

  return (
    <Card
      title="📈 Readings History"
      style={{ marginBottom: 24 }}
      extra={
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <Button
            type="primary"
            size="small"
            onClick={fetchHistoricalData}
            loading={isLoading}
          >
            Refresh
          </Button>
          <Text type="secondary" style={{ fontSize: "12px" }}>
            {Array.isArray(historicalData) ? historicalData.length : 0} records
          </Text>
        </div>
      }
    >
      {!Array.isArray(historicalData) || historicalData.length === 0 ? (
        <Alert
          message="No historical data"
          description="No historical data is available at this time."
          type="warning"
          showIcon
        />
      ) : (
        <Table
          columns={columns}
          dataSource={Array.isArray(historicalData) ? historicalData : []}
          pagination={{
            pageSize: 20,
            showSizeChanger: true,
            pageSizeOptions: ["10", "20", "50", "100"],
            showQuickJumper: true,
            showTotal: (total, range) =>
              `${range[0]}-${range[1]} of ${total} records`,
            size: "small",
          }}
          size="small"
          scroll={{ x: true }}
          rowKey={(record) =>
            record.id ||
            `${record.sensor}-${record.variable}-${record.creation_date}`
          }
          loading={isLoading}
        />
      )}
    </Card>
  );
};
