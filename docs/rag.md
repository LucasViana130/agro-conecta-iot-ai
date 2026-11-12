# RAG existente no Java

Acervo: quatro resumos curtos em src/main/resources/rag/agronomy/*.md. [Manifesto](../knowledge-base/sources.json) lista IDs, título, instituição, URL, tema/seção, data, versão e SHA-256 dos arquivos locais. São resumos do projeto, não cópias integrais nem transcrições certificadas das publicações.

AgronomyRagLoader divide texto em até 1000 caracteres UTF-16, sem sobreposição e sem partir surrogate pairs. IDs determinísticos por fonte/versão/índice; checksum inclui texto, modelo e dimensão. Ingestão faz upsert e remove chunks antigos da fonte. Embedding gemini-embedding-001/768; PGVector, HNSW/cosseno. Ingestão exige provedor disponível quando AI habilitada.

PgVectorAgronomyKnowledge faz topK=4, threshold=.3, filtro corpus='agronomy'. Cultura entra na consulta semântica; **não há filtro estrito por cultura/tema nos metadados**. Metadados topic documentam tema, mas não são usados como isolamento. Cada passagem é limitada a 1600 caracteres, e suficiência exige >=3 passagens atribuídas. Acervo pequeno e limiar precisam de avaliação real; não há evidência de recall/precision.

Fontes válidas exigem sourceId/title/institution/url/version; itens sem atribuição são descartados. O servidor constrói sources a partir da recuperação, ignorando qualquer tentativa do modelo de mudar a lista. Resposta estruturada é validada. Se insuficiente, guidance usa fallback NO_RELEVANT_SOURCES com lista vazia. Contexto sem dados obrigatórios não chama modelo.

Prompt de sistema trata documentos e campos como não confiáveis, recusa instruções embutidas, proíbe inventar medições/fontes, prescrever defensivos ou acionar irrigação. Prompts/completions não são registrados em produção. Isso reduz risco, mas não prova imunidade a prompt injection; avaliação humana e live continuam necessárias.

Referências verificadas nesta execução: [Embrapa/Comunicado 155](https://www.infoteca.cnptia.embrapa.br/handle/doc/974063) e [FAO/irrigação](https://www.fao.org/land-water/water/agricultural-water-management/irrigation/en). As outras duas URLs da Embrapa tiveram 403/timeout; não declarar conteúdo revalidado. Infoteca informa CC BY-NC-ND 4.0 no portal; este pacote apenas referencia a publicação e não redistribui o PDF.
