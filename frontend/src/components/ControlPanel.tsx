import {
  Badge,
  Button,
  Card,
  Col,
  DatePicker,
  Row,
  Select,
  Space,
  Typography,
} from "antd";

const { Text } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

export const ControlPanel = () => {
  return (
    <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
      <Col xs={24} lg={12}>
        <Card
          title="💡 Panel de Control"
          extra={<Button type="primary">Configurar</Button>}
        >
          <Space direction="vertical" style={{ width: "100%" }}>
            <div>
              <Text strong>Sistema de Riego: </Text>
              <Badge
                status={
                  currentData.soilMoisture < 30 ? "processing" : "default"
                }
                text={currentData.soilMoisture < 30 ? "Activo" : "Inactivo"}
              />
            </div>
            <div>
              <Text strong>Ventilación: </Text>
              <Badge
                status={currentData.temperature > 26 ? "processing" : "default"}
                text={currentData.temperature > 26 ? "Activa" : "Inactiva"}
              />
            </div>
            <div>
              <Text strong>Iluminación LED: </Text>
              <Badge status="processing" text="Programada (6:00-20:00)" />
            </div>
            <div>
              <Text strong>Humidificador: </Text>
              <Badge
                status={currentData.humidity < 50 ? "processing" : "default"}
                text={currentData.humidity < 50 ? "Activo" : "Inactivo"}
              />
            </div>
          </Space>
        </Card>
      </Col>

      <Col xs={24} lg={12}>
        <Card title="📊 Filtros de Datos">
          <Space direction="vertical" style={{ width: "100%" }}>
            <div>
              <Text strong>Rango de fechas:</Text>
              <RangePicker style={{ width: "100%", marginTop: 8 }} />
            </div>
            <div>
              <Text strong>Tipo de sensor:</Text>
              <Select
                defaultValue="all"
                style={{ width: "100%", marginTop: 8 }}
              >
                <Option value="all">Todos los sensores</Option>
                <Option value="temperature">Temperatura</Option>
                <Option value="humidity">Humedad</Option>
                <Option value="soil">Humedad del suelo</Option>
                <Option value="co2">CO2</Option>
              </Select>
            </div>
            <Button type="primary" style={{ width: "100%" }}>
              Exportar Datos
            </Button>
          </Space>
        </Card>
      </Col>
    </Row>
  );
};
