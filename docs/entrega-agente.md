# Registro técnico da implementação

Este documento registra decisões e evidências técnicas. Caminhos locais e dados pessoais não fazem parte da entrega.

## Inventário Java

Já existiam JWT/papéis, cadastros, sensores, leituras, perfis versionados, atividades, risco determinístico, outbox/RabbitMQ, alertas, Spring AI, PGVector e corpus de quatro resumos. Planejamento não foi usado como prova: fontes, configurações e testes foram inspecionados. Java 21 é o target real, compilado/executado com JDK 25; Maven Wrapper 3.10.0. O legado GS-2-Codex não foi alterado.

Adições: endpoint demo-only `/api/simulated-readings`, origem forçada e autorização compartilhada; saúde calculada por histórico; fallback explícito sem alterar risco; identificação da simulação no contexto e avisos; testes de fontes, contexto, timeout, saúde e autorização. O contrato de orientação foi preservado na rota `/api/risk-jobs/{id}/guidance`, com campos adicionais. Ver `docs/IOT_AI_INTEGRATION.md` no Java.

## Conteúdo do novo repositório

src/agro_conecta_iot: configuração, modelos, seis cenários, cliente HTTP, CLI e avaliador. evaluation: oito fixtures/runner/assertions. tests: unittest e servidor HTTP real controlado. scripts: integração Java, manifesto e scan. knowledge-base: manifesto de fontes com hashes. postman: coleção e ambiente sem credenciais. docs: arquitetura, integração, fórmulas, RAG, avaliação, segurança, rubrica e demonstração. Docker/Compose, CI e entrega/identificacao.txt completam o pacote.

## Configuração e pendências

Variáveis: JAVA_API_BASE_URL; JAVA_API_TOKEN ou JAVA_API_USERNAME/PASSWORD; CROP_AREA_ID e SENSOR_ID; HTTP_TIMEOUT_SECONDS; SIMULATOR_SEED; EVALUATION_MODE. Java precisa de DB/RabbitMQ/JWT e APP_DEMO_ENABLED. IA real requer APP_AI_ENABLED e GOOGLE_API_KEY. Não versionar valores reais.

Preencher integrantes, RM e turma; revisar em grupo a geração real já registrada; conferir manualmente os resumos das fontes; apresentar e enviar o `.txt` no Portal. O [checklist](checklist-rubrica.md) indica limitações por critério e o [roteiro](roteiro-demonstracao.md) organiza a apresentação. O Mobile existe em repositório separado; .NET e hardware físico permanecem fora deste pacote.

As duas documentações privadas anteriores em AgroConecta-Entrega não fazem parte dos commits. Estes documentos públicos são os novos arquivos explicitamente solicitados para IoT/IA.
