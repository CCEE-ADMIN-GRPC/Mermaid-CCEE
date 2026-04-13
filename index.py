import subprocess
import tempfile
import os
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.post("/render-diagram")
async def render_diagram(request: Request):
    # 1. Recebe o código do diagrama do Coda
    codigo_diagrama = await request.body()
    
    # 2. Cria arquivos temporários para o input (.d2) e output (.svg)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".d2") as f_in, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".svg") as f_out:
        
        f_in.write(codigo_diagrama)
        f_in.flush()
        
        try:
            # 3. Chama o CLI do D2 para gerar o SVG
            # Aqui você pode injetar temas: d2 --theme=200
            subprocess.run(["d2", f_in.name, f_out.name], check=True)
            
            # 4. Lê o SVG gerado
            with open(f_out.name, "r", encoding="utf-8") as svg_file:
                svg_content = svg_file.read()
                
            # 5. Retorna o SVG puro
            return Response(content=svg_content, media_type="image/svg+xml")
            
        except subprocess.CalledProcessError:
            return Response(content="Erro ao renderizar diagrama", status_code=500)
        finally:
            # Limpa os arquivos temporários do servidor
            os.remove(f_in.name)
            os.remove(f_out.name)
