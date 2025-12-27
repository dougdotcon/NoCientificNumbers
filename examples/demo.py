#!/usr/bin/env python3
"""
Demonstração prática do PyNumerology-Matrix

Este script mostra como usar a calculadora numerológica para análise pessoal.
"""

import sys
import os

# Adicionar src ao path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from numerology_calculator import NumerologyCalculator


def main():
    """Função principal da demonstração."""
    print("=== PyNumerology-Matrix: Demonstração Científica ===\n")

    # Inicializar calculadora
    calc = NumerologyCalculator()

    # Exemplo: Data de nascimento (pode ser alterada)
    data_nasc = "1995-08-16"  # Exemplo

    print(f"Data de nascimento: {data_nasc}")

    # Calcular Número do Destino
    numero_destino = calc.calcular_numero_destino(data_nasc)
    print(f"Número do Destino: {numero_destino}")

    # Calcular Ano Pessoal atual
    ano_pessoal = calc.calcular_ano_pessoal(data_nasc)
    print(f"Ano Pessoal atual: {ano_pessoal}")

    # Interpretação
    interpretacao = calc.interpretar_ano_pessoal(ano_pessoal)
    print(f"Interpretação: {interpretacao}\n")

    # Análise de ciclo de vida (próximos 5 anos)
    print("=== Análise de Ciclo de Vida (Próximos 5 anos) ===")
    ciclo = calc.analisar_ciclo_vida(data_nasc, 5)

    for ano, dados in ciclo.items():
        print(f"{ano}: Ano {dados['ano_pessoal']} - {dados['interpretacao']}")

    print("\n=== Interpretação Científica ===")
    print("Este algoritmo trata a numerologia como uma função de hash determinística,")
    print("sem elementos místicos. Os 'ciclos' são projeções matemáticas baseadas")
    print("na data de nascimento, permitindo análise estatística de padrões temporais.")
    print("\nPara análise estatística de eventos históricos, consulte data_processor.py")


if __name__ == "__main__":
    main()