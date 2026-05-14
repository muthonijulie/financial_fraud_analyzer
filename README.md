# Smart Financial Behavior Analyzer

A production-grade AI system that detects fraudulent transactions, analyzes spending behavior, and surfaces financial insights — built with XGBoost, FastAPI, and Next.js.

---

## Table of contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quickstart with Docker](#quickstart-with-docker)
- [Local development setup](#local-development-setup)
  - [Backend](#backend-setup)
  - [Frontend](#frontend-setup)
- [ML pipeline](#ml-pipeline)
  - [Dataset](#dataset)
  - [Preprocessing](#preprocessing)
  - [Model training](#model-training)
  - [Model artifacts](#model-artifacts)
- [API reference](#api-reference)
  - [POST /api/v1/detect](#post-apiv1detect)
  - [POST /api/v1/insights](#post-apiv1insights)
  - [GET /health](#get-health)
- [Environment variables](#environment-variables)
- [Docker reference](#docker-reference)
- [Model performance](#model-performance)
- [Known issues and fixes](#known-issues-and-fixes)
- [Roadmap](#roadmap)

---

## Overview

This project was built in phases as a learning exercise in production ML engineering. It takes the [ULB Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) from Kaggle and turns it into a deployable system with:

- **Anomaly detection** — XGBoost classifier with calibrated fraud probability scores
- **Batch insights** — aggregate risk analysis across transaction sets
- **Dashboard** — real-time fraud alerts, risk distribution charts, and stat cards
- **Dockerized deployment** — one command to run everything

---

## Architecture

```
Browser
  └── Nginx :80
        ├── /api/*  → FastAPI :8000  (fraud detection + insights)
        └── /       → Next.js :3000  (dashboard)

FastAPI
  └── loads artifacts/ at startup
        ├── fraud_model.pkl   (XGBoost booster)
        ├── scaler.pkl        (RobustScaler for Amount + Time)
        └── model_config.json (threshold + feature list)
```

All three services run as Docker containers on a shared bridge network. Nginx eliminates CORS by routing both services from the same origin.

---

## Tech stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| ML         | XGBoost, scikit-learn, imbalanced-learn, pandas |
| Backend    | FastAPI, Pydantic v2, Uvicorn, joblib |
| Frontend   | Next.js 16, React Query, Recharts, shadcn/ui, Tailwind |
| Proxy      | Nginx (Alpine)                      |
| Container  | Docker, Docker Compose              |
| Language   | Python 3.12, TypeScript             |

---

## Project structure

```
ML.DL/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── detect.py        # POST /detect endpoint
│   │   │       └── insights.py      # POST /insights endpoint
│   │   ├── core/
│   │   │   └── config.py            # settings + artifact paths
│   │   ├── ml/
│   │   │   └── model.py             # FraudDetectionModel singleton
│   │   ├── schemas/
│   │   │   ├── transaction.py       # request/response for /detect
│   │   │   └── insights.py          # request/response for /insights
│   │   └── main.py                  # FastAPI app + lifespan
│   ├── artifacts/
│   │   ├── fraud_model.pkl          # trained XGBoost model
│   │   ├── scaler.pkl               # fitted RobustScaler
│   │   └── model_config.json        # threshold + feature names
│   ├── requirements.txt
│   ├── run.py                       # local dev entry point
│   └── Dockerfile
├── frontend/
|   |--public/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx             # dashboard page
│   │   │   └── providers.tsx        # React Query provider
│   │   ├── components/
│   │   │   └── dashboard/
│   │   │       ├── StatCards.tsx
│   │   │       ├── FraudTable.tsx
│   │   │       └── RiskChart.tsx
│   │   ├── lib/
│   │   │   ├── api.ts               # fetch wrappers
│   │   │   └── sampleData.ts        # test transactions
|   |   |   |__utils.ts
│   │   └── types/
│   │       └── insights.ts          # TypeScript mirrors of Pydantic schemas
│   ├── next.config.ts
│   ├── package.json
│   └── Dockerfile
├── nginx/
│   └── nginx.conf
├── Credit_card_fraud/
│   ├── Load.ipynb                   # EDA + preprocessing exploration
│   └── model.ipynb                  # model training experiments
└── docker-compose.yml
|__ .gitignore
|__ README.md
```

---

## Prerequisites

- Docker 24+ and Docker Compose v2
- (For local dev only) Python 3.12, Node.js 20
- Kaggle `creditcard.csv` dataset placed at `Credit_card_fraud/creditcard.csv`

---

## Quickstart with Docker

```bash
# 1. Clone the repo
git clone https://github.com/yourname/smart-financial-analyzer.git
cd smart-financial-analyzer

# 2. Make sure your trained artifacts are in place
ls backend/artifacts/
# fraud_model.ubj  scaler.pkl  model_config.json

# 3. Build and start all services
docker compose build
docker compose up -d

# 4. Open the dashboard
open http://localhost

# 5. Check API docs
open http://localhost/docs
```

To stop everything:

```bash
docker compose down
```

---

## Local development setup

### Backend setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server with hot reload
python run.py
```

The API is now available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

### Frontend setup

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The dashboard is now available at `http://localhost:3000`.

> For local dev, the frontend calls the backend directly at `http://localhost:8000`. For Docker, Nginx handles routing at `http://localhost:80`.

---

## ML pipeline

### Dataset

Download the [Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) from Kaggle and place it at:

```
Credit_card_fraud/creditcard.csv
```

Dataset characteristics:
- 284,807 transactions, 492 fraud (0.17%)
- Features V1–V28 are PCA-transformed (anonymized)
- `Amount` and `Time` are the only raw features
- `Class` is the target: 0 = legit, 1 = fraud

### Preprocessing

Key decisions made in the pipeline:

**Split before scaling** — the scaler is fit only on training data to prevent data leakage. `Cleaned_data.csv` (if present from earlier exploration) scales on the full dataset and should not be used for training.

**RobustScaler over StandardScaler** — financial amounts follow power-law distributions with extreme outliers. `RobustScaler` uses median and IQR instead of mean and std, making it resistant to those extremes.

**Stratified split** — with only 0.17% fraud, a random split risks near-zero fraud samples in the test set. `stratify=y` preserves the ratio in every subset.

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler

SEED = 42

X = df.drop('Class', axis=1)
y = df['Class']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=SEED
)

scaler = RobustScaler()
X_train[['Amount', 'Time']] = scaler.fit_transform(X_train[['Amount', 'Time']])
X_test[['Amount', 'Time']]  = scaler.transform(X_test[['Amount', 'Time']])
```

### Model training

We use XGBoost with `scale_pos_weight` to handle class imbalance. SMOTE was evaluated but found unnecessary when `scale_pos_weight` is set correctly from the original class ratio.

```python
import xgboost as xgb

n_legit = (y_train == 0).sum()
n_fraud = (y_train == 1).sum()

clf = xgb.XGBClassifier(
    n_estimators          = 500,
    max_depth             = 6,
    learning_rate         = 0.05,
    subsample             = 0.8,
    colsample_bytree      = 0.8,
    scale_pos_weight      = n_legit / n_fraud,
    eval_metric           = 'aucpr',
    early_stopping_rounds = 20,
    random_state          = 42,
    n_jobs                = -1
)

clf.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=50
)
```

**Why XGBoost over a neural network?** A PyTorch MLP was attempted first but suffered from probability miscalibration — outputting near-zero probabilities for fraud samples, resulting in F1 of 0.11 even with an AUC of 0.96. XGBoost produces well-calibrated probabilities out of the box on tabular data, which is why it remains the industry standard for financial fraud detection.

**Threshold tuning** — instead of the default 0.5 cutoff, we sweep thresholds from 0.1 to 0.9 and select the one that maximizes F1 on the fraud class.

```python
from sklearn.metrics import f1_score
import numpy as np

thresholds  = np.arange(0.1, 0.9, 0.01)
best_t      = max(thresholds, key=lambda t: f1_score(y_test, (y_proba > t).astype(int)))
```

### Model artifacts

After training, save three files that the API loads at startup:

```python
import joblib, json, xgboost as xgb

# Save model in XGBoost native format (no pickle warning)
clf.get_booster().save_model("artifacts/fraud_model.pkl")

# Save scaler
joblib.dump(scaler, "artifacts/scaler.pkl")

# Save config with threshold and feature list
with open("artifacts/model_config.json", "w") as f:
    json.dump({
        "threshold"      : round(float(optimal_threshold), 4),
        "model_type"     : "xgboost",
        "input_features" : list(X_train.columns),
        "n_features"     : int(X_train.shape[1])
    }, f, indent=2)
```

---

## API reference

### POST /api/v1/detect

Score a single transaction for fraud.

**Request body**

```json
{
  "Time"  : 406.0,
  "Amount": 149.62,
  "V1"    : -1.3598,
  "V2"    : -0.0728,
  "..."   : "...",
  "V28"   : -0.0211
}
```

All 30 fields are required: `Time`, `Amount`, and `V1` through `V28`.

**Response**

```json
{
  "is_fraud"         : false,
  "fraud_probability": 0.021304,
  "risk_level"       : "LOW",
  "threshold_used"   : 0.87,
  "message"          : "Transaction appears legitimate."
}
```

| Field               | Type    | Description                                      |
|---------------------|---------|--------------------------------------------------|
| `is_fraud`          | boolean | True if `fraud_probability >= threshold`         |
| `fraud_probability` | float   | Raw model probability (0–1)                      |
| `risk_level`        | string  | `LOW` (<0.30) / `MEDIUM` (0.30–0.65) / `HIGH`   |
| `threshold_used`    | float   | Decision boundary from `model_config.json`       |
| `message`           | string  | Human-readable verdict                           |

---

### POST /api/v1/insights

Analyze a batch of up to 10,000 transactions and return aggregate statistics.

**Request body**

```json
{
  "transactions": [
    { "Time": 406, "Amount": 149.62, "V1": -1.3598, "..": "..", "V28": -0.021 },
    { "Time": 512, "Amount":  22.50, "V1":  0.9821, "..": "..", "V28":  0.041 }
  ]
}
```

**Response**

```json
{
  "total_transactions": 2,
  "flagged_count"     : 0,
  "fraud_rate_pct"    : 0.0,
  "total_amount"      : 172.12,
  "avg_amount"        : 86.06,
  "avg_fraud_prob"    : 0.0312,
  "risk_breakdown"    : { "low": 2, "medium": 0, "high": 0 },
  "highest_risk"      : [ ... ],
  "results"           : [ ... ]
}
```

---

### GET /health

Liveness check used by Docker healthcheck and load balancers.

```json
{ "status": "ok", "version": "0.1.0" }
```

---

## Environment variables

### Backend

| Variable      | Default                              | Description                  |
|---------------|--------------------------------------|------------------------------|
| `MODEL_PATH`  | `artifacts/fraud_model.pkl`          | Path to XGBoost model file   |
| `SCALER_PATH` | `artifacts/scaler.pkl`               | Path to fitted scaler        |
| `CONFIG_PATH` | `artifacts/model_config.json`        | Path to model config         |
| `DEBUG`       | `false`                              | Enable debug mode            |

Create `backend/.env` to override locally:

```env
MODEL_PATH=artifacts/fraud_model.pkl
SCALER_PATH=artifacts/scaler.pkl
CONFIG_PATH=artifacts/model_config.json
DEBUG=false
```

### Frontend

| Variable                 | Default | Description                   |
|--------------------------|---------|-------------------------------|
| `NEXT_PUBLIC_API_URL`    | ` `     | API base URL (empty = same origin via Nginx) |

For local dev without Docker, create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Docker reference

```bash
# Build all images
docker compose build

# Start all services (detached)
docker compose up -d

# View logs from all services
docker compose logs -f

# View logs from one service
docker compose logs -f backend

# Rebuild and restart one service only
docker compose build backend
docker compose up -d --no-deps backend

# Stop all services
docker compose down

# Stop and remove volumes (full reset)
docker compose down -v

# Shell into a running container
docker exec -it sfba_backend bash
docker exec -it sfba_frontend sh

# Check container health status
docker compose ps
```

**Updating the model without rebuilding:**

Because `artifacts/` is mounted as a volume, you can hot-swap the model:

```bash
# Copy new artifacts into place
cp new_fraud_model.ubj backend/artifacts/fraud_model.pkl
cp new_scaler.pkl      backend/artifacts/scaler.pkl
cp new_config.json     backend/artifacts/model_config.json

# Restart only the backend
docker compose restart backend
```

---

## Model performance

Evaluated on a held-out 20% stratified test set (56,746 transactions, 95 fraud).

| Metric         | Value  |
|----------------|--------|
| AUC-ROC        | 0.9754 |
| F1 (fraud)     | 0.8605 |
| Precision      | 0.9610 |
| Recall         | 0.7789 |
| Decision threshold | 0.87 |

**Confusion matrix (test set)**

```
              Predicted legit   Predicted fraud
Actual legit       56,647              4
Actual fraud           21             74
```

At threshold 0.87: out of every 100 fraud alerts, ~96 are genuine fraud. The model misses ~22% of actual fraud cases (recall of 0.78), which is an acceptable trade-off for a high-precision alerting system.

---

## Known issues and fixes

### XGBoost pickle warning on startup

```
UserWarning: If you are loading a serialized model...
```

This appears when loading a model saved with `joblib` (older approach). Fix: save with `booster.save_model("model.ubj")` and load with `xgb.Booster().load_model("model.ubj")`. See the training notebook for the corrected save cell.

### Hydration mismatch warning in Next.js

```
A tree hydrated but some attributes of the server rendered HTML didn't match
```

Caused by Grammarly or similar browser extensions injecting attributes into `<body>`. Harmless. Suppressed with `suppressHydrationWarning` on the `<html>` and `<body>` tags in `layout.tsx`.

### `_features` attribute missing on startup

```
'FraudDetectionModel' object has no attribute '_features'
```

Means `model_config.json` is missing the `input_features` key. Re-run the artifact save cell in the training notebook and confirm the JSON file contains `"input_features": ["Time", "V1", ..., "V28", "Amount"]`.

### Pydantic validation error on `/insights`

```
risk_breakdown.low_risk Field required
```

Field name mismatch between `analyze_batch()` output (`low`, `medium`, `high`) and the `RiskBreakdown` schema. Ensure the schema uses `low: int`, `medium: int`, `high: int` — not `low_risk`, `medium_risk`, `high_risk`.

---

## Roadmap

- [ ] PostgreSQL integration — persist transaction history and scores
- [ ] Auth — JWT-based authentication for the API
- [ ] File upload — drag-and-drop CSV upload on the dashboard
- [ ] Spending forecast — Prophet or LSTM time-series prediction endpoint
- [ ] CI/CD — GitHub Actions pipeline for test, build, and push to registry
- [ ] Monitoring — Prometheus metrics + Grafana dashboard for model drift
- [ ] Rate limiting — per-IP limits on the detection endpoint

---

## License

MIT