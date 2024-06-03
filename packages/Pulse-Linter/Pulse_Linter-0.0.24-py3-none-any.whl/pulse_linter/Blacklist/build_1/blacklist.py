from pulse_linter.Blacklist.build_1.base_dictionary import build_blacklist
from pulse_linter.Blacklist.build_1.cwe import Cwe
class Blacklist_2:
    @staticmethod
    def gen_blacklist():
        sets = []
        sets.append(build_blacklist("Incomplete URL sanitization",
                                      1,
                                      Cwe.INCOMPLETE_URL_SANITIZATION,
                                      [r'\burl\s*=\s*req\.param\(["\']url["\']\)',
                                                r'url\s*=\s*request\.args\.get\(["\']url["\']\)',
                                                 r'urlLib\.parse\(url\)\.hostname'],
                                      "Improper Input Validation, Category A03:2021 - Injection",
                                      "based on context"


                                      ))
        sets.append(build_blacklist("Tar Slip",
                                      2,
                                      Cwe.TAR_SLIP,
                                      [r'\b(input|raw_input|get|fetch|request)\([\'"]?[a-zA-Z_][a-zA-Z0-9_]*[\'"]?\)',
                                       r'[\'"]?(open|os\.(system|popen|execve))\([\'"]?[a-zA-Z_][a-zA-Z0-9_]*[\'"]?\s*\+\s*[\'"]?[a-zA-Z_][a-zA-Z0-9_]*[\'"]?\)',
                                       r'\b(eval|exec|execfile)\([\'"]?[a-zA-Z_][a-zA-Z0-9_]*[\'"]?\)',
                                       r'(\b(subprocess\.(Popen|check_output))|os\.(system|popen|execve))\([\'"]?[a-zA-Z_][a-zA-Z0-9_]*[\'"]?\)',
                                       r'\b(select|update|delete|insert)\s.*\b(from|where)\s[\'"]?[a-zA-Z_][a-zA-Z0-9_]*[\'"]?'],
                                      "CWE (22) Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal'),Category A01:2021 - Broken Access Contro",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Path Traversal",
                                      3,
                                      Cwe.PATH_TRAVERSAL,
                                      [r'\.\./|\.\.|\\\.\\\.\\|\\\.\\\.'],
                                      "Relative Path Traversal,  Category A01:2021 - Broken Access Control",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Command Injection",
                                      4,
                                      Cwe.COMMAND_INJECTION,
                                      [r'os\.system|subprocess\.run|subprocess\.call|subprocess\.Popen'],
                                      "CWE (78) Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection'),Category A03:2021 - Injection",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Cross-site Scripting (XSS)",
                                      5,
                                      Cwe.CROSS_SITE_SCRIPTING,
                                      [
                                          r'\b(mark_safe)\([\'"].*[\'"]\)',  # Django's mark_safe function
                                          r'\b(escape)\([\'"].*[\'"]\)',  # Django's escape function
                                          r'\b(html.escape)\([\'"].*[\'"]\)',  # Python's html.escape function
                                          r'\b(jinja2.escape)\([\'"].*[\'"]\)',  # Jinja2's escape function
                                      ],
                                      "CWE (79) Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting'), Category A03:2021 - Injection",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Jinja auto-escape is set to false",
                                      6,
                                      Cwe.JINJA_AUTO_ESCAPE,
                                      [
                                          r'\{\{.*\}\}',  # Jinja template expressions
                                          r'\{%.*%\}',  # Jinja template tags
                                      ],
                                      "CWE (79) Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting'), Category A03:2021 - Injection",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("SQL Injection",
                                      7,
                                      Cwe.SQL_INJECTION,
                                      [
                                          r'[\s;]SELECT\s.*\sFROM\s.*',  # SQL SELECT statement
                                          r'[\s;]INSERT\sINTO\s.*\sVALUES\s.*',  # SQL INSERT statement
                                          r'[\s;]UPDATE\s.*\sSET\s.*',  # SQL UPDATE statement
                                          r'[\s;]DELETE\sFROM\s.*',  # SQL DELETE statement
                                          r'[\s;]DROP\sTABLE\s.*',  # SQL DROP TABLE statement
                                          r'[\s;]TRUNCATE\sTABLE\s.*',  # SQL TRUNCATE TABLE statement
                                          r'[\s;]ALTER\sTABLE\s.*',  # SQL ALTER TABLE statement
                                          r'[\s;]CREATE\sTABLE\s.*',  # SQL CREATE TABLE statement
                                          r'[\s;]GRANT\s.*\sTO\s.*',  # SQL GRANT statement
                                          r'[\s;]REVOKE\s.*\sFROM\s.*',  # SQL REVOKE statement
                                          r'[\s;]EXEC\s.*',  # SQL EXEC statement
                                          r'[\s;]CALL\s.*',  # SQL CALL statement
                                      ],
                                      "CWE (89) Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection'),Category A03:2021 - Injection",
                                      "based on context"

                                      ))
        sets.append((build_blacklist("Code Injection",
                                       8,
                                       Cwe.CODE_INJECTION,
                                       [
                                           r'[\s;]eval\s*\(.*\)',  # eval() function call
                                           r'[\s;]exec\s*\(.*\)',  # exec() function call
                                           r'[\s;]os\.(system|popen|execve)\(.*\)',
                                           # Calls to os.system(), os.popen(), os.execve()
                                           r'[\s;]subprocess\.(Popen|check_output)\(.*\)',
                                           # Calls to subprocess.Popen(), subprocess.check_output()
                                           r'[\s;]input\([\'"].*[\'"]\)',  # Calls to input() function
                                           r'[\s;](request|get|fetch)\(.*\)',
                                           # Calls to request(), get(), fetch() functions
                                       ],
                                       "CWE (94) Improper Control of Generation of Code ('Code Injection'),  Category A03:2021 - Injection",
                                       "based on context"

                                       )))
        sets.append(build_blacklist("Static Code Injection",
                                      9,
                                      Cwe.STATIC_CODE_INJECTION,
                                      [
                                          r'[\s;]eval\s*\(.*\)',  # eval() function call
                                          r'[\s;]exec\s*\(.*\)',  # exec() function call
                                          r'[\s;]os\.(system|popen|execve)\(.*\)',
                                          # Calls to os.system(), os.popen(), os.execve()
                                          r'[\s;]subprocess\.(Popen|check_output)\(.*\)',
                                          # Calls to subprocess.Popen(), subprocess.check_output()
                                          r'[\s;]input\([\'"].*[\'"]\)',  # Calls to input() function
                                          r'[\s;](request|get|fetch)\(.*\)',
                                          # Calls to request(), get(), fetch() functions
                                      ],
                                      " Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection'),  Category A03:2021 - Injection",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Server Information Exposure",
                                      10,
                                      Cwe.SERVER_INFORMATION_EXPOSURE,
                                      [
                                          r'\b(server|platform|sys|os|uname)\.platform\b',
                                          # Accessing platform information
                                          r'\b(server|platform|sys|os|uname)\.uname\b',  # Accessing system information
                                          r'\b(server|platform|sys|os)\.version\b',  # Accessing version information
                                          r'\b(server|platform|sys|os)\.release\b',  # Accessing release information
                                          r'\b(server|platform|sys|os)\.system\b',  # Accessing system information
                                          r'\b(server|platform|sys|os)\.cpu_count\b',  # Accessing CPU count
                                      ],
                                      "CWE (209) Generation of Error Message Containing Sensitive Information,  Category A04:2021 - Insecure Design",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Use of Hardcoded Credentials",
                                      11,
                                      Cwe.HARD_CODED_CREDENTIALS,
                                      [
                                          r'\b(password|passwd|pwd)\s*=\s*[\'"][^\'"]+[\'"]\b',
                                          # Detects assignment of hard-coded passwords
                                          r'\b(username|user|login)\s*=\s*[\'"][^\'"]+[\'"]\b',
                                          # Detects assignment of hard-coded usernames
                                          r'\b(api_key|api_secret|token)\s*=\s*[\'"][^\'"]+[\'"]\b',
                                          # Detects assignment of hard-coded API keys or tokens
                                          r'\b(secret_key|access_key)\s*=\s*[\'"][^\'"]+[\'"]\b',
                                          # Detects assignment of hard-coded secret/access keys
                                          r'\b(credentials|auth_token)\s*=\s*[\'"][^\'"]+[\'"]\b',
                                          # Detects assignment of hard-coded credentials or authentication tokens
                                      ],
                                      "CWE (259, 798) Use of Hard-coded Password, Use of Hard-coded Credentials,  Category A07:2021 - Identification and Authentication Failures",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Insufficient Permissions or Privileges",
                                      12,
                                      Cwe.HANDLING_OF_INSUFFICIENT_PERMISSION,
                                      [
                                          r'\bchmod\(',  # Detects calls to chmod which may change file permissions
                                          r'\bchown\(',  # Detects calls to chown which may change file ownership
                                          r'\bsetuid\(',  # Detects calls to setuid which may escalate privileges
                                          r'\bsetgid\(',  # Detects calls to setgid which may escalate privileges
                                          r'\bseteuid\(',  # Detects calls to seteuid which may escalate privileges
                                          r'\bsetegid\(',  # Detects calls to setegid which may escalate privileges
                                          r'\bsudo\b',  # Detects mentions of sudo which may imply elevated privileges
                                          r'\broot\b',
                                          # Detects mentions of root user which may imply elevated privileges
                                          r'\bprivileged\b',  # Detects mentions of privileged operations
                                          r'\bgrant\(',  # Detects calls to grant permissions
                                          r'\bdeny\(',  # Detects calls to deny permissions
                                          r'\bpermission\b',  # Detects mentions of permission control
                                          r'\bprivilege\b',  # Detects mentions of privilege control
                                      ],
                                      ' Improper Handling of Insufficient Permissions or Privileges, Category A04:2021 - Insecure Desig',
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Improper Access Control",
                                      13,
                                      Cwe.IMPROPER_ACCESS_CONTROL,
                                      [
                                          r'\b0\.0\.0\.0\b',  # Detects bindings to all network interfaces
                                          r'\bsocket\.bind\(.*\("0\.0\.0\.0"',
                                          # Detects socket bindings to all network interfaces
                                          r'\bsocket\.bind\(.*\(\'0\.0\.0\.0\'',
                                          # Detects socket bindings to all network interfaces
                                      ],
                                      "CWE (284) Improper Access Control,  Category A01:2021 - Broken Access Control",
                                      "based on context"
                                      ))
        sets.append(build_blacklist(" Broken User Authentication",
                                      14,
                                      Cwe.IMPROPER_AUTHENTICATION,
                                      [
                                          r'\blogin\b',  # Detects references to login functionality
                                          r'\bauthenticate\b',  # Detects references to authentication processes
                                          r'\bcredentials\b',  # Detects references to user credentials
                                          r'\bpassword\b',  # Detects references to passwords
                                          r'\bsession\b',  # Detects references to session management
                                          r'\btoken\b',  # Detects references to authentication tokens
                                          r'\bJWT\b',  # Detects references to JSON Web Tokens (JWT)
                                          r'\boauth\b',  # Detects references to OAuth authentication
                                          r'\bauth\b',  # Detects references to authentication in general
                                          r'\blogin_required\b',
                                          # Detects decorators or functions enforcing login requirements
                                          r'\buser_authenticated\b',
                                          # Detects variables or functions indicating user authentication status
                                          r'\bvalidate_token\b',  # Detects functions used for token validation
                                          r'\bsession_timeout\b',  # Detects references to session timeout settings
                                          r'\bremember_me\b',  # Detects references to "remember me" functionality
                                          r'\blogout\b',  # Detects references to logout functionality
                                          r'\bunauthorized\b',  # Detects references to unauthorized access
                                      ],
                                      "Improper Authentication,  Category A07:2021 - Identification and Authentication Failures",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Improper Certificate Validation",
                                      15,
                                      Cwe.IMPROPER_CERTIFICATE_VALIDATION,
                                      [
                                          r'\bssl\.CERT_NONE\b',
                                          # Detects usages of CERT_NONE, which disables certificate validation
                                          r'\bssl\.create_default_context\(ssl\.Purpose\.(SERVER_AUTH|CLIENT_AUTH)\)\b',
                                          # Detects creation of SSL contexts without customizing certificate validation
                                          r'\bssl\.match_hostname\b',
                                          # Detects usages of match_hostname, which should be used to validate server hostnames
                                          r'\bssl\.CERT_OPTIONAL\b',
                                          # Detects usages of CERT_OPTIONAL, which might indicate lax certificate validation
                                          r'\bverify\s*=\s*False\b',
                                          # Detects disabling of certificate verification in network requests
                                          r'\bca_certs\s*=\s*None\b',
                                          # Detects not providing CA certificates for certificate validation
                                          r'\bcheck_hostname\s*=\s*False\b',
                                          # Detects disabling hostname checking during certificate validation
                                          r'\bvalidate_certificate\b',
                                          # Detects custom functions for certificate validation
                                          r'\bssl\.get_server_certificate\b',
                                          # Detects obtaining server certificates without validation
                                          r'\bssl\.create_default_context\(ssl\.Purpose\.(SERVER_AUTH|CLIENT_AUTH), cafile=.+\)',
                                          # Detects creation of SSL contexts with custom CA certificates
                                          r'\bssl\.SSLContext\.load_verify_locations\(',
                                          # Detects loading CA certificates into SSL contexts for validation
                                          r'\bssl\.SSLContext\.load_cert_chain\(',
                                          # Detects loading client certificates into SSL contexts for client authentication
                                          r'\bvalidate_certificate_chain\b',
                                          # Detects custom functions for validating certificate chains
                                      ],
                                      "Improper Certificate Validation,  Category A07:2021 - Identification and Authentication Failures",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Cryptographic Issues",
                                      16,
                                      Cwe.CRYPTOGRAPHIC_ISSUE,
                                      [
                                          r'\bhashlib\.(md5|sha1)\(',
                                          # Detects usage of insecure hash functions like MD5 or SHA-1
                                          r'\bCrypto\.Hash\.(MD2|MD4|MD5|SHA)\.new\(',
                                          # Detects usage of insecure hash functions from PyCryptodome
                                          r'\bcryptography\.hazmat\.primitives\.hashes\.(MD5|SHA1)\(',
                                          # Detects usage of insecure hash functions from the cryptography library
                                          r'\brandom\.(Random|random|randrange|randint|choice|choices|uniform|triangular|randbytes)\(',
                                          # Detects usage of insecure random number generators
                                          r'\bsecrets\.(token_hex|token_bytes)\(',
                                          # Detects insecure generation of cryptographic tokens
                                          r'\bCryptodome\.(Cipher|PublicKey|Signature)\.',
                                          # Detects usage of cryptographic functions from PyCryptodome
                                          r'\bcryptography\.hazmat\.(primitives\.ciphers|primitives\.asymmetric\.rsa)\.',
                                          # Detects usage of cryptographic functions from the cryptography library
                                          r'\bparamiko\.(RSAKey|DSAKey|EVPKey)\(',
                                          # Detects usage of cryptographic functions from the paramiko library
                                          r'\bhmac\.(HMAC|new)\(',  # Detects usage of HMAC with insecure hash functions
                                          r'\bcryptography\.x509\.(load_pem_x509_certificate|load_der_x509_certificate)\(',
                                          # Detects loading X.509 certificates from PEM or DER formats
                                          r'\bcryptography\.x509\.(Certificate|CertificateBuilder)\(',
                                          # Detects creation or manipulation of X.509 certificates
                                          r'\bcryptography\.fernet\.',
                                          # Detects usage of the Fernet symmetric encryption algorithm
                                          r'\bpickle\.(load|loads)\(',
                                          # Detects deserialization using pickle, which can lead to security issues
                                          r'\bdill\.(load|loads)\(',
                                          # Detects deserialization using dill, which can lead to security issues
                                          r'\bjsonpickle\.(decode|unpickler\.decode)\(',
                                          # Detects deserialization using jsonpickle, which can lead to security issues
                                          r'\bpandas\.read_pickle\(',
                                          # Detects deserialization using pandas.read_pickle, which can lead to security issues
                                          r'\bpycryptodome\.(PublicKey|Ciphertext)\(',
                                          # Detects usage of cryptographic functions from PyCryptodome
                                          r'\bfernet\.(Fernet|MultiFernet)\(',
                                          # Detects usage of the Fernet symmetric encryption algorithm
                                          r'\bpycryptodomex\.(PublicKey|Ciphertext)\(',
                                          # Detects usage of cryptographic functions from PyCryptodomeX
                                      ],
                                      " Cryptographic Issues, Category A02:2021 - Cryptographic Failures",
                                      "based on context"))
        sets.append(build_blacklist("Authentication over HTTP",
                                      17,
                                      Cwe.PLAINTEXT_TRANSMISSION_SENSITIVE_INFORMATION,
                                      [
                                          r'\bhttp\.client\.HTTPConnection\(',
                                          # Detects HTTP connections without encryption
                                          r'\bhttp\.client\.HTTPSConnection\(',
                                          # Detects HTTPS connections without proper certificate validation
                                          r'\bhttp\.client\.HTTPResponse\(',
                                          # Detects handling of HTTP responses without checking for secure status codes
                                          r'\bhttp\.client\.HTTPResponse\.read\(',
                                          # Detects reading HTTP responses without encryption
                                          r'\bhttp\.client\.HTTPResponse\.readline\(',
                                          # Detects reading HTTP response lines without encryption
                                          r'\bhttp\.client\.HTTPResponse\.getheaders\(',
                                          # Detects retrieving HTTP response headers without encryption
                                          r'\bhttp\.client\.HTTPResponse\.getheader\(',
                                          # Detects retrieving a specific HTTP response header without encryption
                                          r'\bsocket\.(socket|create_connection)\(',
                                          # Detects socket connections without encryption
                                          r'\bsocket\.socket\.send\(',
                                          # Detects sending data over a socket connection without encryption
                                          r'\bsocket\.socket\.sendall\(',
                                          # Detects sending all data over a socket connection without encryption
                                          r'\bsocket\.socket\.recv\(',
                                          # Detects receiving data over a socket connection without encryption
                                          r'\bsocket\.socket\.recv_into\(',
                                          # Detects receiving data into a buffer over a socket connection without encryption
                                          r'\bos\.(popen|system)\(',
                                          # Detects running shell commands without encryption
                                          r'\bos\.execve\(',  # Detects executing a new process without encryption
                                          r'\bftplib\.(FTP|FTP_TLS)\(',
                                          # Detects FTP connections without encryption or with weak TLS encryption
                                          r'\bparamiko\.(SSHClient|Transport)\(',
                                          # Detects SSH connections without encryption or with weak encryption algorithms
                                          r'\bparamiko\.SSHClient\.connect\(',
                                          # Detects SSH connections without encryption or with weak encryption algorithms
                                          r'\bsmtplib\.(SMTP|SMTP_SSL)\(',
                                          # Detects SMTP connections without encryption or with weak SSL/TLS encryption
                                          r'\bimaplib\.(IMAP4|IMAP4_SSL)\(',
                                          # Detects IMAP connections without encryption or with weak SSL/TLS encryption
                                          r'\bpoplib\.(POP3|POP3_SSL)\(',
                                          # Detects POP3 connections without encryption or with weak SSL/TLS encryption
                                          r'\bsmtplib\.(sendmail|send_message|send_message|starttls)\(',
                                          # Detects sending emails without encryption or with weak TLS encryption
                                          r'\bssl\.(wrap_socket|create_default_context)\(',
                                          # Detects SSL connections without encryption or with weak encryption algorithms
                                          r'\bssl\.match_hostname\(',
                                          # Detects hostname verification without encryption
                                      ],
                                      "CWE (319) Cleartext Transmission of Sensitive Information, Category A02:2021 - Cryptographic Failures",
                                      "based on context"

                                      ))
        sets.append(build_blacklist("Hardcoded Cryptographic Key",
                                      18,
                                      Cwe.HARD_CODED_CREDENTIALS,
                                      [
                                          r'\b[A-Fa-f0-9]{32}\b',
                                          # Detects 128-bit AES keys (32 hexadecimal characters)
                                          r'\b[A-Fa-f0-9]{64}\b',
                                          # Detects 256-bit AES keys (64 hexadecimal characters)
                                          r'\b[A-Fa-f0-9]{128}\b',
                                          # Detects 512-bit AES keys (128 hexadecimal characters)
                                          r'\b[A-Za-z0-9+/]{44}={0,2}\b',
                                          # Detects Base64-encoded keys (assuming 32 bytes)
                                          r'\b[A-Za-z0-9+/]{88}={0,2}\b',
                                          # Detects Base64-encoded keys (assuming 64 bytes)
                                          r'\b[A-Za-z0-9+/]{176}={0,2}\b',
                                          # Detects Base64-encoded keys (assuming 128 bytes)
                                          r'\b[A-Za-z0-9]{16}\b',  # Detects 128-bit DES keys (16 characters)
                                          r'\b[A-Za-z0-9]{24}\b',  # Detects 192-bit Triple DES keys (24 characters)
                                          r'\b[A-Za-z0-9]{32}\b',  # Detects 256-bit Triple DES keys (32 characters)
                                          r'\b[A-Za-z0-9]{40}\b',  # Detects 160-bit SHA-1 hash keys (40 characters)
                                          r'\b[A-Za-z0-9]{64}\b',  # Detects 256-bit SHA-256 hash keys (64 characters)
                                          r'\b[A-Za-z0-9]{128}\b',  # Detects 1024-bit RSA keys (128 characters)
                                          r'\b[A-Za-z0-9]{256}\b',  # Detects 2048-bit RSA keys (256 characters)
                                          r'\b[A-Za-z0-9]{512}\b',  # Detects 4096-bit RSA keys (512 characters)
                                          r'\b[A-Za-z0-9]{64}:[A-Za-z0-9]{64}\b',
                                          # Detects 256-bit HMAC keys in the format "key:iv"
                                          r'\b0x[A-Fa-f0-9]{32}\b',
                                          # Detects hexadecimal representation of AES keys (32 characters)
                                          r'\b0x[A-Fa-f0-9]{64}\b',
                                          # Detects hexadecimal representation of AES keys (64 characters)
                                          r'\b0x[A-Fa-f0-9]{128}\b',
                                          # Detects hexadecimal representation of AES keys (128 characters)
                                          r'\b0x[A-Fa-f0-9]{16}\b',
                                          # Detects hexadecimal representation of DES keys (16 characters)
                                          r'\b0x[A-Fa-f0-9]{24}\b',
                                          # Detects hexadecimal representation of Triple DES keys (24 characters)
                                          r'\b0x[A-Fa-f0-9]{32}\b',
                                          # Detects hexadecimal representation of Triple DES keys (32 characters)
                                          r'\b0x[A-Fa-f0-9]{40}\b',
                                          # Detects hexadecimal representation of SHA-1 hash keys (40 characters)
                                          r'\b0x[A-Fa-f0-9]{64}\b',
                                          # Detects hexadecimal representation of SHA-256 hash keys (64 characters)
                                          r'\b0x[A-Fa-f0-9]{128}\b',
                                          # Detects hexadecimal representation of RSA keys (128 characters)
                                          r'\b0x[A-Fa-f0-9]{256}\b',
                                          # Detects hexadecimal representation of RSA keys (256 characters)
                                          r'\b0x[A-Fa-f0-9]{512}\b',
                                          # Detects hexadecimal representation of RSA keys (512 characters)
                                          r'\b[A-Za-z0-9]+_[A-Za-z0-9]+_[A-Za-z0-9]+\b'
                                          # Detects keys in the format "XXXX_YYYY_ZZZZ"
                                      ],
                                      "CWE (321) Use of Hard-coded Cryptographic Key, Category A02:2021 - Cryptographic Failures",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Inadequate Encryption Strength",
                                      19,
                                      Cwe.INADEQUATE_ENCRYPTION_STRENGTH,
                                      [
                                          r'\bMD2\b',  # Detects the use of MD2 hash function
                                          r'\bMD4\b',  # Detects the use of MD4 hash function
                                          r'\bMD5\b',  # Detects the use of MD5 hash function
                                          r'\bDES\b',  # Detects the use of DES encryption algorithm
                                          r'\b3DES\b|\bTriple DES\b|\bTDES\b',
                                          # Detects the use of Triple DES encryption algorithm
                                          r'\bRC4\b',  # Detects the use of RC4 encryption algorithm
                                          r'\bRC5\b',  # Detects the use of RC5 encryption algorithm
                                          r'\bRC6\b',  # Detects the use of RC6 encryption algorithm
                                          r'\bSingle DES\b|\bSingle-DES\b',
                                          # Detects the use of Single DES encryption algorithm
                                          r'\bSHA-1\b',  # Detects the use of SHA-1 hash function
                                          r'\bRSA\b',  # Detects the use of RSA encryption algorithm
                                          r'\bAES-128\b',  # Detects the use of AES-128 encryption algorithm
                                          r'\bAES-192\b',  # Detects the use of AES-192 encryption algorithm
                                          r'\bAES-256\b',  # Detects the use of AES-256 encryption algorithm
                                          r'\b128-bit\b',  # Detects the mention of 128-bit encryption strength
                                          r'\b192-bit\b',  # Detects the mention of 192-bit encryption strength
                                          r'\b256-bit\b',  # Detects the mention of 256-bit encryption strength
                                          r'\bLow encryption strength\b',  # Detects mentions of low encryption strength
                                          r'\bWeak encryption strength\b',
                                          # Detects mentions of weak encryption strength
                                          r'\bInadequate encryption\b'
                                          # Detects mentions of inadequate encryption strength
                                      ],
                                      "CWE (326) Inadequate Encryption Strength, Category A02:2021 - Cryptographic Failures",
                                      "based on context"

                                      ))
        sets.append(build_blacklist("Broken or Risky Cryptographic Algorithm",
                                      20,
                                      Cwe.RISK_CRYPTOGRAPHIC_ALGORITHM,
                                      [
                                          r'\bMD2\b',  # Detects the use of MD2 hash function
                                          r'\bMD4\b',  # Detects the use of MD4 hash function
                                          r'\bMD5\b',  # Detects the use of MD5 hash function
                                          r'\bSHA-1\b',  # Detects the use of SHA-1 hash function
                                          r'\bRC4\b',  # Detects the use of RC4 encryption algorithm
                                          r'\bRC5\b',  # Detects the use of RC5 encryption algorithm
                                          r'\bRC6\b',  # Detects the use of RC6 encryption algorithm
                                          r'\bDES\b',  # Detects the use of DES encryption algorithm
                                          r'\bTriple DES\b|\b3DES\b|\bTDES\b',
                                          # Detects the use of Triple DES encryption algorithm
                                          r'\bSingle DES\b|\bSingle-DES\b',
                                          # Detects the use of Single DES encryption algorithm
                                          r'\bECB\b',  # Detects the use of ECB mode
                                          r'\bCBC\b',  # Detects the use of CBC mode
                                          r'\bCFB\b',  # Detects the use of CFB mode
                                          r'\bOFB\b',  # Detects the use of OFB mode
                                          r'\bPKCS1\b',  # Detects the use of PKCS1 padding
                                          r'\bPKCS5\b',  # Detects the use of PKCS5 padding
                                          r'\bPKCS7\b',  # Detects the use of PKCS7 padding
                                          r'\bMD5\b',  # Detects the use of MD5 hash function
                                          r'\bSHA\b',
                                          # Detects the use of SHA hash function (without version specification)
                                          r'\bMD4\b',  # Detects the use of MD4 hash function
                                          r'\bMD5\b',  # Detects the use of MD5 hash function
                                          r'\bRC4\b',  # Detects the use of RC4 encryption algorithm
                                          r'\bRC5\b',  # Detects the use of RC5 encryption algorithm
                                          r'\bRC6\b',  # Detects the use of RC6 encryption algorithm
                                          r'\bECB\b',  # Detects the use of ECB mode
                                          r'\bCBC\b',  # Detects the use of CBC mode
                                          r'\bCFB\b',  # Detects the use of CFB mode
                                          r'\bOFB\b',  # Detects the use of OFB mode
                                          r'\bPKCS1\b',  # Detects the use of PKCS1 padding
                                          r'\bPKCS5\b',  # Detects the use of PKCS5 padding
                                          r'\bPKCS7\b',  # Detects the use of PKCS7 padding
                                          r'\bECB\b',  # Detects the use of ECB mode
                                          r'\bCBC\b',  # Detects the use of CBC mode
                                          r'\bCFB\b',  # Detects the use of CFB mode
                                          r'\bOFB\b',  # Detects the use of OFB mode
                                          r'\bPKCS1\b',  # Detects the use of PKCS1 padding
                                          r'\bPKCS5\b',  # Detects the use of PKCS5 padding
                                          r'\bPKCS7\b',  # Detects the use of PKCS7 padding
                                          r'\bSHA\b',
                                          # Detects the use of SHA hash function (without version specification)
                                          r'\bECB\b',  # Detects the use of ECB mode
                                          r'\bCBC\b',  # Detects the use of CBC mode
                                          r'\bCFB\b',  # Detects the use of CFB mode
                                          r'\bOFB\b',  # Detects the use of OFB mode
                                          r'\bPKCS1\b',  # Detects the use of PKCS1 padding
                                          r'\bPKCS5\b',  # Detects the use of PKCS5 padding
                                          r'\bPKCS7\b'  # Detects the use of PKCS7 padding
                                      ],
                                      "CWE (327) Use of a Broken or Risky Cryptographic Algorithm,  Category A02:2021 - Cryptographic Failures",
                                      "based on context"
                                      ))
        sets.append(build_blacklist(" Missing protocol in ssl.wrap_socket",
                                      21,
                                      Cwe.MISSING_PROTOCOL_SSL,
                                      [r'ssl\.wrap_socket\((?![^,]*protocol\s*=\s*ssl\.PROTOCOL_TLS)(?![^,]*protocol\s*=\s*ssl\.PROTOCOL_SSL)'],
                                      "Use of a Broken or Risky Cryptographic Algorithm, Category A02:2021 - Cryptographic Failures",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Use of Hardcoded Cryptographic Initialization Value",
                                      22,
                                      Cwe.PREDICTABLE_IV,
                                      [
                                          r'IV\s*=\s*b[\'"]\s*.\s*join\s*\(\s*[\'"].*[\'"].*rand.*\(.*\)',
                                          # Detects the use of random IV generation
                                          r'IV\s*=\s*os\.urandom\(\s*\d+\s*\)',
                                          # Detects the use of os.urandom for IV generation
                                          r'IV\s*=\s*urandom\(\s*\d+\s*\)',
                                          # Detects the use of urandom for IV generation
                                          r'IV\s*=\s*Random\.new\(\s*SAME\s*\)',  # Detects the use of a fixed IV
                                          r'IV\s*=\s*"\s*.{16}\s*"',  # Detects the use of hardcoded IVs
                                          r'IV\s*=\s*b[\'"].{16}[\'"]',  # Detects the use of hardcoded IVs
                                          r'IV\s*=\s*b[\'"]\s*.\s*join\s*\(\s*map\s*\(.*\)',
                                          # Detects the use of map function for IV generation
                                          r'IV\s*=\s*b[\'"].{16}[\'"]',  # Detects the use of hardcoded IVs
                                          r'IV\s*=\s*bytes\([0-9,\s]*\)',
                                          # Detects the use of bytes() for IV generation
                                          r'IV\s*=\s*bytearray\([0-9,\s]*\)',
                                          # Detects the use of bytearray() for IV generation
                                      ],
                                      "CWE (329) Generation of Predictable IV with CBC Mode,  Category A02:2021 - Cryptographic Failures",
                                      "based on context"

                                      ))
        sets.append(build_blacklist("Origin Validation Error",
                                      23,
                                      Cwe.ORIGIN_VALIDATION_ERROR,
                                      [
                                          r'origin\s*=\s*request\.headers\.get\(["\']Origin["\']\)',
                                          # Detects retrieval of the Origin header
                                          r'if\s*origin\s*!=\s*trusted_origin:',
                                          # Detects comparison of origin with a trusted value
                                          r'if\s*not\s*validate_origin\(origin\):',
                                          # Detects validation of origin using a custom function
                                          r'origin\s*=\s*request\.headers\.get\(["\']Referer["\']\)',
                                          # Detects retrieval of the Referer header as origin
                                          r'if\s*not\s*origin\s*or\s*not\s*is_valid_origin\(origin\):',
                                          # Detects validation of origin from Referer header
                                          r'origin\s*=\s*request\.headers\.get\(["\']Host["\']\)',
                                          # Detects retrieval of the Host header as origin
                                      ],
                                      "CWE (346, 942) Origin Validation Error, Permissive Cross-domain Policy with Untrusted Domains, Category A07:2021 - Identification and Authentication Failures",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Cross-Site Request Forgery (CSRF)",
                                      24,
                                      Cwe.CROSS_SITE_REQUEST_FORGERY,
                                      [
                                          r'csrf_token\s*=\s*request\.cookies\.get\(["\']csrf_token["\']\)',
                                          # Detects retrieval of CSRF token from cookies
                                          r'csrf_token\s*=\s*request\.headers\.get\(["\']X-CSRF-Token["\']\)',
                                          # Detects retrieval of CSRF token from headers
                                          r'csrf_token\s*=\s*request\.args\.get\(["\']csrf_token["\']\)',
                                          # Detects retrieval of CSRF token from URL parameters
                                          r'csrf_token\s*=\s*request\.form\.get\(["\']csrf_token["\']\)',
                                          # Detects retrieval of CSRF token from form data
                                          r'if\s*csrf_token\s*!=\s*session\["\']csrf_token["\']:',
                                          # Detects comparison of CSRF token with session token
                                          r'if\s*csrf_token\s*!=\s*request\.headers\.get\(["\']X-CSRF-Token["\']\):',
                                          # Detects comparison of CSRF token with header token
                                          r'if\s*csrf_token\s*!=\s*request\.args\.get\(["\']csrf_token["\']\):',
                                          # Detects comparison of CSRF token with URL parameter token
                                          r'if\s*csrf_token\s*!=\s*request\.form\.get\(["\']csrf_token["\']\):',
                                          # Detects comparison of CSRF token with form token
                                          r'csrf_token\s*=\s*request\.cookies\.get\(["\']csrf_token["\']\)',
                                          # Detects retrieval of CSRF token from cookies
                                          r'if\s*not\s*validate_csrf_token\(csrf_token\):',
                                          # Detects validation of CSRF token using a custom function
                                      ],
                                      "CWE (352) Cross-Site Request Forgery (CSRF),  Category A01:2021 - Broken Access Control",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Insecure Temporary File",
                                      25,
                                      Cwe.INSECURE_FILE_PERMISSION,
                                      [
                                          r'tempfile\.mktemp\(',  # Detects usage of insecure mktemp function
                                          r'tempfile\.TemporaryFile\(',
                                          # Detects creation of temporary files without secure permissions
                                          r'open\(.*[, ]["\']w[+"\']\)',
                                          # Detects opening files in write mode without proper security checks
                                          r'open\(.*[, ]["\']a[+"\']\)',
                                          # Detects opening files in append mode without proper security checks
                                          r'file\.write\(.*request\.data\)',
                                          # Detects writing user-supplied data directly to a file
                                          r'file\.write\(.*input\("Enter file contents: "\)\)',
                                          # Detects writing user input directly to a file
                                          r'file\.write\(.*input\("Enter file name: "\)\)',
                                          # Detects writing user input directly to a file name
                                          r'file\.write\(.*sys\.argv\[\d\]\)',
                                          # Detects writing command-line arguments directly to a file
                                          r'file\.write\(.*os\.getenv\("TEMP"\)\)',
                                          # Detects writing environment variables directly to a file
                                      ],
                                      "CWE (377) Insecure Temporary File,  Category A01:2021 - Broken Access Control",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Regular Expression Denial of Service (ReDoS",
                                      26,
                                      Cwe.UNCONTROLLED_RESOURCE_CONSUMPTION,
                                      [
                                          r'\b\w*(\w)\1{3,}\w*\b',  # Detects repetitive characters in a word
                                          r'\b\d+(\d+)\1{3,}\d*\b',  # Detects repetitive digits in a number
                                          r'\b[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*@[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)+\b',
                                          # Detects email regex with potential exponential backtracking
                                          r'\b[a-z]+(?:-[a-z]+)*\b',
                                          # Detects hyphenated words regex with potential exponential backtracking
                                          r'\b(?:[a-z]+)+\b',  # Detects repetitive patterns in word boundaries
                                          r'([a-zA-Z]+)\1{4,}',
                                          # Detects repetitive patterns in word boundaries with alphabetic characters
                                          r'(a+)+\s(b+)+',  # Detects nested repetition in regex
                                          r'^(a+)+$',
                                          # Detects repetition in regex starting and ending with the same character
                                          r'\b[A-Za-z]+\b',
                                          # Detects simple word regex with potential exponential backtracking
                                      ],
                                      "CWE (400) Uncontrolled Resource Consumption",
                                      "based on context"

                                      ))
        sets.append(build_blacklist("Insecure default value",
                                      27,
                                      Cwe.INSECURE_DEFAULT_VALUE,
                                      [
                                          r'password\s*=\s*[\'"].*[\'"]',  # Detects hardcoded passwords
                                          r'api_key\s*=\s*[\'"].*[\'"]',  # Detects hardcoded API keys
                                          r'secret_key\s*=\s*[\'"].*[\'"]',  # Detects hardcoded secret keys
                                          r'token\s*=\s*[\'"].*[\'"]',  # Detects hardcoded tokens
                                          r'key\s*=\s*[\'"].*[\'"]',  # Detects hardcoded keys
                                          r'passphrase\s*=\s*[\'"].*[\'"]',  # Detects hardcoded passphrases
                                          r'auth\s*=\s*[\'"].*[\'"]',  # Detects hardcoded authentication credentials
                                          r'config\.username\s*=\s*[\'"].*[\'"]',
                                          # Detects hardcoded usernames in configurations
                                          r'config\.password\s*=\s*[\'"].*[\'"]',
                                          # Detects hardcoded passwords in configurations
                                          r'config\.key\s*=\s*[\'"].*[\'"]',  # Detects hardcoded keys in configurations
                                          r'config\.secret\s*=\s*[\'"].*[\'"]',
                                          # Detects hardcoded secrets in configurations
                                          r'config\.token\s*=\s*[\'"].*[\'"]',
                                          # Detects hardcoded tokens in configurations
                                      ],
                                      "CWE (453) Insecure Default Variable Initialization",
                                      "based on context"

                                      ))
        sets.append(build_blacklist("Debug Mode Enabled",
                                      28,
                                      Cwe.ACTIVE_DEBUG_CODE,
                                      [
                                          r'debug\s*=\s*(True|true|1)',  # Detects if debug mode is set to True
                                          r'debug\s*=\s*(\'|\")?on(\'|\")?',  # Detects if debug mode is set to 'on'
                                          r'debug\s*=\s*[\'"]?enabled[\'"]?',
                                          # Detects if debug mode is set to 'enabled'
                                          r'debug\s*=\s*(\'|\")?yes(\'|\")?',  # Detects if debug mode is set to 'yes'
                                      ],
                                      "CWE (489) Active Debug Code",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Deserialization of Untrusted Data",
                                      29,
                                      Cwe.DESERIALIZATION_OF_UNTRUSTED_DATA,
                                      [
                                          r'pickle\.loads\(',  # Detects pickle deserialization
                                          r'pickle\.load\(',  # Detects pickle deserialization
                                          r'dill\.loads\(',  # Detects dill deserialization
                                          r'dill\.load\(',  # Detects dill deserialization
                                          r'shelve\.open\(',  # Detects shelve deserialization
                                          r'jsonpickle\.decode\(',  # Detects jsonpickle deserialization
                                          r'pandas\.read_pickle\(',  # Detects pandas read_pickle deserialization
                                          r'marshal\.loads\(',  # Detects marshal deserialization
                                          r'marshal\.load\(',  # Detects marshal deserialization
                                      ],
                                      "CWE (502) Deserialization of Untrusted Data, Category A08:2021 - Software and Data Integrity Failures",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Hardcoded Secret",
                                      30,
                                      Cwe.HARD_CODED_SECRET,
                                      [
                                          r'password\s*=\s*[\'"].*[\'"]',  # Detects hardcoded passwords
                                          r'api_key\s*=\s*[\'"].*[\'"]',  # Detects hardcoded API keys
                                          r'token\s*=\s*[\'"].*[\'"]',  # Detects hardcoded tokens
                                          r'secret\s*=\s*[\'"].*[\'"]',  # Detects hardcoded secrets
                                      ],
                                      "CWE (547) Use of Hard-coded, Security-relevant Constants, Category A05:2021 - Security Misconfiguration",
                                      "based on context"
                                      ))
        sets.append(build_blacklist(" Open Redirect",
                                      31,
                                      Cwe.OPEN_REDIRECT,
                                      [
                                          r'redirect\s*=\s*[\'"].*[\'"]',
                                          # Detects potential redirect parameter assignments
                                          r'redirect_url\s*=\s*[\'"].*[\'"]',
                                          # Detects potential redirect URL parameter assignments
                                          r'url\s*=\s*[\'"].*[\'"]',  # Detects potential URL parameter assignments
                                          r'location\s*=\s*[\'"].*[\'"]',
                                          # Detects potential location header assignments
                                          r'window\.location\s*=\s*[\'"].*[\'"]'
                                          # Detects potential JavaScript redirects
                                      ],
                                      "CWE (601) URL Redirection to Untrusted Site ('Open Redirect'), Category A01:2021 - Broken Access Control",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Insecure Xml Parser",
                                      32,
                                      Cwe.INSECURE_XML_PARSER,
                                      [
                                          r'xml\.etree\.cElementTree\.parse',  # cElementTree XML parsing
                                          r'xml\.etree\.ElementTree\.parse',  # ElementTree XML parsing
                                          r'xml\.sax\.parse',  # SAX XML parsing
                                          r'xml\.dom\.minidom\.parse',  # minidom XML parsing
                                          r'xml\.dom\.pulldom\.parse',  # pulldom XML parsing
                                          r'lxml\.etree\.parse',  # lxml XML parsing
                                          r'lxml\.etree\.fromstring',  # lxml XML parsing from string
                                          r'lxml\.etree\.RestrictedElement',  # lxml RestrictedElement parsing
                                          r'lxml\.etree\.GlobalParserTLS',  # lxml GlobalParserTLS parsing
                                          r'lxml\.etree\.getDefaultParser',  # lxml getDefaultParser parsing
                                          r'lxml\.etree\.check_docinfo',  # lxml check_docinfo parsing
                                      ],
                                      "CWE (611) Improper Restriction of XML External Entity Reference, Category A05:2021 - Security Misconfiguration",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Sensitive Cookie in HTTPS Session Without 'Secure' Attribute",
                                      33,
                                      Cwe.HTTPS_SESSION_WITHOUT_SECURE_ATTRIBUTE,
                                      [r"(?i)set-cookie:\s*(?!.*\bsecure\b)(?=.*\b(?:sessionid|auth|token)\b)"],
                                      "CWE (614) Sensitive Cookie in HTTPS Session Without 'Secure' Attribute,  Category A05:2021 - Security Misconfiguration",
                                      "based on context"
                                      ))
        sets.append(build_blacklist(" XPath Injection",
                                      34,
                                      Cwe.XPATH_INJECTION,
                                      [r'\.xpath\(\s*["\'][^"\']*{{user_input}}[^"\']*["\']\s*\)'],
                                      "CWE (643) Improper Neutralization of Data within XPath Expressions ('XPath Injection'), Category A03:2021 - Injection",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Insecure File Permissions",
                                      35,
                                      Cwe.INSECURE_FILE_PERMISSION,
                                      [r'os\.chmod\(|os\.chown\(|os\.umask\(|os\.open\(|open\(|os\.makedirs\(|shutil\.copy2\(|shutil\.move\(|os\.rename\(|tempfile\.mkstemp\(|tempfile\.NamedTemporaryFile\(|tempfile\.TemporaryFile\(|os\.fdopen\(|os\.lchown\(|os\.chmod\(|os\.fchmod\(|os\.lchmod\(|os\.open\(|os\.mknod\(|os\.mmap\(|os\.utime\('],
                                      "CWE (732) Incorrect Permission Assignment for Critical Resource",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Selection of Less-Secure Algorithm During Negotiation (SSL instead of TLS)",
                                      36,
                                      Cwe.MISSING_PROTOCOL_SSL,
                                      [r'ssl\.(PROTOCOL_SSLv23|SSLContext|wrap_socket|create_default_context|_create_unverified_context)'],
                                      "CWE (757) Selection of Less-Secure Algorithm During Negotiation ('Algorithm Downgrade'),  Category A02:2021 - Cryptographic Failures",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Use of Password Hash With Insufficient Computational Effort",
                                      37,
                                      Cwe.PASSWORD_HASH_WITHOUT_SUFFICIENT_COMPUTATION,
                                      [
                                          r'crypt\.(crypt|crypt_sha256|crypt_sha512)|hashlib\.(md5|sha1)',
                                          # Basic hashing functions
                                          r'bcrypt\.(hashpw|gensalt)',  # bcrypt hashing functions
                                          r'argon2\.(hash_password|Hasher\.hash\(|PasswordHasher\()',
                                          # Argon2 hashing functions
                                          r'scrypt\.(hash|encrypt)',  # scrypt hashing functions
                                          r'passlib\.(hash|pwd\.)',  # passlib hashing functions
                                          r'\bPBKDF2\b',  # PBKDF2 hashing function
                                          r'\bsha256_crypt\b',  # sha256_crypt hashing function
                                          r'\bsha512_crypt\b',  # sha512_crypt hashing function
                                          r'\bmd5_crypt\b',  # md5_crypt hashing function
                                          r'\bsha1_crypt\b',  # sha1_crypt hashing function
                                          r'\bsha256_pbkdf2\b',  # sha256_pbkdf2 hashing function
                                          r'\bsha512_pbkdf2\b',  # sha512_pbkdf2 hashing function
                                          r'\bargon2_cffi\b',  # argon2_cffi hashing function
                                          r'\bpycryptodome\.(pbkdf2|hashers)\b',  # pycryptodome hashing functions
                                          r'\bpy-bcrypt\b',  # py-bcrypt hashing function
                                      ],
                                      "CWE (916) Use of Password Hash With Insufficient Computational Effort, Category A02:2021 - Cryptographic Failures",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Server-Side Request Forgery (SSRF)",
                                      38,
                                      Cwe.SERVER_SIDE_REQUEST_FORGERY,
                                      [
                                          r'\burllib\.request\.(urlopen|urlretrieve|URLopener|FancyURLopener)|\brequests\.(get|head|post|put|patch|delete)',
                                          # urllib and requests library usage for making HTTP requests
                                          r'\bhttplib2\.Http\.request|tornado\.httpclient\.HTTPClient\.fetch|aiohttp\.ClientSession\.(get|post|put|patch|delete)',
                                          # HTTP client libraries usage
                                          r'\bhttp\.client\.HTTPConnection\.request|http\.client\.HTTPSConnection\.request',
                                          # HTTP client usage in Python 3
                                          r'\bsocket\.socket\.connect\b',  # Direct socket connection attempt
                                          r'\bparamiko\.SSHClient\.connect\b',  # SSH client connection attempt
                                          r'\bfabric\.Connection\.connect\b',  # Fabric library SSH connection attempt
                                          r'\bparamiko\.SFTPClient\.from_transport\b',
                                          # Paramiko SFTP connection attempt
                                          r'\bsocketserver\.(TCPServer|UDPServer)\b',  # Socket server creation
                                      ],
                                      "CWE (918) Server-Side Request Forgery (SSRF),  Category A10:2021 - Server-Side Request Forgery (SSRF)",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("NoSQL Injection",
                                      39,
                                      Cwe.NOSQL_INJECTION,
                                      [
                                          r'\bfind_one\b',  # MongoDB find_one method
                                          r'\bfind\b',  # MongoDB find method
                                          r'\bfind_and_modify\b',  # MongoDB find_and_modify method
                                          r'\baggregate\b',  # MongoDB aggregate method
                                          r'\bupdate\b',  # MongoDB update method
                                          r'\bremove\b',  # MongoDB remove method
                                          r'\bdelete_one\b',  # MongoDB delete_one method
                                          r'\bdelete_many\b',  # MongoDB delete_many method
                                          r'\binsert\b',  # MongoDB insert method
                                          r'\binsert_one\b',  # MongoDB insert_one method
                                          r'\binsert_many\b',  # MongoDB insert_many method
                                          r'\breplace_one\b',  # MongoDB replace_one method
                                          r'\bdistinct\b',  # MongoDB distinct method
                                          r'\bmap_reduce\b',  # MongoDB map_reduce method
                                          r'\bdatabase\.query\b',  # Generic database query method
                                          r'\bdatabase\.execute\b',  # Generic database execute method
                                          r'\bexecute_query\b',  # Generic execute_query method
                                      ],
                                      "CWE (943) Improper Neutralization of Special Elements in Data Query Logic",
                                      "based on context"
                                      ))
        sets.append(build_blacklist("Sensitive Cookie Without 'HttpOnly' Flag",
                                      40,
                                      Cwe.SENSITIVE_COOKIE_HTTPONLY_FLAG,
                                      [
                                          r'\bset_cookie\([^\)]*HttpOnly\b',  # Cookie setting with HttpOnly flag
                                          r'\bSet-Cookie:.*HttpOnly\b',  # HTTP response header with HttpOnly flag
                                      ],
                                      "CWE (1004) Sensitive Cookie Without 'HttpOnly' Flag, Category A05:2021 - Security Misconfiguration",
                                      "based on context"
                                      ))
        sets.append(build_blacklist(" Python 2 source code",
                                      41,
                                      Cwe.UNMAINTAINED_THIRD_PARTY_COMPONENTS,
                                      [
                                          r'\bimport\s+unmaintained_module\b',
                                          # Import statement for the unmaintained module
                                          r'\bfrom\s+unmaintained_package\b',
                                          # Import statement for the unmaintained package
                                          r'\bunmaintained_module\b',  # Direct reference to the unmaintained module
                                          r'\bunmaintained_package\b',  # Direct reference to the unmaintained package
                                          r'\brequire\(\'unmaintained_package\'\)',
                                          # JavaScript require statement for the unmaintained package
                                          r'\bimport \(require\("unmaintained_package"\)\)',
                                          # ES6 import statement for the unmaintained package
                                      ],
                                      "CWE (1104) Use of Unmaintained Third Party Components, Category A06:2021 - Vulnerable and Outdated Components",
                                      "based on context"

                                      ))
        return sets

    def full_blacklist(self):
        blist = self.gen_blacklist()
        result = {item['name']: item for item in blist}
        return result


# tester function:

# instance = Blacklist_2()
# blist = instance.gen_blacklist()
# blacklist = instance.full_blacklist()
# print(blist)