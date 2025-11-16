import { Badge, Card, Col, Row, Space, Typography } from "antd";

const { Text } = Typography;

export const SystemHealth = () => {
  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} md={12}>
        <Card title="⚙️ Estado del Sistema">
          <Space direction="vertical" style={{ width: "100%" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <Text>Conectividad WiFi:</Text>
              <Badge status="success" text="Conectado" />
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <Text>Última sincronización:</Text>
              <Text type="secondary">{new Date().toLocaleTimeString()}</Text>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <Text>Batería del sistema:</Text>
              <Text strong style={{ color: "#3f8600" }}>
                87%
              </Text>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <Text>Memoria disponible:</Text>
              <Text strong>2.1 GB</Text>
            </div>
          </Space>
        </Card>
      </Col>

      <Col xs={24} md={12}>
        <Card title="🌿 Información de Cultivo">
          <Space direction="vertical" style={{ width: "100%" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <Text>Tipo de cultivo:</Text>
              <Text strong>Lechugas hidropónicas</Text>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <Text>Días desde siembra:</Text>
              <Text strong>23 días</Text>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <Text>Fase de crecimiento:</Text>
              <Badge status="processing" text="Vegetativo" />
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <Text>Cosecha estimada:</Text>
              <Text strong>En 2 semanas</Text>
            </div>
          </Space>
        </Card>
      </Col>
    </Row>
  );
};
