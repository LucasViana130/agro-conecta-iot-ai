# Avaliação executável

Oito casos: alerta válido, normal, leitura antiga, dados insuficientes, ausência de fonte, indisponibilidade/timeout, sinais conflitantes e prompt injection. Entradas, expectativas e saídas mock estão em evaluation/cases.json. Todas são **fixtures de teste**, não saídas capturadas do Gemini.

O avaliador confere preservação do risco, fallback/motivo, atribuição de fontes, identificação da simulação, presença de limitações, resumo com tamanho válido, marcador de injection e fatos estruturados quando presentes. Os testes negativos alteram deliberadamente fonte, medição, risco, avisos e marcador para verificar que o avaliador falha. Não avaliamos por igualdade exata de texto.

[Relatório mock executado](evidencias/evaluation-mock.json): oito casos passaram. Isso comprova o comportamento do avaliador sobre fixtures conhecidas. **Não mede taxa de acerto, grounding semântico ou resistência real do modelo**. Clareza semântica, fatos implícitos e recomendações em prosa exigem revisão humana; o contrato Java atual não tem campo facts, portanto a verificação numérica estruturada não cobre sua prosa.

[Integração local executada](evidencias/java-integration.json): seis cenários Python → HTTP → Java → PostgreSQL/RabbitMQ → resultado/fallback passaram. Foram conferidos source, regras esperadas, saúde, isolamento entre dois produtores, rejeição de entrada inválida e JWT ausente. AI desabilitada: não houve geração Gemini nessa execução.

Java usa fakes de AgronomicAiClient/VectorStore para timeout, ausência de fontes, contexto insuficiente, atribuição, preservação do risco e autorização. O teste do prompt verifica que instruções maliciosas ficam no conteúdo não confiável, sem se tornar mensagem de sistema. Não demonstra imunidade do modelo em produção.

Modo live: preparar jobs controlados, registrar IDs de fontes recuperadas independentemente e executar `python -m agro_conecta_iot evaluate --live --bindings reports/bindings.json`. Sem binding, cada caso aparece como não executado e o comando retorna falha. Não injete falhas de provedor em produção. Para validar timeout/injection real, use ambiente de teste e corpus controlado. Modelo retornado e data são registrados. Não invente nem preencha resultados antes de executar.

Não executados: Gemini/embeddings reais (sem chave configurada), revisão agronômica humana, UI Mobile e coleção no Runner Postman. A coleção foi validada como JSON; as mesmas rotas foram exercitadas pelo cliente Python real. Ver [resumo de evidências](evidencias/README.md).
