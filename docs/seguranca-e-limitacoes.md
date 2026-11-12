# Segurança e limitações

JWT e autorização por proprietário são aplicados no Java, incluindo simulação e orientação. Respostas de acesso cruzado usam 404; papéis inválidos usam 403. Dados de contexto não incluem e-mail, token ou senha. A orientação recebe somente fatos pertinentes; não pode alterar o RiskJob.result.

Python oculta credenciais no repr e não exibe exceções remotas. HTTP fora de localhost exige HTTPS e redirects são recusados para não reenviar Bearer. Não registrar .env, tokens, relatórios com dados pessoais ou bindings reais. CI faz busca básica de padrões, não certificação completa de ausência de segredos. Não há credencial real nos exemplos.

Somente sensores simulados; não existe calibração de hardware validada. Risco, perfil de demonstração e saúde não substituem avaliação agronômica. Não há acionamento físico de irrigação, prescrição ou diagnóstico definitivo. A fonte realmente recuperada pode ser irrelevante semanticamente; uma lista atribuída não garante verdade de toda a resposta. Proteção por prompt não garante resistência absoluta a injection.

Avaliação fixture valida o avaliador e os critérios estruturais; não demonstra funcionamento do modelo real. Avaliação live exige API, acervo indexado e credencial de provedor; o usuário deve revisar fatos em prosa, clareza e adequação agronômica. Interface Mobile ainda deve ser implementada por outro projeto.
