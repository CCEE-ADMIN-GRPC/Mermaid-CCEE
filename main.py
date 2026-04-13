import subprocess
import tempfile
import os
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.post("/render-diagram")
async def render_diagram(request: Request):
    # 1. Garante que o texto vindo do Coda seja lido perfeitamente
    body_bytes = await request.body()
    codigo_texto = body_bytes.decode("utf-8")
    
    # 2. Cria arquivos temporários de forma mais segura para o Linux
    fd_in, path_in = tempfile.mkstemp(suffix=".d2")
    fd_out, path_out = tempfile.mkstemp(suffix=".svg")
    
    try:
        # 3. Escreve o código no arquivo de entrada
        with open(path_in, "w", encoding="utf-8") as f_in:
            f_in.write(codigo_texto)
        
        # 4. Roda o D2 e captura qualquer erro para mostrar no log
        resultado = subprocess.run(
            ["./bin/d2", path_in, path_out],
            capture_output=True, text=True, check=True
        )
        
        # 5. Lê o SVG gerado
        with open(path_out, "r", encoding="utf-8") as f_out:
            svg_content = f_out.read()
            
        return Response(content=svg_content, media_type="image/svg+xml")
        
    except subprocess.CalledProcessError as e:
        # SE O D2 FALHAR: Imprime o erro real nos logs do Render
        print(f"--- ERRO DO MOTOR D2 ---\n{e.stderr}")
        return Response(content="Erro interno no motor D2", status_code=500)
        
    except Exception as e:
        # SE O PYTHON FALHAR: Imprime o erro nos logs
        print(f"--- ERRO DO PYTHON ---\n{str(e)}")
        return Response(content="Erro interno no Python", status_code=500)
        
    finally:
        # Limpa os arquivos temporários da memória
        os.close(fd_in)
        os.close(fd_out)
        if os.path.exists(path_in): os.remove(path_in)
        if os.path.exists(path_out): os.remove(path_out)
