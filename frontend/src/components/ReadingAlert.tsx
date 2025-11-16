import { Alert } from "antd";

export const ReadingAlert = () => {
  return (
    <Alert
      message="¡Atención! Condiciones críticas detectadas"
      description="Revisa los valores de los sensores y toma las acciones necesarias."
      type="error"
      showIcon
      style={{ marginBottom: 24 }}
    />
  );
};
