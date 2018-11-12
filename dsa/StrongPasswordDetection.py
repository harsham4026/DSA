import re

def is_strong_password(password):
  if re.match(r'([a-zA-z0-9_.*&%$#@]).{8,}', password):
    print('strong password')
  else:
    print('weak password. Consider changing it!!')

if __name__ == '__main__':
    password = "Harsha1@#"
    is_strong_password(password)