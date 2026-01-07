# 🌍 TripMind — AI-powered personalized travel experiences

**TripMind** is an AI-powered travel planning system that leverages a dataset of Vietnamese tourist attractions and reviews to convert natural language requests into sentiment-aware, geographically optimized itineraries using a modular, multi-agent architecture.

---

## Overview
TripMind breaks the travel planning problem into specialized components (agents), leveraging the dataset of Vietnamese tourist attractions and reviews. Each step uses the data to provide more personalized, informed recommendations:

User query → Semantic recall (vector search using attraction names, categories, and review text) → Sentiment ranking (based on review ratings and content) → Route optimization (using attraction coordinates) → Natural-language story generation (summarizing recommended destinations with context from reviews).

---

## Dataset

The dataset consists of **14,527 reviews** of **964 attractions** in **34 Vietnamese provinces**.

Each review record contains:

- `review_id`: Unique ID for the review
- `text`: Review text
- `review_rating`: Numerical rating (1–5)
- `published_date`: Date the review was published
- `trip_type`: Type of trip (family, solo, couple, etc.)

Each review also includes a nested `destination` object containing attraction information:

- `destination_id`: Unique attraction ID
- `name`: Normalized attraction name
- `overall_rating`: Overall rating from the platform
- `coordinates`: Latitude and longitude
- `province`: ID and name
- `categories`: List of category IDs and names

There is an additional dataset of restaurants in Hanoi.

---

## Repository Structure

Top-level layout (abridged):

```
TripMind/
├── agent1_choosing_destination/    # semantic recall, gateway components
├── agent2_sentiment_analysis/      # sentiment model & tooling
├── agent3_optimize_route/          # route optimization & RL components
├── tripmind_vector_db/             # local vector DB + weights
├── data/                           # cleaned and reformatted datasets
├── figure/                         # visualizations
├── extract_name_from_query.py
└── test_system.py                  # end-to-end integration tests
```

---

## Installation & Setup

### 1. Environment Setup
It is recommended to use a virtual environment (Conda or venv) to manage dependencies:

```bash
conda activate dl_env
pip install flask fastapi uvicorn torch requests chromadb together gymnasium numpy
```
### 2. Together.ai Configuration

Open agent/src/api.py and insert your personal API key to enable Agent 4 (Narrative Output):
```bash
TOGETHER_CLIENT = Together(api_key="TOGETHER_AI_API_KEY")
```
### How to Run
To operate the system, you must start the agents in three separate terminal windows:

Step 1: Start Agent 3 (Route Optimizer)

```bash
python agent3_optimize_route/api.py
```
Step 2: Start Agent 2 (Sentiment Ranker)

```bash
python agent2_sentiment_analysis/api.py
```
Step 3: Start Agent 1 - Gateway (Main API)

```bash
python agent/src/api.py
```
Step 4: Run Integrated Test

```bash
python test_system.py
```