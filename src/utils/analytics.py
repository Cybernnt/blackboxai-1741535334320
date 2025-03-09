if not os.path.exists(self.analytics_file):
            return {
                "start_time": datetime.now().isoformat(),
                "sessions": 0,
                "actions": {}
            }
            
        try:
            with open(self.analytics_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            log_activity(f"Error loading analytics: {str(e)}", level="error")
            return {}

    def track_action(self, action_name):
        """Track a specific action"""
        if action_name not in self.data["actions"]:
            self.data["actions"][action_name] = 0
        self.data["actions"][action_name] += 1
        self._save_data()

    def start_session(self):
        """Track a new session"""
        self.data["sessions"] += 1
        self._save_data()

    def _save_data(self):
        """Save analytics data to file"""
        try:
            with open(self.analytics_file, 'w') as f:
                json.dump(self.data, f, indent=4)
            return True
        except Exception as e:
            log_activity(f"Error saving analytics: {str(e)}", level="error")
            return False

    def get_usage_statistics(self):
        """Get usage statistics"""
        return {
            "total_sessions": self.data["sessions"],
            "most_used_action": max(self.data["actions"], key=self.data["actions"].get),
            "actions": self.data["actions"]
        }
