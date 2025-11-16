import { Layout, Typography } from "antd";
import { AlertsPanel } from "./AlertsPanel";

const { Header } = Layout;
const { Title } = Typography;

export const PageHeader = () => {
  return (
    <Header
      style={{
        background: "#001529",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <Title level={3} style={{ color: "white", margin: 0 }}>
        🌱 Smart Urban Micro-Greenhouse
      </Title>
      <AlertsPanel />
    </Header>
  );
};
