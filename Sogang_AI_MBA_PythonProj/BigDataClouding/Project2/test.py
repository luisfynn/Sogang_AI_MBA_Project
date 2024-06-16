import pandas as pd

# Load the CSV file
file_path = r"C:\Users\luisf\OneDrive\desktop\WorkSpace\Sogang_AI_MBA_Project\Sogang_AI_MBA_PythonProj\BigDataClouding\Project2\project2.csv"
data = pd.read_csv(file_path)

# Strip whitespace and print unique values in the 'gender' column
# data['gender'] = data['여자'].str.strip()
unique_genders = data.iloc[ :, 0].unique()

print(unique_genders)
