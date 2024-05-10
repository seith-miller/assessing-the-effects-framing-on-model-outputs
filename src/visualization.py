import matplotlib.pyplot as plt
import numpy as np

def plot_data(model_results):
    categories = ['Framed', 'Unframed']
    num_models = len(model_results)
    models = list(model_results.keys())
    width = 0.35  # Width of the bars
    fig, ax = plt.subplots(figsize=(10, 6))

    # Base position for each model group
    base_positions = np.arange(len(models))

    # Calculate the width for each bar to fit all within the group at each model position
    total_width = width * len(categories)
    individual_width = total_width / len(categories)

    # Define colors for each category
    colors = {'Framed': 'blue', 'Unframed': 'orange'}

    # Iterate through each model and category to calculate percentages
    for model_index, (model_name, prompts) in enumerate(model_results.items()):
        true_counts = {cat: 0 for cat in categories}
        total_counts = {cat: 0 for cat in categories}

        # Accumulate counts for each category
        for prompt_name, details in prompts.items():
            for cat in categories:
                if cat in prompt_name:
                    if details['response_correct'].lower() == 'true':
                        true_counts[cat] += 1
                    total_counts[cat] += 1

        # Calculate percentage of True responses
        true_percentages = [true_counts[cat] / total_counts[cat] * 100 if total_counts[cat] > 0 else 0 for cat in categories]

        # Plot bars for each category for this model
        for cat_index, cat in enumerate(categories):
            ax.bar(base_positions[model_index] + cat_index * individual_width, true_percentages[cat_index], individual_width, color=colors[cat], label=f'{cat}' if model_index == 0 else "")

    ax.set_xlabel('Models')
    ax.set_ylabel('Percentage of True Responses')
    ax.set_title('Accuracy of Responses by Model and Prompt Type')
    ax.set_xticks(base_positions + total_width / 2 - individual_width / 2)
    ax.set_xticklabels(models)
    ax.set_ylim(0, 100)  # Percentage limits

    # Create the legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors[cat], label=cat) for cat in categories]
    ax.legend(handles=legend_elements)

    plt.tight_layout()
    plt.savefig('data/output/combined_bar_chart.png')

def process_data(all_responses):
    """
    Process data to count true and false responses for framed and unframed prompts from all models.
    """
    model_results = {}

    for model, responses in all_responses.items():
        true_counts = {'Framed': 0, 'Unframed': 0}
        false_counts = {'Framed': 0, 'Unframed': 0}
        for key, value in responses.items():
            category = 'Framed' if 'Framed' in key else 'Unframed'
            if value['response_correct'].lower() == 'true':
                true_counts[category] += 1
            else:
                false_counts[category] += 1
        model_results[model] = (true_counts, false_counts)
    return model_results
