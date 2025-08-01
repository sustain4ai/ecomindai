from os import path

import gradio as gr
import pandas as pd
from matplotlib import pyplot as plt

from src.dto.InputData import InputData
from src.dto.ResultData import ResultData
from src.dto.OutputEstimation import OutputEstimation
from src.dto.InputEstimationLLMInference import InputEstimationLLMInference


from src.services.serviceLLM.util import humanize_energy_consumption_units, humanize_mass_units, humanize_volume_units
from src.dao.recommendations import get_recommendations
from typing import List
from src.dao.inputParameters import fetch_llm_model_configs, fetch_ai_types

# correspondance entre les infrastructureType de l'API et les noms en base
infra_dict = {"SERVER_DC": "Server",
              "LAPTOP": "Laptop", "DESKTOP": "Desktop"}
PROJECT_IMPACT = "Project's impact"
INFERENCE = "Inference"

csv_path = path.join(path.dirname(__file__), "../../../assets/data/")

# lecture des fichiers csv nécessaire aux calculs
param_conf_llm = pd.read_csv(csv_path + "input_parameters_llm.csv")
embodied_impacts = pd.read_csv(csv_path + "embodied_impact.csv")
mixelecs = pd.read_csv(csv_path + "mixelecs.csv")
equivalents = pd.read_csv(csv_path + "equivalents.csv")


def list_AI_types() -> List[str]:
    """
    Liste tous les types d'IA pour lesquels on peut lancer un calcul
    """
    return fetch_ai_types()


def list_llm_model_configs():
    """
    Liste toutes les configurations de llm qui sont disponibles (modèle, nb paramètres, framework & quantization)
    """
    return fetch_llm_model_configs()


def launch_estimation_LLM_inference(input_estimation: InputEstimationLLMInference) -> OutputEstimation:
    """
    Récupère les paramètres d'entrée pour créer le bon ovjet et lancer le calcul de l'impact environnemental pour la partie inférence d'un LLM
    """

    input_parameters = InputData(
        PROJECT_IMPACT, 1, input_estimation.modelName, input_estimation.nbParameters,
        input_estimation.framework, input_estimation.quantization,
        [INFERENCE], 1, 1, input_estimation.totalGeneratedTokens, 0, 0,
        0, "",
        infra_dict[input_estimation.infrastructureType], input_estimation.nbCpuCores,
        input_estimation.nbGpu, input_estimation.gpuMemory,
        input_estimation.ramSize, 1, 1, "France")

    _, results = calculate_impact_llm(input_parameters)
    return OutputEstimation(electricityConsumption=results.electricityConsumption, runtime=results.runtime, recommendations=results.recommendations)


