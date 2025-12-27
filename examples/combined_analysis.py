#!/usr/bin/env python3
"""
Análise Combinada: Múltiplas Fontes de Dados

Este script combina dados de Wikidata, OWID e outras fontes
para uma análise estatística mais robusta da hipótese numerológica.
"""

import sys
import os
import pandas as pd

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processor import NumerologyDataAnalyzer


def main():
    """Análise combinada de múltiplas fontes."""
    print("=== PyNumerology-Matrix: Análise Combinada de Múltiplas Fontes ===\n")

    analyzer = NumerologyDataAnalyzer()

    # Coletar dados de múltiplas fontes
    all_events = []
    all_analysis = []

    sources = ['wikidata', 'owid']

    for source in sources:
        print(f"🔍 Coletando dados de {source.upper()}...")
        try:
            results = analyzer.collect_and_analyze(source=source, limit=1000)

            if 'events_data' in results and not results['events_data'].empty:
                events_df = results['events_data']
                analysis_df = results['analysis_data']

                print(f"   ✅ {len(events_df)} eventos coletados")
                print(f"   ✅ {len(analysis_df)} eventos analisados")

                all_events.append(events_df)
                all_analysis.append(analysis_df)
            else:
                print(f"   ❌ Nenhum dado coletado de {source}")

        except Exception as e:
            print(f"   ❌ Erro em {source}: {e}")

    # Combinar todos os dados
    if not all_events:
        print("\n❌ Nenhum dado coletado de nenhuma fonte. Usando dados demo...")
        create_combined_demo(analyzer)
        return

    combined_events = pd.concat(all_events, ignore_index=True)
    combined_analysis = pd.concat(all_analysis, ignore_index=True)

    # Remover duplicatas se houver
    combined_events = combined_events.drop_duplicates()
    combined_analysis = combined_analysis.drop_duplicates()

    print(f"\n📊 TOTAL COMBINADO:")
    print(f"   Eventos únicos: {len(combined_events)}")
    print(f"   Análises num.: {len(combined_analysis)}")
    print(f"   Fontes: {combined_events['source'].nunique()} diferentes")

    # Análise estatística combinada
    hypothesis = analyzer.test_hypothesis_ano_9(combined_analysis)
    decade_analysis = analyzer.analyze_by_decade(combined_analysis)

    print(f"\n🎯 TESTE ESTATÍSTICO COMBINADO ({len(combined_analysis)} eventos):")
    print("=" * 60)
    print(f"Total de eventos: {hypothesis['total_events']}")
    print(f"Eventos no Ano 9: {hypothesis['ano_9_count']} ({hypothesis['ano_9_percentage']}%)")
    print(f"Esperado (uniforme): {hypothesis['expected_uniform']:.1f}")
    print(f"Desvio: {hypothesis['deviation']:.1f}")
    print(f"Z-Score: {hypothesis['z_score']:.2f}")
    print(f"Qui-quadrado: {hypothesis['chi_square_stat']:.2f} (p={hypothesis['p_value']:.4f})")

    if hypothesis['distribution_uniform']:
        print("Distribuição: UNIFORME (estatisticamente)")
    else:
        print("Distribuição: NÃO UNIFORME (p < 0.05)")

    if hypothesis['hypothesis_supported']:
        print("HIPÓTESE: SUPORTADA estatisticamente!")
    else:
        print("HIPÓTESE: NÃO suportada estatisticamente")

    # Distribuição detalhada
    print(f"\n📈 DISTRIBUIÇÃO POR ANO PESSOAL:")
    expected_pct = 100/9
    for ano in range(1, 10):
        count = hypothesis['counts_by_ano'].get(ano, 0)
        actual_pct = count / hypothesis['total_events'] * 100
        marker = "🔴" if actual_pct > expected_pct * 1.2 else "🟢" if actual_pct < expected_pct * 0.8 else "🟡"
        print(f"   Ano {ano}: {count:3d} eventos ({actual_pct:5.1f}%) {marker}")

    # Análise por fonte
    print(f"\n📊 ANÁLISE POR FONTE:")
    for source in combined_analysis['source'].unique():
        source_data = combined_analysis[combined_analysis['source'] == source]
        if len(source_data) > 10:
            ano_9_pct = (source_data['ano_pessoal'] == 9).sum() / len(source_data) * 100
            print(f"   {source}: {len(source_data)} eventos, Ano 9: {ano_9_pct:.1f}%")

    # Análise por década
    if decade_analysis:
        print(f"\n📅 ANÁLISE POR DÉCADA (Ano 9 %):")
        for decade in sorted(decade_analysis.keys()):
            stats = decade_analysis[decade]
            if stats['total_events'] >= 20:  # Só décadas com dados suficientes
                marker = "🔴" if stats['ano_9_percentage'] > 13 else "🟢" if stats['ano_9_percentage'] < 7 else "🟡"
                print(f"   {decade}s: {marker} {stats['ano_9_percentage']:.1f}% ({stats['ano_9_count']}/{stats['total_events']})")

    # Salvar dados combinados
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)

    combined_events.to_csv(os.path.join(output_dir, 'combined_events.csv'), index=False)
    combined_analysis.to_csv(os.path.join(output_dir, 'combined_analysis.csv'), index=False)

    print(f"\n💾 Dados salvos em: {output_dir}")

    # Conclusão
    print(f"\n🔬 CONCLUSÃO CIENTÍFICA:")
    if hypothesis['p_value'] > 0.05:
        print("   Com base em dados de múltiplas fontes científicas,")
        print("   NÃO há evidência estatística de que eventos disruptivos")
        print("   concentrem-se em Anos Pessoais 9. A distribuição é uniforme.")
    else:
        print("   Dados indicam POSSÍVEL padrão não-uniforme, mas são")
        print("   necessários mais dados para confirmação estatística.")


