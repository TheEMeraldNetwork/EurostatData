# Google Trends Analyzer

A comprehensive application for analyzing Google Trends data and generating LinkedIn content ideas based on trending topics.

## Features

- Fetch and analyze current Google Trends data
- Region-specific trend analysis (e.g., Lombardia)
- Generate LinkedIn post ideas based on trending topics
- Historical trend data analysis
- Visualize trend popularity with interactive charts
- Export data and insights for content creation

## Project Structure

```
google-trends/
├── architecture_design.md     # System architecture documentation
├── architecture_diagram.txt   # Visual representation of system
├── backend/                   # Python Flask backend
│   ├── api/                   # API endpoints
│   ├── services/              # Business logic services
│   ├── models/                # Data models
│   └── utils/                 # Helper utilities
├── frontend/                  # React frontend
│   ├── public/                # Static assets
│   └── src/                   # Source code
│       ├── components/        # Reusable UI components
│       ├── pages/             # Page components
│       ├── services/          # API client services
│       └── utils/             # Helper utilities
└── database/                  # Database scripts and migrations
```

## Setup Instructions

### Prerequisites

- Python 3.8+ for backend
- Node.js 14+ for frontend
- SQLite for development, PostgreSQL for production
- Google Trends API access

### Backend Setup

1. Create a virtual environment:
   ```bash
   cd "google trends"/backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install flask flask-restful pytrends pandas numpy python-dotenv celery sqlalchemy
   ```

3. Create a `.env` file:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URL=sqlite:///trends.db
   ```

4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the server:
   ```bash
   flask run
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd "google trends"/frontend
   npm install
   ```

2. Create a `.env` file:
   ```
   REACT_APP_API_URL=http://localhost:5000/api
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Development Roadmap

### Phase 1: Core Functionality
- Setup project structure
- Implement basic trend fetching
- Create simple frontend UI

### Phase 2: Enhanced Features
- Add region-specific trend analysis
- Implement content suggestion engine
- Create visualization components

### Phase 3: Advanced Features
- Historical data analysis
- Machine learning for trend prediction
- Direct LinkedIn integration

## API Reference

### Endpoints

- `GET /api/trends/current` - Get latest trends
- `GET /api/trends/search` - Custom trend queries
- `GET /api/trends/geographic/{region}` - Region-specific trends
- `GET /api/trends/history` - Historical trend data
- `POST /api/content/suggestions` - Generate content ideas

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 