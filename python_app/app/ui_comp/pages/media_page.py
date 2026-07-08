"""
media_page.py

Media library management for Smart Showroom products.
"""

from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QSpinBox,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from app.services.media_engine.media_service import MediaService
from app.services.product_service import ProductService
from app.ui_comp.base import (
    BaseButton,
    BaseCard,
    BaseComboBox,
    BaseLineEdit,
    BasePage,
    BaseTable,
)


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


class MediaPage(BasePage):

    def __init__(self, runtime=None):

        super().__init__(
            title="Media",
            subtitle="Manage product images and videos used by showroom playback"
        )

        self.runtime = runtime
        self.products_by_id = {}
        self.selected_media_id = None
        self.preview_pixmap = QPixmap()

        self.build_page()
        self.load_products()

    # -------------------------------------------------

    def build_page(self):

        self.refresh_btn = BaseButton(
            "Refresh",
            icon="fa5s.sync"
        )
        self.refresh_btn.clicked.connect(self.refresh_media)

        self.new_btn = BaseButton(
            "New Media",
            icon="fa5s.plus",
            button_type=BaseButton.SECONDARY
        )
        self.new_btn.clicked.connect(self.clear_form)

        self.add_toolbar_widget(self.new_btn)
        self.add_toolbar_widget(self.refresh_btn)

        top_row = QHBoxLayout()

        self.product_card = BaseCard(
            "Product",
            "Select the product whose media playlist you want to edit"
        )

        self.product_select = BaseComboBox(
            label="Product",
            placeholder="Choose product...",
            icon="fa5s.box"
        )
        self.product_select.combo.currentIndexChanged.connect(
            self.on_product_changed
        )

        self.product_summary = QLabel("No product selected")
        self.product_summary.setWordWrap(True)
        self.product_summary.setStyleSheet(self._muted_label_style())

        self.product_card.add_widget(self.product_select)
        self.product_card.add_widget(self.product_summary)

        self.preview_card = BaseCard(
            "Preview",
            "Selected media file status"
        )

        self.preview_frame = QWidget()
        self.preview_frame.setMinimumHeight(260)
        self.preview_stack = QStackedLayout(self.preview_frame)
        self.preview_stack.setContentsMargins(0, 0, 0, 0)

        self.preview_label = QLabel("Select a media row")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setWordWrap(True)

        self.preview_video = QVideoWidget()

        self.preview_audio = QAudioOutput()
        self.preview_player = QMediaPlayer(self)
        self.preview_player.setAudioOutput(self.preview_audio)
        self.preview_player.setVideoOutput(self.preview_video)

        self.preview_stack.addWidget(self.preview_label)
        self.preview_stack.addWidget(self.preview_video)

        self.preview_frame.setStyleSheet(
            f"""
            QWidget{{
                background:{self.theme.surface};
                border:1px solid {self.theme.border};
                border-radius:{self.theme.radius_md}px;
            }}
            QLabel{{
                background:transparent;
                border:none;
                color:{self.theme.text_secondary};
                padding:16px;
            }}
            """
        )

        self.preview_card.add_widget(self.preview_frame)

        top_row.addWidget(self.product_card, 1)
        top_row.addWidget(self.preview_card, 1)

        self.add_layout(top_row)

        self.form_card = BaseCard(
            "Media Details",
            "Create or update media records for the selected product"
        )

        form_grid = QGridLayout()
        form_grid.setSpacing(12)

        self.name_input = BaseLineEdit(
            label="Media Name",
            placeholder="Front bottle image",
            icon="fa5s.photo-video"
        )

        self.type_select = BaseComboBox(
            label="Media Type",
            placeholder="image or video",
            icon="fa5s.file-video"
        )
        self.type_select.combo.setEditable(False)
        self.type_select.add_item("image")
        self.type_select.add_item("video")

        self.path_input = BaseLineEdit(
            label="File Path",
            placeholder="media/sesame_premium/front.png",
            icon="fa5s.folder-open"
        )

        browse_row = QHBoxLayout()
        browse_row.addWidget(self.path_input, 1)

        self.browse_btn = BaseButton(
            "Add Files",
            icon="fa5s.folder",
            button_type=BaseButton.SECONDARY
        )
        self.browse_btn.clicked.connect(self.browse_media_files)
        browse_row.addWidget(self.browse_btn)

        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 3600)
        self.duration_input.setValue(10)
        self.duration_input.setSuffix(" sec")

        self.order_input = QSpinBox()
        self.order_input.setRange(1, 999)
        self.order_input.setValue(1)

        self.default_check = QCheckBox("Default media")
        self.active_check = QCheckBox("Active")
        self.active_check.setChecked(True)

        self.description_input = BaseLineEdit(
            label="Description",
            placeholder="Optional notes for this media item",
            icon="fa5s.align-left"
        )

        form_grid.addWidget(self.name_input, 0, 0)
        form_grid.addWidget(self.type_select, 0, 1)
        form_grid.addLayout(browse_row, 1, 0, 1, 2)
        form_grid.addWidget(self._field_box("Duration", self.duration_input), 2, 0)
        form_grid.addWidget(self._field_box("Display Order", self.order_input), 2, 1)
        form_grid.addWidget(self.default_check, 3, 0)
        form_grid.addWidget(self.active_check, 3, 1)
        form_grid.addWidget(self.description_input, 4, 0, 1, 2)

        self.form_card.add_layout(form_grid)

        btn_row = QHBoxLayout()

        self.save_btn = BaseButton(
            "Save Media",
            icon="fa5s.save"
        )
        self.save_btn.clicked.connect(self.save_media)

        self.delete_btn = BaseButton(
            "Delete",
            icon="fa5s.trash",
            button_type=BaseButton.DANGER
        )
        self.delete_btn.clicked.connect(self.delete_media)

        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.delete_btn)
        btn_row.addStretch()

        self.form_card.add_layout(btn_row)

        self.add_widget(self.form_card)

        self.table_card = BaseCard(
            "Media Playlist",
            "Click a row to edit or preview"
        )

        self.media_table = BaseTable()
        self.media_table.set_headers([
            "ID",
            "Name",
            "Type",
            "Path",
            "Duration",
            "Order",
            "Default",
            "Active",
            "Exists",
            "Description",
        ])
        self.media_table.cellClicked.connect(self.load_selected_media)

        self.table_card.add_widget(self.media_table)

        self.add_widget(self.table_card)

        self._style_form_controls()

    # -------------------------------------------------

    def load_products(self):

        current_id = self.current_product_id()

        self.product_select.clear()
        self.products_by_id = {}

        products = ProductService.get_all()

        for product in products:
            self.products_by_id[product.id] = product
            self.product_select.add_item(product.name, product.id)

        if current_id:
            index = self.product_select.combo.findData(current_id)
            if index >= 0:
                self.product_select.set_current_index(index)

        self.refresh_media()

    # -------------------------------------------------

    def on_product_changed(self):

        self.clear_form()
        self.refresh_media()

    # -------------------------------------------------

    def refresh_media(self):

        self.media_table.clear_rows()
        self.selected_media_id = None

        product_id = self.current_product_id()
        product = self.products_by_id.get(product_id)

        if not product:
            self.product_summary.setText(
                "Create a product before adding media."
            )
            self.show_preview_message("No product selected")
            return

        self.product_summary.setText(
            f"Keywords: {product.voice_keywords or '-'}\n"
            f"LED Effect: {product.led_effect or '-'}\n"
            f"Media Path: {product.media_path or '-'}"
        )

        media_items = MediaService.get_all_for_product(product_id)

        for media in media_items:

            exists = "Yes" if MediaService.media_exists(media) else "Missing"

            self.media_table.add_row([
                media.id,
                media.media_name or "",
                media.media_type or "",
                media.file_path or "",
                media.duration or 0,
                media.display_order or 0,
                "Yes" if media.is_default else "No",
                "Yes" if media.is_active else "No",
                exists,
                media.description or "",
            ])

        if not media_items:
            self.show_preview_message("No media records for this product")

    # -------------------------------------------------

    def load_selected_media(self, row, column):

        self.selected_media_id = int(
            self.media_table.item(row, 0).text()
        )

        self.name_input.setText(self.media_table.item(row, 1).text())
        self.type_select.set_current_text(self.media_table.item(row, 2).text())
        self.path_input.setText(self.media_table.item(row, 3).text())
        self.duration_input.setValue(
            self._safe_int(self.media_table.item(row, 4).text(), 10)
        )
        self.order_input.setValue(
            self._safe_int(self.media_table.item(row, 5).text(), 1)
        )
        self.default_check.setChecked(
            self.media_table.item(row, 6).text() == "Yes"
        )
        self.active_check.setChecked(
            self.media_table.item(row, 7).text() == "Yes"
        )
        self.description_input.setText(self.media_table.item(row, 9).text())

        self.update_preview(
            self.path_input.text(),
            self.type_select.current_text()
        )

    # -------------------------------------------------

    def browse_media_files(self):

        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Media Files",
            "",
            "Media Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp *.mp4 *.mov *.avi *.mkv *.webm);;All Files (*)"
        )

        if not file_paths:
            return

        if len(file_paths) == 1:
            self.load_file_into_form(file_paths[0])
            return

        self.add_media_files(file_paths)

    # -------------------------------------------------

    def load_file_into_form(self, file_path):

        path = Path(file_path)
        self.path_input.setText(str(path))

        if not self.name_input.text().strip():
            self.name_input.setText(path.stem.replace("_", " ").title())

        if path.suffix.lower() in VIDEO_EXTENSIONS:
            self.type_select.set_current_text("video")
        else:
            self.type_select.set_current_text("image")

        self.update_preview(str(path), self.type_select.current_text())

    # -------------------------------------------------

    def add_media_files(self, file_paths):

        product_id = self.current_product_id()

        if not product_id:
            QMessageBox.warning(
                self,
                "No Product",
                "Select a product before adding media."
            )
            return

        start_order = self.media_table.rowCount() + 1

        for index, file_path in enumerate(file_paths):

            path = Path(file_path)
            media_type = self.media_type_for_path(path)

            MediaService.add_media(
                product_id=product_id,
                media_name=path.stem.replace("_", " ").title(),
                media_type=media_type,
                file_path=str(path),
                duration=self.duration_input.value(),
                display_order=start_order + index,
                is_default=0,
                is_active=1,
                description=self.description_input.text().strip(),
            )

        self.clear_form()
        self.refresh_media()

    # -------------------------------------------------

    def save_media(self):

        product_id = self.current_product_id()

        if not product_id:
            QMessageBox.warning(
                self,
                "No Product",
                "Select a product before saving media."
            )
            return

        name = self.name_input.text().strip()
        file_path = self.path_input.text().strip()

        if not name or not file_path:
            QMessageBox.warning(
                self,
                "Missing Media",
                "Media name and file path are required."
            )
            return

        media_type = self.type_select.current_text().strip().lower()

        if media_type not in {"image", "video"}:
            QMessageBox.warning(
                self,
                "Invalid Type",
                "Media type must be image or video."
            )
            return

        data = {
            "media_name": name,
            "media_type": media_type,
            "file_path": file_path,
            "duration": self.duration_input.value(),
            "display_order": self.order_input.value(),
            "is_default": 1 if self.default_check.isChecked() else 0,
            "is_active": 1 if self.active_check.isChecked() else 0,
            "description": self.description_input.text().strip(),
        }

        if self.selected_media_id:
            MediaService.update_media(
                self.selected_media_id,
                **data
            )
        else:
            MediaService.add_media(
                product_id=product_id,
                **data
            )

        self.clear_form()
        self.refresh_media()

    # -------------------------------------------------

    def delete_media(self):

        if not self.selected_media_id:
            QMessageBox.warning(
                self,
                "No Media",
                "Select a media row to delete."
            )
            return

        confirm = QMessageBox.question(
            self,
            "Delete Media",
            "Delete selected media record?"
        )

        if confirm == QMessageBox.Yes:
            MediaService.delete_media(self.selected_media_id)
            self.clear_form()
            self.refresh_media()

    # -------------------------------------------------

    def clear_form(self):

        self.selected_media_id = None
        self.name_input.clear()
        self.path_input.clear()
        self.description_input.clear()
        self.type_select.set_current_text("image")
        self.duration_input.setValue(10)
        self.order_input.setValue(1)
        self.default_check.setChecked(False)
        self.active_check.setChecked(True)
        self.stop_preview()

        if self.current_product_id():
            self.show_preview_message("Select a media row")
        else:
            self.show_preview_message("No product selected")

    # -------------------------------------------------

    def update_preview(self, file_path, media_type):

        path = Path(file_path)

        if not path.exists():
            self.show_preview_message(f"Missing file:\n{file_path}")
            return

        if media_type.lower() == "image" or path.suffix.lower() in IMAGE_EXTENSIONS:
            self.stop_preview()

            pixmap = QPixmap(str(path))

            if pixmap.isNull():
                self.show_preview_message(f"Cannot preview image:\n{file_path}")
                return

            self.preview_pixmap = pixmap
            self.set_preview_pixmap()
            self.preview_label.setText("")
            self.preview_stack.setCurrentWidget(self.preview_label)
            return

        if media_type.lower() == "video" or path.suffix.lower() in VIDEO_EXTENSIONS:
            self.preview_label.setPixmap(QPixmap())
            self.preview_stack.setCurrentWidget(self.preview_video)
            self.preview_player.stop()
            self.preview_player.setSource(
                QUrl.fromLocalFile(str(path))
            )
            self.preview_player.play()
            return

        self.show_preview_message(
            f"Unsupported media file:\n{path.name}"
        )

    # -------------------------------------------------

    def stop_preview(self):

        self.preview_player.stop()
        self.preview_pixmap = QPixmap()
        self.preview_label.setPixmap(QPixmap())
        self.preview_stack.setCurrentWidget(self.preview_label)

    # -------------------------------------------------

    def show_preview_message(self, message):

        self.preview_player.stop()
        self.preview_pixmap = QPixmap()
        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setText(message)
        self.preview_stack.setCurrentWidget(self.preview_label)

    # -------------------------------------------------

    def set_preview_pixmap(self):

        if self.preview_pixmap.isNull():
            return

        scaled = self.preview_pixmap.scaled(
            self.preview_frame.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.preview_label.setPixmap(scaled)

    # -------------------------------------------------

    def resizeEvent(self, event):

        self.set_preview_pixmap()

        super().resizeEvent(event)

    # -------------------------------------------------

    def current_product_id(self):

        return self.product_select.current_data()

    # -------------------------------------------------

    @staticmethod
    def media_type_for_path(path):

        suffix = path.suffix.lower()

        if suffix in VIDEO_EXTENSIONS:
            return "video"

        return "image"

    # -------------------------------------------------

    def _field_box(self, label, widget):

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        field_label = QLabel(label)
        field_label.setStyleSheet(self._muted_label_style())

        layout.addWidget(field_label)
        layout.addWidget(widget)

        return container

    # -------------------------------------------------

    def _style_form_controls(self):

        control_style = f"""
        QSpinBox{{
            background:{self.theme.surface};
            border:1px solid {self.theme.border};
            border-radius:{self.theme.radius_md}px;
            color:{self.theme.text};
            padding:8px;
        }}

        QCheckBox{{
            color:{self.theme.text};
            background:transparent;
            spacing:8px;
        }}
        """

        self.duration_input.setStyleSheet(control_style)
        self.order_input.setStyleSheet(control_style)
        self.default_check.setStyleSheet(control_style)
        self.active_check.setStyleSheet(control_style)

    # -------------------------------------------------

    def _muted_label_style(self):

        return f"""
        QLabel{{
            color:{self.theme.text_secondary};
            background:transparent;
            font-size:{self.theme.small_size}px;
        }}
        """

    # -------------------------------------------------

    @staticmethod
    def _safe_int(value, default):

        try:
            return int(value)
        except (TypeError, ValueError):
            return default
