# FleetRent API

A professional backend REST API designed for fleet management, tracking driver shifts, and calculating company and driver commissions (e.g., for taxi fleet or transport companies). This project focuses on real-world business logic and clean backend architecture.

## Core Features

- **Fleet Management (CRUD):** Full control over vehicles (status, mileage) and drivers (individual commission rates).
- **Shift Business Logic:** Built-in validation rules (e.g., preventing a driver from assigning an already occupied vehicle) and automatic calculations of net company profits, fuel expenses, and driver payouts upon closing a shift.
- **Financial Analytics:** A dedicated endpoint that aggregates monthly financial performance metrics (gross revenue, fuel costs, company net profit) directly through optimized database queries.
- **Security & Auth:** Protection of sensitive endpoints (such as finances and resource creation) via API Key Header authentication ('X-API-Key').
- **Layered Architecture:** Clean separation of concerns utilizing Routers, Pydantic Schemas, SQLModel Database Models, and CRUD Operations.
- **System Logging:** Centralized 'logging' module to monitor server actions and track failed validation attempts.

## Tech Stack

- **Python 3.14**
- **FastAPI** - Web framework with automatic Swagger UI documentation
- **SQLModel** - Modern ORM bridging SQLAlchemy and Pydantic v2
- **SQLite** - Lightweight relational database
- **Pydantic v2** - Data validation and settings management

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/Marcin-S-py/fleetrent-api
    cd fleetrent-api
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/macOS
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the development server:
    ```bash
    uvicorn app.main:app --reload
    ```

5. Explore the interactive API documentation:
    ```bash
    http://127.0.0.1:8000/docs
    ```