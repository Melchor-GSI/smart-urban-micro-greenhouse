import { Alert, Col, Row, Spin, Typography } from "antd";
import { SensorCard } from "../components/SensorCard";
import { config } from "../config/config";
import { useSensorData } from "../hooks/useSensorData";
import {
  getCO2Status,
  getHumidityStatus,
  getSoilMoistureStatus,
  getTemperatureStatus,
} from "../utils/sensorUtils";

const { Text } = Typography;

export const MainMetrics = () => {
  const { currentData, isLoading, error, lastUpdated } = useSensorData();

  if (isLoading && !currentData) {
    return (
      <div
        style={{ display: "flex", justifyContent: "center", padding: "50px" }}
      >
        <Spin size="large" />
        <Text style={{ marginLeft: 16 }}>Cargando datos de sensores...</Text>
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error loading data"
        description={`Failed to fetch sensor data: ${error}`}
        type="error"
        showIcon
        style={{ marginBottom: 24 }}
      />
    );
  }

  if (!currentData) {
    return (
      <Alert
        message="No data available"
        description="No sensor data is available at this time"
        type="warning"
        showIcon
        style={{ marginBottom: 24 }}
      />
    );
  }

  return (
    <div>
      {lastUpdated && (
        <Text type="secondary" style={{ marginBottom: 16, display: "block" }}>
          Current time: {lastUpdated.toLocaleTimeString()}
        </Text>
      )}

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} md={6}>
          <SensorCard
            title="Temperature"
            value={currentData.temperature}
            precision={1}
            suffix="°C"
            maxValue={config.thresholds.temperature.critical.max}
            optimalRange={`Optimal range: ${config.thresholds.temperature.warning.min}-${config.thresholds.temperature.warning.max}°C`}
            getStatus={getTemperatureStatus}
          />
        </Col>

        <Col xs={24} sm={12} md={6}>
          <SensorCard
            title="Humidity"
            value={currentData.humidity}
            precision={1}
            suffix="%"
            maxValue={config.thresholds.humidity.critical.max}
            optimalRange={`Optimal range: ${config.thresholds.humidity.warning.min}-${config.thresholds.humidity.warning.max}%`}
            getStatus={getHumidityStatus}
          />
        </Col>

        <Col xs={24} sm={12} md={6}>
          <SensorCard
            title="Soil Moisture"
            value={currentData.soil_moisture}
            precision={1}
            suffix="%"
            maxValue={config.thresholds.soilMoisture.critical.max}
            optimalRange={`Optimal range: ${config.thresholds.soilMoisture.warning.min}-${config.thresholds.soilMoisture.warning.max}%`}
            getStatus={getSoilMoistureStatus}
          />
        </Col>

        <Col xs={24} sm={12} md={6}>
          <SensorCard
            title="CO2 Concentration"
            value={currentData.co2}
            precision={0}
            suffix="ppm"
            maxValue={config.thresholds.co2.critical.max}
            optimalRange={`Optimal range: ${config.thresholds.co2.warning.min}-${config.thresholds.co2.warning.max} ppm`}
            getStatus={getCO2Status}
          />
        </Col>
      </Row>
    </div>
  );
};
