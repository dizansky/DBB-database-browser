import sys
import traceback
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QTextEdit, QListWidget, QFileDialog, QMessageBox, QDialog, QSpinBox,
    QListWidgetItem, QScrollArea, QFormLayout, QGraphicsDropShadowEffect,
    QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QColor
from database_manager import DatabaseManager
GLOBAL_STYLE =
class ModernButton(QPushButton):
    def __init__(self, text, parent=None, is_primary=False):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        if is_primary:
            self.setStyleSheet()
        else:
            self.setStyleSheet()
        self.setMinimumHeight(42)
class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet()
        self.setMinimumHeight(40)
def create_shadow():
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    shadow.setColor(QColor(0, 0, 0, 15))
    return shadow
def create_panel():
    widget = QWidget()
    widget.setStyleSheet()
    widget.setGraphicsEffect(create_shadow())
    return widget
def apply_dialog_style(dialog):
    dialog.setStyleSheet("QDialog { background-color: #ffffff; }")
    dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
class DatabaseBrowser(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = DatabaseManager()
        self.init_ui()
    def init_ui(self):
        self.setStyleSheet("QWidget#MainBg { background-color: #f4f5f7; }")
        self.setObjectName("MainBg")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        header = QWidget()
        header.setStyleSheet("background-color: #ffffff; border-bottom: 1px solid #e0e0e0;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        title_label = QLabel("SQL Browser")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setStyleSheet("color: #0f0f0f; border: none;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        logout_btn = ModernButton("Выход")
        logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(logout_btn)
        main_layout.addWidget(header)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(24)
        content_layout.setContentsMargins(24, 24, 24, 24)
        left_widget = create_panel()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(12)
        conn_title = QLabel("Подключения")
        conn_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        conn_title.setStyleSheet("border: none;")
        left_layout.addWidget(conn_title)
        self.sqlite_btn = ModernButton("🗄️ SQLite", is_primary=True)
        self.mysql_btn = ModernButton("📊 MySQL", is_primary=True)
        self.postgresql_btn = ModernButton("🐘 PostgreSQL", is_primary=True)
        self.disconnect_btn = ModernButton("❌ Отключиться")
        self.sqlite_btn.clicked.connect(self.connect_sqlite)
        self.mysql_btn.clicked.connect(self.connect_mysql)
        self.postgresql_btn.clicked.connect(self.connect_postgresql)
        self.disconnect_btn.clicked.connect(self.disconnect)
        left_layout.addWidget(self.sqlite_btn)
        left_layout.addWidget(self.mysql_btn)
        left_layout.addWidget(self.postgresql_btn)
        left_layout.addWidget(self.disconnect_btn)
        self.status_label = QLabel("❌ Не подключено")
        self.status_label.setFont(QFont("Segoe UI", 11, QFont.Medium))
        self.status_label.setStyleSheet("color: #d32f2f; padding: 12px; background-color: #fef0f0; border-radius: 6px; border: none;")
        self.status_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.status_label)
        left_layout.addSpacing(20)
        tables_title = QLabel("Таблицы")
        tables_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        tables_title.setStyleSheet("border: none;")
        left_layout.addWidget(tables_title)
        search_table = ModernLineEdit("🔍 Поиск")
        left_layout.addWidget(search_table)
        self.tables_list = QListWidget()
        self.tables_list.setStyleSheet()
        self.tables_list.itemClicked.connect(self.on_table_selected)
        left_layout.addWidget(self.tables_list)
        def filter_tables(text):
            for i in range(self.tables_list.count()):
                item = self.tables_list.item(i)
                item.setHidden(text.lower() not in item.text().lower())
        search_table.textChanged.connect(filter_tables)
        left_widget.setMaximumWidth(300)
        center_widget = create_panel()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(24, 24, 24, 24)
        center_layout.setSpacing(16)
        data_title = QLabel("Данные таблицы")
        data_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        data_title.setStyleSheet("border: none;")
        center_layout.addWidget(data_title)
        self.table_view = QTableWidget()
        self.table_view.setStyleSheet()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_view.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table_view.setShowGrid(False)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.verticalHeader().setVisible(False)
        center_layout.addWidget(self.table_view)
        query_title = QLabel("SQL Query")
        query_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        query_title.setStyleSheet("border: none;")
        center_layout.addWidget(query_title)
        self.query_text = QTextEdit()
        self.query_text.setStyleSheet()
        self.query_text.setMaximumHeight(120)
        center_layout.addWidget(self.query_text)
        btn_layout = QHBoxLayout()
        exec_btn = ModernButton("▶️ Выполнить", is_primary=True)
        clear_btn = ModernButton("📋 Очистить")
        refresh_btn = ModernButton("🔄 Обновить")
        export_csv_btn = ModernButton("💾 CSV")
        export_excel_btn = ModernButton("📊 Excel")
        crud_layout = QHBoxLayout()
        insert_btn = ModernButton("➕ Добавить")
        edit_btn = ModernButton("✏️ Редактировать")
        delete_btn = ModernButton("🗑️ Удалить")
        exec_btn.clicked.connect(self.execute_query)
        clear_btn.clicked.connect(lambda: self.query_text.clear())
        refresh_btn.clicked.connect(self.refresh_current_table)
        export_csv_btn.clicked.connect(lambda: self.export_data('csv'))
        export_excel_btn.clicked.connect(lambda: self.export_data('excel'))
        insert_btn.clicked.connect(self.insert_new_row)
        edit_btn.clicked.connect(self.edit_selected_row)
        delete_btn.clicked.connect(self.delete_selected_row)
        btn_layout.addWidget(exec_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(export_csv_btn)
        btn_layout.addWidget(export_excel_btn)
        btn_layout.addStretch()
        crud_layout.addWidget(insert_btn)
        crud_layout.addWidget(edit_btn)
        crud_layout.addWidget(delete_btn)
        crud_layout.addStretch()
        center_layout.addLayout(btn_layout)
        center_layout.addLayout(crud_layout)
        right_widget = create_panel()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(12)
        info_title = QLabel("Информация о таблице")
        info_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        info_title.setStyleSheet("border: none;")
        right_layout.addWidget(info_title)
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setStyleSheet()
        right_layout.addWidget(self.info_text)
        result_title = QLabel("Результаты")
        result_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        result_title.setStyleSheet("border: none;")
        right_layout.addWidget(result_title)
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet()
        right_layout.addWidget(self.result_text)
        right_widget.setMaximumWidth(320)
        content_layout.addWidget(left_widget, 2)
        content_layout.addWidget(center_widget, 6)
        content_layout.addWidget(right_widget, 2)
        main_layout.addLayout(content_layout)
    def connect_sqlite(self):
        file_path = QFileDialog.getOpenFileName(self, "Выберите SQLite Database", "", "SQLite DB (*.db *.sqlite *.sqlite3);;All Files (*.*)")[0]
        if file_path:
            success, message = self.db_manager.connect_sqlite(file_path)
            if success:
                self.update_status()
                self.refresh_tables()
                QMessageBox.information(self, "Успех", message)
            else:
                QMessageBox.critical(self, "Ошибка", message)
    def connect_mysql(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Подключение к MySQL")
        apply_dialog_style(dialog)
        dialog.setMinimumWidth(350)
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Настройки MySQL")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title)
        fields = {
            'Host': ('localhost', 'text'),
            'User': ('root', 'text'),
            'Password': ('', 'password'),
            'Database': ('', 'text'),
            'Port': (3306, 'number')
        }
        entries = {}
        for label, (default, type_) in fields.items():
            field_layout = QVBoxLayout()
            field_layout.setSpacing(5)
            field_label = QLabel(label)
            field_label.setFont(QFont("Segoe UI", 11))
            field_label.setStyleSheet("color: #555555;")
            if type_ == 'password':
                entry = ModernLineEdit()
                entry.setEchoMode(QLineEdit.Password)
            elif type_ == 'number':
                entry = QSpinBox()
                entry.setStyleSheet()
                entry.setValue(default)
                entry.setMinimum(1)
                entry.setMaximum(65535)
                entry.setMinimumHeight(40)
            else:
                entry = ModernLineEdit()
                entry.setText(str(default))
            entries[label.lower()] = entry
            field_layout.addWidget(field_label)
            field_layout.addWidget(entry)
            layout.addLayout(field_layout)
        def connect():
            try:
                host = entries['host'].text() if hasattr(entries['host'], 'text') else str(entries['host'].value())
                success, message = self.db_manager.connect_mysql(
                    host, entries['user'].text(), entries['password'].text(),
                    entries['database'].text(), entries['port'].value()
                )
                if success:
                    self.update_status()
                    self.refresh_tables()
                    QMessageBox.information(self, "Успех", message)
                    dialog.close()
                else:
                    QMessageBox.critical(self, "Ошибка", message)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
        btn = ModernButton("Подключиться", is_primary=True)
        btn.clicked.connect(connect)
        layout.addSpacing(10)
        layout.addWidget(btn)
        dialog.exec_()
    def connect_postgresql(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Подключение к PostgreSQL")
        apply_dialog_style(dialog)
        dialog.setMinimumWidth(350)
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Настройки PostgreSQL")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title)
        fields = {
            'Host': ('localhost', 'text'),
            'User': ('postgres', 'text'),
            'Password': ('', 'password'),
            'Database': ('', 'text'),
            'Port': (5432, 'number')
        }
        entries = {}
        for label, (default, type_) in fields.items():
            field_layout = QVBoxLayout()
            field_layout.setSpacing(5)
            field_label = QLabel(label)
            field_label.setFont(QFont("Segoe UI", 11))
            field_label.setStyleSheet("color: #555555;")
            if type_ == 'password':
                entry = ModernLineEdit()
                entry.setEchoMode(QLineEdit.Password)
            elif type_ == 'number':
                entry = QSpinBox()
                entry.setStyleSheet()
                entry.setValue(default)
                entry.setMinimum(1)
                entry.setMaximum(65535)
                entry.setMinimumHeight(40)
            else:
                entry = ModernLineEdit()
                entry.setText(str(default))
            entries[label.lower()] = entry
            field_layout.addWidget(field_label)
            field_layout.addWidget(entry)
            layout.addLayout(field_layout)
        def connect():
            try:
                host = entries['host'].text() if hasattr(entries['host'], 'text') else str(entries['host'].value())
                success, message = self.db_manager.connect_postgresql(
                    host, entries['user'].text(), entries['password'].text(),
                    entries['database'].text(), entries['port'].value()
                )
                if success:
                    self.update_status()
                    self.refresh_tables()
                    QMessageBox.information(self, "Успех", message)
                    dialog.close()
                else:
                    QMessageBox.critical(self, "Ошибка", message)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
        btn = ModernButton("Подключиться", is_primary=True)
        btn.clicked.connect(connect)
        layout.addSpacing(10)
        layout.addWidget(btn)
        dialog.exec_()
    def disconnect(self):
        self.db_manager.disconnect()
        self.update_status()
        self.tables_list.clear()
        self.table_view.clearContents()
        self.table_view.setRowCount(0)
        self.table_view.setColumnCount(0)
        self.info_text.clear()
        self.result_text.clear()
    def update_status(self):
        if self.db_manager.is_connected():
            self.status_label.setText(f"✅ Подключено ({self.db_manager.db_type})")
            self.status_label.setStyleSheet("color: #1b5e20; padding: 12px; background-color: #e8f5e9; border-radius: 6px; border: none;")
        else:
            self.status_label.setText("❌ Не подключено")
            self.status_label.setStyleSheet("color: #b71c1c; padding: 12px; background-color: #ffebee; border-radius: 6px; border: none;")
    def refresh_tables(self):
        self.tables_list.clear()
        for table in self.db_manager.get_tables():
            self.tables_list.addItem(table)
    def on_table_selected(self, item):
        table_name = item.text()
        self.load_table_data(table_name)
        self.show_table_info(table_name)
    def load_table_data(self, table_name):
        columns, rows = self.db_manager.get_table_data(table_name)
        self.table_view.setColumnCount(len(columns))
        self.table_view.setHorizontalHeaderLabels(columns)
        self.table_view.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value) if value is not None else "NULL")
                self.table_view.setItem(row_idx, col_idx, item)
    def show_table_info(self, table_name):
        structure = self.db_manager.get_table_structure(table_name)
        row_count = self.db_manager.get_row_count(table_name)
        info = f"Таблица: {table_name}\n"
        info += f"Количество строк: {row_count}\n\n"
        info += "Структура:\n" + "-" * 30 + "\n"
        for col in structure:
            info += f"• {col['name']}: {col['type']}\n"
        self.info_text.setText(info)
    def execute_query(self):
        query = self.query_text.toPlainText().strip()
        if not query:
            QMessageBox.warning(self, "Ошибка", "Введите SQL запрос!")
            return
        success, result = self.db_manager.execute_query(query)
        if success:
            if isinstance(result, tuple):
                columns, rows = result
                self.table_view.setColumnCount(len(columns))
                self.table_view.setHorizontalHeaderLabels(columns)
                self.table_view.setRowCount(len(rows))
                for row_idx, row in enumerate(rows):
                    for col_idx, value in enumerate(row):
                        item = QTableWidgetItem(str(value) if value is not None else "NULL")
                        self.table_view.setItem(row_idx, col_idx, item)
                self.result_text.setText(f"✅ Выполнено успешно!\n\nСтрок: {len(rows)}")
            else:
                self.result_text.setText(f"✅ {result}")
        else:
            self.result_text.setText(f"❌ Ошибка: {result}")
    def refresh_current_table(self):
        items = self.tables_list.selectedItems()
        if items:
            self.on_table_selected(items[0])
    def export_data(self, format_type):
        items = self.tables_list.selectedItems()
        if not items:
            QMessageBox.warning(self, "Ошибка", "Выберите таблицу!")
            return
        table_name = items[0].text()
        if format_type == 'csv':
            file_path = QFileDialog.getSaveFileName(self, "Сохранить CSV", "", "CSV Files (*.csv)")[0]
            if file_path:
                success, msg = self.db_manager.export_to_csv(table_name, file_path)
                QMessageBox.information(self, "Успех", msg) if success else QMessageBox.critical(self, "Ошибка", msg)
        else:
            file_path = QFileDialog.getSaveFileName(self, "Сохранить Excel", "", "Excel Files (*.xlsx)")[0]
            if file_path:
                success, msg = self.db_manager.export_to_excel(table_name, file_path)
                QMessageBox.information(self, "Успех", msg) if success else QMessageBox.critical(self, "Ошибка", msg)
    def insert_new_row(self):
        items = self.tables_list.selectedItems()
        if not items:
            QMessageBox.warning(self, "Ошибка", "Выберите таблицу!")
            return
        table_name = items[0].text()
        structure = self.db_manager.get_table_structure(table_name)
        if not structure:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить структуру таблицы!")
            return
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Добавить строку в {table_name}")
        apply_dialog_style(dialog)
        dialog.setMinimumWidth(400)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        title = QLabel("Новая запись")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        form_layout = QVBoxLayout(scroll_content)
        form_layout.setSpacing(10)
        entries = {}
        for col in structure:
            col_name = col['name']
            field_layout = QVBoxLayout()
            field_layout.setSpacing(5)
            field_label = QLabel(col_name)
            field_label.setFont(QFont("Segoe UI", 11))
            field_label.setStyleSheet("color: #555555;")
            entry = ModernLineEdit(f"Введите {col_name}")
            entries[col_name] = entry
            field_layout.addWidget(field_label)
            field_layout.addWidget(entry)
            form_layout.addLayout(field_layout)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        btn_layout = QHBoxLayout()
        ok_btn = ModernButton("✓ Добавить", is_primary=True)
        cancel_btn = ModernButton("✗ Отмена")
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        def insert():
            try:
                values = []
                for col in structure:
                    col_name = col['name']
                    col_type = col['type']
                    value = entries[col_name].text().strip()
                    if value.lower() in ['null', 'none', '']:
                        values.append(None)
                    elif 'int' in col_type.lower():
                        values.append(int(value) if value else 0)
                    elif 'float' in col_type.lower() or 'double' in col_type.lower():
                        values.append(float(value) if value else 0.0)
                    else:
                        values.append(value)
                col_names = ', '.join([f"`{col['name']}`" for col in structure])
                placeholders = ', '.join(['?'] * len(structure)) if self.db_manager.db_type == 'sqlite' else ', '.join(['%s'] * len(structure))
                query = f"INSERT INTO `{table_name}` ({col_names}) VALUES ({placeholders})"
                success, message = self.db_manager.execute_query(query, values)
                if success:
                    QMessageBox.information(self, "Успех", "Строка добавлена!")
                    dialog.close()
                    self.refresh_current_table()
                else:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось добавить: {message}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при вставке: {str(e)}")
        ok_btn.clicked.connect(insert)
        cancel_btn.clicked.connect(dialog.close)
        dialog.exec_()
    def edit_selected_row(self):
        selected = self.table_view.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите ячейку для редактирования!")
            return
        items = self.tables_list.selectedItems()
        if not items:
            QMessageBox.warning(self, "Ошибка", "Выберите таблицу!")
            return
        row = selected[0].row()
        table_name = items[0].text()
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Редактировать строку")
        apply_dialog_style(dialog)
        dialog.setMinimumWidth(400)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        title = QLabel("Редактирование")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        form_layout = QVBoxLayout(scroll_content)
        form_layout.setSpacing(10)
        headers = [self.table_view.horizontalHeaderItem(col).text() for col in range(self.table_view.columnCount())]
        entries = {}
        for col_idx, col_name in enumerate(headers):
            field_layout = QVBoxLayout()
            field_layout.setSpacing(5)
            field_label = QLabel(col_name)
            field_label.setFont(QFont("Segoe UI", 11))
            field_label.setStyleSheet("color: #555555;")
            item = self.table_view.item(row, col_idx)
            current_value = item.text() if item else ""
            entry = ModernLineEdit()
            entry.setText(current_value)
            entries[col_idx] = entry
            field_layout.addWidget(field_label)
            field_layout.addWidget(entry)
            form_layout.addLayout(field_layout)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        btn_layout = QHBoxLayout()
        ok_btn = ModernButton("✓ Сохранить", is_primary=True)
        cancel_btn = ModernButton("✗ Отмена")
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        def save_edit():
            try:
                for col_idx, entry in entries.items():
                    col_name = headers[col_idx]
                    new_value = entry.text().strip()
                    query = f"UPDATE `{table_name}` SET `{col_name}` = ? WHERE rowid = {row + 1}" if self.db_manager.db_type == 'sqlite' else f"UPDATE `{table_name}` SET `{col_name}` = %s WHERE rowid = {row + 1}"
                    self.db_manager.execute_query(query, [new_value])
                QMessageBox.information(self, "Успех", "Изменения сохранены!")
                dialog.close()
                self.refresh_current_table()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при редактировании: {str(e)}")
        ok_btn.clicked.connect(save_edit)
        cancel_btn.clicked.connect(dialog.close)
        dialog.exec_()
    def delete_selected_row(self):
        selected = self.table_view.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите строку для удаления!")
            return
        items = self.tables_list.selectedItems()
        if not items:
            QMessageBox.warning(self, "Ошибка", "Выберите таблицу!")
            return
        row = selected[0].row()
        table_name = items[0].text()
        reply = QMessageBox.question(self, "Подтверждение", f"Вы уверены, что хотите удалить строку {row + 1}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                query = f"DELETE FROM `{table_name}` WHERE rowid = {row + 1}"
                success, message = self.db_manager.execute_query(query)
                if success:
                    QMessageBox.information(self, "Успех", "Строка удалена!")
                    self.refresh_current_table()
                else:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось удалить: {message}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении: {str(e)}")
    def logout(self):
        self.db_manager.disconnect()
        sys.exit(0)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL Browser")
        self.setGeometry(100, 100, 1400, 850)
        self.setStyleSheet(GLOBAL_STYLE)
        browser = DatabaseBrowser(self)
        self.setCentralWidget(browser)
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()