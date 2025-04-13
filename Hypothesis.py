# %% [markdown]
# <div style="background: linear-gradient(90deg, #00B8D9,rgb(12, 68, 76)); padding: 40px 20px; border-radius: 15px; text-align: center; animation: fadeIn 2s ease-in-out;">
#   <h1 style="color: white; font-size: 48px; margin-bottom: 10px;">Career Preferences Report: Gen Z Edition</h1>
#   <h3 style="color: #ECEFF1; font-weight: normal; font-size: 20px;">
#     Insights into Aspirations, Motivations, Industry Choices, and Challenges Shaping the Future of Work
#   </h3>
# </div>
# 
# <style>
# @keyframes fadeIn {
#   from { opacity: 0; transform: translateY(-10px); }
#   to { opacity: 1; transform: translateY(0); }
# }
# </style>
# 

# %%
# Requirements
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots


# %%
# Load the data
df =pd.read_csv("data/GenZ.csv")
df.head()

# %%
print(df.columns)

# %% [markdown]
# # Simplifying Column titles

# %%
# Original column names
original_columns = [
    'Your Current Country.',
    'Your Current Zip Code / Pin Code',
    'Your Gender',
    'Which of the below factors influence the most about your career aspirations ?',
    'Would you definitely pursue a Higher Education / Post Graduation outside of India ? If only you have to self sponsor it.',
    'How likely is that you will work for one employer for 3 years or more ?',
    'Would you work for a company whose mission is not clearly defined and publicly posted.',
    'How likely would you work for a company whose mission is misaligned with their public actions or even their product ?',
    'How likely would you work for a company whose mission is not bringing social impact ?',
    'What is the most preferred working environment for you.',
    'Which of the below Employers would you work with.',
    'Which type of learning environment that you are most likely to work in ?',
    'Which of the below careers looks close to your Aspirational job ?',
    'What type of Manager would you work without looking into your watch ?',
    'Which of the following setup you would like to work ?'
]

# New short names
new_columns = ['country', 'zip_code', 'gender', 'career_factors', 'higher_ed_abroad', 
               'long_term_employer', 'unclear_mission', 'misaligned_mission', 
               'no_social_impact', 'work_env', 'employer_choice', 'learning_env', 
               'asp_job', 'manager_type', 'work_setup']

# Create col_map (short name -> original name)
col_map = dict(zip(new_columns, original_columns))

# Rename the columns
df.columns = new_columns

# Optional: Save col_map to CSV
col_map_df = pd.DataFrame(list(col_map.items()), columns=['Short_Name', 'Original_Name'])
col_map_df.to_csv('data/column_mapping.csv', index=False)

print("Columns renamed and mapping saved to 'column_mapping.csv'")

# %%
df.columns

# %% [markdown]
# Dataframe is updated with new columns titles

# %% [markdown]
# Question 1 : Participant's Current Country and Demographics

# %%
# Count frequencies for country and gender
country_counts = df['country'].value_counts().reset_index()
country_counts.columns = ['country', 'count']

gender_counts = df['gender'].value_counts().reset_index()
gender_counts.columns = ['gender', 'count']

# Create a subplot with 1 row and 2 columns
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'pie'}, {'type': 'pie'}]],  # Specify pie chart types
    subplot_titles=['Participants by Country', 'Participants by Gender'],
    horizontal_spacing=0.4  # Add spacing between subplots
)

# Add Country Pie Chart
fig.add_trace(
    go.Pie(
        labels=country_counts['country'],
        values=country_counts['count'],
        textinfo='percent',
        textposition='inside',
        name='Country',
        showlegend=True,  # Enable legend for this pie
        domain=dict(x=[0, 0.45], y=[0, 1])  # Reduce size by limiting domain
    ),
    row=1, col=1
)

# Add Gender Pie Chart
fig.add_trace(
    go.Pie(
        labels=gender_counts['gender'],
        values=gender_counts['count'],
        textinfo='percent',
        textposition='inside',
        name='Gender',
        showlegend=True,  # Enable legend for this pie
        domain=dict(x=[0.55, 1], y=[0, 1])  # Reduce size by limiting domain
    ),
    row=1, col=2
)

