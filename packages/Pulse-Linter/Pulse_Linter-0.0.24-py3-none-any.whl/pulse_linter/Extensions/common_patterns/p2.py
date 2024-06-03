
import re

pattern = r'\.xpath\(\s*["\'][^"\']*{{user_input}}[^"\']*["\']\s*\)'
compiled_pattern = re.compile(pattern)

print(compiled_pattern)