import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from imblearn.over_sampling import SMOTE
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls"), ("CSV files", "*.csv")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def process_data():
    file_path = entry_file_path.get()
    if not file_path:
        messagebox.showerror("Error", "Please select a dataset.")
        return
    
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path, sheet_name="Full_new")
        else:
            messagebox.showerror("Error", "Unsupported file format. Please select an Excel or CSV file.")
            return
        
        print(df.columns)
        
        df.dropna(inplace=True)
        df['II    beta-HCG(mIU/mL)'] = pd.to_numeric(df['II    beta-HCG(mIU/mL)'], errors='coerce')
        df['AMH(ng/mL)'] = pd.to_numeric(df['AMH(ng/mL)'], errors='coerce')
        
        if 'Unnamed: 44' in df.columns:
            df.drop('Unnamed: 44', axis=1, inplace=True)
        
        if 'PCOS (Y/N)' not in df.columns:
            messagebox.showerror("Error", "'PCOS (Y/N)' column not found.")
            return
        
        correlation_with_target = df.corr()['PCOS (Y/N)'].abs().sort_values(ascending=False)
        top_10_features = correlation_with_target[:11].index.tolist()
        df_new = df[top_10_features]
        df_new.dropna(inplace=True)

        X = df_new.drop(['PCOS (Y/N)'], axis=1)
        y = df_new['PCOS (Y/N)']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        logreg = LogisticRegression()
        logreg.fit(X_train, y_train)
        y_pred = logreg.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        messagebox.showinfo("Model Training", f"Model trained successfully! Accuracy: {accuracy:.2f}")
        
        def predict_new_data():
            new_data = [float(entry_values[i].get()) for i in range(len(X.columns))]
            prediction = logreg.predict([new_data])
            result_label.config(text=f"Predicted PCOS status: {'Positive' if prediction[0] == 1 else 'Negative'}")
        
        predict_window = tk.Toplevel(root)
        predict_window.title("Predict PCOS")
        
        tk.Label(predict_window, text="Enter values for prediction:").pack()
        entry_values = []
        for col in X.columns:
            frame = tk.Frame(predict_window)
            frame.pack()
            tk.Label(frame, text=col).pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.RIGHT)
            entry_values.append(entry)
        
        predict_button = tk.Button(predict_window, text="Predict", command=predict_new_data)
        predict_button.pack()
        result_label = tk.Label(predict_window, text="")
        result_label.pack()
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("PCOS Prediction")

frame = tk.Frame(root)
frame.pack(pady=20)

entry_file_path = tk.Entry(frame, width=50)
entry_file_path.pack(side=tk.LEFT, padx=5)
btn_browse = tk.Button(frame, text="Browse", command=load_file)
btn_browse.pack(side=tk.RIGHT)

btn_process = tk.Button(root, text="Process Dataset", command=process_data)
btn_process.pack(pady=10)

root.mainloop()


# In[ ]:




