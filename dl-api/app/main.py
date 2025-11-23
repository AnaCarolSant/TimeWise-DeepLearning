from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
import uvicorn
import os
import time
from model_adapter import ModelAdapter

app = FastAPI(title="DL Productivity Coach API", version="1.0")

API_KEY = os.getenv("DL_API_KEY", "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")  # troque em produção
adapter = ModelAdapter()  # carrega/gestiona modelo

# --- Schemas
class UsuarioSchema(BaseModel):
    id: int
    nome: str
    email: str

class AtividadeSchema(BaseModel):
    nome: str
    tipo: Optional[str]
    tempoInicio: datetime
    tempoFim: Optional[datetime]

class ScoreSchema(BaseModel):
    dataTrabalho: date
    valor: int = Field(..., ge=0, le=10)

class AnaliseRequest(BaseModel):
    usuario: UsuarioSchema
    atividades: List[AtividadeSchema] = []
    scores: List[ScoreSchema] = []
    modo: Optional[str] = "chat"

class Sugestao(BaseModel):
    titulo: str
    descricao: str

class AnaliseResponse(BaseModel):
    status: str
    analise: str
    sugestoes: Optional[List[Sugestao]] = []
    meta: dict

# --- simple API key dependency
def require_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# --- endpoint
@app.post("/v1/analise-produtividade", response_model=AnaliseResponse, dependencies=[Depends(require_api_key)])
def gerar_analise(req: AnaliseRequest):
    start = time.time()
    # validação minima
    if not req.usuario:
        raise HTTPException(status_code=400, detail="usuario é obrigatório")

    # construir prompt - delegamos ao adapter
    try:
        result = adapter.generate_analysis(req.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    latency = int((time.time() - start) * 1000)
    return AnaliseResponse(status="ok", analise=result["text"], sugestoes=result.get("suggestions", []),
                           meta={"model": result.get("model", "unknown"), "latency_ms": latency})

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)