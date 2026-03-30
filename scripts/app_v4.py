# IN CMD
## cd C:/Users/user/Documents/GIT/UNTWIST/WP4/pythonapp/untwist_data_app/scripts/
## activate
## cd C:/Users/user/Documents/GIT/UNTWIST/WP4/pythonapp/
## python app_v3.py


import sys
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QTableView, QLabel, QFileDialog,
    QMessageBox, QProgressBar, QGroupBox, QListWidget, QListWidgetItem,
    QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from itertools import product


DOMAIN_LABELS = {
    0: "No category applies",
    1: "Labour Market",
    2: "Welfare and family",
    3: "Participation and Representation",
    4: "Rights, Discrimination, and Violence",
    5: "Gender-related notions",
}

TOPIC_LABELS = {
    (0, 0): "Undefined",
    (1, 1): "Salary/ Pay gap",
    (1, 2): "Division of labour",
    (1, 3): "Labour rights and discrimination",
    (1, 4): "Other",
    (2, 1): "Parental leave",
    (2, 2): "Childcare and housework",
    (2, 3): "Other care work",
    (2, 4): "Healthcare",
    (2, 5): "Education",
    (2, 6): "Other",
    (3, 1): "Political representation and participation",
    (3, 2): "Social representation and participation",
    (3, 3): "Gender-neutral language",
    (3, 4): "Gender mainstreaming",
    (3, 5): "Other",
    (4, 1): "Reproductive rights and discrimination",
    (4, 2): "Family rights and discrimination",
    (4, 3): "Sexual and gender-based violence",
    (4, 4): "Immigration and citizenship",
    (4, 5): "Other",
    (5, 1): "Feminism",
    (5, 2): "Patriarchy and heteronormativity",
    (5, 3): "LGBTQ+",
    (5, 4): "Other",
}

TOPIC_REMAP = {
    (1, 1): 1,  (1, 2): 2,  (1, 3): 3,  (1, 4): 4,
    (2, 1): 5,  (2, 2): 6,  (2, 3): 7,  (2, 4): 8,  (2, 5): 9,  (2, 6): 10,
    (3, 1): 11, (3, 2): 12, (3, 3): 13, (3, 4): 14, (3, 5): 15,
    (4, 1): 16, (4, 2): 17, (4, 3): 18, (4, 4): 19, (4, 5): 20,
    (5, 1): 21, (5, 2): 22, (5, 3): 23, (5, 4): 24,
}
OTHER_FALLBACK = {1: 4, 2: 10, 3: 15, 4: 20, 5: 24}

CONNOT_MAP = {0: 2, 1: 1, 3: 3}

# remapped topic id (0-24) → display label
TOPIC_ID_TO_LABEL = {
    0:  "Undefined",
    1:  "Salary/ Pay gap",
    2:  "Division of labour",
    3:  "Labour rights and discrimination",
    4:  "Other (Labour Market)",
    5:  "Parental leave",
    6:  "Childcare and housework",
    7:  "Other care work",
    8:  "Healthcare",
    9:  "Education",
    10: "Other (Welfare and family)",
    11: "Political representation and participation",
    12: "Social representation and participation",
    13: "Gender-neutral language",
    14: "Gender mainstreaming",
    15: "Other (Participation and Representation)",
    16: "Reproductive rights and discrimination",
    17: "Family rights and discrimination",
    18: "Sexual and gender-based violence",
    19: "Immigration and citizenship",
    20: "Other (Rights, Discrimination, and Violence)",
    21: "Feminism",
    22: "Patriarchy and heteronormativity",
    23: "LGBTQ+",
    24: "Other (Gender-related notions)",
}

# remapped topic id → numeric domain id
TOPIC_ID_TO_DOMAIN_ID = {
    0: 0,
    1: 1, 2: 1, 3: 1, 4: 1,
    5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2,
    11: 3, 12: 3, 13: 3, 14: 3, 15: 3,
    16: 4, 17: 4, 18: 4, 19: 4, 20: 4,
    21: 5, 22: 5, 23: 5, 24: 5,
}


