import gradio as gr
from src.services.serviceLLM.calculation import calculate_impact_llm
from src.dto.InputData import InputData


def handle_launch(mode, project_duration, duration_slider, model_details, parameters_count, framework,
                  quantization, stages, inference_users, inference_requests,
                  inference_tokens, finetuning_data_size, finetuning_epochs_number,
                  finetuning_batch_size, finetuning_peft,
                  infra_type, infra_cpu_cores, infra_gpu_count, infra_gpu_memory,
                  infra_memory, infra_pue_datacenter, infra_pue_machine, location):
    """
    Lance le calcul d'impact environnemental à partir des paramètres fournis
    et affiche les résultats sur l'interface.
    """
    input_parameters = InputData(mode, duration_slider, model_details, parameters_count, framework,
                                 quantization, stages, inference_users, inference_requests,
                                 inference_tokens, finetuning_data_size, finetuning_epochs_number,
                                 finetuning_batch_size, finetuning_peft,
                                 infra_type, infra_cpu_cores, infra_gpu_count, infra_gpu_memory,
                                 infra_memory, infra_pue_datacenter, infra_pue_machine, location)

    result, _ = calculate_impact_llm(input_parameters)
    best_config = result.more_frugal_conf.split(",")
    return (gr.Tabs(selected=1), gr.update(visible=True),
            gr.update(value="## 📊 Results for " +
                      str(duration_slider)+" years"),
            result.energy_consumption,
            result.carbon_footprint,
            result.abiotic_resource_usage,
            result.water_usage,
            gr.update(value=result.eq_energy_consumption.split("|")[1],
                      label=result.eq_energy_consumption.split("|")[0]),
            gr.update(value=result.eq_carbon_footprint.split("|")[1],
                      label=result.eq_carbon_footprint.split("|")[0]),
            gr.update(value=result.eq_abiotic_resources.split("|")[1],
                      label=result.eq_abiotic_resources.split("|")[0]),
            gr.update(value=result.eq_water_usage.split("|")[1],
                      label=result.eq_water_usage.split("|")[0]),
            result.carbon_footprint_chart,
            result.abiotic_resource_chart,
            result.water_usage_chart,
            gr.update(value="Compare with the most frugal configuration: the model " +
                      best_config[0]+" with " + best_config[1]+" framework"),
            result.percentage_reduction,
            gr.update(value=min(project_duration, duration_slider),
                      maximum=project_duration)
            )
