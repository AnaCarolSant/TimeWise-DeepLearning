from typing import Dict
import os
from openai import OpenAI


class ModelAdapter:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.remote_model = "gpt-4.1-mini"   # rápido, barato e excelente para análise

    # -------------------------
    # PROMPT (lógica alinhada ao serviço Java)
    # -------------------------
    def _build_prompt(self, data: Dict) -> str:
        u = data["usuario"]

        atividades = data.get("atividades", [])
        scores = data.get("scores", [])

        # Monta texto das atividades
        ativs = "\n".join([
            f"- {a['nome']} ({a.get('tipo','')}) {a['tempoInicio']} a {a.get('tempoFim','')}"
            for a in atividades[:30]
        ]) or "Nenhuma atividade registrada neste período."

        # Monta texto dos scores
        scs = "\n".join([
            f"- {s['dataTrabalho']}: Score {s['valor']}"
            for s in scores[:7]
        ]) or "Nenhum score registrado neste período."

        # Prompt alinhado com o Spring AIService
        return f"""
Você é um **Coach de Produtividade e Bem-estar pessoal**.

Usuário: {u['nome']}

DADOS DOS ÚLTIMOS 7 DIAS:

ATIVIDADES:
{ativs}

SCORES DIÁRIOS (0-10):
{scs}

TAREFA — Com base *estritamente* nos dados acima:
1. Analise como o padrão de pausas (ou ausência delas) está influenciando os scores.
2. Se houver poucos dados, explique isso e ofereça orientações gerais.
3. Dê **3 sugestões práticas, objetivas e personalizadas** para {u['nome']} aplicar na próxima semana.
4. Mantenha um tom empático, direto e orientado a resultados.
5. Trate o usuário sempre pelo nome **{u['nome']}**.
"""

    # -------------------------
    # CHAMADA AO CHATGPT
    # -------------------------
    def generate_analysis(self, req_json: Dict):
        prompt = self._build_prompt(req_json)

        try:
            response = self.client.chat.completions.create(
                model=self.remote_model,
                messages=[
                    {"role": "system", "content": "Você é um coach de produtividade altamente qualificado."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )

            text = response.choices[0].message.content
            suggestions = self._extract_suggestions_from_text(text)

            return {
                "text": text,
                "suggestions": suggestions,
                "model": self.remote_model
            }

        except Exception as e:
            raise RuntimeError(f"Erro ao chamar ChatGPT API: {str(e)}")

    # -------------------------
    # EXTRAÇÃO DAS SUGESTÕES (melhorada)
    # -------------------------
    def _extract_suggestions_from_text(self, text: str):
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        suggestions = []

        for l in lines:
            starts = (
                l.startswith("1.") or
                l.startswith("2.") or
                l.startswith("3.") or
                l.startswith("-") or
                l.startswith("•")
            )
            if starts:
                suggestions.append({
                    "titulo": l.split(".", 1)[-1][:40].strip(),
                    "descricao": l
                })

            if len(suggestions) >= 3:
                break

        return suggestions




