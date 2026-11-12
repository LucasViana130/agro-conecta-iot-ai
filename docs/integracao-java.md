# Contrato de integração

Java: Spring Boot 4.1.2, target Java 21; execução local com JDK 25 e Maven Wrapper 3.10.0. Não usar JDK 17 neste repositório. O diretório GS-2-Codex contém legado; a implementação atual está no GS-FINAL.

Inicie `docker compose up -d` no Java com RABBITMQ_USERNAME/PASSWORD definidos e depois `./mvnw spring-boot:run`. Configure DB_URL/USERNAME/PASSWORD, JWT_SECRET, RabbitMQ e APP_DEMO_ENABLED=true. APP_AI_ENABLED=false permite risco e fallback. IA real exige APP_AI_ENABLED=true e GOOGLE_API_KEY; não publique a chave. Swagger: /swagger-ui/index.html e /v3/api-docs.

| Operação | Método e rota | Retorno |
|---|---|---|
| Login | POST /api/auth/login | 200, token |
| Cadastro | POST /api/auth/register | 201, token |
| Leitura simulada | POST /api/simulated-readings | 201, ReadingResponse source=SIMULATED |
| Criar análise | POST /api/crop-areas/{id}/risk-jobs | 202, id/status |
| Consultar | GET /api/risk-jobs/{id} | 200, result após conclusão |
| Alerta | GET /api/alerts/{id} | 200, RiskJob; id do alerta é id do job |
| Entender alerta | POST /api/risk-jobs/{id}/guidance | 200, RiskJob com guidance |
| Saúde | GET /api/sensors/{id}/health | 200, comunicação/admin/calculatedHealth |

Reading JSON: sensorId positivo, measuredAt ISO UTC, source SIMULATED, temperatureCelsius [-50,70], airHumidityPercent/soilMoisturePercent/batteryPercent [0,100]. Campos opcionais são omitidos, nunca substituídos por zero. WEATHER_STATION aceita combinações parciais. rainfallMillimeters >=0 exige rainfallIntervalStart anterior a measuredAt. Medições suportam até três decimais. Não enviar cropAreaId no payload; o Java resolve pelo sensor e confere proprietário.

JWT Bearer obrigatório. 400 para validação, 401 sem JWT, 403 para papel inválido, 404 para ausente **ou de outro proprietário** (contrato existente evita enumeração), 409 para cultivo arquivado/sensor inativo/job não concluído. Erros seguem ProblemDetail Java. Rota de simulação não existe quando a flag está desligada.

Guidance preserva summary, recommendation, recommendedActions, warnings, sources e adiciona signals, riskLevel, fallback; contingência adiciona reason. Fontes existentes têm sourceId/title/institution/url/version. Não criamos rota concorrente ai-guidance. Contexto insuficiente, sem fontes ou provedor indisponível retornam 200 com fallback=true, sources=[], motivo explícito; não é geração bem-sucedida. Fallback não é persistido/cacheado para permitir nova tentativa. Orientação válida é persistida.

GET tem até 3 tentativas em timeout/429/502/503/504. POST e PUT têm uma tentativa; timeout de escrita deixa resultado incerto e exige consulta antes de reenvio. Não há garantia de idempotência para ingestão simulada. Poll de job limitado a 30 consultas.
