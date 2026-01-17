from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
import json

app = FastAPI(title="Request Inspector")
templates = Jinja2Templates(directory="templates")

# Lista de WebSocket connections ativas
connections: list[WebSocket] = []

# Configuração de resposta customizada
class ResponseConfig(BaseModel):
    status_code: int = 200
    payload: str = '{"status": "received", "message": "Requisição capturada e exibida no inspector"}'

response_config = ResponseConfig()


async def broadcast_request(data: dict):
    """Envia dados da requisição para todos os clientes conectados"""
    for connection in connections:
        try:
            await connection.send_json(data)
        except:
            pass


def serialize_headers(headers) -> dict:
    """Converte headers para dicionário"""
    return dict(headers)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal que mostra as requisições"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para comunicação em tempo real"""
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections.remove(websocket)


@app.get("/config")
async def get_config():
    """Retorna a configuração atual de resposta"""
    return response_config


@app.post("/config")
async def set_config(config: ResponseConfig):
    """Atualiza a configuração de resposta"""
    global response_config
    response_config = config
    return {"status": "ok", "config": response_config}


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(request: Request, path: str):
    """Captura todas as requisições para /api/*"""

    # Lê o body se existir
    body = None
    try:
        body_bytes = await request.body()
        if body_bytes:
            try:
                body = json.loads(body_bytes)
            except:
                body = body_bytes.decode("utf-8", errors="ignore")
    except:
        pass

    # Monta os dados da requisição
    request_data = {
        "timestamp": datetime.now().isoformat(),
        "method": request.method,
        "path": f"/api/{path}",
        "query_params": dict(request.query_params),
        "headers": serialize_headers(request.headers),
        "body": body,
        "client": request.client.host if request.client else None,
    }

    # Envia para todos os clientes conectados via WebSocket
    await broadcast_request(request_data)

    # Retorna resposta customizada
    try:
        payload = json.loads(response_config.payload)
    except json.JSONDecodeError:
        payload = response_config.payload

    return JSONResponse(content=payload, status_code=response_config.status_code)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
