# File: shutdown.py
import os

def schedule_shutdown(minutes):
    os.system(f"shutdown -s -t {minutes * 60}")  # Schedule shutdown after specified minutes

def cancel_shutdown():
    os.system("shutdown -a")  # Cancel scheduled shutdown

# File: main.py
import tkinter as tk
from shutdown import schedule_shutdown, cancel_shutdown

def count_down(label, time_sec):
    if count_down.running:
        mins, secs = divmod(time_sec, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        label.config(text=time_format)
        if time_sec > 0:
            label.after(1000, count_down, label, time_sec - 1)
        else:
            label.config(text="Timer ended")

def shutdown_window():
    new_window = tk.Toplevel(root)
    new_window.title("Schedule Shutdown")
    new_window.geometry("450x450")
    new_window.resizable(False, False)

    label = tk.Label(new_window, text="Shutdown after (mins):")
    label.pack(pady=20)

    # Validate function to ensure numeric input
    def validate_input(P):
        if P.isdigit() or P == "":
            return True
        return False

    validate_command = new_window.register(validate_input)

    # Add an entry widget for user input with validation
    entry = tk.Entry(new_window, validate="key", validatecommand=(validate_command, '%P'))
    entry.pack(pady=10)

    # Add a label to display warnings
    warning_label = tk.Label(new_window, text="", fg="red")
    warning_label.pack(pady=5)

    # Add a label to display the timer
    timer_label = tk.Label(new_window, text="00:00")
    timer_label.pack(pady=10)

    # Add a label to display cancel notification
    cancel_label = tk.Label(new_window, text="", fg="red")
    cancel_label.pack(pady=5)

    # Define a function to process the input
    def process_input():
        user_input = entry.get()
        if user_input == "":
            warning_label.config(text="Please enter a time in minutes.")
        else:
            try:
                minutes = int(user_input)
                schedule_shutdown(minutes)
                count_down.running = True
                count_down(timer_label, minutes * 60)
                warning_label.config(text="")  # Clear any previous warning
            except ValueError:
                warning_label.config(text="Please enter a valid number")


    # Add a button to process the input
    process_button = tk.Button(new_window, text="Submit", command=process_input)
    process_button.pack(pady=10)

    # Define a function to cancel the shutdown and stop the timer
    def cancel_timer():
        count_down.running = False
        cancel_shutdown()
        cancel_label.config(text="Shutdown canceled!")
        # Clear the notification after 100 milliseconds (0.1 second)
        new_window.after(500, lambda: cancel_label.config(text=""))

    # Add a cancel button
    cancel_button = tk.Button(new_window, text="Cancel Shutdown", command=cancel_timer)
    cancel_button.pack(pady=10)

root = tk.Tk()
root.title("Shutdown Scheduler")
root.iconbitmap("Icon.ico")
root.geometry("450x450")
root.resizable(False, False)

# Create a text label
text_label = tk.Label(root, text="Please choose an option:")
text_label.pack(pady=20)

# Create the "Schedule Shutdown" button
schedule_button = tk.Button(root, text="Schedule Shutdown", command=shutdown_window)
schedule_button.pack(pady=10)

# Create the "Cancel Shutdown" button
cancel_button = tk.Button(root, text="Cancel Shutdown", command=cancel_shutdown)
cancel_button.pack(pady=10)

# Run the application
root.mainloop()
