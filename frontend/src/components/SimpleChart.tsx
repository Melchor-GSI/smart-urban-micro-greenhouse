import { Card } from "antd";
import React from "react";

interface ChartData {
  label: string;
  value: number;
  color?: string;
}

interface SimpleChartProps {
  title: string;
  data: ChartData[];
  type: "bar" | "line";
  height?: number;
}

export const SimpleChart: React.FC<SimpleChartProps> = ({
  title,
  data,
  type = "bar",
  height = 200,
}) => {
  const maxValue = Math.max(...data.map((d) => d.value));

  const renderBarChart = () => (
    <div
      style={{
        display: "flex",
        alignItems: "end",
        height: height - 40,
        gap: "8px",
      }}
    >
      {data.map((item, index) => (
        <div
          key={index}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            flex: 1,
          }}
        >
          <div
            style={{
              width: "100%",
              height: `${(item.value / maxValue) * (height - 80)}px`,
              backgroundColor: item.color || "#1890ff",
              borderRadius: "4px 4px 0 0",
              minHeight: "2px",
              transition: "all 0.3s ease",
            }}
          />
          <div
            style={{
              fontSize: "10px",
              marginTop: "4px",
              textAlign: "center",
              color: "#666",
            }}
          >
            {item.label}
          </div>
          <div
            style={{
              fontSize: "12px",
              fontWeight: "bold",
              color: "#333",
            }}
          >
            {item.value.toFixed(1)}
          </div>
        </div>
      ))}
    </div>
  );

  const renderLineChart = () => {
    const width = 100;
    const points = data.map((item, index) => ({
      x: (index / (data.length - 1)) * width,
      y: height - 60 - (item.value / maxValue) * (height - 80),
    }));

    const pathData = points.reduce((path, point, index) => {
      return (
        path +
        (index === 0 ? `M ${point.x} ${point.y}` : ` L ${point.x} ${point.y}`)
      );
    }, "");

    return (
      <div style={{ position: "relative", height: height - 40 }}>
        <svg
          width="100%"
          height={height - 40}
          viewBox={`0 0 100 ${height - 40}`}
        >
          <defs>
            <linearGradient id="lineGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#1890ff" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#1890ff" stopOpacity="0" />
            </linearGradient>
          </defs>

          {/* Área bajo la línea */}
          <path
            d={`${pathData} L ${points[points.length - 1].x} ${height - 60} L ${
              points[0].x
            } ${height - 60} Z`}
            fill="url(#lineGradient)"
          />

          {/* Línea principal */}
          <path d={pathData} stroke="#1890ff" strokeWidth="2" fill="none" />

          {/* Puntos */}
          {points.map((point, index) => (
            <circle
              key={index}
              cx={point.x}
              cy={point.y}
              r="3"
              fill="#1890ff"
              stroke="white"
              strokeWidth="2"
            />
          ))}
        </svg>

        {/* Etiquetas */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            fontSize: "10px",
            color: "#666",
            marginTop: "8px",
          }}
        >
          {data.map((item, index) => (
            <span key={index}>{item.label}</span>
          ))}
        </div>
      </div>
    );
  };

  return (
    <Card title={title} size="small">
      {type === "bar" ? renderBarChart() : renderLineChart()}
    </Card>
  );
};
