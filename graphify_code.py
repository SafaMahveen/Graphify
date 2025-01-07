import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk 

# Global variable to store the dataset
dataset = None

# Function to load dataset
def load_dataset():
    global dataset
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            dataset = pd.read_csv(file_path)
            messagebox.showinfo("Success", f"Dataset loaded successfully!\nShape: {dataset.shape}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dataset: {str(e)}")
    else:
        messagebox.showwarning("Warning", "No file selected!")

# Function to display dataset preview
def view_dataset():
    global dataset
    if dataset is not None:
        preview_window = tk.Toplevel(root)
        preview_window.title("Dataset Preview")
        preview_window.geometry("800x400")
        preview_window.configure(bg="#f0f8ff")  # Background color
        
        cols = list(dataset.columns)
        tree = ttk.Treeview(preview_window, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)

        # Add rows to the table
        for _, row in dataset.iterrows():
            tree.insert("", tk.END, values=row.tolist())
        
        tree.pack(fill=tk.BOTH, expand=True)
    else:
        messagebox.showerror("Error", "No dataset loaded!")

# Function to explain dataset
def explain_dataset():
    global dataset
    if dataset is not None:
        explain_window = tk.Toplevel(root)
        explain_window.title("Dataset Explanation")
        explain_window.geometry("500x400")
        explain_window.configure(bg="#f0f8ff")  
        
        text = tk.Text(explain_window, wrap=tk.WORD, bg="#ffffff", fg="#000000", font=("Arial", 12))
        text.insert(tk.END, f"Shape of Dataset: {dataset.shape}\n\n")
        text.insert(tk.END, f"Columns:\n{dataset.dtypes}\n\n")
        text.insert(tk.END, f"Missing Values:\n{dataset.isnull().sum()}\n")
        text.pack(fill=tk.BOTH, expand=True)
    else:
        messagebox.showerror("Error", "No dataset loaded!")

# Function to update the X and Y axis dropdowns based on the selected plot type
def update_axis_dropdowns(plot_type, x_axis, y_axis):
    if plot_type == "Bar Plot":
        x_axis['values'] = [col for col in dataset.columns if dataset[col].dtype == 'object']
        y_axis['values'] = [col for col in dataset.columns if dataset[col].dtype in ['int64', 'float64']]
    elif plot_type in ["Line Plot", "Scatter Plot"]:
        x_axis['values'] = [col for col in dataset.columns if dataset[col].dtype in ['int64', 'float64']]
        y_axis['values'] = [col for col in dataset.columns if dataset[col].dtype in ['int64', 'float64']]
    elif plot_type == "Box Plot":
        x_axis['values'] = [col for col in dataset.columns if dataset[col].dtype == 'object']
        y_axis['values'] = [col for col in dataset.columns if dataset[col].dtype in ['int64', 'float64']]
    elif plot_type == "Heatmap":
        x_axis['values'] = [col for col in dataset.columns if dataset[col].dtype in ['int64', 'float64']]
        y_axis['values'] = [col for col in dataset.columns if dataset[col].dtype in ['int64', 'float64']]

