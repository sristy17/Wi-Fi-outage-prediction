import streamlit as st
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
import os

st.title("Wi-Fi Outage Prediction Dashboard")

st.header("Model Training Results")
train_result = subprocess.run(['python3', '/home/sristy/Desktop/wifi-outage-prediction/ml_model/scripts/train.py'], capture_output=True, text=True)
st.text_area("Training Output", train_result.stdout, height=200)

report_file_path = '/home/sristy/Desktop/wifi-outage-prediction/ml_model/scripts/report.py'
if os.path.exists(report_file_path):
    report_df = pd.read_csv(report_file_path)
    
    st.header("Model Report")
    st.dataframe(report_df)

    if 'model_name' in report_df.columns and 'Test MSE' in report_df.columns and 'Test R²' in report_df.columns:
        
        st.subheader("Distribution of Test MSE")
        mse_values = report_df.set_index('model_name')['Test MSE']
        fig_mse, ax_mse = plt.subplots()
        ax_mse.pie(mse_values, labels=mse_values.index, autopct='%1.1f%%', startangle=90)
        ax_mse.axis('equal')  
        st.pyplot(fig_mse)

        st.subheader("Distribution of Test R² Score")
        r2_values = report_df.set_index('model_name')['Test R²']
        fig_r2, ax_r2 = plt.subplots()
        ax_r2.pie(r2_values, labels=r2_values.index, autopct='%1.1f%%', startangle=90)
        ax_r2.axis('equal') 
        st.pyplot(fig_r2)
        
    else:
        st.warning("Required columns for pie chart not found in the model report.")

    prediction_result = subprocess.run(['python3', '/home/sristy/Desktop/wifi-outage-prediction/ml_model/scripts/predict.py'], capture_output=True, text=True)
   

    prediction_file_path = '/home/sristy/Desktop/wifi-outage-prediction/ml_model/scripts/predictions.csv' 
    if os.path.exists(prediction_file_path):
        predictions_df = pd.read_csv(prediction_file_path)

        st.header("Predictions")
        st.dataframe(predictions_df)

        st.write("Columns in predictions DataFrame:", predictions_df.columns.tolist())


        
    else:
        st.warning(f"Prediction data not found at {prediction_file_path}. Please ensure predictions.csv is generated.")
else:
    st.warning(f"Report data not found at {report_file_path}. Please ensure report_results.csv is generated.")
