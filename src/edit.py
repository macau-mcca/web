import os
import sys
import time
import requests
import base64
from ast import literal_eval
# Request the subscription URL

JMS_SV = os.getenv('JMS_SV')
JMS_ID = os.getenv('JMS_ID')

response = requests.get(f'https://jmssub.net/members/getsub.php?service={JMS_SV}&id={JMS_ID}')

# Get the content and decode from base64
if response.status_code == 200:
    text = base64.b64decode(response.text).decode('utf-8')
    IPS = []
    for line in text.split('\n'):
        if line.startswith("ss://"):
            line = line[5:line.find('#')]
            line = base64.b64decode(line + '=' * (-len(line) % 4)).decode('utf-8')
            IP = line.split('@')[1].split(':')[0]
            
        elif line.startswith("vmess://"):
            line = line[8:]
            line = base64.b64decode(line + '=' * (-len(line) % 4)).decode('utf-8')
            line = literal_eval(line)
            IP = line['add']
        
        else:
            print(line)
            
        IPS.append(IP)
        
    with open('mccavpn.html', 'r+') as f:
        content = f.read()
        # Find the proxies section and update IPs
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line == '':
                continue
            
            if line == 'proxies:':
                ip_index = 0
                j = i + 1
                while j < len(lines) and lines[j].startswith('-') or lines[j].startswith('  '):
                    # Find the server line within each proxy block
                    k = j + 1
                    while k < len(lines) and lines[k].startswith('  '):
                        if 'server:' in lines[k] and ip_index < len(IPS):
                            # Replace the IP while keeping the indentation
                            indent = lines[k][:lines[k].find('server:')]
                            lines[k] = f"{indent}server: {IPS[ip_index]}"
                            ip_index += 1
                            break
                        k += 1
                    j = k + 1
                    
        content = '\n'.join(lines)
        
        f.seek(0)
        f.write(content)
        f.truncate()
    
    print("Updated mccavpn.html")
else:
    print("WARNING: Failed to fetch content from JMS Sub. Status code: ", response.status_code)

response = requests.get(f'https://justmysocks5.net/members/getbwcounter.php?service={JMS_SV}&id={JMS_ID}')

if response.status_code == 200:
    dic = literal_eval(response.text)
    # Get current date info
    CUR_DATE = time.strftime("%Y-%m-%d").split('-')
    CUR_DATE[-1] = str(dic['bw_reset_day_of_month'])
    CUR_DATE = '-'.join(CUR_DATE)
    
    EXPIRE_TIMESTAMP = int(time.mktime(time.strptime(CUR_DATE, "%Y-%m-%d")))
    
    # Update header lines
    with open('_headers', 'r+') as f:
        content = f.read()
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'Subscription-Userinfo:' in line:
                parts = line.split(';')
                for j, part in enumerate(parts):
                    if 'download=' in part:
                        parts[j] = f" download={dic['bw_counter_b']}"
                    elif 'expire=' in part:
                        parts[j] = f" expire={EXPIRE_TIMESTAMP}"
                lines[i] = ';'.join(parts)
        
        content = '\n'.join(lines)
        f.seek(0)
        f.write(content)
        f.truncate()
        
    print("Updated _headers")
else:
    print("WARNING: Failed to fetch content from JMS Counter. Status code: ", response.status_code)
        