def calculate_impact_llm(input_data: InputData) -> tuple[ResultData, OutputEstimation]:
    """
    Calcule et retourne le résultat de l'impact environnemental à partir des paramètres fournis.
    """

    # Calcul des indicateurs de la configuration sélectionnée
    inference_total_tokens = compute_total_number_tokens(input_data.inference_users,
                                                         input_data.inference_requests,
                                                         input_data.inference_tokens,
                                                         input_data.project_duration)

    coef_selected_config = search_coef_by_parameters(input_data.model_details,
                                                     input_data.parameters_count,
                                                     input_data.framework,
                                                     input_data.quantization)

    conf_energy_consumption = compute_energy_consumption_by_stages(input_data.stages,
                                                                   coef_selected_config,
                                                                   inference_total_tokens)
    runtime = compute_runtime(conf_energy_consumption)

    embodied_impact_list = compute_embodied_impact(runtime,
                                                   input_data.infra_type)

    total_energy_consumption = compute_total_energy_consumption(conf_energy_consumption,
                                                                input_data.infra_pue_datacenter,
                                                                input_data.infra_pue_machine)

    usage_impact_list = compute_usage_impact(total_energy_consumption,
                                             input_data.location)

    # Calcul des indicateurs de la configuration pour la meilleure configuration existante
    best_configuration = find_best_configuration()

    coef_best_configuration = best_configuration.iloc[0]["slope_origin"]

    result_data = ResultData(
        # Renvoie les indicateurs de la configuration sélectionnée
        energy_consumption=str(
            humanize_energy_consumption_units(total_energy_consumption)),
        carbon_footprint=str(
            humanize_mass_units(embodied_impact_list[0] + usage_impact_list[0])) + "CO2eq",
        abiotic_resource_usage=str(
            humanize_mass_units(embodied_impact_list[1] + usage_impact_list[1])) + "Sbeq",
        water_usage=str(humanize_volume_units(
            embodied_impact_list[2] + usage_impact_list[2])),

        # Renvoie les équivalences des indicateurs de la configuration sélectionnée
        eq_energy_consumption=compute_equivalent(
            total_energy_consumption, "energy"),
        eq_carbon_footprint=compute_equivalent(embodied_impact_list[0] + usage_impact_list[0],
                                               "climate change"),
        eq_abiotic_resources=compute_equivalent(embodied_impact_list[1] + usage_impact_list[1],
                                                "abiotic ressources"),
        eq_water_usage=compute_equivalent(embodied_impact_list[2] + usage_impact_list[2],
                                          "water use"),

        # Renvoie les graphiques de la configuration sélectionnée
        carbon_footprint_chart=generate_indicator_summary_fig("carbon_footprint",
                                                              usage_impact_list[0],
                                                              embodied_impact_list[0]),
        abiotic_resource_chart=generate_indicator_summary_fig("abiotic_resource",
                                                              usage_impact_list[1],
                                                              embodied_impact_list[1]),
        water_usage_chart=generate_indicator_summary_fig("water_usage",
                                                         usage_impact_list[2],
                                                         embodied_impact_list[2]),

        # Résultat la partie comment faire mieux
        more_frugal_conf=str(best_configuration.iloc[0]["model"]) + "-" +
        str(best_configuration.iloc[0]["parameters"]) + "," +
        str(best_configuration.iloc[0]["framework"]) + "," +
        str(best_configuration.iloc[0]["quantization"]),
        percentage_reduction="## " +
        str(100-round(coef_best_configuration/coef_selected_config*100))+"%"
    )

    # get static recommendations from database
    reco = get_recommendations()
    # set the right description and expected reduction percentage for the last recommandation of the list which specific & dynamic
    more_frugal_str = "Compare with the most frugal configuration: model=" + str(best_configuration.iloc[0]["model"]) + "-" + str(
        best_configuration.iloc[0]["parameters"]) + ", framework=" + str(best_configuration.iloc[0]["framework"]) + ", & quantization=" + str(best_configuration.iloc[0]["quantization"])
    p_reduction = str(100-round(coef_best_configuration /
                      coef_selected_config*100))+"%"
    reco[len(reco) - 1].example = more_frugal_str
    reco[len(reco) - 1].expectedReduction = p_reduction

    output_estimation = OutputEstimation(
        electricityConsumption=conf_energy_consumption,
        runtime=runtime,
        recommendations=reco
    )

    return result_data, output_estimation


def generate_indicator_summary_fig(criteria, usage_impact, embodied_impact):
    """
    Génère le graphique récapitulatif des indicateurs selon le type d'indicateur

    :param criteria: le type d'indicateur dont on souhaite récupérer le graphique
    :param usage_impact: données d'indicateur lié à l'usage
    :param embodied_impact: données d'indicateur inhérente
    :return: renvoie le graphique récapitulatif des indicateurs du type d'indicateur souhaité
    """

    title = "Titre du graphique"
    indicator_labels = ["Use (scope 2)", "Embodied\n(scope 3)"]
    match criteria:
        case "carbon_footprint":
            title = "Carbon footprint : " + \
                str(humanize_mass_units(usage_impact + embodied_impact))
        case "abiotic_resource":
            title = "Abiotic resource use : " + str(
                humanize_mass_units(usage_impact + embodied_impact))
        case "water_usage":
            title = "Water usage : " + \
                str(humanize_volume_units(usage_impact + embodied_impact))

    indicator_summary_fig, indicator_summary_ax = plt.subplots()
    indicator_summary_fig.set_size_inches(5, 4)
    indicator_summary_values = [usage_impact, embodied_impact]

    indicator_summary_ax.pie(
        x=indicator_summary_values,
        labels=indicator_labels,
        colors=["#0a9396", "#94d2bd"],
        autopct="%1.2f%%",
        radius=1
    )
    indicator_summary_ax.set_title(label=title)
    # Fermer l'interface à chaque fois pour éviter de garder toutes les figures créées et sur consommer de la mémoire
    plt.close()
    return indicator_summary_fig


