# Request Inspector

Ferramenta de debugging HTTP em tempo real. Captura requisições enviadas para `/api/*` e exibe no browser via WebSocket.

## Funcionalidades

- Captura requisições HTTP (GET, POST, PUT, DELETE, PATCH)
- Exibe em tempo real via WebSocket
- Mostra método, path, headers, query params e body
- Interface web responsiva com tema escuro

## Tecnologias

| Tecnologia | Versão |
|------------|--------|
| Python | 3.11+ |
| FastAPI | 0.115.0 |
| Uvicorn | 0.30.0 |
| Jinja2 | 3.1.4 |

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
python main.py
```

Ou com hot-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Uso

1. Acesse http://localhost:8000 para abrir o inspector
2. Envie requisições para `http://localhost:8000/api/seu-endpoint`
3. As requisições aparecem em tempo real na interface

## Docker

```bash
docker build -t request-inspector .
docker run -d -p 8000:8000 request-inspector
```