# Update layout for size and separate legends
fig.update_layout(
    title_text='Distribution of Participants: Country and Gender',
    width=1000,  # Half of 1400
    height=350,  # Half of 700
    legend=dict(
        title='',  # Legend title for the first pie
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=0.25  # Position near the country pie
    ),
    # Add a second legend for gender pie
    annotations=[
        dict(
            text='',  # Legend title for gender
            x=1.05, y=0.5,  # Position near the gender pie
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=12)
        )
    ],
    margin=dict(t=100, b=50, l=50, r=150)  # Adjust margins
)

# Update traces to separate legends
fig.update_traces(
    legendgroup='country',  # Group country legend
    selector=dict(name='Country')
)
fig.update_traces(
    legendgroup='gender', legend='legend2',  # Separate gender legend
    selector=dict(name='Gender')
)

# Display the chart
fig.show()

# Print summaries
print("Participants' Country Distribution:")
for country, count in country_counts.itertuples(index=False):
    print(f"{country}: {count} participants ({(count / len(df)) * 100:.1f}%)")

print("\nParticipants' Gender Distribution:")
for gender, count in gender_counts.itertuples(index=False):
    print(f"{gender}: {count} participants ({(count / len(df)) * 100:.1f}%)")

# %% [markdown]
# Since Majority participants i.e., 98% participants from India, We can remove the rest of the responses

# %%
# Filter the DataFrame to keep only participants from India
df = df[df['country'] == 'India'].reset_index(drop=True)

# Verify the update
print("Updated DataFrame - Country Distribution:")
print(df['country'].value_counts())
print(f"Total participants after update: {len(df)}")

# %%
# Count frequencies for gender in the updated df
gender_counts = df['gender'].value_counts().reset_index()
gender_counts.columns = ['gender', 'count']

# Create a pie chart
fig = px.pie(
    gender_counts,
    values='count',
    names='gender',
    title='Gender Distribution of Indian Participants',
    width=800,  # Moderate width
    height=300  # Moderate height
)

# Customize the chart
fig.update_traces(
    textinfo='percent',  # Show percentages on the slices
    textposition='inside'  # Place percentages inside the slices
)
fig.update_layout(
    legend_title_text='Gender',  # Legend title
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.1  # Position legend to the right
    ),
    margin=dict(t=50, b=50, l=50, r=150)  # Adjust margins for legend
)

# Display the chart
fig.show()

# Print a summary
print("Gender Distribution (Indian Participants):")
for gender, count in gender_counts.itertuples(index=False):
    print(f"{gender}: {count} participants ({(count / len(df)) * 100:.1f}%)")

# %% [markdown]
# Question 2 : Which of the below factors influence the most about your career aspirations ?

# %%
# Display all values in the 'career_factors' column
print(df['career_factors'].head())

# %%
# Display unique values in 'career_factors'
unique_factors = df['career_factors'].unique()
print("Unique Career Factors:")
for factor in unique_factors:
    print(factor)

print("\n")    
# Count frequencies for career factors
career_counts = df['career_factors'].value_counts().reset_index()

# Display value counts for 'career_factors'
print("Career Factors Distribution:")
print(career_counts.head())

# %%
# Count frequencies for career_factors
career_counts = df['career_factors'].value_counts().reset_index()
career_counts.columns = ['career_factors', 'count']

# Create a pie chart
fig = px.pie(
    career_counts,
    values='count',
    names='career_factors',
    title='Distribution of Career Factors Influencing Aspirations',
    width=800,
    height=350
)
fig.update_traces(textinfo='percent', textposition='inside')
fig.update_layout(
    legend_title_text='Career Factors',
    legend=dict(yanchor="middle", y=0.5, xanchor="left", x=1.1)
)
fig.show()

# %% [markdown]
# Question 3: Would you definitely pursue a Higher Education / Post Graduation outside of India ? If only you have to self sponsor it?

