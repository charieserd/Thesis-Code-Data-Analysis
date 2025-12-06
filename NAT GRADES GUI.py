import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
import threading

# Function to run scripts in separate threads to prevent GUI freezing
def run_in_thread(func):
    def wrapper():
        thread = threading.Thread(target=func)
        thread.start()
    return wrapper

# Script 1: Radix-Insertion Sort Animation
def script1():
    def insertion_sort(arr, low, high):
        for i in range(low + 1, high + 1):
            key = arr[i]
            j = i - 1
            while j >= low and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                yield arr.copy()  # Yield intermediate states for animation
            arr[j + 1] = key
            yield arr.copy()

    def counting_sort_for_radix(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = int(arr[i] // exp) if not np.isnan(arr[i]) else 0
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = int(arr[i] // exp) if not np.isnan(arr[i]) else 0
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1

        for i in range(n):
            arr[i] = output[i]
            yield arr.copy()

    def radix_sort(arr):
        if not arr:  # Handle empty list
            return
        max1 = max(arr)
        exp = 1
        while max1 // exp > 0:
            yield from counting_sort_for_radix(arr, exp)
            exp *= 10

    def hybrid_radix_insertion_sort(arr):
        n = len(arr)
        threshold = 16
        if n <= threshold:
            yield from insertion_sort(arr, 0, n - 1)
        else:
            yield from radix_sort(arr)

    try:
        file_path = filedialog.askopenfilename(title="Select Excel File for Script 1",
                                               filetypes=[("Excel Files", "*.xlsx *.xls")])
        if not file_path:
            return  # User cancelled

        # Read Excel File
        df_14_15 = pd.read_excel(file_path, sheet_name='14-15')
        df_15_16 = pd.read_excel(file_path, sheet_name='15-16')
        df_16_17 = pd.read_excel(file_path, sheet_name='16-17')

        combined_df = pd.concat([df_14_15, df_15_16, df_16_17], ignore_index=True)
        combined_df.fillna(np.nan, inplace=True)

        # Convert columns to numeric
        for subject in ['Math', 'English', 'Science']:
            combined_df[subject] = pd.to_numeric(combined_df[subject], errors='coerce')

        grades_list = combined_df[['Math', 'English', 'Science']].values.flatten().tolist()

        # Handle possible NaN values by replacing them with 0 for sorting
        grades_list = [grade if not np.isnan(grade) else 0 for grade in grades_list]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title('Radix-Insertion Sort Algorithm Visualization for Grade Sorting')
        bar_rects = ax.bar(range(len(grades_list)), grades_list, align="edge")
        ax.set_xlim(0, len(grades_list))
        ax.set_ylim(0, max(grades_list) * 1.1 if grades_list else 1)

        text = ax.text(0.5, 0.95, "", transform=ax.transAxes, ha='center', va='top', fontsize=12)

        def update_fig(frame_data):
            arr = frame_data
            for rect, val in zip(bar_rects, arr):
                rect.set_height(val)
            elapsed_time = time.time() - start_time
            text.set_text(f"Time taken: {elapsed_time:.3f} seconds")
            return bar_rects

        start_time = time.time()
        sorting_animation = animation.FuncAnimation(fig, func=update_fig,
                                                    frames=hybrid_radix_insertion_sort(grades_list),
                                                    interval=50, repeat=False)

        plt.show()
    except Exception as e:
        messagebox.showerror("Error in Script 1", str(e))

# Script 2: Highest Grades by Region and Year
def script2():
    try:
        start_time = time.time()

        file_path = filedialog.askopenfilename(title="Select Excel File for Script 2",
                                               filetypes=[("Excel Files", "*.xlsx *.xls")])
        if not file_path:
            return  # User cancelled

        # Read Excel File
        df_14_15 = pd.read_excel(file_path, sheet_name='14-15')
        df_15_16 = pd.read_excel(file_path, sheet_name='15-16')
        df_16_17 = pd.read_excel(file_path, sheet_name='16-17')

        combined_df = pd.concat([df_14_15, df_15_16, df_16_17], ignore_index=True)
        combined_df.fillna(np.nan, inplace=True)

        # Convert columns to numeric
        for subject in ['Math', 'English', 'Science']:
            combined_df[subject] = pd.to_numeric(combined_df[subject], errors='coerce')

        # Ensure 'Region' and 'Year' columns exist
        if 'Region' not in combined_df.columns or 'Year' not in combined_df.columns:
            raise ValueError("The Excel sheets must contain 'Region' and 'Year' columns.")

        # Get the highest grades and their corresponding regions and years
        highest_math = combined_df.loc[combined_df['Math'].idxmax()]
        highest_english = combined_df.loc[combined_df['English'].idxmax()]
        highest_science = combined_df.loc[combined_df['Science'].idxmax()]

        fig, ax2 = plt.subplots(figsize=(10, 6))

        subjects = ['Math', 'English', 'Science']
        highest_grades = [highest_math['Math'], highest_english['English'], highest_science['Science']]
        regions_years = [
            f"{highest_math['Region']} ({highest_math['Year']})",
            f"{highest_english['Region']} ({highest_english['Year']})",
            f"{highest_science['Region']} ({highest_science['Year']})"
        ]
        colors = ['blue', 'green', 'red']

        bars = ax2.bar(subjects, highest_grades, color=colors)

        for bar, grade, region_year in zip(bars, highest_grades, regions_years):
            height = bar.get_height()
            ax2.annotate(f'{region_year} ({grade:.2f})',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')

        ax2.set_ylabel('Highest Grade')
        ax2.set_title('Highest Grades by Region and Year')

        plt.tight_layout()
        plt.show()

        elapsed_time = time.time() - start_time
        messagebox.showinfo("Script 2 Completed", f"The algorithm took {elapsed_time:.3f} seconds to execute")
    except Exception as e:
        messagebox.showerror("Error in Script 2", str(e))

# Script 3: Average Grades Over the Years
def script3():
    try:
        start_time = time.time()

        file_path = filedialog.askopenfilename(title="Select Excel File for Script 3",
                                               filetypes=[("Excel Files", "*.xlsx *.xls")])
        if not file_path:
            return  # User cancelled

        # Read Excel File
        df_14_15 = pd.read_excel(file_path, sheet_name='14-15')
        df_15_16 = pd.read_excel(file_path, sheet_name='15-16')
        df_16_17 = pd.read_excel(file_path, sheet_name='16-17')

        combined_df = pd.concat([df_14_15, df_15_16, df_16_17], ignore_index=True)
        combined_df.fillna(0, inplace=True)

        # Convert columns to numeric
        for subject in ['Math', 'English', 'Science']:
            combined_df[subject] = pd.to_numeric(combined_df[subject], errors='coerce')

        # Ensure 'Year' column exists
        if 'Year' not in combined_df.columns:
            raise ValueError("The Excel sheets must contain a 'Year' column.")

        # Calculate average grades for each subject over the years
        average_math = combined_df.groupby('Year')['Math'].mean()
        average_english = combined_df.groupby('Year')['English'].mean()
        average_science = combined_df.groupby('Year')['Science'].mean()

        plt.figure(figsize=(10, 6))
        plt.plot(average_math.index, average_math.values, label='Math', marker='o')
        plt.plot(average_english.index, average_english.values, label='English', marker='o')
        plt.plot(average_science.index, average_science.values, label='Science', marker='o')

        plt.xlabel('Year')
        plt.ylabel('Average Grade')
        plt.title('Average NAT Grades Over the Years')
        plt.legend()
        plt.grid(True)
        plt.xticks(combined_df['Year'].unique())
        plt.tight_layout()
        plt.show()

        elapsed_time = time.time() - start_time
        messagebox.showinfo("Script 3 Completed", f"The algorithm took {elapsed_time:.3f} seconds to execute")
    except Exception as e:
        messagebox.showerror("Error in Script 3", str(e))

# Script 4: Top 10 Regions by Average Grade in Each Subject
def script4():
    def insertion_sort(arr, low, high):
        for i in range(low + 1, high + 1):
            key = arr[i]
            j = i - 1
            while j >= low and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

    def counting_sort_for_radix(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = int(arr[i] // exp) if not np.isnan(arr[i]) else 0
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = int(arr[i] // exp) if not np.isnan(arr[i]) else 0
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1

        for i in range(n):
            arr[i] = output[i]

    def radix_sort(arr):
        if not arr:  # Handle empty list
            return
        max1 = max(arr)
        exp = 1
        while max1 // exp > 0:
            counting_sort_for_radix(arr, exp)
            exp *= 10

    def hybrid_radix_insertion_sort(arr):
        n = len(arr)
        threshold = 16
        if n <= threshold:
            insertion_sort(arr, 0, n - 1)
        else:
            radix_sort(arr)

    try:
        start_time = time.time()

        file_path = filedialog.askopenfilename(title="Select Excel File for Script 4",
                                               filetypes=[("Excel Files", "*.xlsx *.xls")])
        if not file_path:
            return  # User cancelled

        # Read Excel File
        df_14_15 = pd.read_excel(file_path, sheet_name='14-15')
        df_15_16 = pd.read_excel(file_path, sheet_name='15-16')
        df_16_17 = pd.read_excel(file_path, sheet_name='16-17')

        combined_df = pd.concat([df_14_15, df_15_16, df_16_17], ignore_index=True)
        combined_df.fillna(np.nan, inplace=True)

        # Convert columns to numeric
        for subject in ['Math', 'English', 'Science']:
            combined_df[subject] = pd.to_numeric(combined_df[subject], errors='coerce')

        # Ensure 'Region' column exists
        if 'Region' not in combined_df.columns:
            raise ValueError("The Excel sheets must contain a 'Region' column.")

        # Calculate average grades for each region for each subject
        subjects = ['Math', 'English', 'Science']
        top_10_regions_subjects = {}

        for subject in subjects:
            region_avg = combined_df.groupby('Region')[subject].mean().reset_index()
            region_avg_sorted = region_avg.sort_values(by=subject, ascending=False).reset_index(drop=True)
            top_10_regions_subjects[subject] = region_avg_sorted.head(10)

        fig, axs = plt.subplots(3, 1, figsize=(12, 24))

        for ax, subject in zip(axs, subjects):
            top_10 = top_10_regions_subjects[subject]
            bars = ax.barh(top_10['Region'], top_10[subject], color='skyblue')
            ax.invert_yaxis()  # Highest on top

            for bar, avg in zip(bars, top_10[subject]):
                width = bar.get_width()
                ax.annotate(f'{avg:.2f}',
                            xy=(width, bar.get_y() + bar.get_height() / 2),
                            xytext=(3, 0),
                            textcoords="offset points",
                            ha='left', va='center')

            ax.set_xlabel('Average Grade')
            ax.set_title(f'Top 10 Regions by Average Grade in {subject}')

        plt.tight_layout()
        plt.show()

        elapsed_time = time.time() - start_time
        messagebox.showinfo("Script 4 Completed", f"The algorithm took {elapsed_time:.3f} seconds to execute")
    except Exception as e:
        messagebox.showerror("Error in Script 4", str(e))

# Script 5: Radix Sort Animation
def script5():
    def counting_sort_for_radix(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = int(arr[i] // exp) if not np.isnan(arr[i]) else 0  # Convert index to integer
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = int(arr[i] // exp) if not np.isnan(arr[i]) else 0  # Convert index to integer
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1

        for i in range(n):
            arr[i] = output[i]
            yield arr  # Yield intermediate states for animation

    def radix_sort(arr):
        max1 = max(arr)
        exp = 1
        while max1 // exp > 0:
            yield from counting_sort_for_radix(arr, exp)
            exp *= 10

    try:
        file_path = filedialog.askopenfilename(title="Select Excel File for Radix Sort Animation",
                                               filetypes=[("Excel Files", "*.xlsx *.xls")])
        if not file_path:
            return  # User cancelled

        # Read the Excel file
        df_14_15 = pd.read_excel(file_path, sheet_name='14-15')
        df_15_16 = pd.read_excel(file_path, sheet_name='15-16')
        df_16_17 = pd.read_excel(file_path, sheet_name='16-17')

        # Combine data from all sheets
        combined_df = pd.concat([df_14_15, df_15_16, df_16_17], ignore_index=True)
        combined_df.fillna(np.nan, inplace=True)

        # Convert columns to numeric type
        for subject in ['Math', 'English', 'Science']:
            combined_df[subject] = pd.to_numeric(combined_df[subject], errors='coerce')

        # Convert the grades to a list for sorting
        grades_list = combined_df[['Math', 'English', 'Science']].values.flatten().tolist()

        # Create figure and axes for sorting animation
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title('Radix Sort Algorithm Visualization for Grade Sorting')
        bar_rects = ax.bar(range(len(grades_list)), grades_list, align="edge")
        ax.set_xlim(0, len(grades_list))
        ax.set_ylim(0, max(grades_list) * 1.1)

        # Text annotation for displaying time taken
        text = ax.text(0.5, 0.95, "", transform=ax.transAxes, ha='center', va='top', fontsize=12)

        # Function to update the bar chart with each frame of the animation
        def update_fig(frame_data):
            arr = frame_data
            for rect, val in zip(bar_rects, arr):
                rect.set_height(val)
            elapsed_time = time.time() - start_time
            text.set_text(f"Time taken: {elapsed_time:.3f} seconds")
            return bar_rects

        # Create the animation
        start_time = time.time()
        sorting_animation = animation.FuncAnimation(fig, func=update_fig,
                                                    frames=radix_sort(grades_list),
                                                    interval=50, repeat=False)

        # Show the animation
        plt.show()
    except Exception as e:
        messagebox.showerror("Error in Radix Sort Animation", str(e))

# Script 6: Insertion Sort Animation
def script6():
    def insertion_sort(arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                yield arr  # Yield intermediate states for animation
            arr[j + 1] = key

    try:
        file_path = filedialog.askopenfilename(title="Select Excel File for Insertion Sort Animation",
                                               filetypes=[("Excel Files", "*.xlsx *.xls")])
        if not file_path:
            return  # User cancelled

        # Read the Excel file
        df_14_15 = pd.read_excel(file_path, sheet_name='14-15')
        df_15_16 = pd.read_excel(file_path, sheet_name='15-16')
        df_16_17 = pd.read_excel(file_path, sheet_name='16-17')

        # Combine data from all sheets
        combined_df = pd.concat([df_14_15, df_15_16, df_16_17], ignore_index=True)
        combined_df.fillna(np.nan, inplace=True)

        # Convert columns to numeric type
        for subject in ['Math', 'English', 'Science']:
            combined_df[subject] = pd.to_numeric(combined_df[subject], errors='coerce')

        # Convert the grades to a list for sorting
        grades_list = combined_df[['Math', 'English', 'Science']].values.flatten().tolist()

        # Create figure and axes for sorting animation
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title('Insertion Sort Algorithm Visualization for Grade Sorting')
        bar_rects = ax.bar(range(len(grades_list)), grades_list, align="edge")
        ax.set_xlim(0, len(grades_list))
        ax.set_ylim(0, max(grades_list) * 1.1)

        # Text annotation for displaying time taken
        text = ax.text(0.5, 0.95, "", transform=ax.transAxes, ha='center', va='top', fontsize=12)

        # Function to update the bar chart with each frame of the animation
        def update_fig(frame_data):
            arr = frame_data
            for rect, val in zip(bar_rects, arr):
                rect.set_height(val)
            elapsed_time = time.time() - start_time
            text.set_text(f"Time taken: {elapsed_time:.3f} seconds")
            return bar_rects

        # Create the animation
        start_time = time.time()
        sorting_animation = animation.FuncAnimation(fig, func=update_fig,
                                                    frames=insertion_sort(grades_list),
                                                    interval=50, repeat=False)

        # Show the animation
        plt.show()
    except Exception as e:
        messagebox.showerror("Error in Insertion Sort Animation", str(e))

# Create the main GUI window
def create_gui():
    root = tk.Tk()
    root.title("Grade 6 Analysis GUI")
    root.geometry("400x400")

    # Create buttons for each script
    btn1 = tk.Button(root, text="Sort Grades Animation", command=run_in_thread(script1), width=40, height=2)
    btn1.pack(pady=10)
                            
    btn2 = tk.Button(root, text="Insertion Sort Animation", command=run_in_thread(script6), width=40, height=2)
    btn2.pack(pady=10)
    

    btn3 = tk.Button(root, text="Radix Sort Animation", command=run_in_thread(script5), width=40, height=2)
    btn3.pack(pady=10)

    btn4 = tk.Button(root, text="Top 10 Regions by Average Grade", command=run_in_thread(script4), width=40, height=2)
    btn4.pack(pady=10)

    btn5 = tk.Button(root, text="Highest Grades by Region", command=run_in_thread(script2), width=40, height=2)
    btn5.pack(pady=10)

    btn6 = tk.Button(root, text="Average Grades Over Years", command=run_in_thread(script3), width=40, height=2)
    btn6.pack(pady=10)

    root.mainloop()

# Start the GUI
create_gui()