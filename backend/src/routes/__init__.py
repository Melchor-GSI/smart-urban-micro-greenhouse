from src.routes.events import events_bp
from src.routes.main import main_bp
from src.routes.readings import readings_bp

bp = [
    events_bp,
    main_bp,
    readings_bp,
]
