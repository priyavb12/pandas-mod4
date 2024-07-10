#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# - Your analysis here
#   
# ---

# In[52]:


# Dependencies and Setup
import pandas as pd
from pathlib import Path

# File to Load (Remember to Change These)
school_data_to_load = Path("./Resources/schools_complete.csv")
student_data_to_load = Path("./Resources/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()


# In[54]:


school_data = pd.read_csv(school_data_to_load)
school_data


# ## District Summary

# In[57]:


# Calculate the total number of unique schools
school_data["school_name"]

total_schools =school_data["school_name"].count()
total_schools


# In[59]:


# Calculate the total number of students
total_students = student_data["student_name"].count()
total_students


# In[61]:


# Calculate the total budget
school_data["budget"]

total_budget = school_data["budget"].sum()
total_budget


# In[63]:


# Calculate the average (mean) math score
student_data["math_score"]

avg_math =student_data["math_score"].sum()/total_students
avg_math


# In[75]:


# Calculate the average (mean) reading score
student_data["reading_score"]

average_reading_score = student_data["reading_score"].sum()/total_students
average_reading_score


# In[79]:


# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math  = school_data_complete.loc[school_data_complete['math_score']>=70, :]['student_name'].count()
passing_percent_math = (passing_math / total_students)*100
passing_percent_math


# In[81]:


# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)
passing_reading = school_data_complete.loc[school_data_complete['reading_score']>=70, :]['student_name'].count()
passing_reading_percentage = (passing_reading / total_students) *100
passing_reading_percentage



# In[83]:


# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = (passing_math_reading_count / total_students) * 100
overall_passing_rate


# In[85]:


# Create a high-level snapshot of the district's key metrics in a DataFrame
district_summary_df = pd.DataFrame(
        {
            'Total Schools' : [total_schools],
            'Total Students' : [total_students],
            'Total Budget' : [total_budget],
            'Average Math Score' : [avg_math],
            'Average Reading Score' : [average_reading_score],
            '% Passing Math' : [passing_percent_math],
            '% Passing Reading' : [passing_reading_percentage],
            '% Overall Passing Rate' : [overall_passing_rate]
        }
)

district_summary_df['Total Students'] = district_summary_df['Total Students'].map(' {:,}'.format)

district_summary_df['Total Budget'] = district_summary_df['Total Budget'].map('$ {:,.2f}'.format)

# district_summary_df = district_summary_df[['Total Schools', 'Total Students', 'Total Budget', 
#                           'Average Math Score', 'Average Reading Score',
#                        '% Passing Math', '% Passing Reading', '% Overall Passing Rate']]

district_summary_df


# ## School Summary

# In[104]:


# Use the code provided to select the type per school from school_data
school_types = school_data.set_index(["school_name"])["type"]


# In[106]:


# Calculate the total student count per school from school_data
per_school_counts =school_data_complete['school_name'].value_counts()
per_school_counts



# In[108]:


# Calculate the total school budget and per capita spending per school from school_data
total_school_budget = school_data_complete.groupby(['school_name'])['budget'].mean ()
total_school_budget

# total_school_budget = school_data_complete.groupby(['school_name']).mean()['budget'] 
# total_school_budget

per_school_capita = total_school_budget / per_school_counts
per_school_capita


# In[110]:


# Calculate the average test scores per school from school_data_complete
per_school_math = school_data_complete.groupby(['school_name'])['math_score'].mean()
per_school_math

per_school_reading =school_data_complete.groupby('school_name')['reading_score'].mean()
per_school_reading


# In[112]:


# Calculate the number of students per school with math scores of 70 or higher from school_data_complete
students_passing_math =school_data_complete[school_data_complete['math_score']>=70]
students_passing_math


# In[114]:


# Calculate the number of students per school with reading scores of 70 or higher from school_data_complete
students_passing_reading =school_data_complete[school_data_complete['reading_score']>=70]
students_passing_reading


# In[116]:


# Use the provided code to calculate the number of students per school that passed both math and reading with scores of 70 or higher
passing_math_and_reading = school_data_complete[
     (school_data_complete["reading_score"] >= 70) & (school_data_complete["math_score"] >= 70)
 ]


# In[118]:


# Use the provided code to calculate the passing rates
per_school_passing_math = students_passing_math.groupby(['school_name']).count()['student_name'] / per_school_counts * 100
per_school_passing_math

per_school_passing_reading =students_passing_reading.groupby(['school_name']).count()['student_name'] / per_school_counts * 100
per_school_passing_reading

overall_passing_rate = passing_math_and_reading.groupby(['school_name']).count()['student_name'] / per_school_counts * 100
overall_passing_rate


# In[120]:


# Create a DataFrame called `per_school_summary` with columns for the calculations above.
per_school_summary = pd.DataFrame(
        {
            'School Type' : school_types,
            'Total Students' : per_school_counts,
            'Total School Budget' : total_school_budget,
            'Per Student Budget' : per_school_capita,
            'Average Math Score' : per_school_math,
            'Average Reading Score' : per_school_reading,
            '% Passing Math'  : per_school_passing_math,
            '% Passing Reading' :  per_school_passing_reading,
            '% Overall Passing' : overall_passing_rate
        }                        
)


# Formatting
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)

