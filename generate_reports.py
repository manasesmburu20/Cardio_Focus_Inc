import os
import glob
from datetime import datetime

def generate_reports_page():
    """Generate reports.html with all test report files"""
    
    # Get all test report files
    report_files = sorted(glob.glob('test_report_*.txt'), reverse=True)
    
    if not report_files:
        print("No test reports found!")
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
                # Extract from "SUMMARY: 10/10 steps passed (100.0%)"
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
    
    # Generate HTML report cards
    report_cards_html = ''
    for idx, report in enumerate(reports_data):
        status_class = 'success' if report['failed'] == 0 else 'warning' if report['passed'] > report['failed'] else 'danger'
        
        report_cards_html += f'''
                <div class="report-card" onclick="viewReport('report{idx}')">
                    <div class="report-header">
                        <div class="report-title">Test Report #{len(reports_data) - idx}</div>
                        <div class="report-date">{report['start_time']}</div>
                    </div>
                    <div class="report-stats">
                        <div class="stat">
                            <span class="stat-label">Total Steps:</span>
                            <span class="stat-value">{report['total_steps']}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Passed:</span>
                            <span class="stat-value {status_class}">{report['passed']}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Failed:</span>
                            <span class="stat-value {'danger' if report['failed'] > 0 else ''}">{report['failed']}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Success Rate:</span>
                            <span class="stat-value {status_class}">{report['success_rate']}%</span>
                        </div>
                    </div>
                </div>
'''
    
    # Generate JavaScript for viewing reports
    view_report_js = 'function viewReport(reportType) {\n            let reportContent = \'\';\n            \n'
    for idx, report in enumerate(reports_data):
        escaped_content = report['content'].replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
        view_report_js += f'''            if (reportType === 'report{idx}') {{
                reportContent = `{escaped_content}`;
            }} else '''
    
    view_report_js += '''{
                reportContent = 'Report not found';
            }
            
            alert(reportContent);
        }'''
    
    # Generate full HTML page
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CardioFocus Portal - Reports</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: #f5f5f5; }}
        .header {{ background: #667eea; color: white; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; }}
        .header h1 {{ font-size: 24px; }}
        .logout-btn {{ background: rgba(255,255,255,0.2); color: white; padding: 8px 20px; border: 1px solid white; border-radius: 5px; cursor: pointer; text-decoration: none; }}
        .logout-btn:hover {{ background: rgba(255,255,255,0.3); }}
        .nav {{ background: white; padding: 15px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .nav a {{ margin-right: 20px; color: #667eea; text-decoration: none; font-weight: 500; }}
        .nav a:hover {{ text-decoration: underline; }}
        .content {{ padding: 30px; max-width: 1200px; margin: 0 auto; }}
        .reports-container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .report-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #667eea; cursor: pointer; transition: all 0.3s; }}
        .report-card:hover {{ background: #e9ecef; transform: translateX(5px); }}
        .report-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        .report-title {{ font-size: 18px; font-weight: 600; color: #333; }}
        .report-date {{ color: #666; font-size: 14px; }}
        .report-stats {{ display: flex; gap: 20px; margin-top: 10px; }}
        .stat {{ font-size: 14px; }}
        .stat-label {{ color: #666; }}
        .stat-value {{ font-weight: 600; margin-left: 5px; }}
        .success {{ color: #28a745; }}
        .warning {{ color: #ffc107; }}
        .danger {{ color: #dc3545; }}
        .refresh-btn {{ background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-bottom: 20px; }}
        .refresh-btn:hover {{ background: #5568d3; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>CardioFocus Device Portal</h1>
        <button onclick="logout()" class="logout-btn">Logout</button>
    </div>
    <div class="nav">
        <a href="dashboard.html">Dashboard</a>
        <a href="devices.html">Devices</a>
        <a href="reports.html">Reports</a>
        <a href="#">Settings</a>
    </div>
    <div class="content">
        <div class="reports-container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2>Test Reports ({len(reports_data)} total)</h2>
                <button class="refresh-btn" onclick="location.reload()">Refresh Reports</button>
            </div>
            <div id="reports-list">
{report_cards_html}
            </div>
        </div>
    </div>

    <script src="auth.js"></script>
    <script>
        {view_report_js}
    </script>
</body>
</html>
'''
    
    # Write to file
    with open('mock_portal/reports.html', 'w') as f:
        f.write(html_content)
    
    print(f"[SUCCESS] Generated reports.html with {len(reports_data)} reports")

if __name__ == '__main__':
    generate_reports_page()
