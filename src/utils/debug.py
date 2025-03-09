import traceback
from PyQt6.QtWidgets import QMessageBox
from src.utils.logger import log_activity

class DebugHelper:
    @staticmethod
    def handle_exception(exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions"""
        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        log_activity(f"Unhandled exception: {error_msg}", level="critical")
        
        # Show error message to user
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("An unexpected error occurred")
        msg.setInformativeText(str(exc_value))
        msg.setWindowTitle("Error")
        msg.setDetailedText(error_msg)
        msg.exec()

    @staticmethod
    def enable_debug_mode():
        """Enable debug mode with additional logging"""
        import sys
        sys.excepthook = DebugHelper.handle_exception
        log_activity("Debug mode enabled", level="info")

    @staticmethod
    def log_memory_usage():
        """Log current memory usage"""
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        log_activity(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")

    @staticmethod
    def log_system_info():
        """Log system information"""
        import platform
        system_info = {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        }
        log_activity(f"System info: {system_info}")
