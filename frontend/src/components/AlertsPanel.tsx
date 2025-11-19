import {
  BellOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  InfoCircleOutlined,
  WarningOutlined,
} from "@ant-design/icons";
import {
  Alert as AntAlert,
  Badge,
  Button,
  Drawer,
  Empty,
  List,
  message,
  Segmented,
  Space,
  Spin,
  Tag,
  Tooltip,
  Typography,
} from "antd";
import { useState } from "react";
import { useAlerts } from "../hooks/useAlerts";
import type { Alert, AlertStatus } from "../types/alertsData";

const { Text, Title } = Typography;

const getUrgencyColor = (urgency: Alert["urgency"]) => {
  switch (urgency) {
    case "high":
      return "error";
    case "medium":
      return "warning";
    case "low":
      return "default";
    default:
      return "default";
  }
};

const getUrgencyIcon = (urgency: Alert["urgency"]) => {
  switch (urgency) {
    case "high":
      return <ExclamationCircleOutlined />;
    case "medium":
      return <WarningOutlined />;
    case "low":
      return <InfoCircleOutlined />;
    default:
      return <InfoCircleOutlined />;
  }
};

const getEventTypeText = (eventType: Alert["event_type"]) => {
  switch (eventType) {
    case "over_limit":
      return "Over Limit";
    case "under_limit":
      return "Under Limit";
    case "warning_bottom":
      return "Low Warning";
    case "warning_top":
      return "High Warning";
    case "disconnected":
      return "Disconnected";
    default:
      return eventType;
  }
};

const getVariableIcon = (variable: Alert["variable"]) => {
  switch (variable) {
    case "temperature":
      return "🌡️";
    case "humidity":
      return "💧";
    case "soil_moisture":
      return "🌱";
    case "co2":
      return "💨";
    default:
      return "📊";
  }
};

interface AlertsPanelProps {
  style?: React.CSSProperties;
}

export const AlertsPanel: React.FC<AlertsPanelProps> = ({ style }) => {
  const [visible, setVisible] = useState(false);
  const [statusFilter, setStatusFilter] = useState<AlertStatus>("active");

  // Use polling for background updates only when component is mounted
  const { alerts, loading, error, refetch, acknowledgeAlert, lastFetch } =
    useAlerts(statusFilter, true); // Enable polling

  // Separate hook to get active alerts count (always polling)
  const { alerts: activeAlerts } = useAlerts("active", true);

  console.log("🚀 ~ AlertsPanel ~ alerts:", alerts);

  // Ensure alerts is always an array
  const safeAlerts = Array.isArray(alerts) ? alerts : [];
  const safeActiveAlerts = Array.isArray(activeAlerts) ? activeAlerts : [];

  const activeAlertsCount = safeActiveAlerts.length;

  const handleAcknowledge = async (alertId: string) => {
    try {
      await acknowledgeAlert(alertId);
      message.success("Alert acknowledged successfully");
    } catch {
      message.error("Failed to acknowledge alert");
    }
  };

  const showDrawer = () => {
    setVisible(true);
    refetch(); // Refresh alerts when opening
  };

  const onClose = () => {
    setVisible(false);
  };

  return (
    <>
      <Space style={style}>
        <Tooltip title={`${activeAlertsCount} active alerts`}>
          <Button
            type="text"
            icon={
              <BellOutlined
                style={{
                  color: activeAlertsCount > 0 ? "#ff4d4f" : "white",
                  fontSize: activeAlertsCount > 0 ? "18px" : "16px",
                  animation:
                    activeAlertsCount > 0 ? "pulse 2s infinite" : "none",
                }}
              />
            }
            onClick={showDrawer}
            style={{
              color: "white",
              display: "flex",
              alignItems: "center",
              gap: "8px",
              border: activeAlertsCount > 0 ? "1px solid #ff4d4f" : "none",
              borderRadius: "6px",
              padding: "4px 12px",
            }}
          >
            {activeAlertsCount > 0 && (
              <Badge
                count={activeAlertsCount}
                size="small"
                style={{
                  backgroundColor: "#ff4d4f",
                }}
              />
            )}
            <Text
              style={{
                color: activeAlertsCount > 0 ? "#ff4d4f" : "white",
                fontWeight: activeAlertsCount > 0 ? "600" : "normal",
              }}
            >
              Alerts
            </Text>
          </Button>
        </Tooltip>
      </Space>

      <style>
        {`
          @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.6; }
            100% { opacity: 1; }
          }
        `}
      </style>

      <Drawer
        title={
          <Space>
            <BellOutlined />
            <Title level={4} style={{ margin: 0 }}>
              System Alerts
            </Title>
          </Space>
        }
        placement="right"
        onClose={onClose}
        open={visible}
        width={600}
        extra={
          <Space>
            <Button onClick={refetch} loading={loading}>
              Refresh
            </Button>
          </Space>
        }
      >
        <Space direction="vertical" style={{ width: "100%" }}>
          {lastFetch && (
            <Text
              type="secondary"
              style={{
                fontSize: "12px",
                textAlign: "center",
                display: "block",
              }}
            >
              Last updated: {lastFetch.toLocaleTimeString()}
            </Text>
          )}

          <Segmented
            options={[
              { label: "Active", value: "active" },
              { label: "Acknowledged", value: "acknowledged" },
              { label: "Resolved", value: "resolved" },
            ]}
            value={statusFilter}
            onChange={(value) => setStatusFilter(value as AlertStatus)}
            style={{ marginBottom: 16 }}
          />

          {error && (
            <AntAlert
              message="Error loading alerts"
              description={error}
              type="error"
              showIcon
              style={{ marginBottom: 16 }}
            />
          )}

          {loading ? (
            <div style={{ textAlign: "center", padding: "20px" }}>
              <Spin size="large" />
            </div>
          ) : safeAlerts.length === 0 ? (
            <Empty
              description={`No ${statusFilter} alerts`}
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            />
          ) : (
            <List
              dataSource={safeAlerts}
              renderItem={(alert) => (
                <List.Item
                  key={alert.id}
                  actions={
                    alert.status === "active"
                      ? [
                          <Button
                            key="acknowledge"
                            size="small"
                            type="primary"
                            ghost
                            icon={<CheckCircleOutlined />}
                            onClick={() => handleAcknowledge(alert.id!)}
                          >
                            Acknowledge
                          </Button>,
                        ]
                      : undefined
                  }
                >
                  <List.Item.Meta
                    avatar={
                      <Space>
                        {getVariableIcon(alert.variable)}
                        {getUrgencyIcon(alert.urgency)}
                      </Space>
                    }
                    title={
                      <Space>
                        <Text strong>{alert.sensor}</Text>
                        <Tag color={getUrgencyColor(alert.urgency)}>
                          {alert.urgency.toUpperCase()}
                        </Tag>
                      </Space>
                    }
                    description={
                      <Space direction="vertical" size="small">
                        <Text type="secondary">
                          {alert.variable.replace("_", " ")}:{" "}
                          {getEventTypeText(alert.event_type)}
                        </Text>
                        {alert.creation_date && (
                          <Text type="secondary" style={{ fontSize: "12px" }}>
                            {new Date(alert.creation_date).toLocaleString()}
                          </Text>
                        )}
                      </Space>
                    }
                  />
                </List.Item>
              )}
            />
          )}
        </Space>
      </Drawer>
    </>
  );
};
