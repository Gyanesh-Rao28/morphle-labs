from flask import Flask
import subprocess
import datetime
import pytz
import os

app = Flask(__name__)

def get_full_top_output():
    try:
        cmd = "top -b -n 1"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        
        lines = result.stdout.split('\n')
        
        header_lines = []
        process_lines = []
        
        for line in lines:
            if any(keyword in line for keyword in ['top -', 'Tasks:', '%Cpu', 'MiB Mem', 'MiB Swap']):
                header_lines.append(line)
            elif 'PID' in line or ('codespa' in line or 'root' in line):
                process_lines.append(line)

        full_output = '\n'.join(header_lines)
        full_output += '\n\n' + '\n'.join(process_lines)
        return full_output
    except Exception as e:
        return f"Error getting top output: {str(e)}"

@app.route('/htop')
def htop():
    ist = pytz.timezone('Asia/Kolkata')
    server_time = datetime.datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    response = f"""Name: sample_name
user: codespace
Server Time (IST): {server_time}
TOP output:
{get_full_top_output()}"""
    
    return response, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)