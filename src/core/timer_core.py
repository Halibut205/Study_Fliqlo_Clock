"""
Timer Core Module - Dual Clock System (Main + Break)
"""

class TimerCore:
    def __init__(self):
        # Dual clock system
        self.main_running = False
        self.break_running = False
        self.main_time = 0  # Main timer elapsed time
        self.break_time = 0  # Break timer elapsed time
        
        # Session management
        self.current_session = 0
        self.target_sessions = 8
        self.session_duration = 3600  # 1 hour = 3600 seconds
        self.break_duration = 300  # 5 minutes = 300 seconds
        self.auto_continue = False
        self.last_session_check = 0  # Track last session completion time
        
        # State management
        self.session_completed = False
        self.all_sessions_completed = False
        self.waiting_for_user_choice = False
        
        # Callbacks để update UI
        self.on_main_timer_update = None
        self.on_break_timer_update = None
        self.on_state_change = None
        self.on_session_update = None
        self.on_session_complete = None
        self.on_all_sessions_complete = None
        self.on_choice_required = None  # New callback for user choice

    def format_time(self, seconds):
        """Format thời gian thành HH:MM:SS"""
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hrs:02}:{mins:02}:{secs:02}"

    def start_main_timer(self):
        """Bắt đầu main timer, freeze break timer"""
        if not self.waiting_for_user_choice:
            self.main_running = True
            self.break_running = False
            self.waiting_for_user_choice = False
            if self.on_state_change:
                self.on_state_change("main_running")

    def start_break_timer(self):
        """Bắt đầu break timer, freeze main timer"""
        if not self.waiting_for_user_choice:
            self.main_running = False
            self.break_running = True
            self.waiting_for_user_choice = False
            if self.on_state_change:
                self.on_state_change("break_running")

    def pause_main_start_break(self):
        """Pause main timer và start break timer"""
        self.main_running = False
        self.break_running = True
        if self.on_state_change:
            self.on_state_change("break_running")

    def pause_break_start_main(self):
        """Pause break timer và resume main timer"""
        self.break_running = False
        self.main_running = True
        if self.on_state_change:
            self.on_state_change("main_running")

    def freeze_all(self):
        """Freeze cả hai đồng hồ"""
        self.main_running = False
        self.break_running = False
        if self.on_state_change:
            self.on_state_change("all_frozen")

    def reset_timers(self):
        """Reset cả hai timer về 0"""
        self.main_running = False
        self.break_running = False
        self.main_time = 0
        self.break_time = 0
        self.current_session = 0
        self.last_session_check = 0  # Reset session check
        self.session_completed = False
        self.all_sessions_completed = False
        self.waiting_for_user_choice = False
        if self.on_state_change:
            self.on_state_change("reset")

    def tick(self):
        """Update timers mỗi giây"""
        # Update main timer
        if self.main_running:
            self.main_time += 1
            if self.on_main_timer_update:
                self.on_main_timer_update(self.format_time(self.main_time))
            
            # Check session completion - mỗi session_duration giây
            if self.main_time > 0 and self.main_time % self.session_duration == 0:
                if self.main_time > self.last_session_check:
                    self.last_session_check = self.main_time
                    self._handle_session_complete()
        
        # Update break timer
        if self.break_running:
            self.break_time += 1
            if self.on_break_timer_update:
                self.on_break_timer_update(self.format_time(self.break_time))

    def _handle_session_complete(self):
        """Xử lý khi hoàn thành một session"""
        self.current_session += 1
        # KHÔNG reset main timer - để tiếp tục chạy từ thời gian hiện tại
        self.session_completed = True
        
        # Freeze cả hai đồng hồ
        self.freeze_all()
        self.waiting_for_user_choice = True
        
        # Cập nhật session display
        if self.on_session_update:
            self.on_session_update(self.current_session, self.target_sessions)
        
        # Check if all sessions completed
        if self.current_session >= self.target_sessions:
            self.all_sessions_completed = True
            if self.on_all_sessions_complete:
                self.on_all_sessions_complete()
        else:
            # Play completion sound và show choice dialog
            if self.on_session_complete:
                self.on_session_complete()
            if self.on_choice_required:
                self.on_choice_required()

    def choose_continue_session(self):
        """User chọn tiếp tục session tiếp theo"""
        if self.waiting_for_user_choice and not self.all_sessions_completed:
            self.session_completed = False
            self.waiting_for_user_choice = False
            self.start_main_timer()

    def choose_take_break(self):
        """User chọn nghỉ break"""
        if self.waiting_for_user_choice and not self.all_sessions_completed:
            self.session_completed = False
            self.waiting_for_user_choice = False
            self.start_break_timer()

    # Getters for UI
    def get_main_time_text(self):
        return self.format_time(self.main_time)
    
    def get_break_time_text(self):
        return self.format_time(self.break_time)
    
    def is_main_running(self):
        return self.main_running
    
    def is_break_running(self):
        return self.break_running
    
    def is_waiting_for_choice(self):
        return self.waiting_for_user_choice

    # Session management
    def set_target_sessions(self, sessions):
        self.target_sessions = sessions

    def set_session_duration(self, duration):
        self.session_duration = duration

    def set_auto_continue(self, auto_continue):
        self.auto_continue = auto_continue

    def reset_sessions(self):
        self.current_session = 0
        if self.on_session_update:
            self.on_session_update(self.current_session, self.target_sessions)

    def get_session_progress(self):
        """Lấy tiến độ của session hiện tại (0-100%)"""
        if self.session_duration <= 0:
            return 0
        # Tính progress của session hiện tại
        current_session_time = self.main_time % self.session_duration
        return min(current_session_time / self.session_duration * 100, 100)

    def get_state(self):
        """Lấy trạng thái hiện tại của timer"""
        return {
            'main_running': self.main_running,
            'break_running': self.break_running,
            'main_time': self.main_time,
            'break_time': self.break_time,
            'formatted_main_time': self.format_time(self.main_time),
            'formatted_break_time': self.format_time(self.break_time),
            'current_session': self.current_session,
            'target_sessions': self.target_sessions,
            'session_progress': self.get_session_progress(),
            'waiting_for_choice': self.waiting_for_user_choice,
            'all_sessions_completed': self.all_sessions_completed
        }

