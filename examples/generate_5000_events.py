#!/usr/bin/env python3
"""
Geração de Dataset de 5000 Eventos para Análise Numerológica

Cria dataset sintético-realista baseado em padrões históricos
para análise estatística robusta da hipótese numerológica.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime


def generate_5000_events():
    """
    Gera exatamente 5000 eventos históricos com distribuição realista.
    """

    # Base de eventos históricos reais por categoria
    event_templates = {
        'Guerra/Conflito': [
            'Guerra em {region} ({year})',
            'Conflito armado na {region}',
            'Batalha de {location} ({year})',
            'Invasão de {country}',
            'Revolução em {country}',
            'Golpe militar em {country}',
            'Crise internacional envolvendo {countries}',
        ],
        'Crise Econômica': [
            'Crise financeira em {region}',
            'Recessão econômica global',
            'Colapso bancário em {country}',
            'Inflação alta em {region}',
            'Dívida soberana de {country}',
            'Quebra da bolsa em {location}',
            'Crise cambial em {region}',
        ],
        'Avanço Científico/Tecnológico': [
            'Descoberta científica em {field}',
            'Avanço tecnológico em {field}',
            'Novo tratamento médico para {disease}',
            'Lançamento de {technology}',
            'Sequenciamento do {organism}',
            'Descoberta de {element}',
            'Teoria revolucionária em {field}',
        ],
        'Desastre Natural': [
            'Terremoto em {location}',
            'Furacão {name} atinge {region}',
            'Inundação em {region}',
            'Tsunami no {ocean}',
            'Erupção vulcânica em {volcano}',
            'Seca prolongada em {region}',
            'Incêndio florestal em {region}',
        ],
        'Evento Político/Social': [
            'Eleições presidenciais em {country}',
            'Independência de {country}',
            'Tratado internacional assinado',
            'Movimento social em {country}',
            'Mudança constitucional em {country}',
            'Reforma política em {region}',
            'Acordo de paz em {region}',
        ],
        'Avanço Médico/Saúde': [
            'Vacina desenvolvida para {disease}',
            'Novo medicamento para {condition}',
            'Avanço em cirurgia {type}',
            'Descoberta sobre {disease}',
            'Programa de saúde pública em {country}',
            'Crise de saúde global',
            'Pandemia de {disease}',
        ],
        'Avanço Espacial/Astronômico': [
            'Lançamento de {satellite}',
            'Missão espacial para {destination}',
            'Descoberta astronômica: {discovery}',
            'Novo telescópio: {name}',
            'Exploração de {planet}',
            'Cometa {name} observado',
            'Eclipse {type} visível em {region}',
        ]
    }

    # Dados para preenchimento dos templates
    regions = ['Europa', 'Ásia', 'América do Norte', 'América do Sul', 'África',
               'Oceania', 'Oriente Médio', 'Sudeste Asiático', 'América Central']

    countries = ['Estados Unidos', 'Reino Unido', 'França', 'Alemanha', 'Itália',
                 'Japão', 'China', 'Índia', 'Brasil', 'Rússia', 'Canadá', 'Austrália',
                 'México', 'Argentina', 'Espanha', 'Coreia do Sul', 'Arábia Saudita']

    cities = ['Nova York', 'Londres', 'Paris', 'Berlim', 'Tóquio', 'Pequim',
              'Moscou', 'Sydney', 'Rio de Janeiro', 'Cidade do México']

    fields = ['Física', 'Química', 'Biologia', 'Medicina', 'Engenharia', 'Matemática',
              'Astronomia', 'Geologia', 'Psicologia', 'Economia']

    diseases = ['Câncer', 'Diabetes', 'HIV/AIDS', 'Malária', 'Tuberculose',
                'Alzheimer', 'Parkinson', 'Cardiovasculares']

    technologies = ['Computador', 'Internet', 'Telefone celular', 'Carro elétrico',
                   'Inteligência Artificial', 'Robô', 'Drones', 'Realidade Virtual']

    # Gerar 5000 eventos
    events = []
    np.random.seed(42)  # Para reprodutibilidade

    for i in range(5000):
        # Escolher categoria baseada em distribuição histórica realista
        category_weights = {
            'Guerra/Conflito': 0.25,      # 25% - guerras são frequentes na história
            'Crise Econômica': 0.15,      # 15% - crises econômicas recorrentes
            'Avanço Científico/Tecnológico': 0.20,  # 20% - avanços constantes
            'Desastre Natural': 0.10,     # 10% - desastres naturais
            'Evento Político/Social': 0.15,  # 15% - eventos políticos
            'Avanço Médico/Saúde': 0.10,  # 10% - avanços médicos
            'Avanço Espacial/Astronômico': 0.05  # 5% - eventos espaciais mais raros
        }

        category = np.random.choice(list(category_weights.keys()),
                                   p=list(category_weights.values()))

        # Escolher template
        template = np.random.choice(event_templates[category])

        # Gerar ano com distribuição não-uniforme (mais eventos recentes)
        # Usar distribuição exponencial para favorecer anos recentes
        recent_bias = np.random.exponential(scale=30)  # Eventos mais recentes têm mais probabilidade
        year = int(2025 - min(recent_bias, 120))  # Máximo 120 anos atrás
        year = max(1900, min(2025, year))

        # Preencher template com dados aleatórios
        event_text = template.format(
            region=np.random.choice(regions),
            country=np.random.choice(countries),
            countries=f"{np.random.choice(countries)} e {np.random.choice(countries)}",
            location=np.random.choice(cities),
            field=np.random.choice(fields),
            disease=np.random.choice(diseases),
            technology=np.random.choice(technologies),
            name=f"Evento_{i}",
            ocean="Pacífico",
            volcano="Vulcão_X",
            organism="Genoma_Y",
            element="Elemento_Z",
            type="Cardíaca",
            satellite="Satélite_X",
            destination="Marte",
            discovery="Novo planeta",
            planet="Marte",
            condition="Hipertensão",
            year=year
        )

        # Determinar impacto baseado na categoria
        impact_weights = {
            'Guerra/Conflito': {'Alto': 0.7, 'Médio': 0.2, 'Baixo': 0.1},
            'Crise Econômica': {'Alto': 0.6, 'Médio': 0.3, 'Baixo': 0.1},
            'Avanço Científico/Tecnológico': {'Alto': 0.5, 'Médio': 0.3, 'Baixo': 0.2},
            'Desastre Natural': {'Alto': 0.8, 'Médio': 0.15, 'Baixo': 0.05},
            'Evento Político/Social': {'Alto': 0.4, 'Médio': 0.4, 'Baixo': 0.2},
            'Avanço Médico/Saúde': {'Alto': 0.6, 'Médio': 0.3, 'Baixo': 0.1},
            'Avanço Espacial/Astronômico': {'Alto': 0.7, 'Médio': 0.2, 'Baixo': 0.1}
        }

        impact = np.random.choice(['Alto', 'Médio', 'Baixo'],
                                 p=list(impact_weights[category].values()))

        events.append({
            'date': f'{year}-01-01',
            'year': year,
            'eventLabel': event_text,
            'typeLabel': category,
            'category': category,
            'impact': impact,
            'source': 'Synthetic_Historical_Dataset',
            'event_id': i + 1
        })

    return pd.DataFrame(events)


def save_5000_events_dataset():
    """Salva dataset de 5000 eventos."""
    print("Gerando dataset de 5000 eventos históricos...")

    df = generate_5000_events()

    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, 'historical_events_5000_synthetic.csv')
    df.to_csv(filepath, index=False)

    print("✅ Dataset salvo com sucesso!")
    print(f"📊 Total de eventos: {len(df)}")
    print(f"📅 Período: {df['year'].min()}-{df['year'].max()}")
    print(f"📂 Categorias únicas: {df['category'].nunique()}")
    print(f"🎯 Distribuição por categoria:")
    print(df['category'].value_counts())
    print(f"🎯 Distribuição por impacto:")
    print(df['impact'].value_counts())
    print(f"📈 Eventos por ano (top 5):")
    print(df['year'].value_counts().head())

    return df


if __name__ == "__main__":
    save_5000_events_dataset()