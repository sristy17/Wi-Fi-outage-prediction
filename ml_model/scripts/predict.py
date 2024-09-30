import pandas as pd
import pickle
import numpy as np

def load_model(model_path):
    with open(model_path, 'rb') as model_file:
        return pickle.load(model_file)

def read_test_data(file_path):
    try:
        data = pd.read_csv(file_path, header=None)
        return data.values 
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None
    except pd.errors.ParserError as e:
        print(f"Error parsing the CSV file: {e}")
        return None

def get_status(prediction):
    status_map = {
        1: "Poor",
        2: "Medium",
        3: "Good",
        4: "Very Good",
        5: "Best"
    }
    return status_map.get(prediction, "Unknown")

def main():
    model_path = 'model.pkl'
    model = load_model(model_path)

    test_data_path = '/home/sristy/Desktop/wifi-outage-prediction/ml_model/data/parsedfromlog.csv'
    test_data = read_test_data(test_data_path)

    if test_data is not None:
        predictions = model.predict(test_data)

        predicted_statuses = [get_status(int(prediction)) for prediction in predictions]

        predictions_df = pd.DataFrame(predicted_statuses, columns=['Predicted_Status'])

        print("Predicted Statuses:", predicted_statuses)

        output_file_path = '/home/sristy/Desktop/wifi-outage-prediction/ml_model/scripts/predictions.csv'
        predictions_df.to_csv(output_file_path, index=False)
        print(f"Predictions saved to {output_file_path}")

if __name__ == "__main__":
    main()
