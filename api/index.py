from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
import re

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse parameter dari URL
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        # Ambil User-Agent dari query ?ua=... atau dari header
        user_agent = query_params.get('ua', [self.headers.get('User-Agent', '')])[0]

        # Logika Deteksi Cerdas Berdasarkan Pola Umum User-Agent & Kode Model (misal: SM-S921B)
        brand = "Unknown"
        model = "Smart Device"
        
        ua_lower = user_agent.lower()
        
        # Deteksi Samsung & Mapping Kode Model Umum
        if "samsung" in ua_lower or "sm-" in ua_lower or "sec" in ua_lower:
            brand = "Samsung"
            if "sm-s921" in ua_lower or "s921" in ua_lower:
                model = "Galaxy S24"
            elif "sm-s928" in ua_lower or "s928" in ua_lower:
                model = "Galaxy S24 Ultra"
            elif "sm-s911" in ua_lower or "s911" in ua_lower:
                model = "Galaxy S23"
            elif "sm-a556" in ua_lower:
                model = "Galaxy A55"
            else:
                # Ambil kode SM-xxxx jika ada
                sm_match = re.search(r'(sm-[a-z0-9]+)', ua_lower)
                model = sm_match.group(1).upper() if sm_match else "Galaxy Device"

        # Deteksi Xiaomi / Redmi / Poco
        elif "xiaomi" in ua_lower or "redmi" in ua_lower or "poco" in ua_lower or "mifw" in ua_lower:
            brand = "Xiaomi"
            if "note 14" in ua_lower:
                model = "Redmi Note 14"
            elif "poco x6" in ua_lower:
                model = "Poco X6"
            else:
                model = "Redmi / Xiaomi Device"

        # Deteksi Oppo / Realme / Vivo
        elif "oppo" in ua_lower:
            brand = "Oppo"
            model = "Oppo Device"
        elif "realme" in ua_lower:
            brand = "Realme"
            model = "Realme Device"
        elif "vivo" in ua_lower:
            brand = "Vivo"
            model = "Vivo Device"
        elif "iphone" in ua_lower or "ipad" in ua_lower:
            brand = "Apple"
            model = "iPhone / iOS Device"
        else:
            # Fallback jika tidak dikenali, ambil potongan string dari UA
            match = re.search(r'\(([^)]+)\)', user_agent)
            if match:
                model = match.group(1).split(';')[0][:30] # Ambil info dalam kurung pertama

        # URL Gambar Badge / Logo Inisial Profesional yang anti 404
        image_url = f"https://ui-avatars.com/api/?name={brand}&size=512&background=0D1117&color=00E5FF&bold=true&format=png&rounded=true"

        response_data = {
            "error": False,
            "deviceBrand": brand,
            "model": model,
            "image_url": image_url,
            "userAgent": user_agent
        }

        # Kirim header respons JSON
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(response_data, indent=4).encode('utf-8'))
        return
