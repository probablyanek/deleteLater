import streamlit as st
import schedule
import time
import threading
from datetime import datetime, timedelta
import plotly.graph_objs as go
from KNN.predict import danger

# Mocking the predict.danger function (replace this with your actual implementation)
def predict_danger(nosPreg, glucose, bp, bmi, age):
    # Simple example: If glucose is higher than 180, it's considered dangerous
    if glucose > 180:
        return "Danger: High glucose level!"
    else:
        return "Glucose level is normal."

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

if 'glucose_levels' not in st.session_state:
    st.session_state['glucose_levels'] = []
if 'timestamps' not in st.session_state:
    st.session_state['timestamps'] = []

# Left sidebar inputs for additional user data
st.sidebar.header("User Inputs")
nosPreg = st.sidebar.number_input("Enter number of times pregnant:", min_value=0, value=0, step=1)
bp = st.sidebar.number_input("Enter blood pressure:", min_value=0, max_value=300, value=120, step=1)
bmi = st.sidebar.number_input("Enter BMI:", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
age = st.sidebar.number_input("Enter age:", min_value=0, value=30, step=1)
email = st.sidebar.text_input("Enter emergency contact email:", value="me@anek.lol")
# Prompt user for reminder interval in seconds
interval = st.sidebar.number_input("Enter reminder interval (in seconds)", min_value=1, value=30, step=1)

# Create a two-column layout (making the right column wider for the graph)
col1, col2 = st.columns([2, 3])

# Left column (Main content)
with col1:
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
            
            # Store glucose level and timestamp
            st.session_state['glucose_levels'].append(glucose_level)
            st.session_state['timestamps'].append(datetime.now().strftime("%H:%M:%S"))
            
            # Call the predict.danger function with the inputs
            result = danger(nosPreg, glucose_level, bp, bmi, age, email)
            st.write(f"Prediction: {result}")
            
            # Reset the countdown state and start the timer again
            st.session_state['countdown_complete'] = False
            countdown_timer(interval)  # Restart countdown with same interval

# Right column (Plot)
with col2:
    if st.session_state['glucose_levels']:
        st.write("Glucose Level Over Time")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=st.session_state['timestamps'], y=st.session_state['glucose_levels'], mode='lines+markers', name='Glucose Level'))
        
        # Customize layout
        fig.update_layout(
            title='Real-Time Glucose Level Monitoring',
            xaxis_title='Time',
            yaxis_title='Glucose Level',
            xaxis=dict(showline=True, showgrid=False),
            yaxis=dict(showline=True, showgrid=False),
            autosize=True
        )
        
        # Display the plot in the right-hand side with more width
        st.plotly_chart(fig, use_container_width=True)
