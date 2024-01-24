import pygetwindow as gw

def open_runelite_client_function():
    try:
        window_title = "RuneLite - Dukadelmin"
        windows = gw.getWindowsWithTitle(window_title)

        if windows:
            window = windows[0]
            if window.isActive:
                print(f"Window '{window_title}' is already active.")
            else:
                window.maximize()
                window.activate()
                print(f"Window '{window_title}' maximized and activated.")
        else:
            print(f"Window '{window_title}' not found.")

        return "Window operation completed successfully."

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error: {e}"

open_runelite_client_function()