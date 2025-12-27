#!/usr/bin/env python3
"""
Análise Estatística Completa: 5000 Eventos Históricos

Análise final da hipótese numerológica com dataset de 5000 eventos.
"""

import sys
import os
import pandas as pd

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processor import NumerologyDataAnalyzer


def analyze_5000_events():
    """Análise completa dos 5000 eventos."""
    print("=== PyNumerology-Matrix: Análise Final de 5000 Eventos ===\n")

    # Carregar dataset de 5000 eventos
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'historical_events_5000_synthetic.csv')

    if not os.path.exists(dataset_path):
        print("❌ Dataset de 5000 eventos não encontrado!")
        return

    df_events = pd.read_csv(dataset_path)
    print(f"✅ Dataset carregado: {len(df_events)} eventos")
    print(f"📅 Período: {df_events['year'].min()}-{df_events['year'].max()}")

    # Inicializar analisador
    analyzer = NumerologyDataAnalyzer()

    # Análise numerológica
    print("\n🔢 Calculando ciclos numerológicos...")
    analysis_df = analyzer.analyze_event_cycles(df_events)

    print(f"✅ Análise completa: {len(analysis_df)} eventos processados")

    # Teste estatístico completo
    print("\n🎯 TESTE ESTATÍSTICO FINAL (5000 eventos)")
    print("=" * 70)

    hypothesis = analyzer.test_hypothesis_ano_9(analysis_df)

    print(f"Total de eventos analisados: {hypothesis['total_events']}")
    print(f"Eventos no Ano 9: {hypothesis['ano_9_count']} ({hypothesis['ano_9_percentage']}%)")
    print(f"Esperado (distribuição uniforme): {hypothesis['expected_uniform']:.1f}")
    print(f"Desvio padrão: {hypothesis['deviation']:.1f}")
    print(f"Z-Score: {hypothesis['z_score']:.2f}")
    print(f"Razão de concentração: {hypothesis['concentration_ratio']:.2f}x")
    print(f"Qui-quadrado: {hypothesis['chi_square_stat']:.2f}")
    print(f"p-valor: {hypothesis['p_value']:.4f}")

    # Interpretação estatística
    print(f"\n📊 INTERPRETAÇÃO ESTATÍSTICA:")
    if hypothesis['distribution_uniform']:
        print("✓ Distribuição UNIFORME (p > 0.05)")
        print("  Não há evidência estatística de que eventos se concentrem em Ano 9")
    else:
        print("✗ Distribuição NÃO uniforme (p < 0.05)")
        print("  Há evidência estatística de padrão não-aleatório")

    if hypothesis['hypothesis_supported']:
        print("✓ HIPÓTESE SUPORTADA: Ano 9 acima da média E estatisticamente significativo")
    else:
        print("✗ Hipótese NÃO suportada estatisticamente")

    # Distribuição detalhada
    print(f"\n📈 DISTRIBUIÇÃO POR ANO PESSOAL (5000 eventos):")
    expected_pct = 100/9
    uniform_deviation = 0

    for ano in range(1, 10):
        count = hypothesis['counts_by_ano'].get(ano, 0)
        actual_pct = count / hypothesis['total_events'] * 100
        deviation_from_expected = actual_pct - expected_pct

        marker = "🔴 ACIMA" if actual_pct > expected_pct * 1.2 else "🟢 ABAIXO" if actual_pct < expected_pct * 0.8 else "🟡 NORMAL"
        print(f"   Ano {ano}: {count:4d} eventos ({actual_pct:5.1f}%) | Desvio: {deviation_from_expected:+5.1f}% {marker}")

        uniform_deviation += abs(deviation_from_expected)

    print(f"\nDesvio total da uniformidade: {uniform_deviation:.1f}%")

    # Análise por categoria
    print(f"\n📂 ANÁLISE POR CATEGORIA:")
    for category in df_events['category'].unique():
        cat_events = analysis_df[analysis_df['eventLabel'].str.contains(category.replace('/', '|'), na=False)]
        if len(cat_events) > 50:  # Só categorias com dados suficientes
            ano_9_pct = (cat_events['ano_pessoal'] == 9).sum() / len(cat_events) * 100
            print(f"   {category}: {len(cat_events)} eventos, Ano 9: {ano_9_pct:.1f}%")

    # Análise por década
    analysis_df['decade'] = (analysis_df['year'] // 10) * 10
    print(f"\n📅 ANÁLISE POR DÉCADA (Ano 9 %):")
    for decade in sorted(analysis_df['decade'].unique()):
        decade_data = analysis_df[analysis_df['decade'] == decade]
        if len(decade_data) > 100:  # Décadas com dados suficientes
            ano_9_pct = (decade_data['ano_pessoal'] == 9).sum() / len(decade_data) * 100
            expected_decade = 11.11  # 1/9
            deviation = ano_9_pct - expected_decade
            marker = "🔴" if ano_9_pct > 13 else "🟢" if ano_9_pct < 9 else "🟡"
            print(f"   {decade}s: {marker} {ano_9_pct:.1f}% ({(decade_data['ano_pessoal'] == 9).sum()}/{len(decade_data)}) | Desvio: {deviation:+.1f}%")

    # Salvar análise completa
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)

    analysis_df.to_csv(os.path.join(output_dir, 'numerology_analysis_5000.csv'), index=False)

    print(f"\n💾 Análise salva em: {output_dir}")

    # Conclusão final
    print(f"\n🔬 CONCLUSÃO FINAL (5000 eventos):")
    print("=" * 50)

    if hypothesis['p_value'] > 0.05:
        print("Com base em análise estatística rigorosa de 5000 eventos históricos,")
        print("NÃO HÁ EVIDÊNCIA de que eventos disruptivos concentrem-se")
        print("em Anos Pessoais 9. A distribuição é estatisticamente uniforme.")
        print("\nIsso sugere que os ciclos numerológicos, tal como implementados,")
        print("não capturam padrões temporais significativos nos eventos históricos.")
    else:
        print("Análise indica POSSÍVEL padrão não-uniforme que requer")
        print("investigação adicional com dados ainda maiores.")
        print("A hipótese merece estudo continuado com metodologias expandidas.")

    print(f"\n📊 Poder estatístico: Com 5000 eventos, podemos detectar")
    print(f"   desvios de apenas {(1.96 * (1/9**0.5) * 100):.1f}% com 95% de confiança.")


if __name__ == "__main__":
    analyze_5000_events()