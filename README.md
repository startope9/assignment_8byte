# Stock Market Pipeline

A lightweight ETL pipeline to fetch daily stock market data from Alpha Vantage and store it in a PostgreSQL database, orchestrated by Apache Airflow and Docker Compose.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Prerequisites](#prerequisites)
4. [Environment Variables](#environment-variables)
5. [Setup & Installation](#setup--installation)
6. [Usage](#usage)
7. [Database Initialization & Verification](#database-initialization--verification)
8. [Accessing the Airflow UI](#accessing-the-airflow-ui)
9. [Project Details](#project-details)
10. [Testing](#testing)
11. [Future Improvements](#future-improvements)
12. [License](#license)

---

## Project Overview

This project implements a daily ETL (Extract, Transform, Load) pipeline that:

* **Extracts** daily stock price data from the Alpha Vantage API.
* **Transforms** the data into a consistent tuple format.
* **Loads** the cleaned data into a PostgreSQL database table (`stock_prices`).
* **Orchestrates** the workflow using Apache Airflow, scheduled to run once per day.
* **Containerizes** all components with Docker Compose for easy local development and deployment.

---

## Repository Structure

```
pipeline/
├── docker-compose.yml         # Docker Compose configuration for Airflow and PostgreSQL
├── .env                       # Environment variables for credentials and defaults
├── README.md                  # This README file
├── db_script/                 # Initialization SQL scripts for PostgreSQL
│   └── db_init.sql            # Creates stocks DB and stock_prices table
└── airflow/
    └── dag/
        ├── dag_pipeline.py    # Main Airflow DAG definition
        └── fetch.py           # Python functions for fetching and storing data
```

---

## Prerequisites

* Docker & Docker Compose (v3.8+)
* Git (to clone the repository)
* A valid Alpha Vantage API key (free at [Alpha Vantage](https://www.alphavantage.co))

---

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```dotenv
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow           # Metadata DB for Airflow
PIPELINE_DB=stocks            # Target DB for stock data (auto-created)
ALPHAVANTAGE_API_KEY=YOUR_API_KEY
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
SYMBOL=AAPL                   # Default stock symbol to fetch
```

**Setting the `ALPHAVANTAGE_API_KEY` in your OS environment:**

* **Windows (CMD):**

  ```cmd
  set ALPHAVANTAGE_API_KEY=your_api_key_here
  ```
* **Windows (PowerShell):**

  ```powershell
  $Env:ALPHAVANTAGE_API_KEY = "your_api_key_here"
  ```
* **macOS/Linux (bash/zsh):**

  ```bash
  export ALPHAVANTAGE_API_KEY=your_api_key_here
  ```
* **macOS/Linux (fish shell):**

  ```fish
  set -x ALPHAVANTAGE_API_KEY your_api_key_here
  ```

---

## Setup & Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/startope9/assignment_8byte
   cd assignment_8byte
   ```

2. **Bring up containers**

   ```bash
   docker-compose up --build
   ```

This command will:

* Start a PostgreSQL container (`postgres:13`) with:

  * `airflow` metadata database
  * **Auto-create** `stocks` database and `stock_prices` table via `/docker-entrypoint-initdb.d/01_init_stocks.sql`
* Start an Airflow container (`apache/airflow:2.9.0`) running both the webserver and scheduler.

---

## Usage

Once the containers are running, Airflow will automatically schedule the DAG `stock_market_pipeline` to run daily (at midnight UTC by default).

To manually trigger a run:

1. Open the Airflow UI at `http://localhost:8080` (username/password: `admin` / `admin`).
2. Find the **stock\_market\_pipeline** DAG and click the **Trigger** button.

---

## Database Initialization & Verification

On the very first `docker-compose up`, both the **stocks** database and **stock\_prices** table are auto-created—no manual `createdb` commands needed.

**To verify and inspect the table contents:**

```bash
# 1. Open psql in the 'airflow' metadata database container
docker exec -it postgres psql -U airflow -d airflow

# 2. Switch to the 'stocks' database
\c stocks

# 3. Query the first 5 rows of stock_prices
SELECT * FROM stock_prices LIMIT 5;
```

---

## Accessing the Airflow UI

* **URL:** `http://localhost:8080`
* **Login:** `admin` / `admin`
* **DAG Folder:** `/opt/airflow/dag`

---

## Project Details

* **DAG Definition (`dag_pipeline.py`)**

  * Defines a single task `fetch_and_store_stock_data` that executes `fetch_and_store()` daily.
  * Uses retries and retry delays configured in `default_args`.

* **Fetch & Store Logic (`fetch.py`)**

  * `fetch_data(symbol)`: Calls the Alpha Vantage API, parses JSON, and returns a list of tuples.
  * `store_data(records)`: Connects to Postgres, ensures the `stock_prices` table exists (though already created), and bulk-inserts records with `ON CONFLICT DO NOTHING`.
  * `fetch_and_store()`: Combines both steps into one callable for Airflow.

---
**Note:** The current implementation uses a single stock symbol via environment variables. For scalability, symbols can alternatively be loaded from a database table, configuration file, or Airflow Variables depending on project needs and scale.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
"# assignment_8byte" 
