import http.server
import socketserver
import os
import urllib.parse

PORT = int(os.environ.get("PORT", 8000))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, "pdfs")
POSTS_FOLDER = os.path.join(BASE_DIR, "posts")

if not os.path.exists(POSTS_FOLDER):
    os.makedirs(POSTS_FOLDER)


class BlogHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        # --------- EDITOR ----------
        if self.path == "/editor":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            html = """
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Editor - Pibes Lectores</title>
                <style>
                    body {font-family:Arial;background:#f4f4f4;padding:40px;}
                    input, textarea {
                        width:100%;
                        padding:10px;
                        margin:10px 0;
                        font-size:16px;
                    }
                    button {
                        padding:10px 20px;
                        background:#2c3e50;
                        color:white;
                        border:none;
                        cursor:pointer;
                    }
                </style>
            </head>
            <body>
                <h1>Nuevo Post</h1>
                <form method="POST" action="/guardar_post">
                    <input type="text" name="titulo" placeholder="Título" required>
                    <textarea name="contenido" rows="15" placeholder="Escribí tu texto..." required></textarea>
                    <button type="submit">Publicar</button>
                </form>
                <p><a href="/">← Volver</a></p>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
            return

        # --------- VER POST ----------
        if self.path.startswith("/post/"):
            slug = self.path.replace("/post/", "")
            archivo = os.path.join(POSTS_FOLDER, slug + ".html")

            if os.path.exists(archivo):
                with open(archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()

                html = f"""
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>{slug}</title>
                    <style>
                        body {{
                            font-family:Georgia;
                            max-width:800px;
                            margin:60px auto;
                            line-height:1.8;
                            font-size:20px;
                        }}
                        a {{text-decoration:none;color:#2c3e50;}}
                    </style>
                </head>
                <body>
                    <a href="/">← Volver</a>
                    <h1>{slug.replace('-', ' ')}</h1>
                    {contenido}
                </body>
                </html>
                """

                self.wfile.write(html.encode("utf-8"))
                return

        # --------- HOME ----------
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            posts = [f.replace(".html", "") for f in os.listdir(POSTS_FOLDER)]

            html = """
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Pibes Lectores</title>
                <style>
                    body {font-family:Arial;background:#f4f4f4;margin:0;}
                    header {background:#2c3e50;color:white;padding:40px;text-align:center;}
                    .container {max-width:800px;margin:40px auto;}
                    .post {background:white;padding:20px;margin-bottom:20px;border-radius:8px;}
                    a {text-decoration:none;color:#2c3e50;}
                    footer {text-align:center;padding:20px;background:#2c3e50;color:white;margin-top:60px;}
                </style>
            </head>
            <body>
                <header>
                    <h1>Pibes Lectores</h1>
                    <p>Una Vaga Idea de Crear</p>
                </header>
                <div class="container">
            """

            for post in posts:
                html += f"""
                <div class="post">
                    <h2><a href="/post/{post}">{post.replace('-', ' ')}</a></h2>
                </div>
                """

            html += """
                </div>
                <footer>
                    <a href="/editor" style="color:white;">✍️ Escribir nuevo post</a>
                </footer>
            </body>
            </html>
            """

            self.wfile.write(html.encode("utf-8"))
            return

        super().do_GET()

    def do_POST(self):

        if self.path == "/guardar_post":

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = urllib.parse.parse_qs(post_data.decode("utf-8"))

            titulo = params["titulo"][0]
            contenido = params["contenido"][0]

            slug = titulo.lower().replace(" ", "-")
            archivo = os.path.join(POSTS_FOLDER, slug + ".html")

            with open(archivo, "w", encoding="utf-8") as f:
                f.write(f"<p>{contenido.replace(chr(10), '</p><p>')}</p>")

            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()


with socketserver.TCPServer(("0.0.0.0", PORT), BlogHandler) as httpd:
    print(f"Servidor funcionando en puerto {PORT}")
    httpd.serve_forever()
