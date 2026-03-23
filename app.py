import streamlit as st
from datetime import date
from diary_utils import get_working_days
from gemini import generate_diary_entries
from vtu_portal import VTUPortal
import time

st.title("Internship Diary Automation")

st.sidebar.header("User Inputs")

start_date = st.sidebar.date_input("Start Date", date.today())
end_date = st.sidebar.date_input("End Date", date.today())

diary_context = st.sidebar.text_area("Diary Context/Description", "Enter the details of the internship tasks and activities here.")

if start_date > end_date:
    st.error("Error: End date must be after start date.")
else:
    working_days = get_working_days(start_date, end_date)
    num_working_days = len(working_days)
    st.write("## Diary Details")
    st.write(f"**Number of working days:** {num_working_days}")
    
    # Store working days in session state to access them across reruns
    st.session_state.working_days = working_days

    if 'diary_entries' not in st.session_state:
        st.session_state.diary_entries = {}
    
    if 'edited_entries' not in st.session_state:
        st.session_state.edited_entries = {}

    if st.button("Generate Diary Entries"):
        with st.spinner("Generating diary entries..."):
            # Generate all entries in a single API call
            st.session_state.diary_entries = generate_diary_entries(st.session_state.working_days, diary_context)
    
    if st.session_state.diary_entries:
        st.write("## Generated Diary Entries")
        
        # Create editable entries
        st.session_state.edited_entries = {}
        
        for day, entry in st.session_state.diary_entries.items():
            with st.expander(f"Diary Entry for {day.strftime('%Y-%m-%d')}"):
                date_key = day.strftime('%Y-%m-%d')
                
                # Work Summary
                work_summary = st.text_area(
                    "Work Summary",
                    value=entry["work_summary"],
                    key=f"work_summary_{date_key}",
                    height=100
                )
                
                # Learnings/Outcomes
                learnings = st.text_area(
                    "Learnings/Outcomes",
                    value=entry["learnings_outcomes"],
                    key=f"learnings_{date_key}",
                    height=100
                )
                
                # Skills - make it editable
                skills = st.text_input(
                    "Skills",
                    value=entry.get("skills", "Java"),
                    key=f"skills_{date_key}"
                )
                
                # Hours Worked - make it editable
                hours_worked = st.selectbox(
                    "Hours Worked",
                    options=["4", "6", "8", "10"],
                    index=2 if entry.get("hours_worked", "8") == "8" else ["4", "6", "8", "10"].index(entry.get("hours_worked", "8")),
                    key=f"hours_{date_key}"
                )
                
                # Store edited entry
                st.session_state.edited_entries[day] = {
                    "work_summary": work_summary,
                    "learnings_outcomes": learnings,
                    "skills": skills,
                    "hours_worked": hours_worked
                }

    if st.session_state.diary_entries and st.button("Submit to VTU Portal"):
        submitted_entries = []
        failed_entries = []
        
        st.info(f"Submitting {len(st.session_state.diary_entries)} diary entries...")
        
        portal = VTUPortal()
        
        try:
            portal.login()
            
            # Use edited entries if available, otherwise use original
            entries_to_submit = st.session_state.edited_entries if 'edited_entries' in st.session_state else st.session_state.diary_entries
            
            for day, entry in entries_to_submit.items():
                try:
                    st.write(f"Processing {day.strftime('%Y-%m-%d')}...")
                    
                    # Navigate to diary page for each entry
                    portal.go_to_diary_page(skip_login=True)
                    
                    # Fill and submit the entry
                    portal.fill_diary_entry(day, entry)
                    
                    st.success(f"Successfully submitted for {day.strftime('%Y-%m-%d')}")
                    submitted_entries.append(day.strftime('%Y-%m-%d'))
                    
                    # Wait before next entry
                    time.sleep(2)
                    
                except Exception as entry_error:
                    st.error(f"Failed to submit {day.strftime('%Y-%m-%d')}: {entry_error}")
                    failed_entries.append((day.strftime('%Y-%m-%d'), str(entry_error)))
                    # Continue to next entry instead of stopping
                    continue
                    
        except Exception as e:
            st.error(f"An error occurred during portal interaction: {e}")
            import traceback
            st.text(traceback.format_exc())
        finally:
            portal.close()
        
        # Show final summary
        st.write("---")
        if submitted_entries:
            st.success(f"Submitted {len(submitted_entries)} diary entries successfully!")
        if failed_entries:
            st.warning(f"Failed to submit {len(failed_entries)} entries:")
            for date_str, error in failed_entries:
                st.write(f"  - {date_str}: {error}")

