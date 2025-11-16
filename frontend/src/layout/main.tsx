import { Layout } from "antd";
// import { SimpleChart } from "../components/SimpleChart";
import { MainMetrics } from "./MainMetrics";
// import { ControlPanel } from "../components/ControlPanel";
import { DataHistory } from "../components/DataHistory";
// import { SystemHealth } from "../components/SystemHealth";
// import { ReadingAlert } from "../components/ReadingAlert";

const { Content } = Layout;

export const PageLayout = () => {
  return (
    <Content style={{ padding: "24px" }}>
      {/* <ReadingAlert /> */}
      <MainMetrics />
      {/* <TrendCharts /> */}
      {/* <ControlPanel /> */}
      <DataHistory />
      {/* <SystemHealth /> */}
    </Content>
  );
};
