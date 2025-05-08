import os
import re

def extract_logs(input_file, output_file):
  input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_file)
  print(f"Input file path: {input_file_path}") # デバッグメッセージ

  with open(input_file_path, 'r') as input_log, open(output_file, 'w') as output_log:
      for line in input_log:
          match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) INFO sqlalchemy\.engine\.Engine.*?\(\'([^\']+)\',\)', line, re.DOTALL)
          if match:
              timestamp = match.group(1)
              user_identifier = match.group(2)
              output_log.write(f"{timestamp} {user_identifier}\n")

if __name__ == "__main__":
  input_filename = "error.log"
  output_filename = "access_user.log"
  extract_logs(input_filename, output_filename)
