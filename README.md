# 🌱 Smart Urban Micro-Greenhouse - IoT Final Project

A comprehensive IoT system for smart balconies featuring real-time sensor monitoring, data collection, and alert management. This project demonstrates a complete IoT stack using MQTT, Node-RED, Flask API, React frontend, and MongoDB database.

## 🏗️ System Architecture

- **Frontend**: React + TypeScript + Ant Design
- **Backend**: Flask API with Swagger documentation
- **Database**: MongoDB for data persistence
- **Message Broker**: MQTT (Eclipse Mosquitto)
- **Data Processing**: Node-RED for workflow automation
- **Simulator**: Python-based sensor data simulator
- **Deployment**: Docker Compose for orchestration

## 🚀 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- At least 4GB of available RAM
- Ports 1883, 1880, 3000, 5001, and 27017 available

### 1. Clone and Setup
```bash
git clone <repository-url>
cd iot-final-project
```

### 2. Environment Configuration
Create environment files from examples:
```bash
# Backend environment
cp backend/.env.example backend/.env

# Simulator environment  
cp simulator/.env.example simulator/.env
```

### 3. Deploy the Complete Stack
```bash
# Start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access the Services
- **Frontend Dashboard**: http://localhost:3000
- **API Documentation (Swagger)**: http://localhost:5001
- **Node-RED Interface**: http://localhost:1880
- **MQTT Broker**: localhost:1883

## 📊 Available API Endpoints

### Health Check
- `GET /api/health` - Check system health status

### Sensor Readings
- `GET /api/readings/` - Get all historical readings
- `GET /api/readings/now/` - Get current readings for all sensors
- `POST /api/readings/` - Create a new sensor reading
- `GET /api/readings/<sensor>` - Get readings for specific sensor
- `GET /api/readings/<variable>/last-hours` - Get readings for last N hours

### Events & Alerts
- `GET /api/events/` - Get all events (optionally filter by status)
- `POST /api/events/` - Create a new alert event
- `PATCH /api/events/` - Update event status (acknowledge/resolve)

### API Request Examples

#### Create a sensor reading:
```bash
curl -X POST http://localhost:5001/api/readings/ \
  -H "Content-Type: application/json" \
  -d '{
    "variable": "temperature",
    "sensor": "temp_01", 
    "value": 23.5
  }'
```

#### Get current readings:
```bash
curl http://localhost:5001/api/readings/now/
```

#### Get temperature readings from last 6 hours:
```bash
curl http://localhost:5001/api/readings/temperature/last-hours?hours=6
```

#### Create an alert event:
```bash
curl -X POST http://localhost:5001/api/events/ \
  -H "Content-Type: application/json" \
  -d '{
    "sensor": "temp_01",
    "variable": "temperature", 
    "event_type": "over_limit",
    "urgency": "high"
  }'
```

## 🔧 Individual Service Deployment

### Backend Only
```bash
cd backend
docker-compose up --build
```
Access API at: http://localhost:5001

### Frontend Only  
```bash
cd frontend
npm install
npm run dev
```
Access dashboard at: http://localhost:5173

### MQTT Broker Only
```bash
cd mosquitto_broker  
docker-compose up
```
MQTT available at: localhost:1883

## 📈 Sensor Data

The system monitors four environmental variables:
- **Temperature** (°C): Optimal range 20-26°C
- **Humidity** (%). Optimal range 50-70%
- **Soil Moisture** (%): Optimal range 30-70%
- **CO2 Concentration** (ppm): Optimal range 350-550 ppm

## 🚨 Alert System

Automated alerts are generated for:
- **Critical**: Values outside safe operating ranges
- **Warning**: Values approaching critical thresholds  
- **Low/Medium/High** urgency levels
- **Active/Acknowledged/Resolved** status tracking

## 📱 Frontend Features

- Real-time sensor data dashboard
- Historical data visualization
- Alert management panel
- Responsive design for mobile devices
- Automatic data refresh every second

## 🔄 Data Flow

1. **Simulator** generates sensor data → MQTT broker
2. **Node-RED** processes MQTT messages → Flask API
3. **Flask API** stores data → MongoDB  
4. **React Frontend** fetches data → User interface
5. **Alerts** generated automatically based on thresholds

## 🛠️ Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend Development  
```bash
cd frontend
npm install
npm run dev
```

### Simulator Development
```bash
cd simulator  
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m sensors.run_simulator
```

## 📝 Configuration

### Environment Variables

**Backend (.env)**:
```env
MONGODB_URI=mongodb://admin:password123@mongodb:27017/iot_db?authSource=admin
FLASK_ENV=production
SECRET_KEY=your-secret-key
```

**Simulator (.env)**:
```env
MQTT_BROKER=mqtt-broker
NUM_DEVICES=1
PUBLISH_INTERVAL=5.0
SIMULATOR_DEBUG=True
```

## 🏥 Health Monitoring

All services include health checks:
- API responds at `/api/health`
- Database connectivity verified
- MQTT broker accessibility tested
- Container health status monitoring

## 🔒 Security Features

- CORS configured for cross-origin requests
- Non-root user execution in containers
- Environment variable-based configuration
- Input validation on all API endpoints

## 📊 Data Models

### Reading Model
```json
{
  "id": "uuid",
  "variable": "temperature|humidity|soil_moisture|co2",
  "sensor": "sensor_id", 
  "value": 23.5,
  "creation_date": "2025-01-01T12:00:00Z"
}
```

### Event Model  
```json
{
  "id": "uuid",
  "sensor": "sensor_id",
  "variable": "temperature",
  "event_type": "over_limit|under_limit|warning_top|warning_bottom", 
  "urgency": "low|medium|high",
  "status": "active|acknowledged|resolved",
  "creation_date": "2025-01-01T12:00:00Z"
}
```

## 🧹 Cleanup

Stop and remove all containers:
```bash
docker-compose down -v
```

Remove images:
```bash
docker-compose down --rmi all -v
```

## 🆘 Troubleshooting

### Common Issues

**Port conflicts**: Ensure ports 1883, 1880, 3000, 5001, 27017 are available
```bash
# Check if ports are in use
lsof -i :1883
lsof -i :5001
```

**Database connection**: Verify MongoDB is running and accessible
```bash
docker-compose logs mongodb
```

**MQTT connection**: Check broker status
```bash 
docker-compose logs mqtt-broker
```

**Frontend API calls**: Verify backend is accessible
```bash
curl http://localhost:5001/api/health
```

## 📄 License

This project is for educational purposes as part of IoT coursework.

---

*Smart Urban Micro-Greenhouse ©2025 - IoT System for smart balconies*