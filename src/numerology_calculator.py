"""
PyNumerology-Matrix: Calculadora Numerológica Científica

Este módulo implementa cálculos numerológicos baseados em princípios matemáticos,
removendo o misticismo e focando em algoritmos determinísticos.
"""

import datetime
from typing import Union, Tuple


class NumerologyCalculator:
    """
    Calculadora para análises numerológicas científicas.

    Baseada em aritmética modular e redução de dígitos, similar a funções de hash.
    """

    def __init__(self):
        """Inicializa a calculadora."""
        pass

    def _reduzir_digito(self, numero: int) -> int:
        """
        Reduz um número a um dígito único através de soma iterativa.

        Args:
            numero: Número a ser reduzido

        Returns:
            Dígito único (1-9, exceto se entrada for múltiplo de 9)
        """
        if numero == 0:
            return 0

        # Redução por soma de dígitos
        while numero > 9:
            numero = sum(int(d) for d in str(numero))

        return numero

    def calcular_numero_destino(self, data_nasc: str) -> int:
        """
        Calcula o Número do Destino baseado na data de nascimento completa.

        Args:
            data_nasc: Data no formato 'YYYY-MM-DD'

        Returns:
            Número do Destino (1-9)
        """
        # Remover hífens e somar todos os dígitos
        soma_total = sum(int(d) for d in data_nasc.replace('-', ''))

        return self._reduzir_digito(soma_total)

    def calcular_ano_pessoal(self, data_nasc: str, ano_atual: Union[int, None] = None) -> int:
        """
        Calcula o Ano Pessoal para um ano específico.

        Args:
            data_nasc: Data de nascimento no formato 'YYYY-MM-DD'
            ano_atual: Ano para cálculo (padrão: ano atual)

        Returns:
            Ano Pessoal (1-9)
        """
        if ano_atual is None:
            ano_atual = datetime.datetime.now().year

        # Número do Destino
        numero_destino = self.calcular_numero_destino(data_nasc)

        # Ano pessoal = destino + ano_atual, reduzido
        ano_pessoal = numero_destino + ano_atual

        return self._reduzir_digito(ano_pessoal)

    def calcular_mes_pessoal(self, data_nasc: str, ano: int, mes: int) -> int:
        """
        Calcula o Mês Pessoal para um mês específico.

        Args:
            data_nasc: Data de nascimento
            ano: Ano do cálculo
            mes: Mês do cálculo (1-12)

        Returns:
            Mês Pessoal (1-9)
        """
        ano_pessoal = self.calcular_ano_pessoal(data_nasc, ano)
        mes_pessoal = ano_pessoal + mes

        return self._reduzir_digito(mes_pessoal)

    def calcular_dia_pessoal(self, data_nasc: str, data: str) -> int:
        """
        Calcula o Dia Pessoal para uma data específica.

        Args:
            data_nasc: Data de nascimento
            data: Data alvo no formato 'YYYY-MM-DD'

        Returns:
            Dia Pessoal (1-9)
        """
        # Extrair dia da data alvo
        dia = int(data.split('-')[2])

        # Mês pessoal para o mês da data alvo
        ano, mes, _ = data.split('-')
        mes_pessoal = self.calcular_mes_pessoal(data_nasc, int(ano), int(mes))

        dia_pessoal = mes_pessoal + dia

        return self._reduzir_digito(dia_pessoal)

    def interpretar_ano_pessoal(self, ano_pessoal: int) -> str:
        """
        Interpretação científica do Ano Pessoal baseada em analogia física.

        Args:
            ano_pessoal: Ano Pessoal calculado

        Returns:
            Interpretação técnica
        """
        interpretacoes = {
            1: "Status do Sistema: Boot inicial. Instalando novos drivers e protocolos.",
            2: "Status do Sistema: Modo cooperativo. Construindo alianças e redes.",
            3: "Status do Sistema: Modo criativo. Expressão e comunicação intensas.",
            4: "Status do Sistema: Modo estrutural. Construção de fundamentos sólidos.",
            5: "Status do Sistema: Modo de liberdade. Mudanças e expansões.",
            6: "Status do Sistema: Modo harmonioso. Equilíbrio e responsabilidade.",
            7: "Status do Sistema: Modo introspectivo. Análise e reflexão profunda.",
            8: "Status do Sistema: Modo executivo. Manifestação e realização material.",
            9: "Status do Sistema: Limpeza de Cache. Removendo dependências obsoletas."
        }

        return interpretacoes.get(ano_pessoal, "Status desconhecido.")

    def analisar_ciclo_vida(self, data_nasc: str, anos_a_frente: int = 10) -> dict:
        """
        Analisa o ciclo de vida numerológico.

        Args:
            data_nasc: Data de nascimento
            anos_a_frente: Quantos anos analisar à frente

        Returns:
            Dicionário com análise por ano
        """
        ano_atual = datetime.datetime.now().year
        analise = {}

        for i in range(anos_a_frente + 1):
            ano = ano_atual + i
            ano_pessoal = self.calcular_ano_pessoal(data_nasc, ano)
            analise[ano] = {
                'ano_pessoal': ano_pessoal,
                'interpretacao': self.interpretar_ano_pessoal(ano_pessoal)
            }

        return analise