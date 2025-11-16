import { Badge, Layout, Space, Typography } from "antd";

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
      <Space>
        <Badge status="processing" text="Online" style={{ color: "white" }} />
      </Space>
    </Header>
  );
};
