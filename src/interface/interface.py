from os import path

import gradio as gr
import pandas as pd

from src.services.serviceLLM.doc import load_doc
from src.interface.handlers import handle_launch

head_path = path.join(path.dirname(__file__),
                      "../../assets/partials/head.html")
css_path = path.join(path.dirname(__file__), "../../assets/styles/app.css")
csv_path = path.join(path.dirname(__file__), "../../assets/data/")


# Point d'entrée de l'application
with gr.Blocks(title="EcoMindAI v2", head_paths=head_path, css_paths=css_path,
               analytics_enabled=False) as io:
    title = gr.HTML("""<h1 class=\"logo\">EcoMindAI</h1>
        <p>Estimating the environmental impact of an language model project </p>""")

    with gr.Tabs() as tabs:

        # Onglet des paramètres d'entrée
        with gr.Tab("📝 Input parameters", id=0, elem_classes="page") as calculator:
            with gr.Row():
                with gr.Column(scale=2):
                    gr.Markdown("## 📝 Input parameters")
                launch_btn = gr.Button("⯈ Launch impact estimation",
                                       variant="primary", scale=1, interactive=True)

            # Choix du mode
            mode = gr.Radio(
                ["Project's impact"], label="Mode", value="Project's impact")

            # Mode "impact projet"
            with gr.Column(visible=True) as project_impact:
                gr.HTML("<hr>", padding=False)
                project_duration = gr.Number(value=5, label="Estimated project duration (in years)",
                                             minimum=1, maximum=50)

                gr.Markdown("### Algorithm")
                with gr.Row() as algorithm:
                    dataframe = pd.read_csv(
                        csv_path + "input_parameters_llm.csv")
                    model_details = gr.Dropdown(label="Model details",
                                                choices=list(dict.fromkeys(
                                                    dataframe["model"].tolist())),
                                                value="llama3")
                    model_details_df = dataframe[(
                        dataframe["model"] == "llama3")]
                    parameters_count = gr.Dropdown(label="Parameters",
                                                   choices=list(dict.fromkeys(
                                                       model_details_df["parameters"].tolist())),
                                                   value="13b")
                    model_parameters_df = model_details_df[
                        (model_details_df["parameters"] == "13b")]
                    framework = gr.Dropdown(label="Framework",
                                            choices=list(dict.fromkeys(
                                                model_parameters_df["framework"].tolist())),
                                            value="llamacpp")
                    model_parameters_framework_df = model_parameters_df[
                        (model_details_df["framework"] == "llamacpp")]
                    quantization = gr.Dropdown(label="Quantization",
                                               choices=list(dict.fromkeys(
                                                   model_parameters_framework_df["quantization"]
                                                   .tolist())),
                                               value="8bit0")

                def handle_model_details(selected_model):
                    filtered_df = dataframe[(
                        dataframe["model"] == selected_model)]
                    return (
                        gr.Dropdown(label="Parameters",
                                    choices=list(dict.fromkeys(
                                        filtered_df["parameters"].tolist())),
                                    value=filtered_df.iloc[0]["parameters"]),
                        gr.Dropdown(label="Framework",
                                    choices=list(dict.fromkeys(
                                        filtered_df["framework"].tolist())),
                                    value=filtered_df.iloc[0]["framework"]),
                        gr.Dropdown(label="Quantization", choices=list(
                            dict.fromkeys(filtered_df["quantization"].tolist())),
                            value=filtered_df.iloc[0]["quantization"]))

                model_details.change(handle_model_details, inputs=model_details,
                                     outputs=[parameters_count, framework, quantization])

                def handle_parameters_count(selected_model, selected_parameters):
                    filtered_df = dataframe[(dataframe["model"] == selected_model) &
                                            (dataframe["parameters"] == selected_parameters)]
                    return (
                        gr.Dropdown(label="Framework", choices=list(dict.fromkeys(
                            filtered_df["framework"].tolist())),
                            value=filtered_df.iloc[0]["framework"]),
                        gr.Dropdown(label="Quantization", choices=list(dict.fromkeys(
                            filtered_df["quantization"].tolist())),
                            value=filtered_df.iloc[0]["quantization"]))

                parameters_count.change(handle_parameters_count,
                                        inputs=[model_details,
                                                parameters_count],
                                        outputs=[framework, quantization])

                def handle_framework(selected_model, selected_parameters, selected_framework):
                    filtered_df = dataframe[(dataframe["model"] == selected_model) &
                                            (dataframe["parameters"] == selected_parameters) &
                                            (dataframe["framework"] == selected_framework)]
                    return (
                        gr.Dropdown(label="Quantization", choices=list(
                            dict.fromkeys(filtered_df["quantization"].tolist())),
                            value=filtered_df.iloc[0]["quantization"]))

                framework.change(handle_framework,
                                 inputs=[model_details,
                                         parameters_count, framework],
                                 outputs=quantization)

                # Affichage dynamique des étapes
                gr.Markdown("### Stages")
                # La phase d'inférence est cochée par défaut
                stages = gr.CheckboxGroup(
                    choices=["Inference", "Finetuning ⚠️"], show_label=False, value="Inference")

                with gr.Column(visible=True) as inference_stage:
                    gr.Markdown("#### Inference")
                    with gr.Column():
                        with gr.Row():
                            inference_users = gr.Number(label="Number of users per year", minimum=1,
                                                        maximum=1000000000, value=10000, elem_classes="inference")
                            inference_requests = gr.Number(label="Average number of requests per year",
                                                           minimum=1, maximum=1000000000, value=200, elem_classes="inference")
                            inference_tokens = gr.Number(
                                label="Average number of tokens generated per request",
                                minimum=1, maximum=1000000000, value=500, elem_classes="inference"
                            )
                            inference_total_tokens_str = gr.Text(
                                label="⤇ Total number of generated tokens", value="5.0G", interactive=False, elem_classes="inference"
                            )
                with gr.Column(visible=False, elem_classes="wip") as finetuning_stage:
                    gr.Markdown(
                        """#### 🏗️ Finetuning WIP: it will not be taken into account in your estimation
                        We will need more data to factor it into the estimate""")
                    with gr.Row():
                        finetuning_type = gr.Radio(
                            ["supervised finetuning", "RLHF"], label="Type of finetuning", interactive=False)
                        finetuning_data_size = gr.Number(label="Size of the new dataset (in GB)",
                                                         minimum=1,
                                                         maximum=1000000000, value=500, interactive=False)
                        finetuning_epochs_number = gr.Number(label="Number of epochs",
                                                             minimum=1, maximum=1000000000,
                                                             value=12, interactive=False)
                        finetuning_batch_size = gr.Number(label="Size of the batch",
                                                          minimum=1, maximum=1000000000,
                                                          value=10000, interactive=False)
                        finetuning_peft = gr.Dropdown(label="PEFT method used",
                                                      choices=["LoRA", "prefix tuning", "p-tuning",
                                                               "prompt tuning"])

                def show_stages(selected_stages):
                    return gr.update(visible=("Inference" in selected_stages)), gr.update(
                        visible=("Finetuning ⚠️" in selected_stages))

                stages.change(show_stages, inputs=stages,
                              outputs=[inference_stage, finetuning_stage])

                gr.HTML("<hr>", padding=False)
                gr.Markdown("### Infrastructure")
                with gr.Row():
                    infra_type = gr.Dropdown(label="Type",
                                             choices=["Server", "Desktop", "Laptop",
                                                      "AI Cloud Service"])
                with gr.Column() as infra_dedicated:
                    with gr.Row():
                        infra_cpu_cores = gr.Number(label="CPU cores", minimum=0, maximum=1024,
                                                    value=30)
                        infra_gpu_count = gr.Number(label="GPU count", minimum=0, maximum=1024,
                                                    value=2)
                        infra_gpu_memory = gr.Number(label="GPU memory (GB)", minimum=0,
                                                     maximum=2048, value=32)
                        infra_memory = gr.Number(label="RAM size (GB)", minimum=1, maximum=2048,
                                                 value=64)
                    gr.Markdown("#### Power effectiveness")
                    with gr.Row():
                        infra_pue_datacenter = gr.Number(label="Datacenter PUE", minimum=1,
                                                         maximum=10, value=1.5, step=0.01,
                                                         info="To learn more about the Power Usage Effectiveness and how it is calculated, check this page related to [PUE](https://en.wikipedia.org/wiki/Power_usage_effectiveness).",
                                                         elem_classes="show-disabled")
                        infra_pue_machine = gr.Number(label="Complementary PUE", minimum=1,
                                                      maximum=10, value=1.3, step=0.01,
                                                      info="Power used for the operating of OS, virtualization, control plan, idle... To learn more about it, visit our documentation page.", )
                with gr.Column(visible=False) as infra_service:
                    gr.HTML(
                        "<div class=\"not-implemented\">🏗️ Not implemented yet</div>")

                def handle_inference_total_tokens(project_duration, inference_users, inference_requests, inference_tokens):
                    total = project_duration*inference_users * \
                        inference_requests*inference_tokens
                    if (total > 1000000000):
                        total_str = str(round(total/1000000000, 3))+"G"
                    elif (total > 1000000):
                        total_str = str(round(total/1000000, 3))+"M"
                    elif (total > 1000):
                        total_str = str(round(total/1000, 3))+"k"
                    else:
                        total_str = str(total)
                    return gr.update(value=total_str)

                project_duration.change(handle_inference_total_tokens, inputs=[project_duration, inference_users, inference_requests, inference_tokens],
                                        outputs=inference_total_tokens_str)
                inference_users.change(handle_inference_total_tokens, inputs=[project_duration, inference_users, inference_requests, inference_tokens],
                                       outputs=inference_total_tokens_str)
                inference_requests.change(handle_inference_total_tokens, inputs=[project_duration, inference_users, inference_requests, inference_tokens],
                                          outputs=inference_total_tokens_str)
                inference_tokens.change(handle_inference_total_tokens, inputs=[project_duration, inference_users, inference_requests, inference_tokens],
                                        outputs=inference_total_tokens_str)

                def handle_infra_type(infra_type):
                    if infra_type == "AI Cloud Service":
                        return gr.update(visible=False), gr.update(
                            visible=True), None, None, None, None, None
                    elif infra_type == "Desktop":
                        return gr.update(visible=True), gr.update(visible=False), gr.update(
                            value=1.0, interactive=False), gr.update(value=8), gr.update(
                            value=1), gr.update(value=12), gr.update(value=32)
                    elif infra_type == "Laptop":
                        return gr.update(visible=True), gr.update(visible=False), gr.update(
                            value=1.0, interactive=False), gr.update(value=8), gr.update(
                            value=0), gr.update(value=0), gr.update(value=16)
                    # infratype = "Server"
                    else:
                        return gr.update(visible=True), gr.update(visible=False), gr.update(
                            value=1.5, interactive=True), gr.update(value=30), gr.update(
                            value=2), gr.update(value=32), gr.update(value=64)

                infra_type.change(handle_infra_type, inputs=infra_type,
                                  outputs=[infra_dedicated, infra_service, infra_pue_datacenter,
                                           infra_cpu_cores, infra_gpu_count, infra_gpu_memory,
                                           infra_memory])

                # peremttre d'appuyer sur le bouton uniquement quand les champs nécéssaires sont remplis
                def enable_launch_button(infra_type, mode, selected_stages):
                    if (
                            infra_type != "AI Cloud Service" and mode == "Project's impact" and "Inference" in selected_stages):
                        return gr.update(interactive=True)
                    else:
                        return gr.update(interactive=False)

                infra_type.change(enable_launch_button, inputs=[infra_type, mode, stages],
                                  outputs=launch_btn)

                mode.change(enable_launch_button, inputs=[infra_type, mode, stages],
                            outputs=launch_btn)

                stages.change(enable_launch_button, inputs=[infra_type, mode, stages],
                              outputs=launch_btn)

                gr.HTML("<hr>", padding=False)
                gr.Markdown("### Energy efficiency")
                with gr.Row() as energy_efficiency:
                    location_df = pd.read_csv(csv_path + "mixelecs.csv")
                    location = gr.Dropdown(label="Location", choices=list(dict.fromkeys(
                        location_df["location"].tolist())),
                        value="Germany")

        # Onglet des résultats
        with gr.Tab("📊 Results", id=1, visible=False, elem_classes="page") as results:

            with gr.Row(elem_classes="duration"):
                results_title = gr.Markdown("## 📊 Results for X years")
                duration_slider = gr.Slider(1, 5, value=3, step=1,
                                            label='Choose the duration for which you want to visualize your impact', elem_classes="slider")

            gr.Markdown("### Environmental impact "
                        "<small>(for both stages use and embodied)</small>")
            with gr.Row():
                energy_consumption = gr.Text(label="⚡ Energy consumption", value="X Wh",
                                             elem_classes="result")
                carbon_footprint = gr.Text(label="🌫️ Carbon footprint", value="X gCO2eq",
                                           elem_classes="result")
                abiotic_resource_usage = gr.Text(label="⛏️ Abiotic resource use", value="X gSbeq",
                                                 elem_classes="result")
                water_usage = gr.Text(
                    label="💧 Water usage *", value="X mL", elem_classes="result")
            with gr.Row():
                gr.Markdown("↕", elem_classes="equiv")
                gr.Markdown("↕", elem_classes="equiv")
                gr.Markdown("↕", elem_classes="equiv")
                gr.Markdown("↕", elem_classes="equiv")

            with gr.Row():
                eq_energy_consumption = gr.Text(label="Energy consumption", value="X hours",
                                                elem_classes="result")
                eq_carbon_footprint = gr.Text(label="Carbon footprint", value="X",
                                              elem_classes="result")
                eq_abiotic_resources = gr.Text(label="Abiotic resources", value="X",
                                               elem_classes="result")
                eq_water_usage = gr.Text(
                    label="Water usage", value="X", elem_classes="result")

            gr.Markdown(
                "\* the water usage is calculated only for the scope 3 because of the lack of open data about the water usage related to energy consumption", elem_classes="asterisk")
            gr.Markdown(
                "### Visualize the proportion of use and embodied impacts")
            with gr.Row():
                carbon_footprint_chart = gr.Plot(
                    show_label=False, container=False)
                abiotic_resource_chart = gr.Plot(
                    show_label=False, container=False)
                water_usage_chart = gr.Plot(show_label=False, container=False)

            gr.HTML("<hr>", padding=False)
            gr.Markdown("## 🌳 How to do better?")

            gr.Markdown("### Recommendations")

            with gr.Column(elem_classes="grid-css"):

                gr.Markdown("### Type", elem_classes="reco")
                gr.Markdown("### Topic", elem_classes="reco")
                gr.Markdown("### Example", elem_classes="reco")
                gr.Markdown("### Expected reduction",
                            elem_classes="reco")

                gr.Markdown("Quantified", elem_classes="reco")
                gr.Markdown("⚡ Use the right quantization !",
                            elem_classes="reco")
                gr.Markdown(
                    """On llamacpp, using q4ks instead of no quantization can lead to a reduction of impact by""", elem_classes="reco")
                gr.Markdown("## 33%", elem_classes="reco")

                gr.Markdown("Quantified", elem_classes="reco")
                gr.Markdown("⚡ Use the right framework !", elem_classes="reco")
                gr.Markdown(
                    """Using the framework vllm instead of llamacpp for some model can lead
                    to a reduction of impact by""", elem_classes="reco")
                gr.Markdown("## 18%", elem_classes="reco")

                gr.Markdown("Quantified", elem_classes="reco")
                gr.Markdown(
                    "⚡ Use the lightest possible model that meets your needs !", elem_classes="reco")
                gr.Markdown(
                    """Using the model llama3-8b instead of 13b can lead to a reduction of impact by""", elem_classes="reco")
                gr.Markdown("## 30%", elem_classes="reco")

                gr.Markdown("Quantified", elem_classes="reco")
                gr.Markdown(
                    """🌫️ Locate servers in a country where energy production has less impact""", elem_classes="reco")
                gr.Markdown(
                    """Using a server located in Sweden instead of United-States can lead
                    to a reduction of impact by""", elem_classes="reco")
                gr.Markdown("## 93%", elem_classes="reco")

                gr.Markdown("Quantified", elem_classes="reco")
                gr.Markdown(
                    """🌫️⛏️💧 Use as few resources as possible
                    (i.e. the smallest possible machine/server) to suit the need""", elem_classes="reco")
                gr.Markdown(
                    """Using a small gpu server instead of a big one can lead to a reduction of impact by""", elem_classes="reco")
                gr.Markdown("## 41%", elem_classes="reco")

                gr.Markdown("Calculated", elem_classes="reco")
                gr.Markdown(
                    "⚡ Use the most frugal configuration", elem_classes="reco")
                more_frugal_conf = gr.Markdown(elem_classes="reco")
                percentage_reduction = gr.Markdown(elem_classes="reco")

            launch_btn.click(fn=handle_launch,
                             inputs=[mode, project_duration, project_duration, model_details, parameters_count,
                                     framework, quantization, stages, inference_users,
                                     inference_requests, inference_tokens, finetuning_data_size,
                                     finetuning_epochs_number, finetuning_batch_size,
                                     finetuning_peft, infra_type,
                                     infra_cpu_cores, infra_gpu_count, infra_gpu_memory,
                                     infra_memory, infra_pue_datacenter, infra_pue_machine,
                                     location],
                             outputs=[tabs, results, results_title,
                                      energy_consumption, carbon_footprint,
                                      abiotic_resource_usage, water_usage,
                                      eq_energy_consumption, eq_carbon_footprint,
                                      eq_abiotic_resources, eq_water_usage,
                                      carbon_footprint_chart, abiotic_resource_chart,
                                      water_usage_chart,
                                      more_frugal_conf,
                                      percentage_reduction,
                                      duration_slider
                                      ])
            duration_slider.change(fn=handle_launch,
                                   inputs=[mode, project_duration, duration_slider, model_details, parameters_count,
                                           framework, quantization, stages, inference_users,
                                           inference_requests, inference_tokens, finetuning_data_size,
                                           finetuning_epochs_number, finetuning_batch_size,
                                           finetuning_peft, infra_type,
                                           infra_cpu_cores, infra_gpu_count, infra_gpu_memory,
                                           infra_memory, infra_pue_datacenter, infra_pue_machine,
                                           location],
                                   outputs=[tabs, results, results_title,
                                            energy_consumption, carbon_footprint,
                                            abiotic_resource_usage, water_usage,
                                            eq_energy_consumption, eq_carbon_footprint,
                                            eq_abiotic_resources, eq_water_usage,
                                            carbon_footprint_chart, abiotic_resource_chart,
                                            water_usage_chart,
                                            more_frugal_conf,
                                            percentage_reduction,
                                            duration_slider
                                            ])

        # Onglet de la documentation
        with gr.Tab("📗 Documentation", id=2) as documentation:
            gr.Markdown(
                load_doc(path.join(path.dirname(__file__), "../../assets/docs/doc.md")))
