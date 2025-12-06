import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr  # Yield intermediate states for animation
        arr[j + 1] = key

# Read the Excel file for all sheets (14-15, 15-16, and 16-17)
df_14_15 = pd.read_excel(r'C:\Users\Ariese\Documents\Book2.xlsx', sheet_name='14-15')
df_15_16 = pd.read_excel(r'C:\Users\Ariese\Documents\Book2.xlsx', sheet_name='15-16')
df_16_17 = pd.read_excel(r'C:\Users\Ariese\Documents\Book2.xlsx', sheet_name='16-17')

# Combine data from all sheets
combined_df = pd.concat([df_14_15, df_15_16, df_16_17], ignore_index=True)

# Fill disallowed values with NaN
combined_df.fillna(np.nan, inplace=True)

# Convert columns to numeric type
combined_df['Math'] = pd.to_numeric(combined_df['Math'], errors='coerce')
combined_df['English'] = pd.to_numeric(combined_df['English'], errors='coerce')
combined_df['Science'] = pd.to_numeric(combined_df['Science'], errors='coerce')

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
    global start_time
    arr = frame_data
    for rect, val in zip(bar_rects, arr):
        rect.set_height(val)
    # Calculate elapsed time and update text annotation
    elapsed_time = time.time() - start_time
    text.set_text(f"Time taken: {elapsed_time:.3f} seconds")
    return bar_rects

# Create the animation
start_time = time.time()
sorting_animation = animation.FuncAnimation(fig, func=update_fig, frames=insertion_sort(grades_list), 
                                            interval=1, repeat=False)

# Show the animation
plt.show()
