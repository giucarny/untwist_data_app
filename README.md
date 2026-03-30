# Manifesto Gender Analysis (MGA) Aggregation Tool

## Table of Contents
1. [Overview](#1-overview)
2. [Requirements and Setup](#2-requirements-and-setup)
3. [Initialisation](#3-initialisation)
4. [Main structure of the interface](#4-main-structure-of-the-interface)
5. [Loading the dataset](#5-loading-the-dataset)
6. [Filtering the dataset](#6-filtering-the-dataset)
7. [How to use filters](#7-how-to-use-filters)
8. [How to use aggregation](#8-how-to-use-aggregation)
9. [How aggregation works](#9-how-aggregation-works)
10. [Showing results](#10-showing-results)
11. [Switching between views](#11-switching-between-views)
12. [Exporting results](#12-exporting-results)
13. [Summary](#13-summary)

---

## 1. Overview

The **Manifesto Topics Analyzer** is a desktop application built in Python with PySide6 to explore, filter, and aggregate the UNTWIST WP4 manifesto dataset. It is designed to make the dataset easier to inspect before deployment through a simple graphical interface.

The app allows users to:

- load the original manifesto CSV file;
- inspect the filtered data in a table;
- aggregate the data at the **document level**;
- switch between aggregated and non-aggregated views;
- export both filtered and aggregated outputs as CSV files.

Aggregation is always performed at the **document level**, defined by:

- `project`
- `country`
- `edate`
- `party_code`
- `party_name_or`
- `party_name_en`

---

## 2. Requirements and Setup

### Python
You need **Python 3.9 or higher**.

Check with:
```bash
python --version
```

### Required packages
Install dependencies:

```bash
pip install pandas PySide6
```

### (Recommended) Virtual environment

```bash
python -m venv venv
```

Activate:

- Windows:
```bash
venv\Scripts\activate
```

- macOS / Linux:
```bash
source venv/bin/activate
```

Then install packages:
```bash
pip install pandas PySide6
```

---

## 3. Initialisation

### Step 1
Open a terminal.

### Step 2
Navigate to the folder containing the app:

```bash
cd path/to/your/application/folder
```

### Step 3
Run the app:

```bash
python app_v3.py
```

---

## 4. Main structure of the interface

### Left panel
- Load CSV
- Dataset link
- Aggregation Dimensions
- Filters
- Show Results

### Right panel
- Table view
- Toggle view
- Export buttons

---

## 5. Loading the dataset

1. Click **Load CSV File**
2. Select dataset
3. Wait for loading

---

## 6. Filtering the dataset

Filters restrict which rows are used.

Aggregation defines how they are summarized.

---

## 7. How to use filters

1. Select filters
2. Click **Update Filter Menus**
3. Choose values

---

## 8. How to use aggregation

1. Select aggregation dimensions
2. Click **Show Results**

---

## 9. How aggregation works

Aggregation is always at the **document level**.

Each row = one document.

---

## 10. Showing results

Click **Show Results** to refresh.

---

## 11. Switching between views

Toggle between:
- CSV view
- Aggregated view

---

## 12. Exporting results

- Export filtered CSV
- Export aggregated CSV

---

## 13. Summary

Workflow:

1. Load data  
2. Filter  
3. Aggregate  
4. Export  

Aggregation is always document-based.
