# Python Portfolio

Welcome to my central Python portfolio. This repository serves as a curated index of my technical capabilities, ranging from production-grade desktop applications to automated data pipelines and backend systems. 

Each project listed below is self-contained, featuring its own environment configuration (`requirements.txt`) and dedicated documentation.

---

## 🛠️ Tech Stack & Core Competencies
* **Languages:** Python 3.11+, SQL, Bash
* **GUI & Desktop:** Tkinter, PyQt/PySide, CustomTkinter
* **Data & Automation:** Pandas, NumPy, Schedule, Watchdog, ETL Pipelines
* **Backend & APIs:** FastAPI, Flask, SQLite/PostgreSQL
* **DevOps & Tooling:** Git, Virtualenv, Pipenv, Logging Architecture

---

## 📂 Project Index

### 01. Desktop GUI Applications
*Visual, user-facing applications designed for performance, clean UX, and cross-platform compatibility.*

* **[System Metric Monitor](./01-desktop-gui-apps/system-metric-monitor/)** 
  * **Description:** A real-time hardware performance tracker that visualizes CPU, RAM, and Disk utility metrics. 
  * **Key Features:** Multi-threaded polling to prevent UI freezing, low-overhead resource consumption, and dark/light mode toggles.
* **[CSV Schema Cleaner](./01-desktop-gui-apps/csv-schema-cleaner/)**
  * **Description:** A drag-and-drop desktop utility built to sanitize, reformat, and validate massive CSV datasets against custom schemas before database ingestion.

### 02. Data Pipelines & Analytics
*End-to-end data processing solutions focusing on automation, transformation, and predictive insights.*

* **[Price Tracker](./02-data-pipelines/price-tracker/)**
  * **Description:** An automated web scraping and data aggregation pipeline that tracks e-commerce asset pricing, handles anti-bot mitigations, and stores historical trends.
* **[Predictive Maintenance](./02-data-pipelines/predictive-maintenance/)**
  * **Description:** A data pipeline that ingests simulated IoT sensor data, processes feature engineering inputs, and flags mechanical anomalies using statistical modeling.

### 03. Backend & Automation
*Headless scripts, background daemons, and microservices optimized for system efficiency.*

* **[File Organizer Daemon](./03-backend-automation/file-organizer-daemon/)**
  * **Description:** A lightweight background service using OS-level file system event listeners to instantly sort, rename, and route incoming files based on extension rules.
* **[Local Search Engine API](./03-backend-automation/local-search-engine-api/)**
  * **Description:** A high-performance FastAPI microservice that indexes local markdown/text documentation and provides full-text search capability with custom relevance ranking.

---

## 🚀 Getting Started

Because every project inside this portfolio is isolated, you do not need to install global dependencies. 

1. **Clone the repository:**
```bash
   git clone [https://github.com/your-username/python-portfolio.git](https://github.com/your-username/python-portfolio.git)
   cd python-portfolio