# %%
# Count frequencies for higher_ed_abroad
higher_ed_counts = df['higher_ed_abroad'].value_counts().reset_index()
higher_ed_counts.columns = ['higher_ed_abroad', 'count']

# Print a summary
print("Higher Education Abroad Distribution:")
for response, count in higher_ed_counts.itertuples(index=False):
    print(f"{response}: {count} participants ({(count / len(df)) * 100:.1f}%)")

# Create a pie chart
fig = px.pie(
    higher_ed_counts,
    values='count',
    names='higher_ed_abroad',
    title='Willingness to Pursue Higher Education Abroad (Self-Sponsored)',
    width=800,  # Moderate width
    height=300  # Moderate height
)

# Customize the chart
fig.update_traces(
    textinfo='percent',  # Show percentages on the slices
    textposition='inside'  # Place percentages inside the slices
)
fig.update_layout(
    legend_title_text='Response',  # Legend title
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.1  # Position legend to the right
    ),
    margin=dict(t=50, b=50, l=50, r=150)  # Adjust margins for legend
)

# Display the chart
fig.show()


# %% [markdown]
# Question 4:  How likely is that you will work for one employer for 3 years or more ?

# %%
# Count frequencies for long_term_employer
employer_counts = df['long_term_employer'].value_counts().reset_index()
employer_counts.columns = ['long_term_employer', 'count']

# Print a summary
print("Long-Term Employer Distribution:")
for response, count in employer_counts.itertuples(index=False):
    print(f"{response}: {count} participants ({(count / len(df)) * 100:.1f}%)")

# Create a pie chart
fig = px.pie(
    employer_counts,
    values='count',
    names='long_term_employer',
    title='Likelihood of Working for One Employer for 3+ Years',
    width=800,  # Moderate width
    height=300  # Moderate height
)

# Customize the chart
fig.update_traces(
    textinfo='percent',  # Show percentages on the slices
    textposition='inside'  # Place percentages inside the slices
)
fig.update_layout(
    legend_title_text='Likelihood',  # Legend title
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.1  # Position legend to the right
    ),
    margin=dict(t=50, b=50, l=50, r=150)  # Adjust margins for legend
)

# Display the chart
fig.show()

# %% [markdown]
# Question 5: Would you work for a company whose mission is not clearly defined and publicly posted?

# %%
# Count frequencies for unclear_mission
mission_counts = df['unclear_mission'].value_counts().reset_index()
mission_counts.columns = ['unclear_mission', 'count']

# Print a summary
print("Unclear Mission Distribution:")
for response, count in mission_counts.itertuples(index=False):
    print(f"{response}: {count} participants ({(count / len(df)) * 100:.1f}%)")
    
# Create a pie chart
fig = px.pie(
    mission_counts,
    values='count',
    names='unclear_mission',
    title='Willingness to Work for a Company with an Unclear Mission',
    width=600,  # Moderate width
    height=300  # Moderate height
)

# Customize the chart
fig.update_traces(
    textinfo='percent',  # Show percentages on the slices
    textposition='inside'  # Place percentages inside the slices
)
fig.update_layout(
    legend_title_text='Response',  # Legend title
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.1  # Position legend to the right
    ),
    margin=dict(t=50, b=50, l=50, r=150)  # Adjust margins for legend
)

# Display the chart
fig.show()

# %% [markdown]
# Question 6:  How likely would you work for a company whose mission is misaligned with their public actions or even their product ?

# %%
# Count frequencies for misaligned_mission
mission_counts = df['misaligned_mission'].value_counts().reset_index()
mission_counts.columns = ['misaligned_mission', 'count']

# Print a summary
print("Misaligned Mission Distribution:")
for response, count in mission_counts.itertuples(index=False):
    print(f"{response}: {count} participants ({(count / len(df)) * 100:.1f}%)")
    
# Create a pie chart
fig = px.pie(
    mission_counts,
    values='count',
    names='misaligned_mission',
    title='Likelihood of Working for a Company with a Misaligned Mission',
    width=600,  # Moderate width
    height=300  # Moderate height
)

