import matplotlib.pyplot as plt


def plot_data(true_counts, false_counts):
    """Plot the data as a bar chart and save to file."""
    categories = ['Framed', 'Unframed']
    true_values = [true_counts[cat] for cat in categories]
    false_values = [false_counts[cat] for cat in categories]

    fig, ax = plt.subplots()
    bar_width = 0.35
    index = range(len(categories))

    bar1 = ax.bar(index, true_values, bar_width, label='True', color='green')
    bar2 = ax.bar([p + bar_width for p in index], false_values, bar_width, label='False', color='red')

    ax.set_xlabel('Prompt Type')
    ax.set_ylabel('Counts')
    ax.set_title('Accuracy of Responses by Prompt Type')
    ax.set_xticks([p + bar_width / 2 for p in index])
    ax.set_xticklabels(categories)
    ax.legend()

    plt.savefig('bar_chart.png')

def process_data(data):
    """Process data to count true and false responses for framed and unframed prompts."""
    true_counts = {'Framed': 0, 'Unframed': 0}
    false_counts = {'Framed': 0, 'Unframed': 0}
    for key, value in data.items():
        if 'Framed' in key:
            category = 'Framed'
        else:
            category = 'Unframed'
        if value['response_correct'].lower() == 'true':
            true_counts[category] += 1
        else:
            false_counts[category] += 1
    return true_counts, false_counts