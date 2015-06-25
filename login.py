import urllib
import urlparse
import BaseHTTPServer
import webbrowser
import facebook
import ssl


APP_ID = "370621549793415"
APP_SECRET = "908cc56f67aefe0144f3170039782c84"

CODE_URL = "https://www.facebook.com/dialog/oauth?"
TOKEN_URL = "https://graph.facebook.com/oauth/access_token?"
REDIRECT_URL = "https://localhost:8080/"
PERMISSIONS = [
               "read_stream",
               "user_status",
               #"friends_status",
               "user_friends",
               "user_groups",
					"user_photos"
               ]

CODE_ARGS = {
   "client_id":APP_ID,
   "redirect_uri":REDIRECT_URL,
   "scope":','.join(PERMISSIONS)
   }

access_token = None
error = False

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
   def do_GET(self):
      global access_token,error
      
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      
      code = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('code')
      if code is None:
         error = True
         return
      
      token_args = CODE_ARGS
      token_args["client_secret"] = APP_SECRET
      token_args["code"] = code[0]
      
      token_request = TOKEN_URL + urllib.urlencode(token_args)
      response = urllib.urlopen(token_request).read()
      response_dict = urlparse.parse_qs(response)
      access_token = response_dict["access_token"][-1]
      self.wfile.write("You have successfully logged into facebook. You can close this window now.")
   
   # Ensures
   def log_request(self, code='-', size='-'):
      pass

def login():
   global access_token,error
   
   redirect_uri = urlparse.urlparse(CODE_ARGS["redirect_uri"])
   server_params = (redirect_uri.hostname,redirect_uri.port)
   httpd = BaseHTTPServer.HTTPServer(server_params, RequestHandler)
   httpd.socket = ssl.wrap_socket (httpd.socket, certfile='server.pem', server_side=True)

   code_request = CODE_URL + urllib.urlencode(CODE_ARGS)
   webbrowser.open(code_request, new=1)
   while not access_token and not error:
      try:
         httpd.handle_request()
      except:
         error = True
   return access_token

#if __name__=="__main__":
#   execute()
