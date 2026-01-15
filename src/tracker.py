import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import traceback
import pytz

class UsageTracker:
    def __init__(self):
        self.client = None
        self.sheet = None
        self.is_active = False
        
        try:
            # Check if secrets are available
            if "gcp_service_account" in st.secrets:
                # Create credentials object from secrets
                scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                creds_dict = dict(st.secrets["gcp_service_account"])
                
                # Fix private key formatting if needed (replace \n with actual newlines)
                if "private_key" in creds_dict:
                    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
                
                creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
                self.client = gspread.authorize(creds)
                
                # Open the spreadsheet
                # We assume the sheet name is 'NotebookLM_Usage_Log' as per instructions
                try:
                    self.sheet = self.client.open("NotebookLM_Usage_Log").sheet1
                    self.is_active = True
                    print("UsageTracker: Connected to Google Sheets successfully.")
                except gspread.SpreadsheetNotFound:
                    print("UsageTracker Error: Spreadsheet 'NotebookLM_Usage_Log' not found.")
                    st.warning("⚠️ Usage Tracker Error: Could not find Google Sheet 'NotebookLM_Usage_Log'. Please check the name and permissions.")
            else:
                print("UsageTracker: No secrets found. Tracking disabled.")
                
        except Exception as e:
            print(f"UsageTracker Initialization Error: {e}")
            # traceback.print_exc()

    def log_action(self, user_name, action, filename, details=""):
        """
        Logs an action to the Google Sheet.
        Columns: Time, User, Action, File Name, Details
        """
        if not self.is_active or not self.sheet:
            return

        try:
            # Get current time in UTC
            utc_now = datetime.now(pytz.utc)
            # Convert to Taiwan time (Asia/Taipei)
            tw_tz = pytz.timezone('Asia/Taipei')
            tw_now = utc_now.astimezone(tw_tz)
            
            timestamp = tw_now.strftime("%Y-%m-%d %H:%M:%S")
            row = [timestamp, user_name, action, filename, details]
            self.sheet.append_row(row)
            print(f"UsageTracker: Logged action - {action} by {user_name}")
        except Exception as e:
            print(f"UsageTracker Logging Error: {e}")
