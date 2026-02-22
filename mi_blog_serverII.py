import http.server
import socketserver
import feedparser
import os
import urllib.parse

PORT = 8000
BLOG_RSS = "https://pibeslectores.blogspot.com/feeds/posts/default?alt=rss"
PDF_FOLDER = "pdfs"


class BlogHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        # --------- VISOR DE PDF ----------
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
                                margin:0;
                                font-family:Arial;
                                background:#f4f4f4;
                                text-align:center;
                            }}
                            .visor-container {{
                                width:90%;
                                margin:30px auto;
                            }}
                            iframe {{
                                width:100%;
                                height:80vh;
                                border:none;
                                border-radius:10px;
                                box-shadow:0 4px 10px rgba(0,0,0,0.1);
                            }}
                            .volver {{
                                display:inline-block;
                                margin:20px;
                                padding:10px 20px;
                                background:#2c3e50;
                                color:white;
                                text-decoration:none;
                                border-radius:6px;
                            }}
                            .volver:hover {{
                                background:#34495e;
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

        # --------- PÁGINA PRINCIPAL ----------
        if self.path == "/":

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            feed = feedparser.parse(BLOG_RSS)

            if os.path.exists(PDF_FOLDER):
                pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
            else:
                pdf_files = []

            html = """
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Pibes Lectores - Independiente</title>
                <style>
                    body {font-family:Arial;background:#f4f4f4;margin:0;}
                    header {background:#2c3e50;color:white;padding:30px;text-align:center;}
                    .container {max-width:900px;margin:40px auto;}
                    .post {background:white;padding:20px;margin-bottom:20px;border-radius:8px;}
                    .section {
                        background:white;
                        padding:40px 20px;
                        margin:60px auto;
                        text-align:center;
                        border-radius:10px;
                        max-width:900px;
                        box-shadow:0 4px 10px rgba(0,0,0,0.08);
                    }
                    .pdf-list a {
                        display:block;
                        margin:10px 0;
                        text-decoration:none;
                        color:#2980b9;
                        font-weight:bold;
                    }
                    .pdf-list a:hover {text-decoration:underline;}
                    footer {text-align:center;padding:25px;background:#2c3e50;color:white;margin-top:60px;}
                </style>
            </head>
            <body>

            <header>
                <h1>Pibes Lectores</h1>
                <p>Una Vaga Idea de Crear</p>
            </header>

            <div class="container">
            """

            # POSTS
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

            # SECCIÓN ARTÍSTICA
            html += """
            <div class="section">
                <img src="Arte_En_La_Cabeza.jpg" style="max-width:100%; border-radius:12px;">
                <div style="margin-top:15px; font-style:italic;">Arte en acción</div>
            </div>
            """

            # BIBLIOTECA PDF
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

        # Archivos estáticos (como /pdfs/archivo.pdf)
        super().do_GET()


with socketserver.TCPServer(("", PORT), BlogHandler) as httpd:
    print(f"Servidor funcionando en http://localhost:{PORT}")
    httpd.serve_forever()