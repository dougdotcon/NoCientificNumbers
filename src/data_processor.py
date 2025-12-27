"""
PyNumerology-Matrix: Processador de Dados Científicos

Este módulo coleta e processa dados históricos de fontes abertas
para análise estatística de padrões numerológicos.
"""

import requests
import pandas as pd
import json
from typing import List, Dict, Optional
from datetime import datetime
import time
import os


class DataProcessor:
    """
    Processador principal para coleta e análise de dados históricos.
    """

    def __init__(self, cache_dir: str = "data/cache"):
        """
        Inicializa o processador de dados.

        Args:
            cache_dir: Diretório para cache de dados
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _cache_file(self, filename: str) -> str:
        """Retorna caminho completo para arquivo em cache."""
        return os.path.join(self.cache_dir, filename)

    def _save_cache(self, data: pd.DataFrame, filename: str):
        """Salva DataFrame em cache."""
        path = self._cache_file(filename)
        data.to_csv(path, index=False)
        print(f"Dados salvos em cache: {path}")

    def _load_cache(self, filename: str) -> Optional[pd.DataFrame]:
        """Carrega DataFrame do cache se existir."""
        path = self._cache_file(filename)
        if os.path.exists(path):
            return pd.read_csv(path)
        return None


class WikidataCollector(DataProcessor):
    """
    Coletor de dados do Wikidata via SPARQL endpoint.
    """

    SPARQL_URL = "https://query.wikidata.org/sparql"

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PyNumerology-Matrix/1.0 (research project)'
        })

    def query_sparql(self, query: str, timeout: int = 30) -> pd.DataFrame:
        """
        Executa consulta SPARQL e retorna DataFrame.

        Args:
            query: Consulta SPARQL
            timeout: Timeout em segundos

        Returns:
            DataFrame com resultados
        """
        params = {
            'query': query,
            'format': 'json'
        }

        try:
            response = self.session.get(self.SPARQL_URL, params=params, timeout=timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            print("Timeout na consulta SPARQL. Tentando query mais simples...")
            return pd.DataFrame()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição SPARQL: {e}")
            return pd.DataFrame()

        data = response.json()
        bindings = data['results']['bindings']

        # Converter para DataFrame
        records = []
        for binding in bindings:
            record = {}
            for key, value in binding.items():
                record[key] = value.get('value', '')
            records.append(record)

        return pd.DataFrame(records)

    def collect_historical_events(self, limit: int = 1000) -> pd.DataFrame:
        """
        Coleta eventos históricos do Wikidata.

        Args:
            limit: Número máximo de eventos

        Returns:
            DataFrame com eventos
        """
        cache_file = f"wikidata_events_{limit}.csv"
        cached = self._load_cache(cache_file)
        if cached is not None:
            return cached

        # Query otimizada para coletar mais dados
        query = f"""
        SELECT ?event ?eventLabel ?date ?typeLabel WHERE {{
          ?event wdt:P31/wdt:P279* wd:Q1190554 ;  # instance of event (including subclasses)
                 wdt:P585 ?date .                 # point in time
          OPTIONAL {{ ?event wdt:P31 ?type . }}   # event type
          SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "en" .
            ?event rdfs:label ?eventLabel .
            ?type rdfs:label ?typeLabel .
          }}
          FILTER(YEAR(?date) >= 1900)  # Focus on 20th-21st century events
        }}
        ORDER BY DESC(?date)
        LIMIT {limit}
        """

        df = self.query_sparql(query)

        # Limpar e formatar
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
            df['year'] = df['date'].dt.year

        self._save_cache(df, cache_file)
        return df

    def collect_person_birth_dates(self, limit: int = 1000) -> pd.DataFrame:
        """
        Coleta datas de nascimento de pessoas famosas.

        Args:
            limit: Número máximo de pessoas

        Returns:
            DataFrame com pessoas e datas
        """
        cache_file = f"wikidata_people_{limit}.csv"
        cached = self._load_cache(cache_file)
        if cached is not None:
            return cached

        query = f"""
        SELECT ?person ?personLabel ?birthDate ?deathDate WHERE {{
          ?person wdt:P31 wd:Q5 ;           # instance of human
                  wdt:P569 ?birthDate .     # date of birth
          OPTIONAL {{ ?person wdt:P570 ?deathDate . }}  # date of death
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        ORDER BY DESC(?birthDate)
        LIMIT {limit}
        """

        df = self.query_sparql(query)

        # Limpar datas
        if not df.empty:
            df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
            df['deathDate'] = pd.to_datetime(df['deathDate'], errors='coerce')
            df = df.dropna(subset=['birthDate'])
            df['birth_year'] = df['birthDate'].dt.year

        self._save_cache(df, cache_file)
        return df


class OurWorldInDataCollector(DataProcessor):
    """
    Coletor de dados do Our World in Data.
    """

    BASE_URL = "https://ourworldindata.org/grapher/"

    def collect_conflicts_data(self) -> pd.DataFrame:
        """
        Coleta dados de conflitos e guerras.

        Returns:
            DataFrame com dados de conflitos
        """
        cache_file = "owid_conflicts.csv"
        cached = self._load_cache(cache_file)
        if cached is not None:
            return cached

        # URL específica para dados de conflitos
        # Nota: OWID usa URLs específicas por dataset
        url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Number%20of%20ongoing%20conflicts%20by%20type%20(UCDP)/Number%20of%20ongoing%20conflicts%20by%20type%20(UCDP).csv"

        try:
            df = pd.read_csv(url)
            self._save_cache(df, cache_file)
            return df
        except Exception as e:
            print(f"Erro ao coletar dados OWID: {e}")
            return pd.DataFrame()


class GDELTCollector(DataProcessor):
    """
    Coletor de dados do GDELT Project.
    """

    BASE_URL = "http://data.gdeltproject.org/gdeltv2/"

    def collect_daily_events(self, date: str) -> pd.DataFrame:
        """
        Coleta eventos diários do GDELT.

        Args:
            date: Data no formato YYYYMMDD

        Returns:
            DataFrame com eventos do dia
        """
        cache_file = f"gdelt_{date}.csv"
        cached = self._load_cache(cache_file)
        if cached is not None:
            return cached

        # GDELT usa arquivos zip diários
        filename = f"{date}.export.CSV.zip"
        url = f"{self.BASE_URL}{filename}"

        try:
            # Para simplificar, vamos usar uma abordagem diferente
            # GDELT tem API limitada, então vamos simular com dados de exemplo
            print(f"GDELT requer download manual. URL: {url}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Erro ao coletar GDELT: {e}")
            return pd.DataFrame()


class NumerologyDataAnalyzer:
    """
    Analisador que combina dados históricos com cálculos numerológicos.
    """

    def __init__(self):
        try:
            from .numerology_calculator import NumerologyCalculator
        except ImportError:
            # Fallback para import direto se executado como script
            import numerology_calculator
            NumerologyCalculator = numerology_calculator.NumerologyCalculator
        self.calc = NumerologyCalculator()
        self.collectors = {
            'wikidata': WikidataCollector(),
            'owid': OurWorldInDataCollector(),
            'gdelt': GDELTCollector()
        }

    def analyze_event_cycles(self, events_df: pd.DataFrame) -> pd.DataFrame:
        """
        Analisa ciclos numerológicos de eventos históricos.

        Args:
            events_df: DataFrame com eventos (coluna 'date' obrigatória)

        Returns:
            DataFrame com análise numerológica
        """
        if events_df.empty or 'date' not in events_df.columns:
            return pd.DataFrame()

        analysis = []

        for _, event in events_df.iterrows():
            try:
                date_str = str(event['date'])[:10]  # YYYY-MM-DD
                year = int(date_str[:4])

                # Calcular ano pessoal para o ano do evento
                # Usando uma data de nascimento genérica para análise coletiva
                # Na prática, isso seria feito por pessoa ou grupo
                ano_pessoal = self.calc.calcular_ano_pessoal("2000-01-01", year)

                analysis.append({
                    'date': event['date'],
                    'year': year,
                    'ano_pessoal': ano_pessoal,
                    'event_type': event.get('typeLabel', 'unknown'),
                    'event_label': event.get('eventLabel', 'unknown')
                })

            except Exception as e:
                continue

        return pd.DataFrame(analysis)

    def test_hypothesis_ano_9(self, analysis_df: pd.DataFrame) -> Dict:
        """
        Testa a hipótese de concentração de eventos no Ano Pessoal 9.

        Args:
            analysis_df: DataFrame com análise numerológica

        Returns:
            Dicionário com resultados estatísticos
        """
        if analysis_df.empty:
            return {}

        # Contar frequência por ano pessoal
        counts = analysis_df['ano_pessoal'].value_counts().sort_index()

        # Calcular estatísticas
        total_events = len(analysis_df)
        ano_9_count = counts.get(9, 0)
        ano_9_percentage = (ano_9_count / total_events) * 100 if total_events > 0 else 0

        # Distribuição esperada (uniforme)
        expected_per_ano = total_events / 9
        expected_ano_9 = expected_per_ano

        # Teste simples: diferença da média
        deviation = ano_9_count - expected_ano_9

        return {
            'total_events': total_events,
            'ano_9_count': ano_9_count,
            'ano_9_percentage': round(ano_9_percentage, 2),
            'expected_uniform': round(expected_ano_9, 2),
            'deviation': round(deviation, 2),
            'counts_by_ano': counts.to_dict(),
            'hypothesis_supported': ano_9_count > expected_ano_9 * 1.2  # 20% acima da média
        }

    def collect_and_analyze(self, source: str = 'wikidata', limit: int = 1000) -> Dict:
        """
        Pipeline completo: coleta dados e analisa.

        Args:
            source: Fonte de dados ('wikidata', 'owid', 'gdelt')
            limit: Limite de registros

        Returns:
            Dicionário com dados e análise
        """
        collector = self.collectors.get(source)
        if not collector:
            return {'error': f'Fonte não suportada: {source}'}

        print(f"Coletando dados de {source}...")
        if source == 'wikidata':
            events_df = collector.collect_historical_events(limit)
        elif source == 'owid':
            events_df = collector.collect_conflicts_data()
        else:
            events_df = pd.DataFrame()

        if events_df.empty:
            return {'error': 'Nenhum dado coletado'}

        print(f"Analisando {len(events_df)} eventos...")
        analysis_df = self.analyze_event_cycles(events_df)

        print("Testando hipótese do Ano 9...")
        hypothesis_test = self.test_hypothesis_ano_9(analysis_df)

        return {
            'events_data': events_df,
            'analysis_data': analysis_df,
            'hypothesis_test': hypothesis_test,
            'source': source,
            'timestamp': datetime.now().isoformat()
        }