# Function to visualize dataset
def visualize_dataset():
    global dataset
    if dataset is not None:
        vis_window = tk.Toplevel(root)
        vis_window.title("Dataset Visualization")
        vis_window.geometry("600x700")
        vis_window.configure(bg="#f0f8ff")  # Background color
        
        # Plot type selection
        plot_type_label = tk.Label(vis_window, text="Select Plot Type:", bg="#f0f8ff", font=("Arial", 12, "bold"))
        plot_type_label.pack()
        
        plot_type = ttk.Combobox(vis_window, values=["Bar Plot", "Line Plot", "Scatter Plot", "Box Plot", "Heatmap"])
        plot_type.pack()

        # X-axis and Y-axis selection
        x_label = tk.Label(vis_window, text="Select X-axis:", bg="#f0f8ff", font=("Arial", 12, "bold"))
        x_label.pack()
        
        x_axis = ttk.Combobox(vis_window, values=list(dataset.columns))
        x_axis.pack()
        
        y_label = tk.Label(vis_window, text="Select Y-axis:", bg="#f0f8ff", font=("Arial", 12, "bold"))
        y_label.pack()
        
        y_axis = ttk.Combobox(vis_window, values=list(dataset.columns))
        y_axis.pack()

        # Update X and Y axis dropdowns based on plot type
        plot_type.bind("<<ComboboxSelected>>", lambda event: update_axis_dropdowns(plot_type.get(), x_axis, y_axis))

        # Color palette selection (only for non-heatmap plots)
        color_choice_label = tk.Label(vis_window, text="Select Plot Color:", bg="#f0f8ff", font=("Arial", 12, "bold"))
        color_choice_label.pack()
        
        color_choice = ttk.Combobox(
            vis_window, 
            values=["blue", "red", "green", "orange", "purple", "pink", "cyan", "gray", "yellow"]
        )
        color_choice.set("blue")  # Default color
        color_choice.pack()

        # Plot button
        def plot_graph():
            plot_window = tk.Toplevel(vis_window)  # Create a new window for the plot
            plot_window.title("Generated Plot")
            plot_window.geometry("800x600")

            plt.clf()  # Clear the current figure
            plt.figure(figsize=(8, 6))
            try:
                selected_color = color_choice.get() if plot_type.get() != "Heatmap" else None
                
                # Handle plot types
                if plot_type.get() == "Bar Plot":
                    if dataset[x_axis.get()].dtype == "object":
                        sns.barplot(x=dataset[x_axis.get()], y=dataset[y_axis.get()], color=selected_color, errorbar=None)
                    else:
                        sns.barplot(x=dataset[x_axis.get()].astype(str), y=dataset[y_axis.get()], color=selected_color, errorbar=None)

                elif plot_type.get() == "Line Plot":
                    if dataset[x_axis.get()].dtype in ["int64", "float64"] and dataset[y_axis.get()].dtype in ["int64", "float64"]:
                        sns.lineplot(x=dataset[x_axis.get()], y=dataset[y_axis.get()], color=selected_color)

                elif plot_type.get() == "Scatter Plot":
                    if dataset[x_axis.get()].dtype in ["int64", "float64"] and dataset[y_axis.get()].dtype in ["int64", "float64"]:
                        sns.scatterplot(x=dataset[x_axis.get()], y=dataset[y_axis.get()], color=selected_color)

                elif plot_type.get() == "Box Plot":
                    if dataset[x_axis.get()].dtype == "object" and dataset[y_axis.get()].dtype in ["int64", "float64"]:
                        data = dataset[[x_axis.get(), y_axis.get()]].dropna()
                        if data.empty:
                            messagebox.showerror("Error", "No valid data for box plot.")
                            return
                        sns.boxplot(x=data[x_axis.get()], y=data[y_axis.get()], palette=[selected_color])

                elif plot_type.get() == "Heatmap":
                    numerical_data = dataset.select_dtypes(include=["int64", "float64"])
                    if not numerical_data.empty:
                        sns.heatmap(numerical_data.corr(), annot=True, cmap="coolwarm")
                    else:
                        messagebox.showerror("Error", "No numerical data available for Heatmap.")
                        return

                # Embed Matplotlib figure in the new window
                fig_canvas = FigureCanvasTkAgg(plt.gcf(), plot_window)
                fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                fig_canvas.draw()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate plot: {str(e)}")

        plot_button = tk.Button(vis_window, text="Plot", command=plot_graph, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        plot_button.pack(pady=20)
    else:
        messagebox.showerror("Error", "No dataset loaded!")

# Function to clean dataset (drop or fill missing values)
def clean_dataset():
    global dataset
    if dataset is not None:
        clean_window = tk.Toplevel(root)
        clean_window.title("Data Cleaning")
        clean_window.geometry("400x300")
        clean_window.configure(bg="#f0f8ff")  # Background color
        
        # Option to drop or fill missing values
        option_label = tk.Label(clean_window, text="Choose cleaning operation:", bg="#f0f8ff", font=("Arial", 12, "bold"))
        option_label.pack(pady=10)
        
        # Radio buttons to choose between drop or fill
        action = tk.StringVar(value="drop")  # Default action is drop
        drop_button = tk.Radiobutton(clean_window, text="Drop rows with missing values", variable=action, value="drop", bg="#f0f8ff", font=("Arial", 12))
        drop_button.pack(pady=5)
        
        fill_button = tk.Radiobutton(clean_window, text="Fill missing values with a value", variable=action, value="fill", bg="#f0f8ff", font=("Arial", 12))
        fill_button.pack(pady=5)
        
        # If filling, ask for the value to fill
        fill_value_label = tk.Label(clean_window, text="Fill value (mean/median):", bg="#f0f8ff", font=("Arial", 12, "bold"))
        fill_value_label.pack(pady=10)
        
        fill_value_entry = tk.Entry(clean_window, bg="#ffffff", fg="#000000", font=("Arial", 12))
        fill_value_entry.pack(pady=5)
        
        def perform_cleaning():
            if action.get() == "drop":
                dataset.dropna(inplace=True)
                messagebox.showinfo("Success", "Rows with missing values dropped.")
            elif action.get() == "fill":
                fill_value = fill_value_entry.get().lower()
                if fill_value == "mean":
                    dataset.fillna(dataset.mean(), inplace=True)
                    messagebox.showinfo("Success", "Missing values filled with mean.")
                elif fill_value == "median":
                    dataset.fillna(dataset.median(), inplace=True)
                    messagebox.showinfo("Success", "Missing values filled with median.")
                else:
                    messagebox.showwarning("Warning", "Invalid fill value. Use 'mean' or 'median'.")
            
            clean_window.destroy()
        
        # Apply cleaning button
        clean_button = tk.Button(clean_window, text="Clean Data", command=perform_cleaning, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        clean_button.pack(pady=20)
    else:
        messagebox.showerror("Error", "No dataset loaded!")

# Main window setup
root = tk.Tk()
root.title("Graphify: Data Visualization Made Easy")
root.geometry("600x500")
root.configure(bg="#f0f8ff")  # Background color

# Background image setup
background_image = Image.open(r"../Graphify/DATA_VISUALIZE.png")  
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

titlee = tk.Label(root, text="Graphify: Data Visualization Made Easy", font=("Arial", 18,"bold"), fg="white", bg="blue")
titlee.pack(pady=10)

# Create main interface buttons
load_button = tk.Button(root, text="Load Dataset", command=load_dataset, font=("Arial", 14, "bold"), bg="#fc92c4", fg="white")
load_button.pack(pady=10)
view_button = tk.Button(root, text="View Dataset", command=view_dataset, font=("Arial", 14, "bold"), bg="#fc92c4", fg="white")
view_button.pack(pady=10)

clean_button = tk.Button(root, text="Clean Dataset", command=clean_dataset, font=("Arial", 14, "bold"), bg="#fc92c4", fg="white")
clean_button.pack(pady=10)

explain_button = tk.Button(root, text="Explain Dataset", command=explain_dataset, font=("Arial", 14, "bold"), bg="#fc92c4", fg="white")
explain_button.pack(pady=10)

visualize_button = tk.Button(root, text="Visualize Dataset", command=visualize_dataset, font=("Arial", 14, "bold"), bg="#fc92c4", fg="white")
visualize_button.pack(pady=10)
# Contact message at the bottom
contact_label = tk.Label(root, text="For queries, contact: thesafamahveen@gmail.com", font=("Arial", 10), fg="black", bg="#f0f8ff")
contact_label.pack(side=tk.BOTTOM, pady=10)

root.mainloop()