import { Alert, Card, Col, Row, Select, Space, Spin, Typography } from "antd";
import { useCallback, useEffect, useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { config } from "../config/config";
import type { VariableType } from "../types/sensorsData";

interface TooltipProps {
  active?: boolean;
  payload?: Array<{
    value: number;
    color: string;
    dataKey: string;
  }>;
  label?: string;
}

interface ReadingFromAPI {
  id?: string;
  variable: string;
  sensor: string;
  value: number;
  creation_date?: string;
}

const { Title, Text } = Typography;
const { Option } = Select;

interface ChartDataPoint {
  timestamp: string;
  value: number;
  formattedTime: string;
}

interface TimeSeriesData {
  [key: string]: ChartDataPoint[];
}

const VARIABLE_CONFIGS = {
  temperature: {
    label: "Temperature",
    unit: "°C",
    color: "#ff4d4f",
    icon: "🌡️",
  },
  humidity: {
    label: "Humidity",
    unit: "%",
    color: "#1890ff",
    icon: "💧",
  },
  soil_moisture: {
    label: "Soil Moisture",
    unit: "%",
    color: "#52c41a",
    icon: "🌱",
  },
  co2: {
    label: "CO2",
    unit: "ppm",
    color: "#faad14",
    icon: "💨",
  },
} as const;

const HOUR_OPTIONS = [
  { value: 1, label: "1 Hour" },
  { value: 2, label: "2 Hours" },
  { value: 6, label: "6 Hours" },
  { value: 12, label: "12 Hours" },
  { value: 24, label: "24 Hours" },
];

export const TimeSeriesCharts = () => {
  const [chartsData, setChartsData] = useState<TimeSeriesData>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedHours, setSelectedHours] = useState(1);

  const formatTimestamp = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      // Check if date is valid
      if (isNaN(date.getTime())) {
        return timestamp;
      }
      return date.toLocaleTimeString("en-US", {
        hour12: false,
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return timestamp;
    }
  };

  const fetchVariableData = useCallback(
    async (variable: VariableType) => {
      try {
        const response = await fetch(
          `${config.api.baseUrl}/api/readings/${variable}/last-hours?hours=${selectedHours}`
        );

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        // Handle the actual API response structure
        if (result && Array.isArray(result.data)) {
          const formattedData: ChartDataPoint[] = result.data.map(
            (reading: ReadingFromAPI) => ({
              timestamp: reading.creation_date || "",
              value: reading.value,
              formattedTime: formatTimestamp(reading.creation_date || ""),
            })
          );

          return { variable, data: formattedData };
        }

        return { variable, data: [] };
      } catch (err) {
        console.error(`Error fetching data for ${variable}:`, err);
        return { variable, data: [] };
      }
    },
    [selectedHours]
  );

  const fetchAllData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const variables: VariableType[] = [
        "temperature",
        "humidity",
        "soil_moisture",
        "co2",
      ];

      // Fetch data for all variables in parallel
      const promises = variables.map((variable) => fetchVariableData(variable));
      const results = await Promise.all(promises);

      // Combine results into chartsData object
      const newChartsData: TimeSeriesData = {};
      results.forEach(({ variable, data }) => {
        newChartsData[variable] = data;
      });

      setChartsData(newChartsData);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to fetch charts data"
      );
      console.error("Error fetching charts data:", err);
    } finally {
      setLoading(false);
    }
  }, [fetchVariableData]);

  useEffect(() => {
    // Initial fetch
    fetchAllData();

    // Set up interval for periodic updates (every 30 seconds)
    const interval = setInterval(fetchAllData, 30000);

    return () => clearInterval(interval);
  }, [fetchAllData]);

  const CustomTooltip = ({ active, payload, label }: TooltipProps) => {
    if (active && payload && payload.length) {
      const data = payload[0];
      const variable = Object.keys(VARIABLE_CONFIGS).find(
        (key) => VARIABLE_CONFIGS[key as VariableType].color === data.color
      ) as VariableType;

      const config = VARIABLE_CONFIGS[variable];

      return (
        <div
          style={{
            backgroundColor: "rgba(255, 255, 255, 0.95)",
            padding: "12px",
            border: "1px solid #d9d9d9",
            borderRadius: "6px",
            boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
          }}
        >
          <Text strong>{label}</Text>
          <br />
          <Text style={{ color: data.color }}>
            {config.icon} {config.label}: {data.value.toFixed(1)} {config.unit}
          </Text>
        </div>
      );
    }
    return null;
  };

  const renderChart = (variable: VariableType) => {
    const variableConfig = VARIABLE_CONFIGS[variable];
    const data = chartsData[variable] || [];

    return (
      <Card
        key={variable}
        title={
          <Space>
            <span>{variableConfig.icon}</span>
            <span>
              {variableConfig.label} - Last {selectedHours}h
            </span>
          </Space>
        }
        size="small"
        style={{ height: "400px" }}
      >
        {data.length === 0 ? (
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              height: "300px",
              flexDirection: "column",
              color: "#8c8c8c",
            }}
          >
            <Text type="secondary">
              No data available for the selected period
            </Text>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart
              data={data}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis
                dataKey="formattedTime"
                stroke="#666"
                fontSize={11}
                tick={{ fill: "#666" }}
                interval="preserveStartEnd"
              />
              <YAxis
                stroke="#666"
                fontSize={11}
                tick={{ fill: "#666" }}
                label={{
                  value: variableConfig.unit,
                  angle: -90,
                  position: "insideLeft",
                  style: { textAnchor: "middle" },
                }}
              />
              <Tooltip
                content={<CustomTooltip />}
                cursor={{ stroke: variableConfig.color, strokeWidth: 1 }}
              />
              <Line
                type="monotone"
                dataKey="value"
                stroke={variableConfig.color}
                strokeWidth={2}
                dot={{ fill: variableConfig.color, strokeWidth: 0, r: 3 }}
                activeDot={{ r: 5, fill: variableConfig.color }}
                connectNulls={false}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
        <div style={{ textAlign: "center", marginTop: "8px" }}>
          <Text type="secondary" style={{ fontSize: "12px" }}>
            {data.length > 0
              ? `${data.length} data points • Latest: ${
                  data[data.length - 1]?.value?.toFixed(1) || "N/A"
                } ${variableConfig.unit}`
              : "No recent data"}
          </Text>
        </div>
      </Card>
    );
  };

  if (loading && Object.keys(chartsData).length === 0) {
    return (
      <Card title="📊 Time Series Charts" style={{ marginBottom: 24 }}>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "200px",
            flexDirection: "column",
          }}
        >
          <Spin size="large" />
          <Text style={{ marginTop: 16 }}>Loading time series data...</Text>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card title="📊 Time Series Charts" style={{ marginBottom: 24 }}>
        <Alert
          message="Error loading charts"
          description={`Failed to load time series data: ${error}`}
          type="error"
          showIcon
          style={{ marginBottom: 16 }}
        />
      </Card>
    );
  }

  return (
    <div style={{ marginBottom: 24 }}>
      <Card
        title={
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <Space>
              <span>📊</span>
              <Title level={4} style={{ margin: 0 }}>
                Time Series Charts
              </Title>
            </Space>
            <Select
              value={selectedHours}
              onChange={setSelectedHours}
              style={{ width: 120 }}
              size="small"
            >
              {HOUR_OPTIONS.map((option) => (
                <Option key={option.value} value={option.value}>
                  {option.label}
                </Option>
              ))}
            </Select>
          </div>
        }
        style={{ marginBottom: 16 }}
      >
        <Row gutter={[16, 16]}>
          <Col xs={24} lg={12}>
            {renderChart("temperature")}
          </Col>
          <Col xs={24} lg={12}>
            {renderChart("humidity")}
          </Col>
          <Col xs={24} lg={12}>
            {renderChart("soil_moisture")}
          </Col>
          <Col xs={24} lg={12}>
            {renderChart("co2")}
          </Col>
        </Row>

        {loading && (
          <div style={{ textAlign: "center", padding: "16px" }}>
            <Spin size="small" />
            <Text style={{ marginLeft: 8 }} type="secondary">
              Updating charts...
            </Text>
          </div>
        )}
      </Card>
    </div>
  );
};
