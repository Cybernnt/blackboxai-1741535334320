def get(self, key, max_age=None):
        """Get cached data"""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        if not os.path.exists(cache_file):
            return None
            
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
                
                # Check if cache is expired
                if max_age is not None:
                    cache_time = datetime.fromisoformat(data["timestamp"])
                    if datetime.now() - cache_time > timedelta(seconds=max_age):
                        os.remove(cache_file)
                        return None
                        
                return data["value"]
        except Exception as e:
            log_activity(f"Error reading cache: {str(e)}", level="error")
            return None

    def set(self, key, value):
        """Set cached data"""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "value": value
                }, f)
            return True
        except Exception as e:
            log_activity(f"Error writing cache: {str(e)}", level="error")
            return False

    def clear(self, key=None):
        """Clear cached data"""
        try:
            if key is None:
                # Clear all cache
                for file in os.listdir(self.cache_dir):
                    os.remove(os.path.join(self.cache_dir, file))
            else:
                # Clear specific cache
                cache_file = os.path.join(self.cache_dir, f"{key}.json")
                if os.path.exists(cache_file):
                    os.remove(cache_file)
            return True
        except Exception as e:
            log_activity(f"Error clearing cache: {str(e)}", level="error")
            return False
