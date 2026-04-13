@app.post("/render-diagram")
async def render_diagram(request: Request):
    codigo_diagrama = await request.body()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".d2") as f_in, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".svg") as f_out:
        
        f_in.write(codigo_diagrama)
        f_in.flush()
        
        try:
            subprocess.run(["./bin/d2", f_in.name, f_out.name], check=True)
            
            # ATENÇÃO AQUI: Esta linha e as de baixo precisam estar alinhadas corretamente
            with open(f_out.name, "r", encoding="utf-8") as svg_file:
                svg_content = svg_file.read()
                
            return Response(content=svg_content, media_type="image/svg+xml")
            
        except subprocess.CalledProcessError:
            return Response(content="Erro ao renderizar", status_code=500)
        finally:
            os.remove(f_in.name)
            os.remove(f_out.name)
