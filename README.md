# Manifesto Topics Analyzer – User Guide

## Overview

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

## 1. Initialisation

### 1.1. Open the command prompt

Open **Command Prompt** and move to the relevant folders.

### 1.2. Activate the environment

Use the following commands:

```cmd
cd C:/Users/user/Documents/GIT/UNTWIST/WP4/pythonapp/untwist_data_app/scripts/
activate
cd C:/Users/user/Documents/GIT/UNTWIST/WP4/pythonapp/
python app_v3.py
```

### 1.3. Launch the application

After running:

```cmd
python app_v3.py
```

the application window should open.

## 2. Main structure of the interface

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

## 3. Loading the dataset

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

## 4. Filtering the dataset

Filtering and aggregation are handled separately.

### Important distinction

- **Filters** restrict the subset of data that will be displayed or aggregated.
- **Aggregation dimensions** determine how the filtered data are summarised in the aggregated output.

This means that filtering answers the question:  
**“Which rows do I want to keep?”**

Aggregation answers the question:  
**“Across which dimensions do I want to count the retained rows?”**

## 5. How to use filters

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

## 6. How to use aggregation

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

## 7. How aggregation works

Aggregation is always performed at the document level.

Each row in the aggregated output represents one unique document identified by:

- `project`
- `country`
- `edate`
- `party_code`
- `party_name_or`
- `party_name_en`

The additional columns in the aggregated table represent counts of sentence-level annotations within that document.

### Example 1: aggregation by Domain
If you select only **Domain** as aggregation dimension, the output will contain one row per document and separate count columns for each domain.

### Example 2: aggregation by Domain and Connotation
If you select **Domain** and **Connotation**, the output will still contain one row per document, but now the count columns will correspond to combinations such as:

- `1 - Labour Market | 1`
- `1 - Labour Market | 2`
- `1 - Labour Market | 3`
- `2 - Welfare and family | 1`
- etc.

### Example 3: filtering and aggregating together
You may:

- filter to project = `EM`
- filter to connotation = `1`
- aggregate by **Domain** and **Topic**

In that case, the app keeps only rows matching the selected project and connotation, and then counts them by domain-topic combination within each document.

## 8. Showing results

After selecting filters and/or aggregation dimensions, click **Show Results**.

The displayed table depends on the current view mode.

### Aggregated view
This is the default view. It shows one row per document and count columns based on the selected aggregation dimensions.

### CSV view
This shows the filtered dataset in non-aggregated form.

Only the first 1000 rows are displayed in the table for inspection, but exports are not limited to those visible rows.

## 9. Switching between views

Use the button above the table:

- **Switch to CSV View**
- **Switch to Aggregated View**

This lets you move between:

- the filtered sentence-level dataset;
- the document-level aggregated dataset.

This is useful when you want to compare the raw filtered rows with the aggregated output.

## 10. Exporting results

The app provides two export options.

### Export Filtered CSV
This exports the filtered dataset in non-aggregated form.

Use this when you want the retained rows exactly as filtered.

### Export Aggregated CSV
This exports the document-level aggregated table.

Use this when you want counts summarised by the chosen aggregation dimensions.

### Important note
The export buttons become active after results are shown.

## 11. Recommended workflow

A typical workflow is the following.

### Option A: inspect raw filtered data
1. Load the CSV file.
2. Select one or more filters.
3. Click **Update Filter Menus**.
4. Choose filter values.
5. Click **Show Results**.
6. Switch to **CSV View** if needed.
7. Export the filtered CSV if required.

### Option B: create document-level aggregates
1. Load the CSV file.
2. Select one or more filters if needed.
3. Click **Update Filter Menus**.
4. Choose filter values.
5. Select one or more aggregation dimensions.
6. Click **Show Results**.
7. Stay in aggregated view.
8. Export the aggregated CSV.

## 12. Practical examples

### Example 1: all documents aggregated by domain
1. Load the CSV.
2. Do not apply any filters.
3. Tick **Domain** in Aggregation Dimensions.
4. Click **Show Results**.

Result: one row per document, with counts by domain.

### Example 2: European Parliament manifestos only, aggregated by topic
1. Load the CSV.
2. Tick **Project / Manifesto** under Filters.
3. Click **Update Filter Menus**.
4. Select `EM`.
5. Tick **Topic** under Aggregation Dimensions.
6. Click **Show Results**.

Result: one row per document within the EM subset, with counts by topic.

### Example 3: labour-market content only, aggregated by connotation
1. Load the CSV.
2. Tick **Domain** under Filters.
3. Click **Update Filter Menus**.
4. Select `1 - Labour Market`.
5. Tick **Connotation** under Aggregation Dimensions.
6. Click **Show Results**.

Result: one row per document, counting only labour-market rows by connotation.

## 13. Notes on variable handling

### Domains
The app converts numeric domain values into descriptive labels, such as:

- `0 - No category applies`
- `1 - Labour Market`
- `2 - Welfare and family`
- `3 - Participation and Representation`
- `4 - Rights, Discrimination, and Violence`
- `5 - Gender-related notions`

### Topics
Topics are remapped into a global topic scale and displayed with descriptive names.

### Connotation
Connotation values are internally remapped before display and aggregation.

## 14. Troubleshooting

### Nothing happens after changing filters
After ticking filter dimensions, always click **Update Filter Menus** so that the dropdown menus are rebuilt.

### No results found
If the combination of filters is too restrictive, the app will return no rows. In that case, relax one or more filters.

### Aggregation dimensions changed but results look the same
Make sure to click **Show Results** again after changing the aggregation dimensions.

### The table shows only 1000 rows in CSV view
This is only a display limit for the interface. Exported filtered CSV files are not restricted to the first 1000 rows.

## 15. Summary

The app is intended as a practical interface to inspect and summarise the manifesto dataset before deployment. Its main logic is:

1. load the original CSV;
2. optionally filter the data;
3. optionally aggregate the filtered data;
4. display either raw or aggregated output;
5. export the result.

The most important thing to keep in mind is that **aggregation is always document-based**, not sentence-based. The app therefore helps transform sentence-level annotations into document-level summaries while still allowing inspection of the underlying filtered data.
