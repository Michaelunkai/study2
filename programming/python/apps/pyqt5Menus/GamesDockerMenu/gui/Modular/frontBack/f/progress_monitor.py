import os
import re
import time
import threading
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class RsyncProgressMonitor(QObject):
    """
    Monitor and parse rsync progress information.
    Emits signals with progress information that can be connected to UI components.
    """
    # Define signals
    progress_update = pyqtSignal(dict)
    sync_completed = pyqtSignal(bool, str)  # Success flag, Message
    
    def __init__(self, backend, tag, parent=None):
        """
        Initialize the progress monitor
        
        Args:
            backend: The backend module containing Docker/rsync functions
            tag: The Docker container tag being monitored
            parent: Parent QObject
        """
        super().__init__(parent)
        self.backend = backend
        self.tag = tag
        self.is_running = False
        self.current_stats = {
            'percent': 0,
            'speed': '0 B/s',
            'size_transferred': '0 B',
            'total_size': 'Unknown',
            'time_left': 'calculating...',
            'elapsed': '0:00:00',
            'status': 'Starting...',
            'last_update': time.time()
        }
        
        # Internal state
        self._start_time = None
        self._process = None
        self._monitor_thread = None
        self._timer = None
    
    def _parse_rsync_output(self, line):
        """Parse a line of rsync output for progress information"""
        if not line or not isinstance(line, str):
            return
            
        # Check if this is a progress line
        if re.search(r'\d+%', line):
            # Extract percentage
            percent_match = re.search(r'(\d+)%', line)
            if percent_match:
                self.current_stats['percent'] = int(percent_match.group(1))
            
            # Extract speed
            speed_match = re.search(r'(\d+\.?\d*\s+\w+/s)', line)
            if speed_match:
                self.current_stats['speed'] = speed_match.group(1)
                
            # Extract transferred size and total size
            size_match = re.search(r'(\d+\.?\d*\s+\w+)\s+/\s+(\d+\.?\d*\s+\w+)', line)
            if size_match:
                self.current_stats['size_transferred'] = size_match.group(1)
                self.current_stats['total_size'] = size_match.group(2)
            
            # Extract time left
            time_left_match = re.search(r'(\d+:\d+:\d+)\s+\(.*\)', line)
            if time_left_match:
                self.current_stats['time_left'] = time_left_match.group(1)
                
            # Calculate elapsed time
            if self._start_time:
                elapsed_seconds = int(time.time() - self._start_time)
                hours, remainder = divmod(elapsed_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.current_stats['elapsed'] = f"{hours}:{minutes:02d}:{seconds:02d}"
                
            # Update last update time
            self.current_stats['last_update'] = time.time()
                
            # Send progress update
            self.progress_update.emit(dict(self.current_stats))
            
        # Check for completion or errors
        elif "speedup is" in line or "done" in line.lower():
            self.current_stats['status'] = 'Completed'
            self.current_stats['percent'] = 100
            self.progress_update.emit(dict(self.current_stats))
            
    def _check_activity(self):
        """Check if rsync is still active and making progress"""
        # If more than 60 seconds with no update, consider it potentially stuck
        if time.time() - self.current_stats['last_update'] > 60:
            # Check if the rsync process is still running
            if not self.backend.check_rsync_status(self.tag):
                self.is_running = False
                self._timer.stop()
                
                # Check if we successfully transferred files
                if self.current_stats['percent'] > 0:
                    self.sync_completed.emit(True, f"Sync completed: {self.current_stats['size_transferred']} transferred")
                else:
                    self.sync_completed.emit(False, "Sync may have failed or container exited")
                    
    def handle_log_line(self, line):
        """Process a log line from Docker container"""
        if not self.is_running:
            return
            
        self._parse_rsync_output(line)
    
    def start_monitoring(self):
        """Start monitoring rsync progress"""
        self.is_running = True
        self._start_time = time.time()
        self.current_stats['last_update'] = time.time()
        
        # Start the docker process
        self._process, self._monitor_thread = self.backend.run_docker_command(
            self.tag,
            os.path.join(os.path.expanduser("~"), "Games"),  # Default path
            self.handle_log_line
        )
        
        # Set up a timer to periodically check activity
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._check_activity)
        self._timer.start(5000)  # Check every 5 seconds
        
        return self._process is not None
    
    def cancel(self):
        """Cancel the ongoing sync"""
        if self.is_running:
            self.is_running = False
            if self._timer:
                self._timer.stop()
            success = self.backend.cancel_docker_sync(self.tag)
            self.sync_completed.emit(False, "Sync canceled by user" if success else "Failed to cancel sync")
            return success
        return False
