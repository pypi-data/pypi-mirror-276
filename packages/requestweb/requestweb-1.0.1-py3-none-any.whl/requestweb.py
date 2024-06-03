import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtCore import QUrl, QEventLoop, QSize
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import ssl
import socket
import whois
from datetime import datetime
import requests
from urllib.parse import urlparse
import base64

class CustomWebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.enable_logs = False

    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        if self.enable_logs:
            print(f"[{level}] {message} (line {line_number}, {source_id})")

class WebLoader(QWebEnginePage):
    def __init__(self, url, show_gui=False, enable_js=True, auto_close=True):
        super().__init__()
        self.auto_close = auto_close
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, enable_js)
        self.html = None
        self.loadFinished.connect(self.handle_load_finished)
        if show_gui:
            self.view = CustomWebEngineView()
            self.setView(self.view)
            self.window = QMainWindow()
            self.window.setWindowTitle("RequestWeb")
            self.window.setFixedSize(QSize(500, 500))
            self.window.setCentralWidget(self.view)
            self.window.show()
        self.load(QUrl(url))

    def handle_load_finished(self, success):
        if success:
            self.toHtml(self.handle_html)
        else:
            print("Failed to load page.")

    def handle_html(self, html):
        self.html = html
        if self.auto_close:
            QApplication.instance().quit()

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        pass

def load_url(url, enable_logs=False, enable_js=True, show_gui=False, auto_close=True):
    try:
        app = QApplication(sys.argv)
        loader = WebLoader(url, show_gui, enable_js, auto_close)
        if show_gui:
            loader.view.enable_logs = enable_logs
        loop = QEventLoop()
        app.aboutToQuit.connect(loop.quit)
        loop.exec_()
        return loader.html
    except Exception as e:
        return f"An error occurred: {e}"


def getTitle(url):
    try:
        htmltitle = load_url(url, enable_logs=False, enable_js=True, show_gui=False, auto_close=True)
        if htmltitle:
            soup = BeautifulSoup(htmltitle, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.get_text()
            else:
                return "No title found"
        else:
            return "Failed to retrieve HTML"
    except Exception as e:
        return f"An error occurred: {e}"
    


def getFavicon(url):
    try:
        google_favicon_url = "https://www.google.com/s2/favicons?domain="
        domain = urlparse(url).netloc
        favicon_url = f"{google_favicon_url}{domain}"

        # Send a request to the favicon URL
        response = requests.get(favicon_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Get the image data as bytes
            image_data = response.content

            # Encode the image data as a UTF-8 string
            image_data_utf8 = base64.b64encode(image_data).decode('utf-8')

            return "data:image/png;base64," + image_data_utf8
        else:
            return f"Error: Failed to retrieve favicon (status code {response.status_code})"

    except Exception as e:
        return f"An error occurred: {e}"
    
def get_ssl_details(url):
    try:
        hostname = urlparse(url).hostname
        if hostname is None:
            raise ValueError("Invalid URL provided")
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

                # Get certificate expiration date
                expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                is_expired = expiry_date < datetime.utcnow()

                # Get issuer
                issuer = dict(x[0] for x in cert['issuer'])
                issuer_common_name = issuer.get('commonName')

                return {
                    'safe': not is_expired,
                    'expires': expiry_date,
                    'issuer': issuer_common_name,
                }
    except socket.gaierror:
        return {"error": "Invalid hostname or network issue"}
    except ssl.SSLError as e:
        return {"error": f"SSL error: {e}"}
    except Exception as e:
        return {"error": str(e)}
