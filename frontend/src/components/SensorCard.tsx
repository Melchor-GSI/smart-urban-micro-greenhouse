import { ExclamationCircleOutlined } from "@ant-design/icons";
import { Alert, Card, Progress, Statistic, Typography } from "antd";
import type { SensorStatus } from "../utils/sensorUtils";
import { getStatusColor } from "../utils/sensorUtils";

const { Text } = Typography;

interface SensorCardProps {
  title: string;
  value: number | null;
  precision?: number;
  suffix: string;
  maxValue: number;
  optimalRange: string;
  getStatus: (value: number) => SensorStatus;
}

export const SensorCard = ({
  title,
  value,
  precision = 1,
  suffix,
  maxValue,
  optimalRange,
  getStatus,
}: SensorCardProps) => {
  // Si el valor es null, mostrar que el sensor no está funcionando
  if (value === null || value === undefined) {
    return (
      <Card>
        <div style={{ textAlign: "center" }}>
          <ExclamationCircleOutlined
            style={{
              fontSize: "32px",
              color: "#ff4d4f",
              marginBottom: "12px",
              display: "block",
            }}
          />
          <Alert
            message={title}
            description="Sensor not working nor sending data."
            type="error"
            showIcon={false}
            style={{
              border: "none",
              background: "transparent",
              padding: 0,
            }}
          />
        </div>
      </Card>
    );
  }

  const status = getStatus(value);
  const statusColor = getStatusColor(status);

  return (
    <Card>
      <Statistic
        title={title}
        value={value}
        precision={precision}
        suffix={suffix}
        valueStyle={{
          color: statusColor,
        }}
      />
      <Progress
        percent={(value / maxValue) * 100}
        size="small"
        strokeColor={statusColor}
        showInfo={false}
      />
      <Text type="secondary">{optimalRange}</Text>
    </Card>
  );
};
