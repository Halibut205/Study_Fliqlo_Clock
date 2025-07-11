"""
UI Components Module - Quản lý giao diện người dùng
"""

import tkinter as tk
from tkinter import font as tkfont
from .task_ui import TaskUI  # Import DailyStatsUI

# Session duration options - định nghĩa local để tránh import issues
SESSION_DURATION_OPTIONS = {
    "15 min": 15 * 60,    # 900 seconds
    "25 min": 25 * 60,    # 1500 seconds (Pomodoro)
    "30 min": 30 * 60,    # 1800 seconds
    "45 min": 45 * 60,    # 2700 seconds
    "1 hour": 60 * 60,    # 3600 seconds (default)
    "1.5 hours": 90 * 60, # 5400 seconds
    "2 hours": 120 * 60   # 7200 seconds
}

class FliqloUI:
    def __init__(self, root):
        self.root = root
        self._setup_window()
        self._create_widgets()
        
        # Callbacks cho các sự kiện
        self.on_start = None
        self.on_toggle = None
        self.on_reset = None
        self.on_sessions_changed = None
        self.on_auto_continue_changed = None
        self.on_reset_sessions = None
        self.on_session_duration_changed = None  # New callback
        self.on_help_clicked = None  # Help callback
        self.on_stats_clicked = None  # Stats window callback
        
        # Task callbacks
        self.on_add_task = None
        self.on_complete_task = None
        self.on_delete_task = None
        self.on_edit_task = None
        self.on_reactivate_task = None  # New callback for reactivating tasks
        self.on_clear_completed = None
        
        # Sound manager callback
        self.play_sound = None

    def _setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.root.title("Fliqlo Timer")
        self.root.configure(bg='black')
        self.root.geometry("500x600")  # Trở lại kích thước ban đầu
        self.root.resizable(False, False)  # Không cho resize

    def _create_widgets(self):
        """Tạo các widget UI"""
        # Font nhỏ gọn hơn
        self.clock_font = tkfont.Font(family="Courier New", size=36, weight="bold")  # Giảm từ 72
        self.break_font = tkfont.Font(family="Courier New", size=18, weight="bold")  # Giảm từ 36
        self.info_font = tkfont.Font(family="Courier New", size=12, weight="bold")   # Giảm từ 16

        # Session info frame - compact
        self.session_frame = tk.Frame(self.root, bg='black')
        self.session_frame.pack(pady=5)

        # Session counter
        self.session_label = tk.Label(
            self.session_frame,
            text="Session: 0/8",
            font=self.info_font,
            fg="yellow",
            bg="black"
        )
        self.session_label.pack(side=tk.LEFT, padx=10)

        # Progress indicator
        self.progress_label = tk.Label(
            self.session_frame,
            text="Progress: 0%",
            font=self.info_font,
            fg="orange",
            bg="black"
        )
        self.progress_label.pack(side=tk.RIGHT, padx=10)

        # Main timer label - compact (bỏ chữ "Main")
        self.main_timer_label = tk.Label(
            self.root, 
            text="00:00:00", 
            font=self.clock_font, 
            fg="white", 
            bg="black"
        )
        self.main_timer_label.pack(pady=5)

        # Break timer label - compact
        self.break_timer_label = tk.Label(
            self.root, 
            text="Break: 00:00:00", 
            font=self.break_font, 
            fg="cyan", 
            bg="black"
        )
        self.break_timer_label.pack(pady=5)

        # Help and stats buttons frame
        help_frame = tk.Frame(self.root, bg='black')
        help_frame.pack(pady=5)
        
        help_btn_top = tk.Button(
            help_frame,
            text="❓ Trợ giúp / Help",
            font=tkfont.Font(family="Arial", size=10, weight="bold"),
            width=18,
            height=1,
            bg="purple",
            fg="white",
            command=self._on_help_clicked
        )
        help_btn_top.pack(side="left", padx=(0, 5))
        
        # Daily stats button
        stats_btn = tk.Button(
            help_frame,
            text="📊 Daily Stats",
            font=tkfont.Font(family="Arial", size=10, weight="bold"),
            width=18,
            height=1,
            bg="#2c3e50",
            fg="white",
            command=self._on_stats_clicked
        )
        stats_btn.pack(side="left", padx=5)

        # Main control buttons - TO HƠN
        self._create_main_buttons()

        # Settings frame - compact
        self._create_settings()

        # Task management frame - compact
        self.task_ui = TaskUI(self.root)

    def _create_main_buttons(self):
        """Tạo các nút điều khiển chính - TO HƠN"""
        btn_frame = tk.Frame(self.root, bg='black')
        btn_frame.pack(pady=10)

        # Các nút to hơn với font lớn hơn
        btn_font = tkfont.Font(family="Arial", size=14, weight="bold")
        
        self.start_btn = tk.Button(
            btn_frame, 
            text="▶ START", 
            font=btn_font,
            width=12, 
            height=2,
            bg="green",
            fg="white",
            command=self._on_start_clicked
        )
        self.start_btn.grid(row=0, column=0, padx=8, pady=5)

        self.toggle_btn = tk.Button(
            btn_frame, 
            text="⏸ PAUSE", 
            font=btn_font,
            width=12,
            height=2,
            bg="orange",
            fg="white", 
            command=self._on_toggle_clicked
        )
        self.toggle_btn.grid(row=0, column=1, padx=8, pady=5)

        self.reset_btn = tk.Button(
            btn_frame, 
            text="🔄 RESET", 
            font=btn_font,
            width=12,
            height=2,
            bg="red",
            fg="white",
            command=self._on_reset_clicked
        )
        self.reset_btn.grid(row=0, column=2, padx=8, pady=5)

    def _create_settings(self):
        """Tạo phần cài đặt session - compact"""
        settings_frame = tk.Frame(self.root, bg='black')
        settings_frame.pack(pady=5)

        # Session duration setting - NEW
        tk.Label(settings_frame, text="Duration:", fg="white", bg="black", font=("Arial", 9)).grid(row=0, column=0, padx=3)
        self.session_duration_var = tk.StringVar(value="1 hour")
        self.duration_combobox = tk.OptionMenu(
            settings_frame,
            self.session_duration_var,
            *SESSION_DURATION_OPTIONS.keys(),
            command=self._on_session_duration_changed
        )
        self.duration_combobox.config(
            font=("Arial", 8),
            width=8,
            bg="gray20",
            fg="white",
            highlightthickness=0
        )
        self.duration_combobox.grid(row=0, column=1, padx=3)

        # Target sessions setting - compact
        tk.Label(settings_frame, text="Sessions:", fg="white", bg="black", font=("Arial", 9)).grid(row=0, column=2, padx=3)
        self.sessions_var = tk.StringVar(value="8")
        self.sessions_spinbox = tk.Spinbox(
            settings_frame,
            from_=1, to=20,
            textvariable=self.sessions_var,
            width=3,
            font=("Arial", 9),
            command=self._on_sessions_changed
        )
        self.sessions_spinbox.grid(row=0, column=3, padx=3)

        # Auto continue setting - compact
        self.auto_continue_var = tk.BooleanVar(value=False)
        self.auto_continue_cb = tk.Checkbutton(
            settings_frame,
            text="Auto",
            variable=self.auto_continue_var,
            fg="white",
            bg="black",
            selectcolor="black",
            font=("Arial", 9),
            command=self._on_auto_continue_changed
        )
        self.auto_continue_cb.grid(row=0, column=4, padx=5)

        # Reset sessions button - compact
        self.reset_sessions_btn = tk.Button(
            settings_frame,
            text="Reset",
            width=8,
            font=("Arial", 8),
            command=self._on_reset_sessions_clicked
        )
        self.reset_sessions_btn.grid(row=0, column=5, padx=5)

    def _on_start_clicked(self):
        """Xử lý sự kiện click nút Start"""
        if self.play_sound:
            self.play_sound()
        if self.on_start:
            self.on_start()

    def _on_toggle_clicked(self):
        """Xử lý sự kiện click nút Pause/Resume"""
        if self.play_sound:
            self.play_sound()
        if self.on_toggle:
            self.on_toggle()

    def _on_reset_clicked(self):
        """Xử lý sự kiện click nút Reset"""
        if self.play_sound:
            self.play_sound()
        if self.on_reset:
            self.on_reset()

    def _on_sessions_changed(self):
        """Xử lý sự kiện thay đổi target sessions"""
        if self.on_sessions_changed:
            try:
                sessions = int(self.sessions_var.get())
                self.on_sessions_changed(sessions)
            except ValueError:
                pass

    def _on_auto_continue_changed(self):
        """Xử lý sự kiện thay đổi auto continue"""
        if self.play_sound:
            self.play_sound()
        if self.on_auto_continue_changed:
            self.on_auto_continue_changed(self.auto_continue_var.get())

    def _on_reset_sessions_clicked(self):
        """Xử lý sự kiện reset sessions"""
        if self.play_sound:
            self.play_sound()
        if self.on_reset_sessions:
            self.on_reset_sessions()

    def _on_session_duration_changed(self, selected_duration):
        """Xử lý sự kiện thay đổi session duration"""
        if self.play_sound:
            self.play_sound()
        if self.on_session_duration_changed:
            duration_seconds = SESSION_DURATION_OPTIONS[selected_duration]
            self.on_session_duration_changed(duration_seconds, selected_duration)

    def _on_help_clicked(self):
        """Xử lý sự kiện click nút Help"""
        if self.play_sound:
            self.play_sound()
        if self.on_help_clicked:
            self.on_help_clicked()

    def _on_stats_clicked(self):
        """Xử lý sự kiện click nút Daily Stats"""
        if self.play_sound:
            self.play_sound()
        if self.on_stats_clicked:
            self.on_stats_clicked()

    def update_main_timer_display(self, time_text):
        """Cập nhật hiển thị main timer (bỏ chữ Main)"""
        self.main_timer_label.config(text=time_text)

    def update_break_timer_display(self, time_text):
        """Cập nhật hiển thị break timer"""
        self.break_timer_label.config(text=f"Break: {time_text}")

    def update_button_state(self, state):
        """Cập nhật trạng thái các nút theo dual clock system"""
        if state == "main_running":
            self.toggle_btn.config(text="🔄 → BREAK", bg="orange")
            self.main_timer_label.config(fg="lime")  # Active main timer
            self.break_timer_label.config(fg="gray")  # Inactive break timer
        elif state == "break_running":
            self.toggle_btn.config(text="🔄 → MAIN", bg="blue")
            self.main_timer_label.config(fg="gray")  # Inactive main timer
            self.break_timer_label.config(fg="cyan")  # Active break timer
        elif state == "all_frozen":
            self.toggle_btn.config(text="▶ START", bg="green")
            self.main_timer_label.config(fg="white")  # Both frozen
            self.break_timer_label.config(fg="white")
        elif state == "reset":
            self.toggle_btn.config(text="▶ START", bg="green")
            self.main_timer_label.config(text="00:00:00", fg="white")  # Bỏ "Main:"
            self.break_timer_label.config(text="Break: 00:00:00", fg="white")

    def update_session_display(self, current, target):
        """Cập nhật hiển thị session"""
        self.session_label.config(text=f"Session: {current}/{target}")

    def update_progress_display(self, progress):
        """Cập nhật hiển thị tiến độ"""
        self.progress_label.config(text=f"Progress: {progress:.1f}%")

    def show_session_complete_message(self):
        """Hiển thị thông báo hoàn thành session"""
        pass  # Message will be handled by controller via choice dialog

    def show_all_sessions_complete_message(self):
        """Hiển thị thông báo hoàn thành tất cả sessions"""
        import tkinter.messagebox as msgbox
        msgbox.showinfo(
            "🎉 Congratulations! 🎉", 
            f"You completed all {self.sessions_var.get()} sessions today!\n\n"
            "🌟 Amazing work! You are a productivity champion! 🌟\n\n"
            "Take a well-deserved rest and celebrate your achievement!"
        )

    def setup_task_callbacks(self):
        """Thiết lập callbacks cho task UI"""
        self.task_ui.on_add_task = self.on_add_task
        self.task_ui.on_complete_task = self.on_complete_task
        self.task_ui.on_delete_task = self.on_delete_task
        self.task_ui.on_edit_task = self.on_edit_task
        self.task_ui.on_reactivate_task = self.on_reactivate_task  # New callback
        self.task_ui.on_clear_completed = self.on_clear_completed
        self.task_ui.play_sound = self.play_sound  # Thiết lập sound callback

    def update_task_list(self, tasks):
        """Cập nhật danh sách tasks"""
        self.task_ui.update_task_list(tasks)

    def update_completed_task_list(self, completed_tasks):
        """Cập nhật danh sách completed tasks"""
        self.task_ui.update_completed_list(completed_tasks)

    def update_task_summary(self, summary):
        """Cập nhật task summary"""
        self.task_ui.update_summary(summary)

    def show_task_complete_notification(self, task):
        """Hiển thị thông báo hoàn thành task"""
        self.task_ui.show_task_complete_notification(task)

    def get_widgets(self):
        """Trả về dictionary chứa các widget chính"""
        return {
            'main_timer_label': self.main_timer_label,
            'break_timer_label': self.break_timer_label,
            'session_label': self.session_label,
            'progress_label': self.progress_label,
            'start_btn': self.start_btn,
            'toggle_btn': self.toggle_btn,
            'reset_btn': self.reset_btn,
            'sessions_spinbox': self.sessions_spinbox,
            'auto_continue_cb': self.auto_continue_cb,
            'task_ui': self.task_ui
        }
