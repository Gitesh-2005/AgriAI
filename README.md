# 🌾 AgriAI - Dockerized Setup Guide

AgriAI is an AI-powered platform to assist farmers and stakeholders in the agricultural sector through multilingual and finance-aware technologies.

---

AgriAI/

│

├── backend/

│ ├── app/

│ ├── Dockerfile

│ ├── requirements.txt

│ └── ...

│

├── frontend/

│ ├── Dockerfile

│ ├── package.json

│ └── ...

│

├── docker-compose.yml

└── README.md


---

## ⚙️ Prerequisites

Make sure you have the following installed:

- [Docker](https://www.docker.com/products/docker-desktop)

---

## 🚀 Getting Started

### Step 1. Clone the repository 
git clone https://github.com/Gitesh-2005/AgriAI

cd AgriAI

### Step 2. Build Docker Container 

# (Make sure that first docker is running locally)

docker-compose build --no-cache 

### Step 3. Starting the Container

docker-compose up

# If you make changes to dependencies or Dockerfiles:


docker-compose down

docker-compose build

docker-compose up

---

Frontend (React + Vite): http://localhost:5173

Backend (FastAPI): http://localhost:8000/docs — Swagger UI
