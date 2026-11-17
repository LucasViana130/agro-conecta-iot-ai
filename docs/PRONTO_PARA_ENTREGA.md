# Preflight final da entrega IoT/IA

Execute este roteiro na revisão final. Não marque como concluído sem evidência real.

## 1. Identificação e acesso

- [ ] Preencher todos os integrantes, RMs e turmas em `entrega/identificacao.txt`.
- [ ] Remover comentários e todos os marcadores `[PREENCHER]` do arquivo enviado.
- [ ] Repetir nomes e RMs no README, conforme a rubrica.
- [x] Confirmar que o repositório está público e abre sem autenticação.
- [ ] Enviar no Portal apenas o `.txt` exigido para esta disciplina.

Ausência ou identificação incompleta pode descontar 10 pontos. Link sem acesso pode impedir a avaliação.

## 2. Validação automatizada

```bash
python -m pip install -e '.[dev]'
ruff check .
python -m unittest discover -s tests -v
python -m agro_conecta_iot evaluate
python scripts/check_repository.py
```

Para a conferência final, depois de preencher identificação e atualizar evidências:

```bash
python scripts/check_repository.py --delivery
```

O modo `--delivery` deve terminar com sucesso. Ele não substitui a revisão humana.

## 3. Integração com o Java final

- [x] Fixar o hash final Java: `a82309765df9787565df40b0ce2a1e7f2cee067f`.
- [x] Subir PostgreSQL, RabbitMQ e a API Java com Java 21.
- [x] Manter a IA desabilitada na verificação dos seis cenários.
- [x] Executar `python scripts/verify_java.py` em banco descartável.
- [x] Publicar o relatório novo em `docs/evidencias/java-integration.json`.
- [x] Registrar hash, data, versões e limitações em `docs/evidencias/README.md`.
- [x] Gerar a evidência novamente contra o commit Java final.

## 4. Validação real da IA

- [x] Configurar `GOOGLE_API_KEY` somente no ambiente seguro do Java.
- [x] Confirmar `gemini-3.5-flash-lite`, `gemini-embedding-001` e dimensão 768.
- [x] Confirmar que os quatro documentos já estão indexados, evitando reingestão desnecessária.
- [x] Executar uma geração diagnóstica curta.
- [x] Executar uma orientação real para um job controlado.
- [x] Confirmar que o risco determinístico não foi alterado.
- [x] Confirmar que todas as fontes exibidas vieram dos trechos recuperados.
- [x] Registrar modelo, data, resultado e limitações sem salvar chave, token ou resposta técnica bruta.
- [ ] Revisar clareza e segurança da orientação com uma pessoa do grupo; preferencialmente obter revisão agronômica.

Mocks e fallback não comprovam IA generativa funcionando. Se o provedor falhar, registrar a falha honestamente e não apresentar fallback como resposta do Gemini.

## 5. Fontes e documentação

- [x] Verificar as quatro URLs por acesso direto ou índice público em 17/11/2026.
- [x] Conferir títulos e conteúdo indexado das duas fontes Embrapa cujo acesso automatizado direto responde 403.
- [ ] Comparar integralmente cada resumo local com sua fonte em revisão humana.
- [x] Confirmar que títulos, instituições, URLs, versões e hashes estão coerentes.
- [x] Confirmar que README, arquitetura e apresentação não divergem sobre o modelo Gemini.
- [x] Confirmar que NDVI não é apresentado como funcionalidade deste pacote.

## 6. Apresentação presencial

- [ ] Demonstrar a IA integrada à solução, não um chat isolado.
- [ ] Explicar Python -> Java -> PostgreSQL/outbox -> RabbitMQ -> risco -> RAG/Gemini.
- [ ] Mostrar um caso válido com fontes.
- [ ] Mostrar dados insuficientes ou indisponibilidade com fallback explícito.
- [ ] Explicar limitações, proteção de credenciais e ausência de automação de irrigação.
- [ ] Todos os integrantes sabem explicar sua participação.
- [ ] O grupo consegue responder como adaptaria a solução a uma mudança de requisito.

## 7. Estado que ainda depende de ação humana

Na revisão de 17/11/2026 permanecem pendentes apenas ações humanas ou de envio:

- nomes, RMs e turmas;
- revisão do texto produzido no diagnóstico real e revisão integral do acervo;
- ensaio e apresentação presencial;
- envio no Portal até o prazo oficial.
