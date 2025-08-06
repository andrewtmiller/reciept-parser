import subprocess

def get_firefox_current_tab_url():
    try:
        script = """
        tell application "Firefox"
            get URL of current tab of front window
        end tell
        """
        process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output)
        if error:
            print(f"Error: {error.decode('utf-8').strip()}")
            return None
        return output.decode('utf-8').strip()
    except Exception as e:
        return None

current_tab_url = get_firefox_current_tab_url()
if current_tab_url:
    print(f"Current Firefox tab URL: {current_tab_url}")
else:
    print("Could not retrieve the current Firefox tab URL.")