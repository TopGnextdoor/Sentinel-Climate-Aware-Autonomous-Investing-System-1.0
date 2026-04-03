# Sentinel Backend

This is the FastAPI backend for Sentinel.

## Running Locally

### Prerequisites
- Python 3.10+
- pip
- (Optional) Alpaca paper trading account for execution simulation

### 1. Clone the Repository

```bash
git clone https://github.com/TopGnextdoor/Sentinel-Climate-Aware-Autonomous-Investing-System-1.0.git
cd Sentinel-Climate-Aware-Autonomous-Investing-System-1.0
```

### 2. Set Up the Backend

```bash
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in `backend/`:

```env
# Optional: Alpaca API (paper trading)
ALPACA_API_KEY=your_alpaca_key
ALPACA_SECRET_KEY=your_alpaca_secret
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# App settings
DEBUG=true
CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
```

> **Note:** We havent implimented this yet

### 4. Start the Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

The API will be live at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`