def create_combined_demo(analyzer):
    """Cria demonstração com dados combinados simulados."""
    print("Criando análise demo com dados históricos conhecidos...")

    # Dados históricos conhecidos com anos disruptivos
    demo_events = [
        # Guerras Mundiais
        {'year': 1914, 'event': 'Início WWI', 'type': 'Guerra'},
        {'year': 1918, 'event': 'Fim WWI', 'type': 'Guerra'},
        {'year': 1939, 'event': 'Início WWII', 'type': 'Guerra'},
        {'year': 1945, 'event': 'Fim WWII', 'type': 'Guerra'},

        # Crises econômicas
        {'year': 1929, 'event': 'Quebra da Bolsa', 'type': 'Crise Econômica'},
        {'year': 2008, 'event': 'Crise Financeira Global', 'type': 'Crise Econômica'},

        # Eventos disruptivos diversos
        {'year': 1969, 'event': 'Chegada à Lua', 'type': 'Avanço Tecnológico'},
        {'year': 1989, 'event': 'Queda Muro de Berlin', 'type': 'Mudança Política'},
        {'year': 2020, 'event': 'Pandemia COVID-19', 'type': 'Crise Global'},
    ] * 10  # Multiplicar para ter mais dados

    events_df = pd.DataFrame(demo_events)
    analysis_df = analyzer.analyze_event_cycles(events_df)
    hypothesis = analyzer.test_hypothesis_ano_9(analysis_df)

    print(f"\n[DEMO] Análise com {len(analysis_df)} eventos históricos conhecidos")
    print(f"[DEMO] Ano 9: {hypothesis['ano_9_count']}/{hypothesis['total_events']} ({hypothesis['ano_9_percentage']}%)")
    print(f"[DEMO] Distribuição uniforme: {hypothesis['distribution_uniform']}")
    print(f"[DEMO] Hipótese suportada: {hypothesis['hypothesis_supported']}")


if __name__ == "__main__":
    main()