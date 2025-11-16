import { Col, Row } from "antd";
import { SimpleChart } from "./SimpleChart";

export const TrendCharts = () => {
  return (
    <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
      <Col xs={24} lg={12}>
        <SimpleChart
          title="📈 Temperatura (Últimas 6 horas)"
          type="line"
          data={[
            { label: "6h", value: 21.2, color: "#1890ff" },
            { label: "5h", value: 22.1, color: "#1890ff" },
            { label: "4h", value: 23.5, color: "#1890ff" },
            { label: "3h", value: 24.2, color: "#1890ff" },
            { label: "2h", value: 23.8, color: "#1890ff" },
            {
              label: "1h",
              value: currentData.temperature,
              color: "#52c41a",
            },
          ]}
        />
      </Col>
      <Col xs={24} lg={12}>
        <SimpleChart
          title="💧 Humedad del Suelo (Últimas 6 horas)"
          type="bar"
          data={[
            { label: "6h", value: 52, color: "#13c2c2" },
            { label: "5h", value: 48, color: "#13c2c2" },
            { label: "4h", value: 45, color: "#faad14" },
            { label: "3h", value: 41, color: "#faad14" },
            { label: "2h", value: 38, color: "#ff4d4f" },
            {
              label: "1h",
              value: currentData.soilMoisture,
              color:
                getSoilMoistureStatus(currentData.soilMoisture) === "critical"
                  ? "#ff4d4f"
                  : getSoilMoistureStatus(currentData.soilMoisture) ===
                    "warning"
                  ? "#faad14"
                  : "#52c41a",
            },
          ]}
        />
      </Col>
    </Row>
  );
};
