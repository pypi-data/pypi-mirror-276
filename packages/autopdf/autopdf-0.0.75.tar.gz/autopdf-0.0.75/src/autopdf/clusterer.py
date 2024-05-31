from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

import pandas as pd

def cluster_text_positions(text_positions_df):
    clustered_data = []
    
    pages = text_positions_df['page'].unique()
    
    for page in pages:
        page_df = text_positions_df[text_positions_df['page'] == page]
        positions = page_df[['x0', 'y0', 'x1', 'y1']].values
        
        # Standardize the positions
        scaler = StandardScaler()
        positions_scaled = scaler.fit_transform(positions)
        
        # Determine the optimal number of clusters using the Silhouette Score
        silhouette_scores = []
        cluster_range = range(2, min(10, len(page_df)))  # Avoid too many clusters
        
        for n_clusters in cluster_range:
            kmeans = KMeans(n_clusters=n_clusters, random_state=0)
            labels = kmeans.fit_predict(positions_scaled)
            score = silhouette_score(positions_scaled, labels)
            silhouette_scores.append((n_clusters, score))
        
        # Select the number of clusters with the highest silhouette score
        optimal_clusters = max(silhouette_scores, key=lambda x: x[1])[0]
        
        # Perform clustering with the optimal number of clusters
        kmeans = KMeans(n_clusters=optimal_clusters, random_state=0)
        labels = kmeans.fit_predict(positions_scaled)
        
        page_df['cluster'] = labels
        clustered_data.append(page_df)
    
    return pd.concat(clustered_data)