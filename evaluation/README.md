# Avaliação

Execute `python -m agro_conecta_iot evaluate`. Oito fixtures explícitas exercitam o avaliador, não o Gemini. Testes negativos corrompem fontes, risco e fatos para provar que falhas são detectadas.

`evaluate --live --bindings reports/bindings.json` consulta jobs previamente preparados no Java. Exemplo de binding: `{"valid-alert":{"jobId":1,"retrievedSourceIds":["embrapa-irrigacao-milho"]}}`. Fontes esperadas devem vir de evidência independente da recuperação. Casos sem binding são marcados como não executados e o comando falha. Timeout e injection exigem ambiente controlado; não são induzidos no provedor de produção. Não compartilhe tokens nem respostas com dados reais.
