# Clustering
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def view_data_scaled(df):
    dftemp = PowerTransformer().fit_transform(df)
    dftemp = pd.DataFrame(dftemp, columns=df.columns, index=df.index)
    for x in df.columns:
        print(x + ' Showing dist plots of data after scaling:')
        sns.distplot(dftemp[x])
        plt.title('Column ' + x + ' Distribution Plot After Scaling')
        plt.savefig("visualizations/" + x + "_Distribution_Plot_after_scale.png", dpi=600)
        plt.show()
        print('----------------------')


# Determine the optimal number of clusters
# Create empty sse, and labels dictionary
sse = {}
km_labels = {}


# Fit KMeans algorithm on k values between 1 and predifiened number of clusters
def create_kmeans_clusters(df, n_clust=11):
    # # View data after scaling
    # view_data_scaled(df)
    for k in range(1, n_clust):
        pow_trans = PowerTransformer()
        kmeans_c = KMeans(n_clusters=k, n_jobs=-1, random_state=333)
        steps = [('power_transformation', pow_trans), ('kmeans_clustering', kmeans_c)]
        pipeline = Pipeline(steps=steps)
        df = pipeline.fit_transform(df)
        sse[k] = pipeline.steps[1][1].inertia_
        km_labels[k] = pipeline.steps[1][1].labels_

    return sse, km_labels


# Plot Sum of Squared Error (SSE) of the generated clusters
def plot_clusters(sse):
    plt.title('Elbow criterion method chart')
    sns.pointplot(x=list(sse.keys()), y=list(sse.values()))
    plt.xlabel("k")
    plt.ylabel("Sum of Squared Error (SSE)")
    plt.savefig("visualizations/kmeans_clusters_sse.png", dpi=600)
    plt.show()

# Visualize clusters in a heatmap and print the average values
def show_clusters_hmap(df, km_labels, k):
    # Assign the generated labels to a new column
    df_kmeans = df.assign(segment=km_labels[k])
    # K-means segmentation averages
    # Group by the segment label and calculate average column values
    kmeans_averages = df_kmeans.groupby(['segment']).mean().round(0)
    # Print the average column values per each segment
    # Heatmap based on the average column values per each segment
    sns.heatmap(kmeans_averages.T, cmap='YlGnBu', annot=True, fmt='.1f')
    plt.title("Average Column Values per each of " + str(k) + " Segment or Clusters")
    plt.tight_layout()
    plt.savefig("visualizations/kmeans_clusters_" + str(k) + ".png", dpi=1200)
    plt.show()