# Display the DataFrame
per_school_summary


# ## Highest-Performing Schools (by % Overall Passing)

# In[125]:


# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values('% Overall Passing',ascending=False)
top_schools.head(5)


# ## Bottom Performing Schools (By % Overall Passing)

# In[127]:


# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values('% Overall Passing',ascending=True).iloc[0:5,]
bottom_schools.head(5)


# ## Math Scores by Grade

# In[129]:


# Use the code provided to separate the data by grade
students_9  = school_data_complete.loc[school_data_complete['grade'] == '9th',]
students_10 = school_data_complete.loc[school_data_complete['grade'] == '10th',]
students_11 = school_data_complete.loc[school_data_complete['grade'] == '11th',]
students_12 =school_data_complete.loc[school_data_complete['grade'] == '12th',]

students_9_school_count  = students_9.groupby('school_name')['grade'].count()
students_10_school_count = students_10.groupby('school_name')['grade'].count()
students_11_school_count = students_11.groupby('school_name')['grade'].count()
students_12_school_count = students_12.groupby('school_name')['grade'].count()

math_9_school  = students_9.groupby('school_name')['math_score'].sum() / students_9_school_count
math_10_school = students_10.groupby('school_name')['math_score'].sum() / students_10_school_count
math_11_school = students_11.groupby('school_name')['math_score'].sum() / students_11_school_count
math_12_school = students_12.groupby('school_name')['math_score'].sum() / students_12_school_count


math_scores_by_grade = pd.DataFrame (
            { 
                '9th' : math_9_school,
                '10th': math_10_school,
                '11th' : math_11_school,
                '12th' : math_12_school
            }
)
math_scores_by_grade.index.name = None

math_scores_by_grade


# ## Reading Score by Grade 

# In[131]:


# Use the code provided to separate the data by grade
students_9  = school_data_complete.loc[school_data_complete['grade'] == '9th',]
students_10 = school_data_complete.loc[school_data_complete['grade'] == '10th',]
students_11 = school_data_complete.loc[school_data_complete['grade'] == '11th',]
students_12 =school_data_complete.loc[school_data_complete['grade'] == '12th',]

students_9_school_count  = students_9.groupby('school_name')['grade'].count()
students_10_school_count = students_10.groupby('school_name')['grade'].count()
students_11_school_count = students_11.groupby('school_name')['grade'].count()
students_12_school_count = students_12.groupby('school_name')['grade'].count()