def compute_total_number_tokens(nb_users, nb_requests, nb_tokens_one_inference, project_duration):
    return nb_users * nb_requests * nb_tokens_one_inference * project_duration


def compute_energy_consumption_by_stages(stages, coef, inference_total_tokens):
    """
    Calcule la consommation énergétique de la configuration pour une étape donnée

    :param stages: les étapes du cycle de vie du système d'IA pour lesquelles on veut faire les estimations
    :param coef: le coefficient à appliquer pour transformer le nombre de tokens générés en énergie consommée
    :param inference_total_tokens: nombre total de tokens générés pendant toutes les inférences
    :return: l'énergie consommée par la configuration (en Wh)
    """

    match stages[0]:
        case "Inference":
            return coef * inference_total_tokens

        case "Finetuning":
            raise gr.Warning("Finetuning computation is not handled")


def search_coef_by_parameters(model, parameters, framework, quantization):
    """
    Récupère dans le dataframe param_conf_llm le coefficient à appliquer à une configuration

    :param model: modèle utilisée par la configuration
    :param parameters: nombre de paramètres de la configuration
    :param framework: framework de la configuration
    :param quantization: quantification de la configuration
    :return: le coefficient associé à la configuration
    """
    try:
        filtered_df = param_conf_llm[(param_conf_llm["model"] == model) &
                                     (param_conf_llm["parameters"] == parameters) &
                                     (param_conf_llm["quantization"] == quantization) &
                                     (param_conf_llm["framework"] == framework)]

        return float(filtered_df.iloc[0]["slope_origin"])
    except:
        raise gr.Error("Cannot find coefficient for " + str(model) + " parameters " +
                       str(parameters) + " framework " + str(framework) + " quantization " +
                       str(quantization))


def compute_runtime(energy_consumption):
    """
    Calcule le runtime associée à la consommation énergétique d'une solution

    :param energy_consumption: consommation énergétique de la solution
    :return: le runtime associée à la consommation énergétique
    """

    seconds_per_hour = 3600
    runtime_coef = 11757
    return (energy_consumption * runtime_coef) / seconds_per_hour


def compute_embodied_impact(runtime, infrastructure_type):
    """
    Calcule l'impact inhérent à une configuration selon le type d'infrastructure

    :param runtime: runtime associé à la solution
    :param infrastructure_type: type d'infrastructure dont on souhaite obtenir l'impact inhérent
    :return: l'impact inhérent à la configuration
    """

    dataframe = search_embodied_impact(infrastructure_type)

    try:
        climate_change_impact_df = dataframe[(
            dataframe["criteria"] == "Climate change")]
        # Multiplication par 1000 pour avoir les valeurs en grammes au lieu de kg
        climate_change_impact = (float(climate_change_impact_df.iloc[0]["value"]) * runtime /
                                 float(climate_change_impact_df.iloc[0]["hours_life_time"]))
    except:
        raise gr.Error("Cannot find embodied climate change impact")

    try:
        resource_use_impact_df = dataframe[(
            dataframe["criteria"] == "Resource use")]
        # Multiplication par 1000 pour avoir les valeurs en grammes au lieu de kg
        resource_use_impact = (float(resource_use_impact_df.iloc[0]["value"]) * runtime /
                               float(resource_use_impact_df.iloc[0]["hours_life_time"]))
    except:
        raise gr.Error("Cannot find embodied resource use impact")

    try:
        water_use_impact_df = dataframe[(dataframe["criteria"] == "Water use")]
        # Multiplication par 1000 pour avoir les valeurs en L au lieu de m3
        water_use_impact = (float(water_use_impact_df.iloc[0]["value"]) * runtime /
                            float(water_use_impact_df.iloc[0]["hours_life_time"]))
    except:
        raise gr.Error("Cannot find embodied water usage impact")

    return [climate_change_impact, resource_use_impact, water_use_impact]


def search_embodied_impact(infrastructure_type):
    """
    Récupère dans le dataframe embodied_impact_db les impacts inhérents à un type d'infrastructure
    :param infrastructure_type: type d'infrastructure dont on souhaite récupérer les impacts
    :return: les impacts inhérents à l'infrastructure
    """
    return embodied_impacts[(embodied_impacts["infrastructure_type"] == infrastructure_type)]


