# Indicadores determinísticos no Java

- VPD em kPa: es = 0.6108 × exp(17.27T/(T+237.3)); VPD = es × (1-RH/100). Temperatura do ar °C e umidade relativa simultâneas, ou leituras separadas em até cinco minutos.
- Disponibilidade %: (umidade − ponto de murcha)/(capacidade de campo − ponto de murcha) ×100. Perfil calibrado versionado; capacidade deve superar murcha. Retorna valor bruto e visual limitado a 0–100. Acima de 100 indica acima da capacidade, não diagnóstico de saturação.
- Tendência: diferença de umidade / intervalo real em horas, mesmo sensor, ao menos cinco minutos. RECOVERING/STABLE/DRYING_SLOWLY/DRYING_FAST/INSUFFICIENT_DATA. Duplicatas de timestamp não geram divisão por zero.
- Chuva: soma intervalos completos sem sobreposição em 24h/7d e tempo desde último intervalo positivo. Ausência retorna insuficiência apenas para chuva, sem invalidar VPD/disponibilidade. Não rateia intervalo que cruza janela.
- Saúde: calculatedHealth HEALTHY/STALE (24h)/OFFLINE (48h)/POSSIBLE_FAULT/INSUFFICIENT_DATA; communicationStatus legado e administrativeStatus permanecem separados. Seis valores idênticos em ao menos 50 minutos ou salto em até cinco minutos (>40 pontos solo, >20°C ou >50 pontos RH) sinalizam possível falha, sem diagnóstico definitivo.

Regras de risco demo-v1: disponibilidade <=20% CRITICAL; <=40% ATTENTION; VPD>=2kPa ou secagem<=−3 pontos/hora elevam NORMAL a ATTENTION. Ausência de solo recente ou perfil dá INSUFFICIENT_DATA. Leituras futuras não entram no cálculo. Entrada tolera até 5min futuros, mas o cálculo espera que a medição alcance o tempo de referência. Snapshot preserva perfil, regras e leituras.

Todas as constantes são demonstrativas. A IA não calcula nem modifica esses resultados. A saúde não elimina automaticamente uma leitura do risco; UI deve mostrar ambos e pedir verificação. Sequência constante pode ser condição real, logo o aviso é apenas suspeita.
