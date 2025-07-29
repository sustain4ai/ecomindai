def humanize_energy_consumption_units(value):
    """
    Convertit une valeur avec la meilleure unité de consommation énergétique appropriée
    :param value: consommation énergétique à convertir
    :return: consommation énergétique convertit avec la meilleure lisibilité
    """

    return humanize_units(value, ["Wh", "kWh", "MWh", "GWh"])


def humanize_mass_units(value):
    """
    Convertit une valeur avec la meilleure unité de masse appropriée
    :param value: masse à convertir
    :return: masse convertit avec la meilleure lisibilité
    """
    return humanize_units(value, ["g", "kg", "t"])


def humanize_volume_units(value):
    """
    Convertit une valeur avec la meilleure unité de volume appropriée
    :param value: volume à convertir
    :return: volume convertit avec la meilleure lisibilité
    """
    return humanize_units(value, ["L", "m3"])


def humanize_units(value, units):
    """
    Convertit les unités d'une valeur pour obtenir l'unité offrant la meilleure lisibilité possible
    :param value: valeur dont on souhaite calculer l'unité
    :param units: liste des unités possibles pour l'indicateur
    :return: concaténation de la valeur ramené à la meilleure unité lisible et de cette unité
    """
    factor = 1000
    # lors des calculs, les valeurs sont dans leur unité par défaut (kWh, kg ou L), on les remet dans la plus petite unité pour vérifier l'unité la plus adaptée
    value = value * factor
    unit_index = 0

    while (value > factor) and (unit_index < len(units) - 1):
        value = value / factor
        unit_index = unit_index + 1
    return str(round(value, 2)) + " " + str(units[unit_index])
