#!/usr/bin/env python3
"""
Demonstração da Coleta e Análise de Dados Históricos

Este script mostra como coletar dados de fontes abertas e
analisar padrões numerológicos estatisticamente.
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processor import NumerologyDataAnalyzer


def main():
    """Função principal da demonstração de dados."""
    print("=== PyNumerology-Matrix: Analise de Dados Historicos ===\n")

    analyzer = NumerologyDataAnalyzer()

    # Coletar e analisar dados do Wikidata
    print("Coletando dados historicos do Wikidata...")
    try:
        results = analyzer.collect_and_analyze(source='wikidata', limit=50)  # Reduzido para evitar timeout

        if 'error' in results:
            print(f"Erro: {results['error']}")
            print("Criando dados de exemplo para demonstracao...")
            create_sample_data_demo(analyzer)
            return

        events_df = results['events_data']
        analysis_df = results['analysis_data']
        hypothesis = results['hypothesis_test']

        print(f"Coletados {len(events_df)} eventos historicos")
        print(f"Analisados {len(analysis_df)} eventos com ciclos numerologicos")

        # Mostrar estatísticas da hipótese
        print("\nTeste da Hipotese do Ano Pessoal 9:")
        print(f"   Total de eventos: {hypothesis['total_events']}")
        print(f"   Eventos no Ano 9: {hypothesis['ano_9_count']} ({hypothesis['ano_9_percentage']}%)")
        print(f"   Esperado (uniforme): {hypothesis['expected_uniform']}")
        print(f"   Desvio: {hypothesis['deviation']}")

        if hypothesis['hypothesis_supported']:
            print("   Hipotese SUPORTADA: Mais eventos no Ano 9 que o esperado!")
        else:
            print("   Hipotese NAO suportada: Distribuicao proxima a uniforme")

        # Mostrar distribuição por ano pessoal
        print("\nDistribuicao por Ano Pessoal:")
        for ano, count in hypothesis['counts_by_ano'].items():
            print(f"   Ano {ano}: {count} eventos")

        # Salvar resultados
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(output_dir, exist_ok=True)

        events_df.to_csv(os.path.join(output_dir, 'historical_events.csv'), index=False)
        analysis_df.to_csv(os.path.join(output_dir, 'numerology_analysis.csv'), index=False)

        print(f"\nDados salvos em: {output_dir}")

    except Exception as e:
        print(f"Erro durante analise: {e}")
        print("Criando dados de exemplo para demonstracao...")
        create_sample_data_demo(analyzer)


def create_sample_data_demo(analyzer):
    """Cria dados de exemplo para demonstração quando API falha."""
    import pandas as pd
    from datetime import datetime

    # Criar dados de exemplo
    sample_events = [
        {'date': '2020-03-15', 'eventLabel': 'Pandemia COVID-19', 'typeLabel': 'Crise global'},
        {'date': '2008-09-15', 'eventLabel': 'Crise financeira 2008', 'typeLabel': 'Crise economica'},
        {'date': '2011-03-11', 'eventLabel': 'Terremoto no Japao', 'typeLabel': 'Desastre natural'},
        {'date': '2016-06-23', 'eventLabel': 'Brexit', 'typeLabel': 'Evento politico'},
        {'date': '2022-02-24', 'eventLabel': 'Invasao da Ucrania', 'typeLabel': 'Conflito armado'},
        {'date': '2019-12-31', 'eventLabel': 'Transicao para 2020', 'typeLabel': 'Evento temporal'},
        {'date': '2017-08-12', 'eventLabel': 'Protestos Charlottesville', 'typeLabel': 'Conflito social'},
        {'date': '2015-11-13', 'eventLabel': 'Atentados Paris', 'typeLabel': 'Ataque terrorista'},
    ]

    events_df = pd.DataFrame(sample_events)
    events_df['date'] = pd.to_datetime(events_df['date'])

    print(f"\n[DEMO] Usando {len(events_df)} eventos de exemplo")

    # Analisar
    analysis_df = analyzer.analyze_event_cycles(events_df)
    hypothesis = analyzer.test_hypothesis_ano_9(analysis_df)

    print(f"[DEMO] Analisados {len(analysis_df)} eventos com ciclos numerologicos")

    # Mostrar estatísticas
    print("\n[DEMO] Teste da Hipotese do Ano Pessoal 9:")
    print(f"   Total de eventos: {hypothesis['total_events']}")
    print(f"   Eventos no Ano 9: {hypothesis['ano_9_count']} ({hypothesis['ano_9_percentage']}%)")
    print(f"   Esperado (uniforme): {hypothesis['expected_uniform']}")
    print(f"   Desvio: {hypothesis['deviation']}")

    if hypothesis['hypothesis_supported']:
        print("   Hipotese SUPORTADA: Mais eventos no Ano 9 que o esperado!")
    else:
        print("   Hipotese NAO suportada: Distribuicao proxima a uniforme")

    print("\n[DEMO] Distribuicao por Ano Pessoal:")
    for ano, count in hypothesis['counts_by_ano'].items():
        print(f"   Ano {ano}: {count} eventos")

    print("\n[DEMO] Para dados reais, verifique conexao com Wikidata/OWID/GDELT")


if __name__ == "__main__":
    main()