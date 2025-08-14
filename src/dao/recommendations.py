"""
Récupère les données de recommandations
"""
from typing import List
import pandas as pd
from src.dto.Recommendation import Recommendation

recommendationFile = pd.read_csv("./assets/data/recommendations.csv")


def get_recommendations() -> List[Recommendation]:
    """
    Récupère la liste de recommandations liée à l'utilisation de LLM
    """
    recommandations = []
    for _, row in recommendationFile.iterrows():
        recommandations.append(
            Recommendation(
                type=row.Type, topic=row.Topic, example=row.Example,
                expectedReduction=row["Expected reduction"]))
    return recommandations
