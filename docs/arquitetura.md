# Arquitetura e limites

```mermaid
sequenceDiagram
 participant P as Python
 participant J as Java
 participant Q as RabbitMQ
 participant V as PGVector
 participant G as Gemini
 P->>J: JWT + POST /api/simulated-readings
 J->>J: validar, verificar proprietário, persistir + outbox
 P->>J: POST /api/crop-areas/{id}/risk-jobs
 J->>Q: RiskAnalysisRequested com jobId
 Q->>J: consumidor bloqueia job e calcula snapshot
 P->>J: GET /api/risk-jobs/{id}
 P->>J: POST /api/risk-jobs/{id}/guidance
 J->>V: recuperar trechos atribuídos
 alt contexto e provedor disponíveis
 J->>G: contexto fixado + trechos não confiáveis
 G-->>J: orientação estruturada
 else insuficiência ou falha
 J->>J: fallback sem geração e sem fontes inventadas
 end
 J-->>P: RiskJob com result preservado e guidance
```

Python nunca recalcula risco para decidir alertas. O processo Java controla PostgreSQL, outbox com confirmação, retries/DLQ, risco e autorização. Leituras e perfil são fixados no job. Atividades dos últimos 30 dias são consultadas no momento da orientação, limitadas a 10, com corte temporal na criação do job. Alterações retroativas de atividades podem mudar o contexto; não é snapshot integral de atividades.

Mobile, .NET e hardware físico ficam fora deste repositório. A UI futura deve identificar SIMULATED, distinguir fallback, mostrar fontes e conservar o resultado determinístico mesmo em falhas.
