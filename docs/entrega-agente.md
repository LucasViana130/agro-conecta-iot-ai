# Entrega técnica da implementação

Repositório local: C:/Users/Internet/Downloads/agro-conecta-iot-ai (irmão de GS-FINAL-implementacao, sem .git aninhado).

## Inventário Java

Já existiam JWT/papéis, cadastros, sensores, leituras, perfis versionados, atividades, risco determinístico, outbox/RabbitMQ, alertas, Spring AI, PGVector e corpus de quatro resumos. Planejamento não foi usado como prova: fontes, configurações e testes foram inspecionados. Java 21 é o target real, compilado/executado com JDK 25; Maven Wrapper 3.10.0. O legado GS-2-Codex não foi alterado.

Adições: endpoint demo-only /api/simulated-readings, origem forçada e autorização compartilhada; saúde calculada por histórico; fallback explícito sem alterar risco; identificação da simulação no contexto e avisos; testes de fontes, contexto, timeout, saúde e autorização. Contrato legado de orientação foi preservado na rota /api/risk-jobs/{id}/guidance, com campos adicionais. Ver docs/IOT_AI_INTEGRATION.md no Java.

## Conteúdo do novo repositório

src/agro_conecta_iot: configuração, modelos, seis cenários, cliente HTTP, CLI e avaliador. evaluation: oito fixtures/runner/assertions. tests: unittest e servidor HTTP real controlado. scripts: integração Java, manifesto e scan. knowledge-base: manifesto de fontes com hashes. postman: coleção e ambiente sem credenciais. docs: arquitetura, integração, fórmulas, RAG, avaliação, segurança, rubrica e demonstração. Docker/Compose, CI e entrega/identificacao.txt completam o pacote.

## Configuração e pendências

Variáveis: JAVA_API_BASE_URL; JAVA_API_TOKEN ou JAVA_API_USERNAME/PASSWORD; CROP_AREA_ID e SENSOR_ID; HTTP_TIMEOUT_SECONDS; SIMULATOR_SEED; EVALUATION_MODE. Java precisa de DB/RabbitMQ/JWT e APP_DEMO_ENABLED. IA real requer APP_AI_ENABLED e GOOGLE_API_KEY. Não versionar valores reais.

Preencher integrantes, RM, turma e vídeo; executar/revisar geração real; conferir as duas URLs Embrapa cuja revalidação remota falhou; apresentar e enviar .txt no Portal. [Checklist oficial](checklist-rubrica.md) indica limitações por critério e [roteiro](roteiro-demonstracao.md) organiza a apresentação. Mobile, .NET e hardware não foram implementados.

As duas documentações privadas anteriores em AgroConecta-Entrega não fazem parte dos commits. Estes documentos públicos são os novos arquivos explicitamente solicitados para IoT/IA.
