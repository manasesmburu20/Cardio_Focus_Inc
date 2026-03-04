import sys
from datetime import datetime
from ui_automation import run_ui_test
from api_automation import run_api_test
from config import Config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import glob
import os

class IntegratedTestRunner:
    def __init__(self, demo_mode=False):
        self.all_results = []
        self.start_time = None
        self.end_time = None
        self.demo_mode = demo_mode
        
    def run_tests(self, device_id, expected_status, run_ui=True, run_api=True):
        """Run both UI and API tests"""
        self.start_time = datetime.now()
        
        print("\n" + "="*60)
        print("CARDIOFOCUS INTEGRATED TEST SUITE")
        if self.demo_mode:
            print("*** DEMO MODE - Simulated Test Execution ***")
        print(f"Device ID: {device_id}")
        print(f"Expected Status: {expected_status}")
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        if run_api:
            print("\n[1/2] Running API Tests...")
            api_results = run_api_test(device_id, expected_status, demo_mode=self.demo_mode)
            self.all_results.extend([{'type': 'API', **r} for r in api_results])
        
        if run_ui:
            print("\n[2/2] Running UI Tests...")
            ui_results = run_ui_test(device_id, expected_status, demo_mode=self.demo_mode)
            self.all_results.extend([{'type': 'UI', **r} for r in ui_results])
        
        self.end_time = datetime.now()
        
        self.print_summary()
        self.save_report()
        
        return self.all_results
    
    def print_summary(self):
        """Print overall test summary"""
        print("\n" + "="*60)
        print("OVERALL TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.all_results)
        passed_tests = sum(1 for r in self.all_results if r['status'] == 'PASS')
        failed_tests = total_tests - passed_tests
        
        duration = (self.end_time - self.start_time).total_seconds()
        
        print(f"\nTotal Steps: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Completed: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if failed_tests == 0:
            print("\n[SUCCESS] ALL TESTS PASSED!")
        else:
            print("\n[WARNING] SOME TESTS FAILED - Review details above")
        
        print("="*60 + "\n")
    
    def save_report(self):
        """Save test results to file"""
        timestamp = self.start_time.strftime('%Y%m%d_%H%M%S')
        filename = f"test_report_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("="*60 + "\n")
                f.write("CARDIOFOCUS TEST REPORT\n")
                if self.demo_mode:
                    f.write("*** DEMO MODE - Simulated Test Execution ***\n")
                f.write("="*60 + "\n\n")
                f.write(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"End Time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Duration: {(self.end_time - self.start_time).total_seconds():.2f} seconds\n\n")
                
                f.write("TEST RESULTS:\n")
                f.write("-"*60 + "\n")
                
                for result in self.all_results:
                    status_symbol = "[PASS]" if result['status'] == "PASS" else "[FAIL]"
                    f.write(f"{status_symbol} [{result['type']}] {result['step']}: {result['message']}\n")
                
                f.write("\n" + "="*60 + "\n")
                total = len(self.all_results)
                passed = sum(1 for r in self.all_results if r['status'] == 'PASS')
                f.write(f"SUMMARY: {passed}/{total} steps passed ({passed/total*100:.1f}%)\n")
                f.write("="*60 + "\n")
            
            print("[INFO] Test report saved: {}".format(filename))
            
            # Auto-generate reports page
            self.generate_reports_page()
            
            return filename
        except Exception as e:
            print("[ERROR] Failed to save report: {}".format(str(e)))
            return None
    
    def generate_reports_page(self):
        """Auto-generate reports.html with all test report files"""
        try:
            # Get all test report files
            report_files = sorted(glob.glob('test_report_*.txt'), reverse=True)
            
            if not report_files:
                return
            
            # Parse each report file
            reports_data = []
            for report_file in report_files:
                with open(report_file, 'r') as f:
                    content = f.read()
                    
                # Extract data from report
                lines = content.split('\n')
                start_time = ''
                total_steps = 0
                passed = 0
                failed = 0
                success_rate = 0
                
                for line in lines:
                    if 'Start Time:' in line:
                        start_time = line.split('Start Time:')[1].strip()
                    elif 'SUMMARY:' in line:
                        parts = line.split('SUMMARY:')[1].strip()
                        steps_part = parts.split('steps')[0].strip()
                        passed = int(steps_part.split('/')[0])
                        total_steps = int(steps_part.split('/')[1])
                        failed = total_steps - passed
                        success_rate = parts.split('(')[1].split('%')[0]
                
                reports_data.append({
                    'filename': report_file,
                    'start_time': start_time,
                    'total_steps': total_steps,
                    'passed': passed,
                    'failed': failed,
                    'success_rate': success_rate,
                    'content': content
                })
            
            # Generate HTML (simplified version)
            report_cards_html = ''
            for idx, report in enumerate(reports_data):
                status_class = 'success' if report['failed'] == 0 else 'warning'
                report_cards_html += f'''<div class="report-card" onclick="viewReport('report{idx}')">
                    <div class="report-header">
                        <div class="report-title">Test Report #{len(reports_data) - idx}</div>
                        <div class="report-date">{report['start_time']}</div>
                    </div>
                    <div class="report-stats">
                        <div class="stat"><span class="stat-label">Total:</span> <span class="stat-value">{report['total_steps']}</span></div>
                        <div class="stat"><span class="stat-label">Passed:</span> <span class="stat-value {status_class}">{report['passed']}</span></div>
                        <div class="stat"><span class="stat-label">Failed:</span> <span class="stat-value">{report['failed']}</span></div>
                        <div class="stat"><span class="stat-label">Rate:</span> <span class="stat-value {status_class}">{report['success_rate']}%</span></div>
                    </div>
                </div>\n'''
            
            # Generate JavaScript
            view_report_js = 'function viewReport(reportType) { let reportContent = \'\'; '
            for idx, report in enumerate(reports_data):
                escaped = report['content'].replace('\\', '\\\\').replace('\'', '\\\'').replace('\n', '\\n')
                view_report_js += f"if (reportType === 'report{idx}') {{ reportContent = '{escaped}'; }} else "
            view_report_js += "{ reportContent = 'Report not found'; } alert(reportContent); }"
            
            # Write HTML file
            html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Reports</title>
<style>* {{margin:0;padding:0;box-sizing:border-box}} body {{font-family:Arial,sans-serif;background:#f5f5f5}} .header {{background:#667eea;color:white;padding:20px;display:flex;justify-content:space-between;align-items:center}} .header h1 {{font-size:24px}} .logout-btn {{background:rgba(255,255,255,0.2);color:white;padding:8px 20px;border:1px solid white;border-radius:5px;cursor:pointer}} .nav {{background:white;padding:15px 20px}} .nav a {{margin-right:20px;color:#667eea;text-decoration:none;font-weight:500}} .content {{padding:30px;max-width:1200px;margin:0 auto}} .reports-container {{background:white;padding:30px;border-radius:10px}} .report-card {{background:#f8f9fa;padding:20px;border-radius:8px;margin-bottom:15px;border-left:4px solid #667eea;cursor:pointer}} .report-card:hover {{background:#e9ecef}} .report-header {{display:flex;justify-content:space-between;margin-bottom:10px}} .report-title {{font-size:18px;font-weight:600}} .report-date {{color:#666;font-size:14px}} .report-stats {{display:flex;gap:20px}} .stat {{font-size:14px}} .stat-label {{color:#666}} .stat-value {{font-weight:600;margin-left:5px}} .success {{color:#28a745}} .warning {{color:#ffc107}}</style>
</head><body>
<div class="header"><h1>CardioFocus Portal</h1><button onclick="logout()" class="logout-btn">Logout</button></div>
<div class="nav"><a href="dashboard.html">Dashboard</a><a href="devices.html">Devices</a><a href="reports.html">Reports</a></div>
<div class="content"><div class="reports-container"><h2>Test Reports ({len(reports_data)} total)</h2><div id="reports-list">{report_cards_html}</div></div></div>
<script src="auth.js"></script><script>{view_report_js}</script>
</body></html>'''
            
            with open('mock_portal/reports.html', 'w') as f:
                f.write(html)
            
            print("[INFO] Reports page updated with {} reports".format(len(reports_data)))
        except Exception as e:
            print("[WARNING] Could not update reports page: {}".format(str(e)))
    
    def send_email_notification(self):
        """Send email notification with test results"""
        if not all([Config.SENDER_EMAIL, Config.SENDER_PASSWORD, Config.RECIPIENT_EMAIL]):
            print("[WARNING] Email notification skipped - credentials not configured")
            return
        
        try:
            total = len(self.all_results)
            passed = sum(1 for r in self.all_results if r['status'] == 'PASS')
            failed = total - passed
            
            subject = f"CardioFocus Test Results - {'PASSED' if failed == 0 else 'FAILED'}"
            
            body = f"""
CardioFocus Automated Test Results

Test Execution Summary:
- Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
- End Time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}
- Duration: {(self.end_time - self.start_time).total_seconds():.2f} seconds

Results:
- Total Steps: {total}
- Passed: {passed}
- Failed: {failed}
- Success Rate: {(passed/total*100):.1f}%

Status: {'[SUCCESS] ALL TESTS PASSED' if failed == 0 else '[WARNING] SOME TESTS FAILED'}

Detailed results are available in the test report file.
"""
            
            msg = MIMEMultipart()
            msg['From'] = Config.SENDER_EMAIL
            msg['To'] = Config.RECIPIENT_EMAIL
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
                server.starttls()
                server.login(Config.SENDER_EMAIL, Config.SENDER_PASSWORD)
                server.send_message(msg)
            
            print("[INFO] Email notification sent successfully")
        except Exception as e:
            print("[ERROR] Failed to send email: {}".format(str(e)))

def main():
    """Main entry point"""
    # Test configuration
    device_id = "DEV-12345"
    expected_status = "Active"
    
    # Enable demo mode for local testing (set to False for real portal testing)
    demo_mode = True
    
    runner = IntegratedTestRunner(demo_mode=demo_mode)
    runner.run_tests(device_id, expected_status, run_ui=True, run_api=True)
    
    # Send email notification (optional - will skip if not configured)
    # runner.send_email_notification()

if __name__ == "__main__":
    main()