def compute_total_energy_consumption(energy_consumption, datacenter_pue, infra_machine_pue):
    """
    Calcule l'énergie totale consommée par une configuration pour son type d'infrastructure

    :param energy_consumption: énergie consommée par la configuration basé son coéfficient
    :param datacenter_pue: pue du centre de données de l'infrastructure de la configuration
    :param infra_machine_pue: pue propre à l'infrastructure de la configuration
    :return: l'énergie totale consommée par une configuration pour son type d'infrastructure
    """

    return energy_consumption * datacenter_pue * infra_machine_pue


def compute_usage_impact(total_energy_consumption, location):
    """
    Calcule l'impact de l'utilisation de la configuration

    :param total_energy_consumption: énergie totale consommée par la configuration
    :param location: pays dans lequel s'applique la configuration
    :return: impact de l'utilisation de la configuration
    """

    dataframe = search_location_usage_impact(location)

    try:
        climate_change_impact_df = dataframe[(
            dataframe["criteria"] == "Climate change")]
        # Multiplication par 1000 pour avoir les valeurs en grammes au lieu de kg
        climate_change_impact = (total_energy_consumption *
                                 float(climate_change_impact_df.iloc[0]["value"]))
    except:
        print(str(location) + " usedClimateChangeImpact introuvable")
        climate_change_impact = 0

    try:
        resource_use_impact_df = dataframe[(
            dataframe["criteria"] == "Resource use")]
        # Multiplication par 1000 pour avoir les valeurs en grammes au lieu de kg
        resource_use_impact = (total_energy_consumption *
                               float(resource_use_impact_df.iloc[0]["value"]))
    except:
        print(str(location) + " usedResourceUseImpact introuvable")
        resource_use_impact = 0

    try:
        water_use_impact_df = dataframe[(dataframe["criteria"] == "Water use")]
        # Multiplication par 1000 pour avoir les valeurs en L au lieu de m3
        water_use_impact = (total_energy_consumption *
                            float(water_use_impact_df.iloc[0]["value"]))
    except:
        print(str(location) + " usedWaterUseImpact introuvable")
        water_use_impact = 0

    return [climate_change_impact, resource_use_impact, water_use_impact]


def search_location_usage_impact(location):
    """
    Lit un csv et retrouve les impacts de l'utilisation du mix énergétique selon le pays
    :param location: pays de la configuration
    :return: les impacts de l'utilisation du mix énergétique
    """

    return mixelecs[(mixelecs["location"] == location)]


def compute_equivalent(value, criteria):
    """
    Calcule l'équivalence d'un indicateur
    :param value: valeur de l'indicateur dont on souhaite calculer l'équivalence
    :param criteria: type d'indicateur dont on souhaite calculer l'équivalence
    :return: concaténation de l'unité et de la valeur de l'équivalence de l'indicateur
    """
    # lors des calculs, les valeurs sont dans leur unité par défaut (kWh, kg ou L), on les remet ici dans la plus petite unité pour vérifier l'unité la plus adaptée parmis les correspondances
    value = value*1000
    try:
        filtered_df = equivalents[(equivalents["criteria"] == criteria) &
                                  (equivalents["quantity"] < value)]

        equivalence_row = filtered_df[(
            filtered_df["quantity"] == filtered_df["quantity"].max())]

        equivalence_unit = equivalence_row.iloc[0]["equivalent_units"]
        equivalence_value = round(
            value / equivalence_row.iloc[0]["quantity"], 2)

        return str(equivalence_unit) + "|" + str(equivalence_value)
    except:
        try:
            filtered_df = equivalents[(equivalents["criteria"] == criteria)]

            equivalence_row = filtered_df[
                (filtered_df["quantity"] == filtered_df["quantity"].min())]

            equivalence_unit = equivalence_row.iloc[0]["equivalent_units"]
            equivalence_value = round(
                value / equivalence_row.iloc[0]["quantity"], 2)

            return str(equivalence_unit) + "|" + str(equivalence_value)
        except:
            return str(criteria) + "|No equivalence calculated"


def find_best_configuration():
    """
    Lit un csv et retrouve la meilleure configuration connue sur la base du coefficient
    :return: la configuration ayant le plus petit coefficient
    """

    return param_conf_llm[(param_conf_llm["slope_origin"] == param_conf_llm["slope_origin"].min())]
