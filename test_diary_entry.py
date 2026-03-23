from vtu_portal import VTUPortal
from datetime import date

# Test data for March 2, 2026
test_date = date(2026, 3, 2)
test_data = {
    "work_summary": "Presented an end-to-end data transformation demo to the team, successfully showcasing the migration flow for a complex BU.",
    "learnings_outcomes": "Improved the ability to communicate technical workflows and architectural decisions to project stakeholders.",
    "skills": "Java",
    "hours_worked": "8"
}

if __name__ == '__main__':
    print(f"Starting test for diary entry on {test_date.strftime('%Y-%m-%d')}")
    print(f"Data: {test_data}")
    print()
    
    portal = VTUPortal()
    try:
        print("Logging in and navigating to diary page...")
        portal.go_to_diary_page()
        
        print(f"Filling diary entry for {test_date.strftime('%Y-%m-%d')}...")
        portal.fill_diary_entry(test_date, test_data)
        
        print("Test completed successfully!")
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Closing browser...")
        portal.close()
