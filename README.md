If you get any errors please fix it yourself


# Internship Diary Automation

An automated diary entry system for internship tracking that generates diary content using Google's Gemini AI and submits it directly to the VTU (Visvesvaraya Technological University) internship portal.

## 🎯 Features

- **AI-Powered Diary Generation**: Automatically generates personalized diary entries using Google Gemini AI based on internship context
- **Bulk Date Handling**: Generate and submit diary entries for multiple dates in one session
- **Web UI**: User-friendly Streamlit interface for easy interaction
- **Automated VTU Portal Submission**: Directly submits entries to the VTU internship portal using Selenium WebDriver
- **Editable Entries**: Review and edit generated diary entries before submission
- **Error Handling**: Robust error handling with detailed logging for troubleshooting
- **Session Management**: Maintains session state across app reruns

## 📋 Requirements

- **Python**: 3.12.1 or higher
- **Chrome/Chromium Browser**: For automated portal submission
- **VTU Portal Account**: Valid internship credentials for the VTU portal
- **Google Gemini API Key**: For diary content generation

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd d:\PROJECTS\InternshipDiary\internship-diary-automation
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Alternatively, install packages manually:

```bash
pip install streamlit==1.28.1 google-genai==0.3.0 selenium==4.15.2 webdriver-manager==4.0.1
```

### 4. Configure Credentials

Create a `config.py` file in the project root with your VTU portal credentials and Google API key:

```python
# config.py
EMAIL = "your-vtu-email@example.com"
PASSWORD = "your-vtu-password"
GOOGLE_API_KEY = "your-google-gemini-api-key"
```

⚠️ **Important**: Never commit `config.py` to version control. Add it to `.gitignore`:

```
config.py
__pycache__/
.venv/
*.png
test_output.txt
```

## 🎮 Usage

### Start the Web Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8502`

### Using the Streamlit UI

1. **Set Date Range**: Use the sidebar to select start and end dates
2. **Enter Context**: Provide details about your internship tasks and activities
3. **Generate Entries**: Click "Generate Diary Entries" to create AI-generated content
4. **Review & Edit**: Review each generated entry and edit as needed
   - Work Summary
   - Hours Worked
   - Learnings/Outcomes
   - Skills
5. **Submit**: Click "Submit to VTU Portal" to automatically submit all entries

### Testing with Test Script

To test diary submission for a specific date without the UI:

```bash
python test_diary_entry.py
```

## 📁 Project Structure

```
internship-diary-automation/
├── app.py                   # Main Streamlit application
├── vtu_portal.py           # Selenium automation for VTU portal
├── gemini.py               # Google Gemini API integration
├── diary_utils.py          # Utility functions for date calculations
├── config.py               # Configuration (create this file)
├── test_diary_entry.py     # Test script for single entry submission
├── requirements.txt        # Python package dependencies
└── README.md              # This file
```

## 📝 File Descriptions

### `app.py`

The main Streamlit application providing the user interface for:

- Date range selection
- Context input for diary generation
- Diary entry generation and editing
- Batch submission to VTU portal

### `vtu_portal.py`

Handles all VTU portal automation:

- **`login()`**: Authenticates with the VTU portal
- **`go_to_diary_page(skip_login=False)`**: Navigates to the diary submission page
- **`fill_diary_entry(date, diary_data)`**: Two-step form filling:
  - Step 1: Select internship and date
  - Step 2: Fill form fields and submit

### `gemini.py`

Integrates with Google Gemini API:

- **`generate_diary_entries(dates, context)`**: Generates diary entries for multiple dates
- Produces structured content for work summary, learnings, and skills

### `diary_utils.py`

Utility functions:

- **`get_working_days(start_date, end_date)`**: Calculates working days excluding weekends

### `test_diary_entry.py`

Standalone test script for validating the complete workflow:

- Tests diary entry generation and submission
- Useful for debugging before running the full app

## 🔧 How It Works

### Architecture Overview

```
User Input → Gemini AI → Diary Entries → Streamlit UI → VTU Portal
                                             ↓
                                      Selenium WebDriver
```

### Two-Step VTU Form Process

**Step 1: Selection Form** (`check-diary-form`)

- Select internship (Morgan Stanley)
- Pick submission date from React Day Picker calendar
- Click Continue

**Step 2: Entry Form** (`student-diary-form`)

