import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QMessageBox, QFileDialog,
    QScrollArea, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QGridLayout,
    QGraphicsDropShadowEffect, QMenu, QAction, QDialog,
    QApplication, QGroupBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize, QPoint
from PyQt5.QtGui import QFont, QColor, QPalette
from api.django_client import api_client
from ui.error_dialog import ErrorDialog
import json

try:
    import matplotlib
    matplotlib.use('Qt5Agg')
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    import numpy as np
    import scipy.stats
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    FigureCanvas = None  # type: ignore
    Figure = None  # type: ignore
    plt = None  # type: ignore
    np = None  # type: ignore
    print("Warning: matplotlib not installed. Charts will not be available.")


class InteractiveChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        if not MATPLOTLIB_AVAILABLE or Figure is None or FigureCanvas is None:
            raise RuntimeError("Matplotlib not available")
        self.figure = Figure(figsize=(12, 5), facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.setMinimumHeight(400)
        self.canvas.mpl_connect('motion_notify_event', self.on_hover)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.tooltip = None

    def on_hover(self, event):
        if event.inaxes is None:
            if self.tooltip:
                self.tooltip.set_visible(False)
                self.canvas.draw_idle()
            return
        ax = event.inaxes
        if self.tooltip is None:
            self.tooltip = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                bbox=dict(boxstyle="round,pad=0.8", fc="#1f2937", alpha=0.9, ec="none"),
                color="white", fontsize=11, fontweight='bold', zorder=1000)
            self.tooltip.set_visible(False)
        self.tooltip.xy = (event.xdata, event.ydata)
        self.tooltip.set_text(f"Value: {event.ydata:.2f}" if event.ydata else "")
        self.tooltip.set_visible(True)
        self.canvas.draw_idle()

    def plot_line_chart(self, data, column_name):
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            x = list(range(len(data[:20])))
            y = [float(v) if v is not None else 0 for v in data[:20]]
            ax.plot(x, y, color='#2563eb', linewidth=2.5, marker='o', markersize=6)
            ax.set_title(f'{column_name} - Line Chart', fontsize=14, fontweight='bold', color='#1f2937')
            ax.set_xlabel('Index', fontsize=11, color='#666')
            ax.set_ylabel(column_name, fontsize=11, color='#666')
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_facecolor('#f9fafb')
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Error plotting line chart: {e}")

    def plot_bar_chart(self, data, column_name):
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            x = list(range(len(data[:15])))
            y = [float(v) if v is not None else 0 for v in data[:15]]
            bars = ax.bar(x, y, color='#10b981', edgecolor='#059669', linewidth=1.5, alpha=0.85)
            ax.set_title(f'{column_name} - Bar Chart', fontsize=14, fontweight='bold', color='#1f2937')
            ax.set_xlabel('Index', fontsize=11, color='#666')
            ax.set_ylabel('Value', fontsize=11, color='#666')
            ax.grid(True, alpha=0.3, axis='y', linestyle='--')
            ax.set_facecolor('#f9fafb')
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Error plotting bar chart: {e}")

    def plot_pie_chart(self, data, column_name):
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            vals = [abs(float(v)) if v is not None else 0 for v in data[:10]]
            if sum(vals) > 0:
                colors = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#eab308']
                ax.pie(vals, labels=[f'Item {i+1}' for i in range(len(vals))], autopct='%1.1f%%', startangle=90, colors=colors[:len(vals)])
                ax.set_title(f'{column_name} - Pie Chart', fontsize=14, fontweight='bold', color='#1f2937')
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Error plotting pie chart: {e}")

    def plot_histogram(self, data, column_name):
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            clean_data = [float(x) for x in data if x is not None]
            if clean_data:
                ax.hist(clean_data, bins=20, color='#7c3aed', edgecolor='#6d28d9', alpha=0.8, linewidth=1.5)
                ax.set_title(f'{column_name} - Histogram', fontsize=14, fontweight='bold', color='#1f2937')
                ax.set_xlabel(column_name, fontsize=11, color='#666')
                ax.set_ylabel('Frequency', fontsize=11, color='#666')
                ax.grid(True, alpha=0.3, axis='y', linestyle='--')
            ax.set_facecolor('#f9fafb')
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Error plotting histogram: {e}")

    def plot_scatter(self, data_x, data_y, label_x, label_y):
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            x = [float(v) if v is not None else 0 for v in data_x[:20]]
            y = [float(v) if v is not None else 0 for v in data_y[:20]]
            ax.scatter(x, y, alpha=0.6, s=100, color='#f59e0b', edgecolors='#d97706', linewidth=1.5)
            ax.set_title(f'{label_x} vs {label_y} - Scatter Plot', fontsize=14, fontweight='bold', color='#1f2937')
            ax.set_xlabel(label_x, fontsize=11, color='#666')
            ax.set_ylabel(label_y, fontsize=11, color='#666')
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_facecolor('#f9fafb')
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Error plotting scatter: {e}")

    def plot_area_chart(self, data, column_name):
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            x = list(range(len(data[:20])))
            y = [float(v) if v is not None else 0 for v in data[:20]]
            ax.fill_between(x, y, alpha=0.6, color='#06b6d4', edgecolor='#0891b2', linewidth=2)
            ax.set_title(f'{column_name} - Area Chart', fontsize=14, fontweight='bold', color='#1f2937')
            ax.set_xlabel('Index', fontsize=11, color='#666')
            ax.set_ylabel(column_name, fontsize=11, color='#666')
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_facecolor('#f9fafb')
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Error plotting area chart: {e}")

    def plot_box_plot(self, data, column_name):
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            clean_data = [float(x) for x in data if x is not None]
            if clean_data:
                bp = ax.boxplot(clean_data, patch_artist=True, widths=0.5)
                for patch in bp['boxes']:
                    patch.set_facecolor('#ec4899')
                    patch.set_alpha(0.7)
                for whisker in bp['whiskers']:
                    whisker.set(color='#be123c', linewidth=1.5)
                for median in bp['medians']:
                    median.set(color='#7c2d12', linewidth=2)
                ax.set_title(f'{column_name} - Box Plot', fontsize=14, fontweight='bold', color='#1f2937')
                ax.set_ylabel(column_name, fontsize=11, color='#666')
                ax.grid(True, alpha=0.3, axis='y', linestyle='--')
            ax.set_facecolor('#f9fafb')
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Error plotting box plot: {e}")

    def plot_density(self, data, column_name):
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            clean_data = [float(x) for x in data if x is not None]
            if len(clean_data) > 1:
                ax.hist(clean_data, bins=30, color='#14b8a6', alpha=0.6, density=True, label='Histogram', edgecolor='#0d9488')
                from scipy.stats import gaussian_kde
                try:
                    kde = gaussian_kde(clean_data)
                    x_range = np.linspace(min(clean_data), max(clean_data), 100)
                    ax.plot(x_range, kde(x_range), color='#0f766e', linewidth=2.5, label='Density')
                    ax.legend()
                except:
                    pass
                ax.set_title(f'{column_name} - Density Distribution', fontsize=14, fontweight='bold', color='#1f2937')
                ax.set_xlabel(column_name, fontsize=11, color='#666')
                ax.set_ylabel('Density', fontsize=11, color='#666')
                ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_facecolor('#f9fafb')
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Error plotting density: {e}")

    def plot_cumulative(self, data, column_name):
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            clean_data = sorted([float(x) for x in data if x is not None])
            if clean_data:
                y = np.arange(1, len(clean_data) + 1) / len(clean_data)
                ax.plot(clean_data, y, color='#8b5cf6', linewidth=2.5, marker='o', markersize=4, label='CDF')
                ax.set_title(f'{column_name} - Cumulative Distribution', fontsize=14, fontweight='bold', color='#1f2937')
                ax.set_xlabel(column_name, fontsize=11, color='#666')
                ax.set_ylabel('Cumulative Probability', fontsize=11, color='#666')
                ax.grid(True, alpha=0.3, linestyle='--')
                ax.legend()
            ax.set_facecolor('#f9fafb')
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Error plotting cumulative: {e}")


