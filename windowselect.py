import subprocess

def focus_window(name: str):
    # Find the window ID of the target window using xdotool
    window_ids = subprocess.check_output(['xdotool', 'search', '--name', name]).decode('utf-8').strip().split('\n')
    id_ranges = []
    for i in range(int(len(window_ids)/2)):
        id_ranges.append((int(window_ids[2*i].strip()), int(window_ids[2*i+1].strip())))

    for s, e in id_ranges:
        for window_id in range(s, e+1):
            try:
                result = subprocess.check_output(['xdotool', 'windowactivate', str(window_id)], stderr=subprocess.STDOUT, universal_newlines=True)
                if result.strip() == '':
                    break
            except subprocess.CalledProcessError:
                pass
