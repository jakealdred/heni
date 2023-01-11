import pandas as pd
import numpy as np

# Apply regex to rawDim and clean extracted strings
df = pd.read_csv("candidateEvalData/dim_df_correct.csv", usecols=['rawDim'])
regex_string = "(?:\d+(?:[,|\.]\d+\sx\s))?\d+(?:[,|\.]\d+)?\s?(?:x|by|×)\s?\d+(?:[,|.]\d+)?\s?(?:cm|in)"
df['extracted_text'] = df['rawDim'].str.findall(regex_string).str[-1].str.replace(' ', '').str.replace('x', ' ')\
    .str.replace(',', '.').str.replace('cm', '').str.replace('by', ' ').str.replace('×', ' ')

# Make a note of which extracted strings need converting from inches to cm
df['inches'] = np.where(df['extracted_text'].str.contains('in'), True, False)
df['extracted_text'] = df['extracted_text'].str.replace('in', '')

# Extract height, width and depth from cleaned strings and apply inch -> cm conversion if required
for i, col in enumerate(['height', 'width', 'depth']):
    df[col] = df['extracted_text'].str.split(" ").str[i].astype('float64')
    df[col] = np.where(df['inches'] == True, df[col] * 2.54, df[col])

df[['rawDim', 'height', 'width', 'depth']].to_csv('question_2_output.csv', encoding='utf-8', index=False)
