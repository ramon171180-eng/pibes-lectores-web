import http.server
import socketserver
import feedparser
import os
import urllib.parse

PORT = int(os.environ.get("PORT", 8000))
BLOG_RSS = "https://pibeslectores.blogspot.com/feeds/posts/default?alt=rss"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, "pdfs")


class BlogHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        # ==============================
        # VISOR DE PDF
        # ==============================
        if self.path.startswith("/ver_pdf"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)

            if "archivo" in params:
                archivo = params["archivo"][0]
                ruta_pdf = os.path.join(PDF_FOLDER, archivo)

                if os.path.exists(ruta_pdf):

                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()

                    html = f"""
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>{archivo}</title>
                        <style>
                            body {{
                                margin: 0;
                                font-family: 'Segoe UI', sans-serif;
                                background: linear-gradient(135deg, #eef2f3, #dfe9f3);
                                text-align: center;
                            }}
                            .visor-container {{
                                width: 90%;
                                margin: 40px auto;
                            }}
                            iframe {{
                                width: 100%;
                                height: 85vh;
                                border: none;
                                border-radius: 15px;
                                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                            }}
                            .volver {{
                                display: inline-block;
                                margin: 25px;
                                padding: 12px 25px;
                                background: #2a5298;
                                color: white;
                                text-decoration: none;
                                border-radius: 8px;
                                transition: 0.3s;
                            }}
                            .volver:hover {{
                                background: #1e3c72;
                            }}
                        </style>
                    </head>
                    <body>

                        <a class="volver" href="/">← Volver al sitio</a>

                        <div class="visor-container">
                            <iframe src="/pdfs/{archivo}"></iframe>
                        </div>

                    </body>
                    </html>
                    """

                    self.wfile.write(html.encode("utf-8"))
                    return

        # ==============================
        # PÁGINA PRINCIPAL
        # ==============================
        if self.path == "/":

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            feed = feedparser.parse(BLOG_RSS)

            if os.path.exists(PDF_FOLDER):
                pdf_files = [
                    f for f in os.listdir(PDF_FOLDER)
                    if f.lower().endswith(".pdf")
                ]
            else:
                pdf_files = []

            html = """
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Pibes Lectores - Independiente</title>
                <style>
                    body {
                        margin: 0;
                        font-family: 'Segoe UI', sans-serif;
                        background: linear-gradient(135deg, #eef2f3, #dfe9f3);
                        color: #2c3e50;
                    }

                    header {
                        background: linear-gradient(90deg, #1e3c72, #2a5298);
                        color: white;
                        padding: 60px 20px;
                        text-align: center;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                    }

                    header h1 {
                        margin: 0;
                        font-size: 42px;
                        letter-spacing: 2px;
                    }

                    header p {
                        opacity: 0.9;
                        margin-top: 10px;
                        font-style: italic;
                    }

                    .container {
                        max-width: 900px;
                        margin: 60px auto;
                        padding: 0 20px;
                    }

                    .post {
                        background: white;
                        padding: 25px;
                        margin-bottom: 30px;
                        border-radius: 15px;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                    }

                    .post:hover {
                        transform: translateY(-5px);
                        box-shadow: 0 12px 25px rgba(0,0,0,0.1);
                    }

                    .post h2 {
                        margin-top: 0;
                    }

                    .post a {
                        color: #2a5298;
                        font-weight: bold;
                        text-decoration: none;
                    }

                    .post a:hover {
                        text-decoration: underline;
                    }

                    .section {
                        background: white;
                        padding: 50px 30px;
                        margin: 80px auto;
                        border-radius: 20px;
                        text-align: center;
                        max-width: 900px;
                        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
                    }

                    .pdf-list a {
                        display: inline-block;
                        margin: 10px;
                        padding: 10px 18px;
                        background: #2a5298;
                        color: white;
                        border-radius: 8px;
                        text-decoration: none;
                        transition: background 0.3s ease;
                    }

                    .pdf-list a:hover {
                        background: #1e3c72;
                    }

                    footer {
                        text-align: center;
                        padding: 30px;
                        background: #1e3c72;
                        color: white;
                        margin-top: 80px;
                        font-size: 14px;
                        letter-spacing: 1px;
                    }

                    img {
                        transition: transform 0.4s ease;
                    }

                    img:hover {
                        transform: scale(1.03);
                    }
                </style>
            </head>
            <body>

            <header>
                <h1>Pibes Lectores</h1>
                <p>Una Vaga Idea de Crear</p>
            </header>

            <div class="container">
            """

            for entry in feed.entries[:5]:
                html += f"""
                <div class="post">
                    <h2>{entry.title}</h2>
                    <small>{entry.published}</small>
                    <p>{entry.summary}</p>
                    <p><a href="{entry.link}" target="_blank">Leer entrada completa →</a></p>
                </div>
                """

            html += "</div>"

            html += """
            <div class="section">
                <img src="/Arte_En_La_Cabeza.jpg" style="max-width:100%; border-radius:15px;">
                <div style="margin-top:20px; font-style:italic; font-size:18px;">
                    Arte en acción
                </div>
            </div>
            """

            html += """
            <div class="section">
                <h2>Biblioteca en PDF</h2>
                <div class="pdf-list">
            """

            for pdf in pdf_files:
                html += f'<a href="/ver_pdf?archivo={pdf}">📄 {pdf}</a>'

            if not pdf_files:
                html += "<p>No hay archivos PDF disponibles.</p>"

            html += """
                </div>
            </div>

            <footer>
                &copy; 2026 Pibes Lectores
            </footer>

            </body>
            </html>
            """

            self.wfile.write(html.encode("utf-8"))
            return

        super().do_GET()


with socketserver.TCPServer(("0.0.0.0", PORT), BlogHandler) as httpd:
    print(f"Servidor funcionando en puerto {PORT}")
    httpd.serve_forever()
