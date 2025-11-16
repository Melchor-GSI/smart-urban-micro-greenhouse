import { Layout } from "antd";
import { PageFooter } from "./components/PageFooter";
import { PageHeader } from "./components/PageHeader";
import { PageLayout } from "./layout/main";

function App() {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <PageHeader />
      <PageLayout />
      <PageFooter />
    </Layout>
  );
}

export default App;
