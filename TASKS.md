# Internship Diary Automation - Tasks & Requirements

## Project Overview

Create a Streamlit-based UI for automated diary entry generation using Gemini API. The application will accept user input for date range and diary context, calculate working days (excluding Sundays), send this information to Gemini for content generation, and then automatically fill the diary for each day.

---

## Task Breakdown

### Phase 1: UI Setup (Streamlit)

- [x] **1.1** Install and configure Streamlit
- [x] **1.2** Create main Streamlit app file (`app.py` or `diary_ui.py`)
- [x] **1.3** Design page layout with title and sections
- [x] **1.4** Add sidebar or main area for date inputs

### Phase 2: Input Components

- [x] **2.1** Create date input field for **Start Date**
- [x] **2.2** Create date input field for **End Date**
- [x] **2.3** Create text area for **Diary Context/Description**
  - Allow users to specify what the diary should be about
  - Example: "Machine Learning project, implemented neural networks, attended client meetings"
- [x] **2.4** Add input validation
  - Ensure start date <= end date
  - Ensure context is not empty
  - Show error messages if validation fails

### Phase 3: Business Logic - Date Calculation

- [x] **3.1** Create function to calculate days between start and end dates
- [x] **3.2** Implement Sunday exclusion logic
  - Filter out all Sundays from the date range
  - Return list of working dates only
- [x] **3.3** Calculate total number of working days
- [x] **3.4** Test date calculation with various ranges

### Phase 4: Gemini Integration

- [x] **4.1** Prepare data payload for Gemini API
  - Include: number of days, diary context, date range
  - Format: Clear and structured
- [x] **4.2** Send request to Gemini API via existing `gemini.py`
  - Pass: working days count, context, date information
  - Receive: AI-generated content suggestions/outline
- [x] **4.3** Handle API responses gracefully
  - Display loading indicator while waiting
  - Handle errors and timeouts
  - Show formatted response in UI

### Phase 5: UI Results Display

- [x] **5.1** Create section to display Gemini response
  - Show number of days calculated
  - Show generated content/suggestions
  - Format response for readability
- [x] **5.2** Add "Send" button below results
  - Button text: "Fill Diary" or "Generate Entries"
  - Only enable after successful Gemini response

### Phase 6: Diary Entry Generation & Submission

- [x] **6.1** Create function to generate diary entries for each working day
  - Based on Gemini's response
  - One entry per day (excluding Sundays)
  - Include date in each entry
- [x] **6.2** Integrate with VTU portal (`vtu_portal.py`)
  - Use existing portal automation functions
  - Submit entries automatically for each day
- [x] **6.3** Handle submission status
  - Show progress indicator
  - Display success/failure for each day
  - Log any submission errors
- [x] **6.4** Show completion summary
  - Total entries created
  - Total entries submitted successfully
  - Any failed entries with reasons

### Phase 7: Error Handling & Validation

- [x] **7.1** Handle network errors gracefully
- [x] **7.2** Validate all inputs before processing
- [x] **7.3** Add try-catch blocks for API calls
- [x] **7.4** Implement logging for debugging
- [x] **7.5** Display user-friendly error messages

### Phase 8: Testing & Refinement

- [x] **8.1** Test with various date ranges
- [x] **8.2** Test Sunday exclusion logic
- [x] **8.3** Test Gemini API integration
- [x] **8.4** Test portal entry submission
- [x] **8.5** Test error scenarios
- [x] **8.6** Refine UI/UX based on testing

---

## Technical Requirements

### Dependencies

```
streamlit
google-generativeai (for Gemini API)
selenium (for portal automation)
requests
```

### File Structure

```
internship-diary-automation/
├── app.py                 (Main Streamlit UI)
├── config.py              (Configuration & constants)
├── gemini.py              (Gemini API integration)
├── vtu_portal.py          (VTU portal automation)
├── diary_utils.py         (Utility functions)
└── TASKS.md               (This file)
```

### Key Functions Needed

#### `diary_utils.py`

- `calculate_working_days(start_date, end_date)` - Returns list of dates excluding Sundays
- `count_working_days(start_date, end_date)` - Returns number of working days
- `is_sunday(date)` - Check if date is Sunday

#### `app.py`

- Streamlit UI components
- Input validation
- Gemini API call orchestration
- Portal submission orchestration

#### `gemini.py` (Update existing)

- Function to generate diary content with context
- Accept: number of days, context, date range
- Return: AI-generated content/suggestions

#### `vtu_portal.py` (Update if needed)

- Function to submit multiple diary entries
- Accept: date-entry mappings
- Return: submission status

---

## User Flow

1. User opens Streamlit app
2. User selects **Start Date** and **End Date**
3. User enters **Context** (what the diary should be about)
4. User can see:
   - Total working days (excluding Sundays)
   - Specific dates that will be filled
5. App sends to Gemini: "Write diary context for {days} days about {context}"
6. Gemini returns suggestions/outline for the diary
7. App displays Gemini response
8. User clicks **"Fill Diary"** button
9. App generates entries for each working day
10. App submits entries to VTU portal day by day
11. App shows progress and completion summary

---

## Current Dependencies

- Existing: `config.py`, `gemini.py`, `vtu_portal.py`
- Need to create: Streamlit UI app
- Need to create: Utility functions

---

## Notes

- Sunday exclusion is key requirement
- Dates used: {start_date} to {end_date}, excluding all Sundays
- Gemini should be context-aware: "Create {N} unique diary entries about {context}"
- Portal submission should be automated but trackable