# Customize the chart
fig.update_traces(
    textinfo='percent',  # Show percentages on the slices
    textposition='inside'  # Place percentages inside the slices
)
fig.update_layout(
    legend_title_text='Response',  # Legend title
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.1  # Position legend to the right
    ),
    margin=dict(t=50, b=50, l=50, r=150)  # Adjust margins for legend
)

# Display the chart
fig.show()

# %% [markdown]
# Question 7:  How likely would you work for a company whose mission is not bringing social impact ?

# %%
# Count frequencies for misaligned_mission
mission_counts = df['no_social_impact'].value_counts().reset_index()
mission_counts.columns = ['no_social_impact', 'count']

# Print a summary
print("No Social Impact Distribution:")
for response, count in mission_counts.itertuples(index=False):
    print(f"{response}: {count} participants ({(count / len(df)) * 100:.1f}%)")
    
# Create a pie chart
fig = px.pie(
    mission_counts,
    values='count',
    names='no_social_impact',
    title='Likelihood of not Working for a Company with a social impact Mission',
    width=800,  # Moderate width
    height=350  # Moderate height
)

# Customize the chart
fig.update_traces(
    textinfo='percent',  # Show percentages on the slices
    textposition='inside'  # Place percentages inside the slices
)
fig.update_layout(
    legend_title_text='Response',  # Legend title
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.1  # Position legend to the right
    ),
    margin=dict(t=50, b=50, l=50, r=150)  # Adjust margins for legend
)

# Display the chart
fig.show()

# %% [markdown]
# Question 8:  What is the most preferred working environment for you?

# %%
import plotly.express as px

# Count frequencies for work_env
env_counts = df['work_env'].value_counts().reset_index()
env_counts.columns = ['work_env', 'count']

# Print a summary
print("Work Environment Distribution:")
for response, count in env_counts.itertuples(index=False):
    print(f"{response}: {count} participants ({(count / len(df)) * 100:.1f}%)")

# Create a pie chart
fig = px.pie(
    env_counts,
    values='count',
    names='work_env',
    title='Preferred Working Environment',
    width=800,  # Moderate width
    height=300  # Moderate height
)

# Customize the chart
fig.update_traces(
    textinfo='percent',  # Show percentages on the slices
    textposition='inside'  # Place percentages inside the slices
)
fig.update_layout(
    legend_title_text='Work Environment',  # Legend title
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.1  # Position legend to the right
    ),
    margin=dict(t=50, b=50, l=50, r=150)  # Adjust margins for legend
)

# Display the chart
fig.show()

# %% [markdown]
# Question 9:  Which of the below Employers would you work with?

# %%
# Count frequencies for employer_choice
employer_counts = df['employer_choice'].value_counts().reset_index()
employer_counts.columns = ['employer_choice', 'count']

# Print a summary
print("Employer Choice Distribution:")
for response, count in employer_counts.itertuples(index=False):
    print(f"{response}: {count} participants ({(count / len(df)) * 100:.1f}%)")
    
# Create a pie chart
fig = px.pie(
    employer_counts,
    values='count',
    names='employer_choice',
    title='Preferred Employer Choice',
    width=1000,  # Moderate width
    height=350  # Moderate height
)

# Customize the chart
fig.update_traces(
    textinfo='percent',  # Show percentages on the slices
    textposition='inside'  # Place percentages inside the slices
)
fig.update_layout(
    legend_title_text='Employer',  # Legend title
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.1  # Position legend to the right
    ),
    margin=dict(t=50, b=50, l=50, r=150)  # Adjust margins for legend
)

# Display the chart
fig.show()

# %% [markdown]
# Question 10:  Which type of learning environment that you are most likely to work in ?

# %%
# Count frequencies for learning_env
learning_counts = df['learning_env'].value_counts().reset_index()
learning_counts.columns = ['learning_env', 'count']

