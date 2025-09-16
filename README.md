# ✈️ Airline Passenger Satisfaction Data Analysis

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

> A collaborative data analysis project by [@kaganmart9](https://github.com/kaganmart9) & [@ahakanortacbayram](https://github.com/ahakanortacbayram)

---

## 📌 Project Overview

This project explores **airline passenger satisfaction** using data-driven methods. The objective is to understand **how demographic and service-related factors impact customer satisfaction** in commercial air travel.

Using structured and clean code practices in Python, we preprocess, analyze, and visualize data from a real-world airline passenger dataset. The project employs a modular approach, ensuring reproducibility and scalability for future analyses.

---

## 🧠 Key Questions Addressed

- How does **age** affect passenger satisfaction?
- Is there a difference in satisfaction between **genders**?
- Does **flight distance** impact satisfaction levels?
- Which **services (e.g., cleanliness, baggage, online booking)** are most correlated with satisfaction?

---

## 🗂️ Project Structure

AIRLINE-PASSENGER-SATISFACTION-DATA-ANALYSIS/
├── data/
│   ├── raw/                           # Raw dataset (e.g., raw-data.csv)
│   └── processed/                     # Cleaned dataset (e.g., processed.csv)
│
├── docs/
│   └── project-plan.pdf              # Project planning and documentation
│
├── notebooks/                        # Jupyter notebooks for EDA & prototyping
│   ├── 03-analysis-b-age-satisfaction.ipynb
│   ├── 04-analysis-b-gender-satisfaction.ipynb
│   └── flight-distance-satisfaction-scatter-analysis.ipynb
│
├── reports/
│   ├── figures/                      # All generated visualizations (PNG)
│   │   ├── age_group_satisfaction_bar.png
│   │   ├── gender_satisfaction_pies_clean.png
│   │   └── ...
│   └── tables/                       # Output statistics (CSV)
│       ├── flight_distance_satisfaction_stats.csv
│       └── gender_satisfaction_percent.csv
│
├── src/                              # Modular & reproducible Python scripts
│   ├── config.py                     # Path config
│   ├── cleaning.py                   # Data cleaning pipeline
│   ├── age_satisfaction_prc.py       # Age-based satisfaction analysis
│   ├── gender_satisfaction.py        # Gender-based satisfaction analysis
│   ├── distance_satisfaction.py      # Flight distance analysis
│   └── service_correlation.py        # Service factor correlations
│
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation (this file)

---

## 🛠️ Setup & Installation

> 🐍 Python version: **3.11.x**

1. Clone the repository:

```bash
git clone https://github.com/kaganmart9/airline-passenger-satisfaction-data-analysis.git
cd airline-passenger-satisfaction-data-analysis
```

1. (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run Analyses

Each script is **modular and reproducible**. You can run them independently.

### ➤ Clean the raw dataset

The `cleaning.py` script handles missing values, outliers, and standardizes the dataset for further analysis.

```bash
python src/cleaning.py
```

### ➤ Analyze satisfaction by age

The `age_satisfaction_prc.py` script calculates satisfaction percentages across different age groups and generates visualizations.

```bash
python src/age_satisfaction_prc.py
```

### ➤ Analyze satisfaction by gender (CLI options available)

The `gender_satisfaction.py` script provides insights into gender-based satisfaction levels. It supports optional flags for displaying results and adding timestamps to logs.

```bash
python src/gender_satisfaction.py --show --timestamp
```

### ➤ Analyze satisfaction vs. flight distance

The `distance_satisfaction.py` script examines the relationship between flight distance and satisfaction levels, producing scatter plots and statistical summaries.

```bash
python src/distance_satisfaction.py
```

### ➤ Analyze service feature correlations

The `service_correlation.py` script computes correlation coefficients between service-related features (e.g., cleanliness, baggage handling) and satisfaction scores.

```bash
python src/service_correlation.py
```

---

## 📊 Sample Visualizations

### 🎯 Satisfaction by Age Group

![Age Group Bar](reports/figures/age_group_satisfaction_bar.png)

---

### 🧓 Age-wise Pie Charts

![Age Pie](reports/figures/age_satisfaction_pies_clean.png)

---

### 👨‍🦰 Gender Satisfaction Pie Charts

![Gender Pie](reports/figures/gender_satisfaction_pies_clean.png)

---

### 📏 Flight Distance Impact

![Flight Distance](reports/figures/flight_distance_satisfaction.png)

---

## 📈 Output Tables

- `flight_distance_satisfaction_stats.csv`
- `gender_satisfaction_percent.csv`

All are saved under: `reports/tables/`

---

## 👥 Contributors

| Name               | GitHub Handle                              |
|--------------------|---------------------------------------------|
| Ali Kağan Mart         | [@kaganmart9](https://github.com/kaganmart9)       |
| Ahmet Hakan Ortaçbayram| [@ahakanortacbayram](https://github.com/ahakanortacbayram) |

- Both contributors collaborated equally on all parts of the project, including:

- Data preprocessing & cleaning

- Exploratory data analysis (EDA)

- Modular Python scripting

- Visualization and reporting

- Workflow design and documentation

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

Special thanks to the open data contributors that provided the airline passenger satisfaction dataset.