def topics_for_domain(domain_id=None):
    return [
        (tid, lbl)
        for tid, lbl in sorted(TOPIC_ID_TO_LABEL.items())
        if domain_id is None or TOPIC_ID_TO_DOMAIN_ID.get(tid) == domain_id
    ]


class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore()


class ManifestoAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manifesto Topics Analyzer")
        self.resize(1500, 900)

        self.df = None
        self.party_map_english = {}
        self.current_filtered = None
        self.aggregated_df = None

        self.cb_domain_label = None
        self.cb_topic = None
        self.show_aggregated = True
        self.results_shown_once = False

        # ── UI ────────────────────────────────────────────────────────────────
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # Left: filter panel
        filter_panel = QWidget()
        filter_layout = QVBoxLayout(filter_panel)

        btn_load = QPushButton("Load CSV File")
        btn_load.setMinimumHeight(35)
        btn_load.clicked.connect(self.load_file)
        filter_layout.addWidget(btn_load)

        # Dataset link under the load button
        self.lbl_dataset_link = QLabel(
            '<a href="https://zenodo.org/records/11476917/files/WP4_manifesto_zenodo_v1(1).csv?download=1">'
            'Dataset page / download link</a>'
        )
        self.lbl_dataset_link.setOpenExternalLinks(True)
        self.lbl_dataset_link.setTextFormat(Qt.RichText)
        self.lbl_dataset_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.lbl_dataset_link.setWordWrap(True)
        filter_layout.addWidget(self.lbl_dataset_link)

        self.lbl_status = QLabel("No file loaded yet")
        self.lbl_status.setWordWrap(True)
        filter_layout.addWidget(self.lbl_status)

        # Aggregation dimensions
        agg_group = QGroupBox("Aggregation Dimensions")
        agg_layout = QVBoxLayout(agg_group)

        self.agg_checkboxes = {}
        for label, col in [
            ("Project / Manifesto",   "project"),
            ("Domain",                "domain_label"),
            ("Topic",                 "topic"),
            ("Goal / Issue / Policy", "gip"),
            ("Connotation",           "connotation"),
        ]:
            cb = QCheckBox(label)
            self.agg_checkboxes[col] = cb
            agg_layout.addWidget(cb)

        filter_layout.addWidget(agg_group)

        # Filter controls
        filter_select_group = QGroupBox("Filters")
        filter_select_layout = QVBoxLayout(filter_select_group)

        self.filter_checkboxes = {}
        for label, col in [
            ("Project / Manifesto",   "project"),
            ("Domain",                "domain_label"),
            ("Topic",                 "topic"),
            ("Goal / Issue / Policy", "gip"),
            ("Connotation",           "connotation"),
        ]:
            cb = QCheckBox(label)
            self.filter_checkboxes[col] = cb
            filter_select_layout.addWidget(cb)

        btn_update = QPushButton("Update Filter Menus")
        btn_update.clicked.connect(self.create_filter_value_widgets)
        filter_select_layout.addWidget(btn_update)

        filter_layout.addWidget(filter_select_group)

        self.dynamic_filters_widget = QWidget()
        self.dynamic_filters_layout = QVBoxLayout(self.dynamic_filters_widget)
        self.dynamic_filters_layout.setSpacing(4)
        self.dynamic_filters_layout.setContentsMargins(2, 2, 2, 2)

        filter_layout.addWidget(self.dynamic_filters_widget, stretch=1)

        btn_show = QPushButton("Show Results")
        btn_show.clicked.connect(self.show_results_button_clicked)
        btn_show.setStyleSheet("font-weight: bold; font-size: 13px;")
        filter_layout.addWidget(btn_show)

        main_layout.addWidget(filter_panel)

        # Right: table + exports
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.switch_view_button = QPushButton("Switch to CSV View")
        self.switch_view_button.clicked.connect(self.toggle_view)
        self.switch_view_button.setEnabled(False)
        right_layout.addWidget(self.switch_view_button)

        self.table = QTableView()
        self.model = QStandardItemModel()
        self.table.setModel(self.model)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        right_layout.addWidget(self.table, stretch=1)

        export_layout = QHBoxLayout()
        self.btn_export_csv = QPushButton("Export Filtered CSV")
        self.btn_export_csv.clicked.connect(self.export_filtered_csv)
        self.btn_export_csv.setEnabled(False)
        self.btn_export_agg = QPushButton("Export Aggregated CSV")
        self.btn_export_agg.clicked.connect(self.export_aggregated_csv)
        self.btn_export_agg.setEnabled(False)
        export_layout.addWidget(self.btn_export_csv)
        export_layout.addWidget(self.btn_export_agg)
        right_layout.addLayout(export_layout)

        self.progress = QProgressBar()
        self.progress.hide()
        right_layout.addWidget(self.progress)

        main_layout.addWidget(right_panel, stretch=1)

    # ── File loading & remapping ──────────────────────────────────────────────

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Manifesto CSV", "", "CSV Files (*.csv)")
        if not path:
            return
        try:
            self.progress.show()
            self.progress.setRange(0, 0)
            self.lbl_status.setText("Loading and remapping CSV…")
            QApplication.processEvents()

            needed_cols = [
                'project', 'country', 'edate', 'party_code', 'party_name_or', 'party_name_en',
                'pos', 'qsentence', 'domain', 'topic', 'connotation', 'gip',
                'rgender_1', 'rgender_2', 'rsexuality', 'intersect', 'policy_type',
            ]
            
            probe = pd.read_csv(path, nrows=1, encoding='latin-1', sep=';')
            print("Columns in file:", probe.columns.tolist())
            available = [c for c in needed_cols if c in probe.columns]
            if not available:
                raise ValueError("No required columns found — check separator or column names.")

            df = pd.read_csv(path, usecols=available, low_memory=False,
                             encoding='latin-1', sep=';')

            # ── Remap steps (identical logic to the remap script) ─────────────

            # 1. pos → numeric
            if 'pos' in df.columns:
                df['pos'] = pd.to_numeric(df['pos'], errors='coerce').astype('Int64')

            # 2. Ensure domain/topic are integers for dict lookups
            df['domain'] = pd.to_numeric(df['domain'], errors='coerce').fillna(0).astype(int)
            df['topic']  = pd.to_numeric(df['topic'],  errors='coerce').fillna(0).astype(int)

            # 3. domain == 0 → topic = 0
            df.loc[df['domain'] == 0, 'topic'] = 0

            # 4. domain_label  (numeric domain id → human label)
            df['domain_label'] = df['domain'].map(DOMAIN_LABELS).fillna("No category applies")

            # 5. topic_label  (uses original domain+topic before global remap)
            df['topic_label'] = df.apply(
                lambda r: TOPIC_LABELS.get((r['domain'], r['topic']), "Other"), axis=1
            )
            df.loc[(df['domain'] == 0) & (df['topic'] == 0), 'topic_label'] = "Undefined"

            # 6. Remap topic to global 0-24 ids
            df['topic'] = df.apply(
                lambda r: 0 if r['domain'] == 0
                else TOPIC_REMAP.get(
                    (r['domain'], r['topic']),
                    OTHER_FALLBACK.get(r['domain'], 0)
                ),
                axis=1
            )

            # 7. Connotation remap
            if 'connotation' in df.columns:
                df['connotation'] = pd.to_numeric(df['connotation'], errors='coerce').fillna(0).astype(int)
                df['connotation'] = df['connotation'].replace(5, 0)
                df['connotation'] = df['connotation'].map(CONNOT_MAP).fillna(2).astype(int)

            # ── Party name map ─────────────────────────────────────────────────
            if 'party_code' in df.columns and 'party_name_en' in df.columns:
                party_df = df[['party_code', 'party_name_en']].drop_duplicates('party_code')
                self.party_map_english = dict(zip(
                    party_df['party_code'].astype(str),
                    party_df['party_name_en']
                ))

            self.df = df
            self.lbl_status.setText(f"Loaded & remapped {len(df):,} rows.")
            print(f"Loaded {len(df):,} rows. Topics: {sorted(df['topic'].unique())}")

        except Exception as e:
            QMessageBox.critical(self, "Load Error", str(e))
        finally:
            self.progress.hide()

    # ── Dynamic filter widgets ────────────────────────────────────────────────

    def create_filter_value_widgets(self):
        if self.df is None:
            QMessageBox.warning(self, "No data", "Please load a CSV file first.")
            return

        while self.dynamic_filters_layout.count():
            item = self.dynamic_filters_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Reset references to old comboboxes, otherwise they may point
        # to Qt widgets that have already been deleted
        for col in ['domain_label', 'topic', 'project', 'gip', 'connotation']:
            setattr(self, f"cb_{col}", None)

        selected_filter_cols = [
            col for col, cb in self.filter_checkboxes.items() if cb.isChecked()
        ]

        for col in selected_filter_cols:
            title = {
                'project':      "Project / Manifesto",
                'domain_label': "Domain",
                'topic':        "Topic",
                'gip':          "Goal / Issue / Policy",
                'connotation':  "Connotation",
            }.get(col, col.replace("_", " ").title())

            box = QGroupBox(title)
            layout = QVBoxLayout(box)
            combo = NoScrollComboBox()
            combo.addItem("Any")

            if col == "domain_label":
                for did, dlabel in sorted(DOMAIN_LABELS.items()):
                    combo.addItem(f"{did} - {dlabel}")
                self.cb_domain_label = combo
                combo.currentTextChanged.connect(self._on_domain_changed)

            elif col == "topic":
                self.cb_topic = combo
                self._populate_topic_combo(combo, domain_id=None)

            else:
                values = sorted(self.df[col].dropna().unique(), key=lambda x: str(x))
                combo.addItems(map(str, values))

            combo.setMinimumHeight(32)
            layout.addWidget(combo)
            self.dynamic_filters_layout.addWidget(box)
            setattr(self, f"cb_{col}", combo)

        self.dynamic_filters_layout.addStretch()

    def _populate_topic_combo(self, combo, domain_id=None):
        combo.blockSignals(True)
        combo.clear()
        combo.addItem("Any")
        for tid, lbl in topics_for_domain(domain_id):
            combo.addItem(f"{tid} - {lbl}")
        combo.blockSignals(False)

    def _on_domain_changed(self, text):
        if self.cb_topic is None:
            return
        if text == "Any":
            self._populate_topic_combo(self.cb_topic, domain_id=None)
        else:
            try:
                domain_id = int(text.split(" - ", 1)[0])
            except ValueError:
                domain_id = None
            self._populate_topic_combo(self.cb_topic, domain_id=domain_id)

    # ── Filtering ─────────────────────────────────────────────────────────────

    def get_filtered_df(self):
        if self.df is None:
            return None
        filtered = self.df.copy()

        for col in ['domain_label', 'topic', 'project', 'gip', 'connotation']:
            cb = getattr(self, f"cb_{col}", None)
            if cb is None:
                continue

            try:
                raw = cb.currentText()
            except RuntimeError:
                setattr(self, f"cb_{col}", None)
                continue

            if raw == "Any":
                continue

            if col == 'domain_label':
                value = raw.split(" - ", 1)[1] if " - " in raw else raw
                filtered = filtered[filtered['domain_label'] == value]

            elif col == 'topic':
                tid = int(raw.split(" - ", 1)[0])
                filtered = filtered[filtered['topic'] == tid]

            else:
                filtered = filtered[filtered[col].astype(str) == raw]

        return filtered

    # ── Table display ─────────────────────────────────────────────────────────

    def show_results_button_clicked(self):
        self.results_shown_once = True
        self.switch_view_button.setEnabled(True)
        self.btn_export_csv.setEnabled(True)
        self.btn_export_agg.setEnabled(True)
        self.refresh_table()

    def refresh_table(self):
        if not self.results_shown_once:
            return
        filtered = self.get_filtered_df()
        if filtered is None or filtered.empty:
            self.model.clear()
            QMessageBox.information(self, "No Results", "No data found for selected filters.")
            return
        self.current_filtered = filtered
        if self.show_aggregated:
            self.show_aggregated_data(filtered)
        else:
            self.show_raw_data(filtered)
        self.btn_export_csv.setEnabled(True)
        self.btn_export_agg.setEnabled(True)

    def show_raw_data(self, df):
        self.model.clear()
        display_df = df.head(1000).copy()
        display_df.insert(0, 'Party Name', display_df['party_code'].apply(
            lambda c: self.party_map_english.get(str(c), "Unknown")
        ))
        self.model.setHorizontalHeaderLabels(display_df.columns.tolist())
        for _, row in display_df.iterrows():
            self.model.appendRow([QStandardItem(str(v)) for v in row])

    def show_aggregated_data(self, df):
        document_cols = [
            'project', 'country', 'edate', 'party_code', 'party_name_or', 'party_name_en'
        ]

        selected_agg_dims = [
            col for col, cb in self.agg_checkboxes.items() if cb.isChecked()
        ]
        pivot_cols = [c for c in selected_agg_dims if c not in document_cols]

        if not pivot_cols:
            pivot_cols = ['domain_label']

        unique_vals = [
            sorted(
                df[c].dropna().unique(),
                key=lambda x: int(x) if str(x).isdigit() else str(x)
            )
            for c in pivot_cols
        ]
        all_combinations = pd.DataFrame(list(product(*unique_vals)), columns=pivot_cols)

        agg = (
            df.groupby(document_cols + pivot_cols, observed=True)
              .size()
              .reset_index(name='count')
        )

        doc_df = df[document_cols].drop_duplicates()

        full_grid = doc_df.merge(all_combinations, how='cross')
        agg = full_grid.merge(agg, on=document_cols + pivot_cols, how='left')
        agg['count'] = agg['count'].fillna(0).astype(int)

        def col_label(x):
            parts = []
            for c in pivot_cols:
                val = x[c]
                if c == 'topic':
                    val = f"{val} - {TOPIC_ID_TO_LABEL.get(int(val), val)}"
                elif c == 'domain_label':
                    did = next((k for k, v in DOMAIN_LABELS.items() if v == val), "")
                    val = f"{did} - {val}" if did != "" else str(val)
                parts.append(str(val))
            return " | ".join(parts)

        agg['col_name'] = agg.apply(col_label, axis=1)

        pivot_df = (
            agg.pivot(
                index=document_cols,
                columns='col_name',
                values='count'
            )
            .fillna(0)
            .astype(int)
            .reset_index()
        )

        self.aggregated_df = pivot_df
        self.model.clear()
        self.model.setHorizontalHeaderLabels(pivot_df.columns.tolist())
        for _, row in pivot_df.iterrows():
            self.model.appendRow([QStandardItem(str(v)) for v in row])

    def toggle_view(self):
        self.show_aggregated = not self.show_aggregated
        self.switch_view_button.setText(
            "Switch to CSV View" if self.show_aggregated else "Switch to Aggregated View"
        )
        self.refresh_table()

    # ── Export ────────────────────────────────────────────────────────────────

    def export_filtered_csv(self):
        df = self.current_filtered
        if df is None or df.empty:
            QMessageBox.warning(self, "No data", "No filtered data to export.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save Filtered CSV",
                                               "filtered_manifesto.csv", "CSV Files (*.csv)")
        if path:
            df.to_csv(path, index=False)
            QMessageBox.information(self, "Saved", f"Saved {len(df)} rows to {path}")

    def export_aggregated_csv(self):
        if self.aggregated_df is None or self.aggregated_df.empty:
            QMessageBox.warning(self, "No data", "No aggregated data to export.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save Aggregated CSV",
                                               "aggregated_manifesto.csv", "CSV Files (*.csv)")
        if path:
            self.aggregated_df.to_csv(path, index=False)
            QMessageBox.information(self, "Saved", f"Saved {len(self.aggregated_df)} rows to {path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ManifestoAnalyzer()
    window.show()
    sys.exit(app.exec())