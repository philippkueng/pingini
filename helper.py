import re

# INPUT :: http://www.sample.co.uk:8080/folder/file.htm
# OUTPUT :: http://www.sample.co.uk:8080
def get_application_base_url(current_url):
  regex = '(https?://[-\w\.]+(:[0-9]{4})?)'
  match = re.search(regex, current_url)
  if match:
    return match.group(1)
  else:
    return None