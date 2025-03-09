response.raise_for_status()
            latest_version = response.json().get("version")
            
            if version.parse(latest_version) > version.parse(current_version):
                return True, latest_version
            return False, current_version
        except Exception as e:
            log_activity(f"Error checking for updates: {str(e)}", level="error")
            return False, current_version

    def download_update(self, download_url):
        """Download the latest update"""
        try:
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            update_file = "update.zip"
            with open(update_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True, update_file
        except Exception as e:
            log_activity(f"Error downloading update: {str(e)}", level="error")
            return False, str(e)

    def apply_update(self, update_file):
        """Apply the downloaded update"""
        try:
            import zipfile
            with zipfile.ZipFile(update_file, 'r') as zip_ref:
                zip_ref.extractall()
            os.remove(update_file)
            return True
        except Exception as e:
            log_activity(f"Error applying update: {str(e)}", level="error")
            return False, str(e)
