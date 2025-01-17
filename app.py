import streamlit as st
import subprocess

# Streamlit form for inputs
st.title("LinkedIn Job Scrapper")

with st.form("scrapper_form"):
    title = st.text_input("Job Title", value="backend developer")
    location =st.text_input("Job Location", value="newyork")
    data_name = st.text_input("Output File Name", value="backend_jobs")
    
    submit_button = st.form_submit_button("Run Scrapper")

if submit_button:
    
    # Run the scrapping script with the form inputs
    command = f"""poetry run python -m linkedin-scrapper --title "{title}" --location "{location}" --data_name "{data_name}" """
    
    with st.spinner("Crawling in progress..."):
        # Execute the command and display the results
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        st.write("Script Output:")
        st.text(result.stdout)
        
        if result.returncode == 0:
            st.success(f"Data successfully saved in {data_name}.csv")
        else:
            st.error(f"Error: {result.stderr}")