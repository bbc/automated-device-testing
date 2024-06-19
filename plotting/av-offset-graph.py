import pandas as pd
import numpy as np
import cmasher as cmr
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8')


model = "synchformer"

if model not in ["syncnet", "sparsesync", "synchformer", "vocalist"]:
    exit(0)

results = pd.read_csv(f"{model}/predictions.csv")
results = results.iloc[::-1]

if model == "syncnet":
    results['Likelihood'] = results['Likelihood'].apply(lambda l: l / 10)
elif model == "vocalist":
    results['Likelihood'] = results['Likelihood'].apply(lambda l: l / 100)

results = results.loc[results['Likelihood'] > 0.000]
# results['Likelihood'] = results['Likelihood'].apply(lambda l: (l - results['Likelihood'].min()) / (results['Likelihood'].max() - results['Likelihood'].min()))

error_margin = 10000 * 0.05

for model in results['Model'].unique():
    results_by_model = results.loc[results['Model'] == model]

    for clip in results_by_model['Clip'].unique():
        results_by_clip = results_by_model.loc[results_by_model['Clip'] == clip]

        fig, ax = plt.subplots(1, 1, figsize=(17, 9))

        true_offsets = np.array(results_by_clip['True Offset'], dtype=float)
        offset_step = round(abs(np.unique(true_offsets)[0]) - abs(np.unique(true_offsets)[1]), 2)
        predicted_offsets = np.array(results_by_clip['Predicted Offset'], dtype=float)
        colour_map = cmr.get_sub_cmap('Greens', min(results_by_clip['Likelihood']), max(results_by_clip['Likelihood']))

        # ax.plot(true_offsets, true_offsets, c='k', linestyle='--', linewidth=2.5, label='True Offset')
        ax.scatter(true_offsets, true_offsets, c='k', label='True Offset', marker='X', s=200, zorder=5)
        predictions_plot = ax.scatter(true_offsets, predicted_offsets, c=results_by_clip['Likelihood'], cmap=colour_map, s=error_margin)

        for offset in results_by_clip['True Offset'].unique():
            max_likelihood = results_by_clip.loc[results_by_clip.loc[results_by_clip['True Offset'] == offset]['Likelihood'].idxmax()]['Likelihood']
            max_likelihood_prediction = results_by_clip.loc[results_by_clip.loc[results_by_clip['True Offset'] == offset]['Likelihood'].idxmax()]['Predicted Offset']
            ax.scatter(float(offset), float(max_likelihood_prediction), s=error_margin, facecolors='none', edgecolors='k', linewidth=2)

        ax.scatter(float(offset), float(max_likelihood_prediction), s=error_margin, facecolors='none', edgecolors='k', linewidth=2, label="Primary\nprediction")

        y_limit = np.max(np.absolute(predicted_offsets))
        y_limit = round(round(y_limit / offset_step) * offset_step + offset_step, 1)
        x_limit = np.max(np.absolute(true_offsets))

        plt.xticks(fontsize='large', rotation=90)
        plt.yticks(fontsize='large')
        ax.set_ylim([-y_limit, y_limit])
        ax.set_xticks(np.arange(-x_limit, x_limit + offset_step, offset_step))
        ax.set_yticks(np.arange(-y_limit + max(offset_step, 0.1), y_limit, max(offset_step, 0.1)))
        ax.set_ylim([-y_limit, y_limit])
        ax.set_xlabel("True Offset (s)", fontsize='x-large')
        ax.set_ylabel("Predicted Offset (s)", fontsize='x-large')

        ax.set_title(f"Predictions of model '{model}' on test clip '{clip}'\n", fontsize='xx-large')
        ax.grid(which='major', linewidth=1)
        plt.legend(loc='upper left', frameon=True, markerscale=0.5, borderpad=0.7, facecolor='w', fontsize='large')

        cbar = fig.colorbar(predictions_plot, ax=ax, orientation='vertical', extend='both', ticks=np.arange(round(np.min(results_by_clip['Likelihood']), 1), round(np.max(results_by_clip['Likelihood']), 1), 0.1))
        cbar.set_label(label='Likelihood', fontsize='x-large')
        cbar.ax.tick_params(labelsize='large')

        plt.tight_layout()
        plt.savefig(f"{model}/{model}_{clip.replace(' ', '-')}.png")
        plt.close()
        print(f" * Model: {model}, Clip: {clip}")