class DownloadThread(QThread):
    finished = pyqtSignal(bool, str)
    
    def __init__(self, upload_id, save_path):
        super().__init__()
        self.upload_id = upload_id
        self.save_path = save_path
    
    def run(self):
        try:
            result = api_client.download_pdf_report(self.upload_id, self.save_path)
            if "error" not in result:
                self.finished.emit(True, f"PDF saved to: {self.save_path}")
            else:
                self.finished.emit(False, result["error"])
        except Exception as e:
            self.finished.emit(False, str(e))


class ResultsWindow(QMainWindow):
    def __init__(self, upload_id):
        super().__init__()
        self.upload_id = upload_id
        self.current_row_limit = 20
        self.show_all_rows = False
        
        self.setWindowTitle("Analysis Results - Chemizer Analytics")
        self.setGeometry(100, 100, 1400, 900)
        self.showMaximized()
        
        self.analysis_data = self.fetch_analysis_data()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setup_navbar()
        layout.addWidget(self.navbar_widget)

        self.setup_results_content()
        layout.addWidget(self.scroll_area)

        central_widget.setLayout(layout)
        self.load_user_profile()

    def fetch_analysis_data(self):
        response = api_client.get_analysis_results(self.upload_id)
        if "error" in response:
            error_dialog = ErrorDialog("Error", f"Failed to load analysis: {response['error']}", self)
            error_dialog.exec_()
            return {}
        return response

    def setup_navbar(self):
        self.navbar_widget = QFrame()
        self.navbar_widget.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border-bottom: 2px solid rgba(200, 200, 200, 0.4);
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.navbar_widget.setGraphicsEffect(shadow)

        navbar_layout = QHBoxLayout(self.navbar_widget)
        navbar_layout.setContentsMargins(50, 20, 50, 20)
        navbar_layout.setSpacing(40)

        brand_text = QLabel("Chemizer Analytics")
        brand_text.setFont(QFont("Segoe UI", 28, QFont.Bold))
        brand_text.setStyleSheet("color: #1f2937; border: none;")
        navbar_layout.addWidget(brand_text)
        navbar_layout.addStretch()

        back_btn = QPushButton("← Back")
        back_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        back_btn.setMinimumWidth(150)
        back_btn.setStyleSheet("""
            QPushButton { padding: 12px 20px; background-color: #1f2937; color: white;
                border: none; border-radius: 8px; }
            QPushButton:hover { background-color: #374151; }
        """)
        back_btn.clicked.connect(self.go_back_to_dashboard)
        navbar_layout.addWidget(back_btn)

        download_btn = QPushButton("⬇ PDF Report")
        download_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        download_btn.setMinimumWidth(150)
        download_btn.setStyleSheet("""
            QPushButton { padding: 12px 20px; background-color: #2563eb; color: white;
                border: none; border-radius: 8px; }
            QPushButton:hover { background-color: #1d4ed8; }
        """)
        download_btn.clicked.connect(self.handle_download_pdf)
        navbar_layout.addWidget(download_btn)

        self.profile_btn = QPushButton("👤 Profile ")
        self.profile_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.profile_btn.setMinimumWidth(150)
        self.profile_btn.setStyleSheet("""
            QPushButton { padding: 12px 20px; background-color: rgba(31, 41, 55, 0.05);
                color: #1f2937; border: 2px solid rgba(31, 41, 55, 0.1); border-radius: 8px; }
            QPushButton:hover { background-color: rgba(31, 41, 55, 0.1); }
        """)
        profile_menu = QMenu(self)
        profile_menu.setStyleSheet("""
            QMenu { background-color: #ffffff; border: 2px solid #d1d5db; border-radius: 8px; }
            QMenu::item { color: #1f2937; padding: 12px 20px; }
            QMenu::item:selected { background-color: #e5e7eb; }
        """)
        profile_menu.addAction("👤 My Profile", self.show_profile)
        profile_menu.addAction("⚙️ Settings", self.show_settings)
        profile_menu.addSeparator()
        profile_menu.addAction("🚪 Logout", self.logout)
        self.profile_btn.setMenu(profile_menu)
        navbar_layout.addWidget(self.profile_btn)

        self.navbar_widget.setFixedHeight(120)

    def load_user_profile(self):
        response = api_client.get_profile()
        if "error" not in response:
            username = response.get("username", "User")
            full_name = response.get("full_name", username)
            display_name = full_name.split()[0] if full_name else username
            self.profile_btn.setText(f"👤 {display_name} ")

    def setup_results_content(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea { border: none; background-color: #f3f4f6; }
            QScrollBar:vertical { border: none; background: #f3f4f6; width: 12px; }
            QScrollBar::handle:vertical { background: #9ca3af; min-height: 20px; border-radius: 6px; }
        """)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #f3f4f6;")
        self.scroll_area.setWidget(scroll_content)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        rows = self.analysis_data.get('rows', 0)
        columns = self.analysis_data.get('columns', 0)
        summary_stats = self.analysis_data.get('summary_stats', {})
        numeric_cols = list(summary_stats.keys()) if isinstance(summary_stats, dict) else []

        self.add_summary_section(layout, rows, columns, numeric_cols)
        self.add_stats_grid(layout, rows, columns, numeric_cols)
        self.add_highlighted_insights(layout, rows, columns, numeric_cols)
        self.add_data_preview(layout)
        self.add_charts_section(layout, numeric_cols)
        self.add_statistics_section(layout, summary_stats, numeric_cols)
        self.add_column_info(layout)

        layout.addStretch()
        scroll_content.setLayout(layout)

    def add_summary_section(self, layout, rows, columns, numeric_cols):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame { background-color: white; border: 2px solid #d1d5db; border-radius: 12px; padding: 20px; }
        """)
        frame_layout = QVBoxLayout(frame)
        
        title = QLabel("📊 Analysis Summary")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #1f2937; background: transparent; border: none;")
        frame_layout.addWidget(title)

        summary_text = f"This analysis includes {rows:,} rows of equipment data across {columns} columns, with {len(numeric_cols)} numeric parameters. The data has been processed to extract key insights about equipment performance metrics."
        summary_label = QLabel(summary_text)
        summary_label.setFont(QFont("Segoe UI", 12))
        summary_label.setStyleSheet("color: #6b7280; background: transparent; border: none;")
        summary_label.setWordWrap(True)
        frame_layout.addWidget(summary_label)

        layout.addWidget(frame)

    def add_stats_grid(self, layout, rows, columns, numeric_cols):
        grid_frame = QFrame()
        grid_frame.setStyleSheet("background-color: transparent;")
        grid_layout = QGridLayout(grid_frame)
        grid_layout.setSpacing(15)

        stats = [
            ("Total Rows", str(rows)),
            ("Total Columns", str(columns)),
            ("Numeric Columns", str(len(numeric_cols))),
            ("File Size", f"{int(self.analysis_data.get('file_size', 0)) / 1024:.1f} KB")
        ]

        for i, (label, value) in enumerate(stats):
            stat_frame = QFrame()
            stat_frame.setStyleSheet("""
                QFrame { background-color: white; border: 2px solid #d1d5db; border-radius: 12px; padding: 15px; }
            """)
            stat_layout = QVBoxLayout(stat_frame)
            
            label_widget = QLabel(label)
            label_widget.setFont(QFont("Segoe UI", 11))
            label_widget.setStyleSheet("color: #9ca3af; border: none;")
            stat_layout.addWidget(label_widget)

            value_widget = QLabel(value)
            value_widget.setFont(QFont("Segoe UI", 24, QFont.Bold))
            value_widget.setStyleSheet("color: #1f2937; border: none;")
            stat_layout.addWidget(value_widget)

            grid_layout.addWidget(stat_frame, i // 2, i % 2)

        layout.addWidget(grid_frame)

    def add_highlighted_insights(self, layout, rows, columns, numeric_cols):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame { background-color: #cffafe; border: 2px solid #06b6d4; border-radius: 12px; padding: 20px; }
        """)
        frame_layout = QVBoxLayout(frame)

        title = QLabel("🔍 Highlighted Insights")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #1f2937; background: transparent; border: none;")
        frame_layout.addWidget(title)

        insights = [
            f"Dataset contains {len(self.analysis_data.get('data_preview', []))} records available for detailed analysis",
            f"{len(numeric_cols)} numeric columns identified for statistical analysis",
            f"File size: {int(self.analysis_data.get('file_size', 0)) / 1024:.2f} KB"
        ]

        for insight in insights:
            label = QLabel(f"• {insight}")
            label.setFont(QFont("Segoe UI", 11))
            label.setStyleSheet("color: #0c7792; background: transparent; border: none;")
            label.setWordWrap(True)
            frame_layout.addWidget(label)

        layout.addWidget(frame)

    def add_data_preview(self, layout):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame { background-color: #ffffff; border: 2px solid #2563eb; border-radius: 12px; padding: 20px; }
        """)
        frame_layout = QVBoxLayout(frame)

        title = QLabel("📋 Data Preview - Full Table")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #1f2937; background: transparent; border: none;")
        frame_layout.addWidget(title)

        data_preview = self.analysis_data.get('data_preview', [])
        columns = self.analysis_data.get('column_names', [])

        table = QTableWidget()
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        row_height = 35
        header_height = 35
        total_height = header_height + (len(data_preview) * row_height)
        table.setMinimumHeight(min(total_height, 600))
        
        table.setStyleSheet("""
            QTableWidget { border: none; background-color: #ffffff; }
            QTableWidget::item { padding: 8px; border-bottom: 1px solid #e5e7eb; }
            QHeaderView::section { background-color: #2563eb; color: white; padding: 8px; font-weight: bold; border: none; }
            QTableWidget::item:alternate { background-color: #f9fafb; }
        """)
        table.setAlternatingRowColors(True)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        table.setRowCount(len(data_preview))

        for row_idx, row_data in enumerate(data_preview):
            for col_idx, col_name in enumerate(columns):
                value = str(row_data.get(col_name, 'N/A'))
                item = QTableWidgetItem(value)
                item.setFont(QFont("Segoe UI", 10))
                table.setItem(row_idx, col_idx, item)

        frame_layout.addWidget(table)
        layout.addWidget(frame)

    def add_charts_section(self, layout, numeric_cols):
        if not numeric_cols:
            return

        title = QLabel("📈 Charts & Visualizations (10+ Chart Types)")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #1f2937; border: none;")
        layout.addWidget(title)

        data_preview = self.analysis_data.get('data_preview', [])
        col_data = {}
        for col in numeric_cols:
            col_data[col] = [row.get(col) for row in data_preview]

        chart_configs = [
            (0, 'Line Chart', 'plot_line_chart'),
            (1, 'Bar Chart', 'plot_bar_chart'),
            (2, 'Histogram', 'plot_histogram'),
            (3, 'Pie Chart', 'plot_pie_chart'),
            (4, 'Scatter Plot', 'plot_scatter'),
            (5, 'Area Chart', 'plot_area_chart'),
            (6, 'Box Plot', 'plot_box_plot'),
            (7, 'Density Distribution', 'plot_density'),
            (8, 'Cumulative Distribution', 'plot_cumulative'),
            (9, 'Line Chart (Variation)', 'plot_line_chart'),
        ]

        for i, (idx, chart_name, method_name) in enumerate(chart_configs):
            if i >= len(numeric_cols) + 2:
                break
            
            col = numeric_cols[i % len(numeric_cols)]
            
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame { background-color: #ffffff; border: 2px solid #2563eb; border-radius: 12px; padding: 15px; }
            """)
            frame_layout = QVBoxLayout(frame)

            col_title = QLabel(f"📊 {col} - {chart_name}")
            col_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
            col_title.setStyleSheet("color: #2563eb; background: transparent; border: none;")
            frame_layout.addWidget(col_title)

            chart_widget = InteractiveChartWidget()
            
            if method_name == 'plot_line_chart':
                chart_widget.plot_line_chart(col_data[col], col)
            elif method_name == 'plot_bar_chart':
                chart_widget.plot_bar_chart(col_data[col], col)
            elif method_name == 'plot_histogram':
                chart_widget.plot_histogram(col_data[col], col)
            elif method_name == 'plot_pie_chart':
                chart_widget.plot_pie_chart(col_data[col], col)
            elif method_name == 'plot_scatter':
                if i + 1 < len(numeric_cols):
                    col2 = numeric_cols[(i + 1) % len(numeric_cols)]
                    chart_widget.plot_scatter(col_data[col], col_data[col2], col, col2)
                else:
                    chart_widget.plot_line_chart(col_data[col], col)
            elif method_name == 'plot_area_chart':
                chart_widget.plot_area_chart(col_data[col], col)
            elif method_name == 'plot_box_plot':
                chart_widget.plot_box_plot(col_data[col], col)
            elif method_name == 'plot_density':
                chart_widget.plot_density(col_data[col], col)
            elif method_name == 'plot_cumulative':
                chart_widget.plot_cumulative(col_data[col], col)

            frame_layout.addWidget(chart_widget)
            layout.addWidget(frame)

    def add_statistics_section(self, layout, summary_stats, numeric_cols):
        if not numeric_cols:
            return

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame { background-color: white; border: 2px solid #d1d5db; border-radius: 12px; padding: 20px; }
        """)
        frame_layout = QVBoxLayout(frame)

        title = QLabel("📊 Statistics & Calculations")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #1f2937; background: transparent; border: none;")
        frame_layout.addWidget(title)

        for col in numeric_cols:
            if col in summary_stats:
                stats = summary_stats[col]
                stats_frame = QFrame()
                stats_frame.setStyleSheet("""
                    QFrame { background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; }
                """)
                stats_layout = QGridLayout(stats_frame)

                stats_layout.addWidget(QLabel(f"<b>{col}</b>"), 0, 0, 1, 2)
                row = 1
                for key in ['mean', 'median', 'std', 'min', 'max', 'count']:
                    if key in stats:
                        label = QLabel(f"{key.capitalize()}:")
                        label.setFont(QFont("Segoe UI", 10))
                        value = QLabel(f"{stats[key]:.2f}" if isinstance(stats[key], float) else str(stats[key]))
                        value.setFont(QFont("Segoe UI", 10, QFont.Bold))
                        stats_layout.addWidget(label, row, 0)
                        stats_layout.addWidget(value, row, 1)
                        row += 1

                frame_layout.addWidget(stats_frame)

        layout.addWidget(frame)

    def add_column_info(self, layout):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame { background-color: white; border: 2px solid #d1d5db; border-radius: 12px; padding: 20px; }
        """)
        frame_layout = QVBoxLayout(frame)

        title = QLabel("📑 Column Information")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #1f2937; background: transparent; border: none;")
        frame_layout.addWidget(title)

        data_preview = self.analysis_data.get('data_preview', [])
        columns = self.analysis_data.get('column_names', [])
        
        if not data_preview or not columns:
            frame_layout.addWidget(QLabel("No column information available"))
            layout.addWidget(frame)
            return

        data_types = {}
        missing_values = {}
        
        for col in columns:
            missing_values[col] = sum(1 for row in data_preview if row.get(col) is None)
            sample_value = next((row.get(col) for row in data_preview if row.get(col) is not None), None)
            if sample_value is not None:
                try:
                    float(sample_value)
                    data_types[col] = 'Numeric'
                except:
                    data_types[col] = 'Text'
            else:
                data_types[col] = 'Unknown'

        for col in columns:
            info_frame = QFrame()
            info_frame.setStyleSheet("""
                QFrame { background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px; }
            """)
            info_layout = QHBoxLayout(info_frame)

            col_label = QLabel(col)
            col_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            info_layout.addWidget(col_label)

            info_layout.addStretch()

            type_label = QLabel(f"Type: {data_types.get(col, 'Unknown')}")
            type_label.setFont(QFont("Segoe UI", 10))
            type_label.setStyleSheet("color: #6b7280;")
            info_layout.addWidget(type_label)

            missing_label = QLabel(f"Missing: {missing_values.get(col, 0)}")
            missing_label.setFont(QFont("Segoe UI", 10))
            missing_label.setStyleSheet("color: #6b7280;")
            info_layout.addWidget(missing_label)

            frame_layout.addWidget(info_frame)

        layout.addWidget(frame)

    def handle_download_pdf(self):
        from datetime import datetime
        default_filename = f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF Report", default_filename, "PDF Files (*.pdf)")
        if file_path:
            self.download_thread = DownloadThread(self.upload_id, file_path)
            self.download_thread.finished.connect(self.on_download_finished)
            self.download_thread.start()

    def on_download_finished(self, success, message):
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", f"Download failed: {message}")

    def go_back_to_dashboard(self):
        from ui.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def show_profile(self):
        QMessageBox.information(self, "Profile", "Profile window would open here")

    def show_settings(self):
        QMessageBox.information(self, "Settings", "Settings window would open here")

    def logout(self):
        QMessageBox.information(self, "Logout", "Logged out successfully")
        self.close()