# Print a summary
print("Learning Environment Distribution:")
for response, count in learning_counts.itertuples(index=False):
    print(f"{response}: {count} participants ({(count / len(df)) * 100:.1f}%)")
    
# Create a pie chart
fig = px.pie(
    learning_counts,
    values='count',
    names='learning_env',
    title='Preferred Learning Environment',
    width=1000,  # Moderate width
    height=350  # Moderate height
)

# Customize the chart
fig.update_traces(
    textinfo='percent',  # Show percentages on the slices
    textposition='inside'  # Place percentages inside the slices
)
fig.update_layout(
    legend_title_text='Learning Environment',  # Legend title
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.1  # Position legend to the right
    ),
    margin=dict(t=50, b=50, l=50, r=150)  # Adjust margins for legend
)

# Display the chart
fig.show()

# %% [markdown]
# Question 11:  Which of the below careers looks close to your Aspirational job ?

# %%
# Count frequencies for asp_job
job_counts = df['asp_job'].value_counts().reset_index()
job_counts.columns = ['asp_job', 'count']

# Print a summary
#print("Aspirational Job Distribution:")
#for response, count in job_counts.itertuples(index=False):
#    print(f"{response}: {count} participants ({(count / len(df)) * 100:.1f}%)")
    
# Create a pie chart
fig = px.pie(
    job_counts,
    values='count',
    names='asp_job',
    title='Aspirational Job Preferences',
    width=1400,  # Moderate width
    height=500  # Moderate height
)

# Customize the chart
fig.update_traces(
    textinfo='percent',  # Show percentages on the slices
    textposition='inside'  # Place percentages inside the slices
)
fig.update_layout(
    legend_title_text='Aspirational Job',  # Legend title
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.1,  # Position legend to the right
        font=dict(size=8)  # Adjust font size for better readability
    ),
    margin=dict(t=50, b=50, l=50, r=150)  # Adjust margins for legend
)

# Display the chart
fig.show()


# %% [markdown]
# Question 12:  What type of Manager would you work without looking into your watch ?

# %%
# Count frequencies for manager_type
manager_counts = df['manager_type'].value_counts().reset_index()
manager_counts.columns = ['manager_type', 'count']

# Print a summary
print("Manager Type Distribution:")
for response, count in manager_counts.itertuples(index=False):
    print(f"{response}: {count} participants ({(count / len(df)) * 100:.1f}%)")
    
# Create a pie chart
fig = px.pie(
    manager_counts,
    values='count',
    names='manager_type',
    title='Preferred Manager Type',
    width=900,  # Moderate width
    height=400  # Moderate height
)

# Customize the chart
fig.update_traces(
    textinfo='percent',  # Show percentages on the slices
    textposition='inside'  # Place percentages inside the slices
)
fig.update_layout(
    legend_title_text='Manager Type',  # Legend title
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.1, # Position legend to the right
        font=dict(size=8) 
    ),
    margin=dict(t=50, b=50, l=50, r=150)  # Adjust margins for legend
)

# Display the chart
fig.show()

# %% [markdown]
# Question 13:  Which of the following setup you would like to work ?

# %%
# Count frequencies for work_setup
setup_counts = df['work_setup'].value_counts().reset_index()
setup_counts.columns = ['work_setup', 'count']

# Print a summary
print("Work Setup Distribution:")
for response, count in setup_counts.itertuples(index=False):
    print(f"{response}: {count} participants ({(count / len(df)) * 100:.1f}%)")
    
# Create a pie chart
fig = px.pie(
    setup_counts,
    values='count',
    names='work_setup',
    title='Preferred Work Setup',
    width=1200,  # Moderate width
    height=400  # Moderate height
)

# Customize the chart
fig.update_traces(
    textinfo='percent',  # Show percentages on the slices
    textposition='inside'  # Place percentages inside the slices
)
fig.update_layout(
    legend_title_text='Work Setup',  # Legend title
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.1,  # Position legend to the right
        font=dict(size=8) 
    ),
    margin=dict(t=50, b=50, l=50, r=150)  # Adjust margins for legend
)

# Display the chart
fig.show()


