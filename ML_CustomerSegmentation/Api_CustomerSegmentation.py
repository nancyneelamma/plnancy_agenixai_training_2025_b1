# Import Libraries

from fastapi import FastAPI, HTTPException # For api functionality and handling errors
from fastapi.responses import FileResponse # For returning image files i.e., the plots
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib # Loading pre-trained model
import os

# Load model and data

kmeans = joblib.load("kmeans_model.pkl")
data = pd.read_csv("apidata.csv",index_col="CustomerID")

# Initialize api object

app = FastAPI()

# Endpoints : Health Check, Predictions and Plots

# Health Check Endpoint when api is live, if its running well

@app.get("/")
def health_check():
    return{"status":"Running Okay"}

# Prediction and insights endpoint

@app.get("/predict/insights/{customer_id}")
def predictCustomerID(customer_id : int): # Input of customer id
    if customer_id not in data.index: 
        raise HTTPException(status_code=404, detail="Customer ID not valid!")

    customer_info = data.loc[customer_id]

    # Extract features and reshape for model prediction and also convert selected to dictionary
    
    features = customer_info[['Recency', 'Frequency', 'ProductVariety', 'Tenure', 'AOV']].values.reshape(1, -1)
    insights = customer_info[['Recency', 'Frequency', 'ProductVariety', 'Tenure', 'AOV']].to_dict()
    kmeans_cluster = kmeans.predict(features)[0] # Gives live prediction of the model
    # Returns the predictions with insights
    return{
        "CustomerID": customer_id,
        "Insights" : insights,
        "KMeans_Cluster" : int(kmeans_cluster)
    }
    
# Endpoint - Plots for K-Means using features Recency and Frequency

@app.get("/plots/kmeans_scatterPlot")
def kmeansPlot():
    plot_image="recency_frequency_plot.png"

    # Delete it when theres already an existing file

    if os.path.exists(plot_image):
        os.remove(plot_image)

    # Plotting scatterplot
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=data, x='Recency', y='Frequency', hue='Cluster_KMeans', palette='Set2')
    plt.title("Recency-Frequency")
    plt.grid(True)
    plt.savefig(plot_image)
    plt.close()

    return FileResponse(plot_image,media_type="image/png") # Returns the image and also clarifies its an image using media type