- Work Summary (textarea)
- Hours Worked (number input)
- Learnings/Outcomes (textarea)
- Skills (React Select dropdown)
- Submit

## ⚙️ Configuration

### VTU Portal Credentials

Edit `config.py` with your VTU portal credentials:

```python
EMAIL = "your-email@vtu.ac.in"
PASSWORD = "your-secure-password"
GOOGLE_API_KEY = "sk-proj-xxxxxxxxxxxxx"
```

### Available Internship Options

The current implementation is configured for:

- **Morgan Stanley** (ID: 7117)

To use a different internship, modify the internship selection in `vtu_portal.py`, line that sets `internship_value = '7117'`.

## 🐛 Troubleshooting

### ChromeDriver Issues

If you encounter `OSError: [WinError 193] %1 is not a valid Win32 application`:

1. Clear the webdriver cache:

   ```bash
   rmdir /s %USERPROFILE%\.wdm
   ```

2. Uninstall and reinstall Selenium:
   ```bash
   pip uninstall selenium webdriver-manager -y
   pip install selenium==4.15.2 webdriver-manager==4.0.1
   ```

### Gemini API Errors

- Ensure your Google API key is valid and has Gemini API enabled
- Check your API quota in Google Cloud Console
- Verify the key is correctly set in `config.py`

### VTU Portal Login Failures

- Verify your email and password are correct
- Check if the portal is accessible at `https://vtu.internyet.in/`
- Look for "Sign-In link not found" messages in console output
- Check network connectivity

### Skills Dropdown Issues

- The app uses fallback selectors for the React Select dropdown
- If submission fails on skills, ensure the skill exists in the portal's database
- Current default skill: "Java"

## 🔍 Debugging

### Enable Verbose Output

The app prints detailed step-by-step output to the console:

```
Step 1a: Selecting internship (Morgan Stanley)...
Step 1b: Selecting date...
Step 2a: Waiting for form to load...
[OK] Work summary filled
[SUCCESS] Diary entry for 2026-03-02 submitted successfully!
```

### Screenshots on Error

Failed submissions create error screenshots:

- `error_login.png` - Login page issues
- `error_skills.png` - Skills dropdown problems
- `error_diary_{date}.png` - Form submission errors

### Test Log Output

Run with output capture to save logs:

```bash
python test_diary_entry.py > test_output.txt 2>&1
```

## 📊 Supported Dates

- **Current Date**: March 24, 2026
- The app supports any date within the VTU portal's allowed range
- Working days calculation excludes weekends automatically

## 🔐 Security Notes

- ⚠️ **Never commit** `config.py` with credentials to version control
- Use environment variables for sensitive information in production
- The app stores passwords in memory only during the session
- Credentials are not logged or saved to disk

## 🤝 Dependencies

| Package           | Version | Purpose                 |
| ----------------- | ------- | ----------------------- |
| streamlit         | 1.28.1  | Web UI framework        |
| google-genai      | 0.3.0   | Gemini API client       |
| selenium          | 4.15.2  | Browser automation      |
| webdriver-manager | 4.0.1   | ChromeDriver management |

## 📝 Example Workflow

1. **Start App**:

   ```bash
   streamlit run app.py
   ```

2. **Set Dates**: March 3-7, 2026

3. **Enter Context**: "Worked on data transformation and dashboard creation"

4. **Generate**: Click "Generate Diary Entries" (generates for 5 working days)

5. **Review**: Check and edit each entry as needed

6. **Submit**: Click "Submit to VTU Portal" to submit all 5 entries

7. **Verify**: Check the VTU portal to confirm entries are submitted

## ✅ Success Indicators

After successful submission, you should see:

- ✅ "Successfully submitted for YYYY-MM-DD" message for each entry
- ✅ Screenshots saved: `form_page.png`, `submission_result.png`
- ✅ VTU portal shows submitted entries
- ✅ Application continues without crashes

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review console output for detailed error messages
3. Enable screenshot capture to diagnose UI issues
4. Verify all configuration values in `config.py`
5. Test with `test_diary_entry.py` for isolated testing

## 📄 License

This project is provided as-is for educational and personal internship tracking purposes.

---

**Last Updated**: March 24, 2026
**Python Version**: 3.12.1
**Status**: ✅ Fully Functional
