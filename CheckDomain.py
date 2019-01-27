import http.client
import re

class CheckDomain:
  def isEmailDomainBlackListed(self, email):
    domain = re.search(r'(@((\w+\.*)+))', email).group(2)
    conn = http.client.HTTPSConnection("api.apility.net")
    headers = {
      'x-auth-token': "89faa9a5-b9a3-4112-b742-5844e49d5e2f",
    }
    conn.request("GET", "/baddomain/" + domain, headers=headers)
    res = conn.getresponse()
    if res.code == 200:
      return True
    else:
      return False
