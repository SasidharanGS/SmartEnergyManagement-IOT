import streamlit as st

def display_project_explanation():
    # Your content for explaining the IoT project goes here
    st.header("Smart Computer Lab")
    st.write("Computer labs are enclosed, air-conditioned spaces equipped with a variety of electronic devices. The amount of energy required for these devices is dependent on the number of people using the lab at any given time. Additionally, the air-conditioning unit in the lab is responsible for regulating the temperature as well as maintaining a steady flow of fresh air. This is necessary to ensure that the air quality remains healthy and balanced, particularly since oxygen depletes and carbon dioxide accumulates when people are in enclosed spaces for extended periods of time.")
    st.write("### Overview of our Project")
    image_path = "img1.jpeg"  
    image = open(image_path, "rb").read()
    st.image(image, caption='Data Flow Architecture', use_column_width=True)
    st.write("Our proposed solution involves leveraging IoT technology to track the number of people and electricity consumption in the computing facilities. Although measuring electricity consumption is straightforward, measuring it at a granular level can be costly. Therefore, we suggest deriving a probabilistic estimate of electricity consumption by measuring it for a few rows and extrapolating the usage patterns across all rows using data collected over a significant period. Measuring carbon dioxide levels accurately can be challenging due to external factors such as open doors, windows, and human breathing. To overcome this, we use PIR(Passive Infra-red) sensors to count the number of people inside the lab by keeping track of people entering and leaving the facility. This approach will give us a better idea of CO2 levels and enable us to automate airflow regulation, ensuring safety and reducing energy waste.")