reading_9_school  = students_9.groupby('school_name')['reading_score'].sum() / students_9_school_count
reading_10_school = students_10.groupby('school_name')['reading_score'].sum() / students_10_school_count
reading_11_school = students_11.groupby('school_name')['reading_score'].sum() / students_11_school_count
reading_12_school = students_12.groupby('school_name')['reading_score'].sum() / students_12_school_count


reading_scores_by_grade = pd.DataFrame (
            { 
                '9th' : reading_9_school,
                '10th':reading_10_school,
                '11th' : reading_11_school,
                '12th' : reading_12_school
            }
)
math_scores_by_grade.index.name = None
reading_scores_by_grade


# ## Scores by School Spending

# In[138]:


# Establish the bins
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]


# In[140]:


# Create a copy of the school summary since it has the "Per Student Budget"
school_spending_df = per_school_summary.copy()


# In[142]:


# Use `pd.cut` to categorize spending based on the bins.
school_spending_df["Spending Ranges (Per Student)"] = pd.cut(per_school_capita, bins =spending_bins, labels = labels)
school_spending_df


# In[144]:


#  Calculate averages for the desired columns.
spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Math Score"].mean()
spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Reading Score"].mean()
spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Math"].mean()
spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Reading"].mean()
overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Overall Passing"].mean()


# In[148]:


# Assemble into DataFrame
spending_summary = pd.DataFrame({
            'Average Math Score' : spending_math_scores,
         'Average Reading Score' : spending_reading_scores,
            '% Passing Math'  : spending_passing_math,
            '% Passing Reading' :  spending_passing_reading,
            '% Overall Passing' : overall_passing_spending
    
})

# Display results
spending_summary


# ## Scores by School Size

# In[152]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[154]:


# Categorize the spending based on the bins
# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

per_school_summary["School Size"] = pd.cut(per_school_summary['Total Students'],size_bins,labels=labels) 

per_school_summary


# In[156]:


# Calculate averages for the desired columns.
size_math_scores = per_school_summary.groupby(["School Size"])["Average Math Score"].mean()
size_reading_scores = per_school_summary.groupby(["School Size"])["Average Reading Score"].mean()
size_passing_math = per_school_summary.groupby(["School Size"])["% Passing Math"].mean()
size_passing_reading = per_school_summary.groupby(["School Size"])["% Passing Reading"].mean()
size_overall_passing = per_school_summary.groupby(["School Size"])["% Overall Passing"].mean()


# In[158]:


# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_summary = pd.DataFrame (
    {
         'Average Math Score' : size_math_scores,
         'Average Reading Score' : size_reading_scores,
            '% Passing Math'  : size_passing_math,
            '% Passing Reading' :  size_passing_reading,
            '% Overall Passing' : size_overall_passing

     }                    
)

# Display results
size_summary


# ## Scores by School Type

# In[162]:


# Group the per_school_summary DataFrame by "School Type" and average the results.
average_math_score_by_type = per_school_summary.groupby(["School Type"])["Average Math Score"].mean()
average_reading_score_by_type = per_school_summary.groupby(["School Type"])["Average Reading Score"].mean()
average_percent_passing_math_by_type = per_school_summary.groupby(["School Type"])["% Passing Math"].mean()
average_percent_passing_reading_by_type = per_school_summary.groupby(["School Type"])["% Passing Reading"].mean()
average_percent_overall_passing_by_type = per_school_summary.groupby(["School Type"])["% Overall Passing"].mean()


# In[164]:


# Assemble the new data by type into a DataFrame called `type_summary`
type_summary = pd.DataFrame({

       'Average Math Score' : average_math_score_by_type,
         'Average Reading Score' : average_reading_score_by_type,
            '% Passing Math'  : average_percent_passing_math_by_type ,
            '% Passing Reading' :  average_percent_passing_reading_by_type,
            '% Overall Passing' :  average_percent_overall_passing_by_type            

})


# Display results
type_summary


# In[ ]:





# In[ ]:




