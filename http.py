# File: my_http.py
import os.path
from glob import glob
from datetime import datetime

class HttpServer:
    def __init__(self):
        self.sessions = {}
        self.types = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.txt': 'text/plain',
            '.html': 'text/html'
        }

    def response(self, kode=404, message='Not Found', messagebody=bytes(), headers={}):
        tanggal = datetime.now().strftime('%c')
        resp = [
            f"HTTP/1.0 {kode} {message}\r\n",
            f"Date: {tanggal}\r\n",
            "Connection: close\r\n",
            "Server: myserver/1.0\r\n",
            f"Content-Length: {len(messagebody)}\r\n"
        ]
        for kk in headers:
            resp.append(f"{kk}:{headers[kk]}\r\n")
        resp.append("\r\n")

        response_headers = ''.join(resp)
        if type(messagebody) is not bytes:
            messagebody = messagebody.encode()

        return response_headers.encode() + messagebody

    def proses(self, data):
        requests = data.split("\r\n")
        baris = requests[0]
        all_headers = [n for n in requests[1:] if n != '']

        try:
            method, object_address, *_ = baris.split()
            method = method.upper().strip()
            if method == 'GET':
                return self.http_get(object_address, all_headers)
            elif method == 'POST':
                return self.http_post(object_address, all_headers)
            else:
                return self.response(400, 'Bad Request', '', {})
        except:
            return self.response(400, 'Bad Request', '', {})

    def http_get(self, object_address, headers):
        files = glob('./*')
        thedir = './'

        if object_address == '/':
            return self.response(200, 'OK', 'Ini Adalah Web Server Percobaan', {})

        if object_address == '/video':
            return self.response(302, 'Found', '', {'location': 'https://youtu.be/katoxpnTf04'})

        if object_address == '/santai':
            return self.response(200, 'OK', 'santai saja', {})

        if object_address == '/status':
            try:
                with open("status.txt", "r") as f:
                    isi = f.read()
            except:
                isi = "Status file not found."
            return self.response(200, 'OK', isi, {'Content-type': 'text/plain'})

        object_address = object_address[1:]  # hapus '/' di awal
        filepath = thedir + object_address
        if filepath not in files:
            return self.response(404, 'Not Found', '', {})

        with open(filepath, 'rb') as fp:
            isi = fp.read()

        fext = os.path.splitext(filepath)[1]
        content_type = self.types.get(fext, 'application/octet-stream')
        return self.response(200, 'OK', isi, {'Content-type': content_type})

    def http_post(self, object_address, headers):
        return self.response(200, 'OK', 'kosong', {'Content-type': 'text/plain'})