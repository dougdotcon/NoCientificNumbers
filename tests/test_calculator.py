"""
Testes unitários para NumerologyCalculator
"""

import sys
import os
import unittest

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from numerology_calculator import NumerologyCalculator


class TestNumerologyCalculator(unittest.TestCase):
    """Testes para a calculadora numerológica."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.calc = NumerologyCalculator()

    def test_reduzir_digito(self):
        """Testa a redução de dígitos."""
        self.assertEqual(self.calc._reduzir_digito(39), 3)
        self.assertEqual(self.calc._reduzir_digito(12), 3)
        self.assertEqual(self.calc._reduzir_digito(9), 9)
        self.assertEqual(self.calc._reduzir_digito(0), 0)

    def test_calcular_numero_destino(self):
        """Testa cálculo do Número do Destino."""
        # 1995-08-16: 1+9+9+5+0+8+1+6 = 39 -> 3+9 = 12 -> 1+2 = 3
        self.assertEqual(self.calc.calcular_numero_destino("1995-08-16"), 3)

        # 2000-01-01: 2+0+0+0+0+1+0+1 = 4
        self.assertEqual(self.calc.calcular_numero_destino("2000-01-01"), 4)

    def test_calcular_ano_pessoal(self):
        """Testa cálculo do Ano Pessoal."""
        # Para 1995-08-16 (destino 3) em 2025: 3 + 2025 = 2028 -> 2+0+2+8=12 -> 1+2=3
        self.assertEqual(self.calc.calcular_ano_pessoal("1995-08-16", 2025), 3)

        # Mesmo ano, deve ser consistente
        self.assertEqual(self.calc.calcular_ano_pessoal("1995-08-16", 2025), 3)

    def test_interpretar_ano_pessoal(self):
        """Testa interpretações."""
        interpretacao_9 = self.calc.interpretar_ano_pessoal(9)
        self.assertIn("Limpeza de Cache", interpretacao_9)

        interpretacao_1 = self.calc.interpretar_ano_pessoal(1)
        self.assertIn("Boot inicial", interpretacao_1)

    def test_analisar_ciclo_vida(self):
        """Testa análise de ciclo de vida."""
        ciclo = self.calc.analisar_ciclo_vida("1995-08-16", 2)
        self.assertIn(2025, ciclo)
        self.assertIn(2026, ciclo)
        self.assertIn(2027, ciclo)

        # Verificar que cada ano tem ano_pessoal e interpretação
        for ano, dados in ciclo.items():
            self.assertIn('ano_pessoal', dados)
            self.assertIn('interpretacao', dados)
            self.assertIsInstance(dados['ano_pessoal'], int)
            self.assertIsInstance(dados['interpretacao'], str)


if __name__ == '__main__':
    unittest.main()