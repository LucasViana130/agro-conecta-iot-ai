# Evidências reproduzíveis

- evaluation-mock.json: oito casos fixture executados, modo mock explícito.
- java-integration.json: seis cenários por HTTP contra Java, PostgreSQL e RabbitMQ locais, IA desabilitada. Tokens, e-mails e IDs privados não são exportados.
- gemini-live.json: orientação real executada pelo Java no Render, com risco determinístico preservado, quatro fontes e sem fallback. O texto gerado e as credenciais não foram armazenados.
- Python: suíte, lint e avaliação mock reexecutados em 17/11/2026 com Python 3.13.2: 14/14 testes e 8/8 casos aprovados.
- Java final validado: commit `a82309765df9787565df40b0ce2a1e7f2cee067f`. A suíte Java descobriu 182 testes: 181 aprovados, zero falhas/erros e um teste manual do provedor ignorado. Target Java 21 e Maven Wrapper 3.10.0.
- Integração final reexecutada em 17/11/2026 contra imagem construída desse commit, PostgreSQL/PGVector e RabbitMQ locais descartáveis: 6/6 cenários aprovados.
- Provedor real validado em 17/11/2026 pelo deploy desse mesmo commit: `gemini-3.5-flash-lite`, `promptVersion=agronomic-v1`, risco `CRITICAL` preservado e 4 fontes recuperadas.
- Docker: imagem construída; dry-run e evaluate executados com sucesso como usuário sem privilégios.
- OpenAPI consultado na API local: /api/simulated-readings presente e esquema Bearer JWT presente.
- Scan básico de segredos e JSON executado antes de publicar. Não equivale a auditoria de segurança.

Comandos: `python -m unittest discover -s tests -v`, `ruff check .`, `python -m agro_conecta_iot evaluate`, `python scripts/verify_java.py`, `python scripts/verify_live_ai.py`, `docker compose run --rm simulator`, `docker compose run --rm simulator evaluate`.

Os scripts de integração criam dados descartáveis identificados como DEMO. Use banco local e `APP_AI_ENABLED=false` para os seis cenários; o verificador live exige ambiente controlado com IA habilitada. Nenhuma porcentagem de qualidade do Gemini foi calculada. A revisão humana da orientação continua necessária.
