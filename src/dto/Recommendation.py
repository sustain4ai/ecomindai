from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    """
    Recommandations personalisées sur comment s'améliorer, en fonction des données d'entrées 
    """
    type: str = Field(...,
                      description="Type de recommandation: General ou Specific")
    topic: str = Field(..., description="Titre de la recommandation")
    example: str = Field(...,
                         description="Détail et exemple de la recommandation")
    expectedReduction: str = Field(...,
                                   description="Pourcentage de réduction attendu")
