import streamlit as st
import schedule
import time
import threading
from datetime import datetime, timedelta

# Function to send a reminder
def send_reminder():
    st.write("Reminder: Time to check your sugar level!")

# Function to handle scheduling of reminders in seconds
def schedule_reminders(interval):
    schedule.clear()  # Clear any previous schedules
    schedule.every(interval).seconds.do(send_reminder)

    # Run the scheduler in the background
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Start the thread
    threading.Thread(target=run_scheduler, daemon=True).start()

# Function to handle dynamic countdown in seconds
def countdown_timer(seconds):
    end_time = datetime.now() + timedelta(seconds=seconds)
    countdown_placeholder = st.empty()  # Placeholder to update dynamically
    while True:
        remaining_time = end_time - datetime.now()
        if remaining_time.total_seconds() <= 0:
            countdown_placeholder.text("Time for your next check!")
            st.session_state['countdown_complete'] = True  # Set state when countdown completes
            break
        mins, secs = divmod(remaining_time.total_seconds(), 60)
        time_str = f"{int(mins):02d}:{int(secs):02d}"
        countdown_placeholder.markdown(f"<h1 style='color:#C1E1C1; text-align:center; font-size:72px;'>{time_str}</h1>", unsafe_allow_html=True)
        time.sleep(1)  # Sleep for 1 second to update countdown

# Streamlit App UI
st.title("Insulin Shot Reminder")

# Initialize session state to track countdown completion and reminders
if 'countdown_complete' not in st.session_state:
    st.session_state['countdown_complete'] = False

# Prompt user for reminder interval in seconds
interval = st.number_input("Enter reminder interval (in seconds)", min_value=1, value=30, step=1)

if st.button("Start Reminder") and not st.session_state['countdown_complete']:
    st.write(f"Reminder set to notify every {interval} seconds.")
    # Start the countdown
    countdown_timer(interval)  # Start countdown for the first interval

# After countdown, prompt user for glucose input
if st.session_state['countdown_complete']:
    st.write("Please enter your current glucose level:")
    glucose_level = st.number_input("Glucose Level", min_value=0, max_value=1000, step=1)
    if st.button("Submit Glucose Level"):
        st.write(f"Your entered glucose level is: {glucose_level}")
        # Reset the countdown state and start the timer again
        st.session_state['countdown_complete'] = False
        countdown_timer(interval)  # Restart countdown with same interval
