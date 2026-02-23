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
                                font-family: 'Georgia', serif;
                                background: #f8f6f2;
                                animation: fadeIn 1s ease-in-out;
                            }}

                            @keyframes fadeIn {{
                                from {{ opacity: 0; }}
                                to {{ opacity: 1; }}
                            }}

                            .volver {{
                                display: inline-block;
                                margin: 30px;
                                padding: 12px 25px;
                                background: #2c3e50;
                                color: white;
                                text-decoration: none;
                                border-radius: 6px;
                                transition: 0.3s;
                            }}

                            .volver:hover {{
                                background: #1a252f;
                            }}

                            iframe {{
                                width: 90%;
                                height: 85vh;
                                border: none;
                                border-radius: 10px;
                                box-shadow: 0 10px 30px rgba(0,0,0,0.15);
                            }}
                        </style>
                    </head>
                    <body>

                        <a class="volver" href="/">← Volver al sitio</a>

                        <div style="text-align:center;">
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
                <title>Pibes Lectores</title>

                <style>

                    body {
                        margin: 0;
                        font-family: 'Georgia', serif;
                        background: #f8f6f2;
                        color: #2c3e50;
                        overflow-x: hidden;
                    }

                    header {
                        padding: 100px 20px;
                        text-align: center;
                        background: #ffffff;
                        animation: slideDown 1.2s ease-out;
                    }

                    header h1 {
                        font-size: 48px;
                        margin: 0;
                        letter-spacing: 3px;
                    }

                    header p {
                        font-style: italic;
                        margin-top: 15px;
                        font-size: 18px;
                        opacity: 0.7;
                    }

                    @keyframes slideDown {
                        from {
                            transform: translateY(-40px);
                            opacity: 0;
                        }
                        to {
                            transform: translateY(0);
                            opacity: 1;
                        }
                    }

                    .container {
                        max-width: 900px;
                        margin: 60px auto;
                        padding: 0 20px;
                    }

                    .post {
                        background: white;
                        padding: 35px;
                        margin-bottom: 40px;
                        border-radius: 6px;
                        box-shadow: 0 15px 40px rgba(0,0,0,0.05);
                        opacity: 0;
                        transform: translateY(30px);
                        animation: fadeUp 1s ease forwards;
                    }

                    .post:nth-child(1) { animation-delay: 0.2s; }
                    .post:nth-child(2) { animation-delay: 0.4s; }
                    .post:nth-child(3) { animation-delay: 0.6s; }
                    .post:nth-child(4) { animation-delay: 0.8s; }
                    .post:nth-child(5) { animation-delay: 1s; }

                    @keyframes fadeUp {
                        to {
                            opacity: 1;
                            transform: translateY(0);
                        }
                    }

                    .post h2 {
                        margin-top: 0;
                    }

                    .post a {
                        text-decoration: none;
                        color: #34495e;
                        font-weight: bold;
                    }

                    .post a:hover {
                        text-decoration: underline;
                    }

                    .section {
                        background: white;
                        padding: 60px 30px;
                        margin: 100px auto;
                        text-align: center;
                        max-width: 900px;
                        box-shadow: 0 20px 50px rgba(0,0,0,0.06);
                        opacity: 0;
                        transform: translateY(40px);
                        animation: fadeUp 1.2s ease forwards;
                        animation-delay: 1.2s;
                    }

                    img {
                        max-width: 100%;
                        border-radius: 8px;
                        transition: transform 0.4s ease;
                    }

                    img:hover {
                        transform: scale(1.04);
                    }

                    .pdf-list a {
                        display: block;
                        margin: 12px 0;
                        padding: 12px;
                        text-decoration: none;
                        color: #2c3e50;
                        border-bottom: 1px solid #ddd;
                        transition: 0.3s;
                    }

                    .pdf-list a:hover {
                        background: #f0ece6;
                    }

                    footer {
                        text-align: center;
                        padding: 40px;
                        margin-top: 100px;
                        background: #ffffff;
                        font-size: 14px;
                        opacity: 0.6;
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
                <img src="/Arte_En_La_Cabeza.jpg">
                <div style="margin-top:20px; font-style:italic; font-size:20px;">
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
