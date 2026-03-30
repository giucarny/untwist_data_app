# Manifesto Topics Analyzer – User Guide

## Table of Contents
1. [Overview](#overview)
2. [Initialisation](#1-initialisation)
3. [Main structure of the interface](#2-main-structure-of-the-interface)
4. [Loading the dataset](#3-loading-the-dataset)
5. [Filtering the dataset](#4-filtering-the-dataset)
6. [How to use filters](#5-how-to-use-filters)
7. [How to use aggregation](#6-how-to-use-aggregation)
8. [How aggregation works](#7-how-aggregation-works)
9. [Showing results](#8-showing-results)
10. [Switching between views](#9-switching-between-views)
11. [Exporting results](#10-exporting-results)
12. [Summary](#11-summary)

## 1. Overview

The **Manifesto Topics Analyzer** is a desktop application built in Python with PySide6 to explore, filter, and aggregate the UNTWIST WP4 manifesto dataset. It is designed to make the dataset easier to inspect before deployment through a simple graphical interface.

The app allows users to:

- load the original manifesto CSV file;
- inspect the filtered data in a table;
- aggregate the data at the **document level**;
- switch between aggregated and non-aggregated views;
- export both filtered and aggregated outputs as CSV files.

A key feature of the app is that aggregation is always performed at the **document level**, where a document is defined by the unique combination of:

- `project`
- `country`
- `edate`
- `party_code`
- `party_name_or`
- `party_name_en`

This means that the app does not aggregate at the sentence level. Instead, it counts sentence-level annotations within each document and returns one row per document in the aggregated output.

---

## 2. Initialisation

### 2.1. Open a terminal

Open a terminal (e.g., Command Prompt, PowerShell, or Terminal).

### 2.2. Navigate to the application folder

Move to the directory where the application file (`app_v3.py`) is located:

```cmd
cd path/to/your/application/folder
```

### 2.3. Activate your Python environment (if applicable)

If you are using a virtual environment or conda environment, activate it:

```cmd
activate
# or
conda activate <your_environment_name>
```

### 2.4. Launch the application

Run:

```cmd
python app_v3.py
```

The application window should then open.

---

## 3. Main structure of the interface

The interface is divided into two main parts.

### Left panel
This is the control area. It includes:

- **Load CSV File** button
- a link to the dataset
- status message
- **Aggregation Dimensions**
- **Filters**
- **Update Filter Menus** button
- **Show Results** button

### Right panel
This is the output area. It includes:

- the button to switch between aggregated and CSV view
- the results table
- export buttons
- a progress bar during loading

---

## 4. Loading the dataset

### Step 1
Click **Load CSV File**.

### Step 2
Select the manifesto CSV file from your computer.

The app expects the original dataset structure, including columns such as:

- `project`
- `country`
- `edate`
- `party_code`
- `party_name_or`
- `party_name_en`
- `pos`
- `qsentence`
- `domain`
- `topic`
- `connotation`
- `gip`

### Step 3
Wait until loading is complete.

While loading, the app:

- reads the CSV;
- checks that the required columns are present;
- remaps domain labels;
- remaps topic codes;
- remaps connotation values;
- stores party names for display.

Once loading is complete, the status label will indicate how many rows were loaded.

---

## 5. Filtering the dataset

Filtering and aggregation are handled separately.

### Important distinction

- **Filters** restrict the subset of data that will be displayed or aggregated.
- **Aggregation dimensions** determine how the filtered data are summarised in the aggregated output.

This means that filtering answers the question:  
**“Which rows do I want to keep?”**

Aggregation answers the question:  
**“Across which dimensions do I want to count the retained rows?”**

---

## 6. How to use filters

### Step 1
In the **Filters** section, tick the variables for which you want a dropdown menu to appear.

Available filter dimensions are:

- Project / Manifesto
- Domain
- Topic
- Goal / Issue / Policy
- Connotation

### Step 2
Click **Update Filter Menus**.

The app will create dropdown menus only for the selected filters.

### Step 3
Use the dropdown menus to restrict the data.

Each menu contains an **Any** option, which means that no filtering is applied on that dimension.

### Example
You may choose to:

- tick **Project / Manifesto**
- tick **Domain**
- click **Update Filter Menus**
- then select:
  - `EM` for project
  - `1 - Labour Market` for domain

This will keep only rows belonging to the selected project and domain.

### Topic filtering and domain filtering
If both **Domain** and **Topic** are selected as filters, the topic menu updates dynamically when the domain changes. This helps ensure that the topic choices correspond to the selected domain.

---

## 7. How to use aggregation

### Step 1
In the **Aggregation Dimensions** section, tick the dimensions that should define the aggregated columns.

Available aggregation dimensions are:

- Project / Manifesto
- Domain
- Topic
- Goal / Issue / Policy
- Connotation

### Step 2
Click **Show Results**.

If the table is in aggregated mode, the app will:

- first apply the selected filters;
- then aggregate the remaining data at the **document level**;
- then count how many rows belong to each selected aggregation category within each document.

### Default behaviour
If no aggregation dimension is selected, the app defaults to aggregating by **Domain**.

---

## 8. How aggregation works

Aggregation is always performed at the document level.

Each row in the aggregated output represents one unique document identified by:

- `project`
- `country`
- `edate`
- `party_code`
- `party_name_or`
- `party_name_en`

The additional columns in the aggregated table represent counts of sentence-level annotations within that document.

---

## 9. Showing results

After selecting filters and/or aggregation dimensions, click **Show Results**.

The displayed table depends on the current view mode.

### Aggregated view
This is the default view. It shows one row per document and count columns based on the selected aggregation dimensions.

### CSV view
This shows the filtered dataset in non-aggregated form.

Only the first 1000 rows are displayed in the table for inspection, but exports are not limited to those visible rows.

---

## 10. Switching between views

Use the button above the table:

- **Switch to CSV View**
- **Switch to Aggregated View**

---

## 11. Exporting results

### Export Filtered CSV
Exports the filtered dataset (non-aggregated).

### Export Aggregated CSV
Exports the document-level aggregated dataset.

---

## 12. Summary

The app workflow is:

1. load the CSV;
2. optionally filter;
3. optionally aggregate;
4. view results;
5. export outputs.

Aggregation is always performed at the document level.
