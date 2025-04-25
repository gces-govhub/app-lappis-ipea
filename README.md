# Data Pipeline Project

This project implements a modern data stack using Airflow, dbt, Jupyter, and Superset for data orchestration, transformation, analysis, and visualization.

---

## 🚀 Stack Components

- **Apache Airflow**: Workflow orchestration  
- **dbt**: Data transformation  
- **Jupyter**: Interactive data analysis  
- **Apache Superset**: Data visualization and exploration  
- **Docker**: Containerization and local development  
- **Make**: Build automation and setup  

---

## 📋 Prerequisites

- Docker and Docker Compose  
- Make  
- Python 3.x  
- Git  

---

## 🔧 Setup

Clone the repository:

```bash
git clone git@gitlab.com:lappis-unb/gest-odadosipea/app-lappis-ipea.git
cd app-lappis-ipea
```

Run the setup using Make:

```bash
make setup
```

This will:

- Create necessary virtual environments  
- Install dependencies  
- Set up pre-commit hooks  
- Configure development environment  


## 🏃‍♂️ Running Locally

> **Note:** The following step-by-step is for **macOS**. For Linux and Windows, see the specific sections below.

### 1. Install Homebrew (if you don't have it)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python and pip via Homebrew (if needed)

```bash
brew install python
```

Check if `python3` and `pip3` are installed:

```bash
python3 --version
pip3 --version
```

### 3. Create and activate the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install the `cryptography` dependency

```bash
pip install cryptography
```

### 5. Generate a Fernet key

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the generated key for the next step.

### 6. Create the `.env` file

Create a `.env` file in the project root with the following content, replacing `<your_fernet_key>` with the generated key:

```env
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__FERNET_KEY=<your_fernet_key>
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
```

### 7. Start Docker Desktop

Make sure Docker Desktop is open and running before proceeding.

### 8. Start the containers with Docker Compose

```bash
docker compose up -d --build
```

### 9. Access the services

- **Airflow**: http://localhost:8080  
  - Login: `airflow`  
  - Password: `airflow`

- **Jupyter**: http://localhost:8888  
  - Copy the token shown in the terminal

- **Superset**: http://localhost:8088  
  - Login: `admin`  
  - Password: `admin`

## 🐧 Running on **Linux**

> **Note:** This section is under construction. Follow the instructions below and add screenshots after testing on Linux.

### 1. Install dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git docker.io docker-compose
```

### 2. (Optional) Add your user to the docker group

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Clone the repository

```bash
git clone git@gitlab.com:lappis-unb/gest-odadosipea/app-lappis-ipea.git
cd app-lappis-ipea
```

### 4. Create and activate the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5. Install the `cryptography` dependency

```bash
pip install cryptography
```

### 6. Generate the Fernet key

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 7. Create the `.env` file

```env
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__FERNET_KEY=<your_fernet_key>
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
```

### 8. Start the containers with Docker Compose

```bash
docker compose up -d --build
```

### 9. Access the services

- **Airflow**: http://localhost:8080  
- **Jupyter**: http://localhost:8888  
- **Superset**: http://localhost:8088  


## 🪟 Running on **Windows**

> **Note:** This section is under construction. Follow the instructions below and add screenshots after testing on Windows.

### 1. Install [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install) and Ubuntu from Microsoft Store

### 2. Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

- Make sure to enable WSL2 integration in Docker Desktop settings.

### 3. Install Python and Git in Ubuntu (WSL2)

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

### 4. Clone the repository

```bash
git clone git@gitlab.com:lappis-unb/gest-odadosipea/app-lappis-ipea.git
cd app-lappis-ipea
```

### 5. Create and activate the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 6. Install the `cryptography` dependency

```bash
pip install cryptography
```

### 7. Generate the Fernet key

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 8. Create the `.env` file

```env
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__FERNET_KEY=<your_fernet_key>
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
```

### 9. Start the containers with Docker Compose

```bash
docker compose up -d --build
```

### 10. Access the services

- **Airflow**: http://localhost:8080  
- **Jupyter**: http://localhost:8888  
- **Superset**: http://localhost:8088  

## 📸 Installation and Execution Screenshots

### macOS

- Project setup  
  ![print1](prints/print1.png)
- Virtual environment creation and dependency installation  
  ![print2](prints/print2.png)
- Fernet key generation  
  ![print3](prints/print3.png)
- Docker Compose running  
  ![print4](prints/print4.png)
- Airflow access  
  ![print5](prints/print5.png)
- Jupyter access  
  ![print6](prints/print6.png)
- Superset access  
  ![print7](prints/print7.png)

### Linux

> todo

### Windows

> todo


## 💻 Development

### Code Quality

This project uses several tools to maintain code quality:

- Pre-commit hooks  
- Linting configurations  
- Automated testing  

Run linting checks:

```bash
make lint
```

Run tests:

```bash
make test
```

---

### Project Structure

```
.
├── airflow/
│   ├── dags/
│   └── plugins/
├── dbt/
│   └── models/
├── jupyter/
│   └── notebooks/
├── superset/
│   └── dashboards/
├── docker-compose.yml
├── Makefile
└── README.md
```

---

### Makefile Commands

- `make setup`: Initial project setup  
- `make lint`: Run linting checks  
- `make tests`: Run test suite  
- `make clean`: Clean up generated files  
- `make build`: Build Docker images  

## 🔐 Git Workflow

This project requires signed commits. To set up GPG signing:

1. Generate a GPG key:

```bash
gpg --full-generate-key
```

2. Configure Git to use GPG signing:

```bash
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true
```

3. Add your GPG key to your GitLab account


## 📚 Documentation

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [dbt Documentation](https://docs.getdbt.com/)
- [Superset Documentation](https://superset.apache.org/docs/intro)

## 🤝 Contributing

1. Create a new branch for your feature  
2. Make changes and ensure all tests pass  
3. Submit a merge request  
