# Evidências reproduzíveis

- evaluation-mock.json: oito casos fixture executados, modo mock explícito.
- java-integration.json: seis cenários por HTTP contra Java, PostgreSQL e RabbitMQ locais, IA desabilitada. Tokens, e-mails e IDs privados não são exportados.
- Python: 14 testes unittest passaram; ruff passou; dry-run com referência fixa passou.
- Java: `mvnw -B -o verify` concluiu com 159 testes, 158 aprovados, zero falhas/erros e um teste manual Gemini não executado. Após reforçar o teste do prompt, `-Dtest=RagAndPromptTests test` também passou (4 testes). JDK 25, target 21, Maven 3.10.0. Código publicado no Java: 3ff3f622378d60c6cc5c11e76b6ab6f4686fdc7b.
- Docker: imagem construída; dry-run e evaluate executados com sucesso como usuário sem privilégios.
- OpenAPI consultado na API local: /api/simulated-readings presente e esquema Bearer JWT presente.
- Scan básico de segredos e JSON executado antes de publicar. Não equivale a auditoria de segurança.

Comandos: `python -m unittest discover -s tests -v`, `ruff check .`, `python -m agro_conecta_iot evaluate`, `python scripts/verify_java.py`, `docker compose run --rm simulator`, `docker compose run --rm simulator evaluate`.

O script de integração cria dados descartáveis; use banco local e APP_AI_ENABLED=false. Nenhuma porcentagem de qualidade do Gemini foi calculada. O teste manual do provedor Java permanece separado e depende de credencial.
