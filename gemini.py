from google import genai
from config import GEMINI_API_KEY
import json
import time

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_diary_entries(dates, diary_context):
    """
    Generates diary entries for multiple dates in a single API call.
    """
    dates_str = ", ".join([d.strftime('%Y-%m-%d') for d in dates])
    
    prompt = f"""
You are an expert programmer helping an intern generate their daily diary entries.
Based on the following project context, generate brief work summaries and learnings for internship diary entries for these dates: {dates_str}.

**Project Context:**
{diary_context}

**Instructions:**
For each date, create a JSON object with:
1. **Work Summary:** ONE specific task in 1-2 sentences. Mention specific technologies (Java, Spring Boot, MapStruct, JUnit 5, Mockito).
2. **Learnings/Outcomes:** What was learned in 1-2 sentences.

**Output Format:**
Return a JSON object where each key is a date (YYYY-MM-DD) and the value is an object with "work_summary" and "learnings_outcomes". Do not include any other text or formatting.

Example:
{{
    "2026-03-02": {{
        "work_summary": "Implemented custom MapStruct mappers to handle complex nested objects and non-standard date formats from legacy systems, adding unit tests with JUnit 5 and Mockito.",
        "learnings_outcomes": "Gained expertise in advanced MapStruct features and learned best practices for data-driven unit testing."
    }},
    "2026-03-03": {{
        "work_summary": "Conducted integration testing of the Data Transformation Adapter by simulating diverse payloads from multiple legacy Business Units.",
        "learnings_outcomes": "Learned how to apply defensive programming principles and handle edge cases in data pipelines."
    }}
}}
"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )
            cleaned_text = response.text.strip().replace('```json', '').replace('```', '')
            entries_data = json.loads(cleaned_text)
            
            result = {}
            for date in dates:
                date_str = date.strftime('%Y-%m-%d')
                if date_str in entries_data:
                    entry = entries_data[date_str]
                    result[date] = {
                        "work_summary": entry.get("work_summary", "Worked on data transformation and testing."),
                        "learnings_outcomes": entry.get("learnings_outcomes", "Improved proficiency with testing frameworks."),
                        "skills": "Java",
                        "hours_worked": "8"
                    }
                else:
                    # Fallback for missing dates
                    result[date] = {
                        "work_summary": "Conducted development and testing on the transformation pipeline.",
                        "learnings_outcomes": "Reinforced understanding of enterprise data migration patterns.",
                        "skills": "Java",
                        "hours_worked": "8"
                    }
            return result
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing Gemini response: {e}")
            # Return fallback entries for all dates
            result = {}
            for date in dates:
                result[date] = {
                    "work_summary": "Worked on data transformation and testing using Spring Boot and MapStruct.",
                    "learnings_outcomes": "Improved proficiency with testing frameworks and data mapping techniques.",
                    "skills": "Java",
                    "hours_worked": "8"
                }
            return result
            
        except Exception as e:
            error_str = str(e)
            # Check if it's a rate limit error
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count  # Exponential backoff
                    print(f"Rate limit hit. Retrying in {wait_time} seconds... (attempt {retry_count}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    # If all retries exhausted, use fallback
                    print(f"Max retries exceeded. Using fallback.")
                    result = {}
                    for date in dates:
                        result[date] = {
                            "work_summary": "Conducted testing and code review on the transformation pipeline.",
                            "learnings_outcomes": "Reinforced understanding of test-driven development and code quality practices.",
                            "skills": "Java",
                            "hours_worked": "8"
                        }
                    return result
            else:
                print(f"API Error: {type(e).__name__}: {e}")
                result = {}
                for date in dates:
                    result[date] = {
                        "work_summary": "Worked on development tasks for the transformation adapter.",
                        "learnings_outcomes": "Gained practical experience with enterprise data migration patterns.",
                        "skills": "Java",
                        "hours_worked": "8"
                    }
                return result
