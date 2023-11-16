import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap
import random

class DataAnalysis:
    def __init__(self, csv_path, output_folder):
        self.df = pd.read_csv(csv_path)
        self.output_folder = output_folder
        self.create_output_folder()

    def create_output_folder(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def save_plot(self, plot_name):
        plot_path = os.path.join(self.output_folder, plot_name)
        plt.savefig(plot_path)
    

    def analyze_sex_ratios(self):
    
        sex_ratio_total_population = self.df[['State/UT', 'Sex ratio of the total population (females per 1,000 males)']]
        sex_ratio_birth = self.df[['State/UT', 'Sex ratio at birth for children born in the last five years (females per 1,000 males)']]

        
        mean_sex_ratio_total_population = sex_ratio_total_population.groupby('State/UT').mean().reset_index()
        mean_sex_ratio_birth = sex_ratio_birth.groupby('State/UT').mean().reset_index()    
        combined_mean = pd.merge(mean_sex_ratio_total_population, mean_sex_ratio_birth, on='State/UT')

    
        plt.figure(figsize=(12, 10))
        bar_width = 0.2  
        bar_positions = np.arange(len(combined_mean))
        plt.barh(bar_positions, combined_mean['Sex ratio of the total population (females per 1,000 males)'], bar_width, color='blue', alpha=0.9, label='Total Population')
        plt.barh(bar_positions + bar_width, combined_mean['Sex ratio at birth for children born in the last five years (females per 1,000 males)'], bar_width, color='orange', alpha=0.9, label='At Birth')

        plt.yticks(bar_positions + bar_width / 2, combined_mean['State/UT'])
        plt.xlabel('Sex Ratio')
        plt.ylabel('States')
        plt.title('Mean Sex Ratios of Total Population and at Birth for Each State')
        plt.legend()
        plt.tight_layout()
        plot_name = 'Sex_Ratio_Analysis.png'
        self.save_plot(plot_name)
        plt.show()
       

    
        states_higher_birth_ratio = combined_mean[combined_mean['Sex ratio at birth for children born in the last five years (females per 1,000 males)'] > combined_mean['Sex ratio of the total population (females per 1,000 males)']]
        print("States with Sex Ratio at Birth higher than Overall Sex Ratio:")
        print(states_higher_birth_ratio['State/UT'])


    def analyze_alcohol_consumption(self):
           
        women_alcohol = self.df[['State/UT', 'Women age 15 years and above who consume alcohol (%)']]
        men_alcohol = self.df[['State/UT', 'Men age 15 years and above who consume alcohol (%)']]

        women_median = women_alcohol.groupby('State/UT').median().reset_index()
        men_median = men_alcohol.groupby('State/UT').median().reset_index()

        plt.figure(figsize=(6, 4))
        plt.plot(women_median['State/UT'], women_median['Women age 15 years and above who consume alcohol (%)'], label='Women', marker='o', color='red')
        plt.plot(men_median['State/UT'], men_median['Men age 15 years and above who consume alcohol (%)'], label='Men', marker='o', color='blue')

        plt.title('Median Alcohol Consumption by Gender')
        plt.xlabel('State/UT')
        plt.ylabel('Median Alcohol Consumption (%)')
        plt.tight_layout()
        plt.xticks(rotation=90, fontsize=5, fontweight='bold')
        plt.yticks(fontsize=6, fontweight='bold')
        

        plt.legend()
        plot_name = 'alcohol_consumption_analysis.png'
        self.save_plot(plot_name)
        plt.show()
        
        
        

   
    def analyze_blood_pressure(self):
    
        women_mild = self.df["Women age 15 years and above wih Mildly elevated blood pressure (Systolic 140-159 mm of Hg and/or Diastolic 90-99 mm of Hg) (%)"].mean()
        women_moderate = self.df["Women age 15 years and above wih Moderately or severely elevated blood pressure (Systolic ≥160 mm of Hg and/or Diastolic ≥100 mm of Hg) (%)"].mean()
        women_elevated = self.df["Women age 15 years and above wih Elevated blood pressure (Systolic ≥140 mm of Hg and/or Diastolic ≥90 mm of Hg) or taking medicine to control blood pressure (%)"].mean()

        men_mild = self.df["Men age 15 years and above wih Mildly elevated blood pressure (Systolic 140-159 mm of Hg and/or Diastolic 90-99 mm of Hg) (%)"].mean()
        men_moderate = self.df["Men age 15 years and above wih Moderately or severely elevated blood pressure (Systolic ≥160 mm of Hg and/or Diastolic ≥100 mm of Hg) (%)"].mean()
        men_elevated = self.df["Men age 15 years and above wih Elevated blood pressure (Systolic ≥140 mm of Hg and/or Diastolic ≥90 mm of Hg) or taking medicine to control blood pressure (%)"].mean()

    
        comparison_table = pd.DataFrame({
            'Category': ['Mildly Elevated', 'Severely Elevated', 'Elevated'],
            'Women': [women_mild, women_moderate, women_elevated],
            'Men': [men_mild, men_moderate, men_elevated]
        })

        
        ax = comparison_table.plot(x='Category', y=['Women', 'Men'], kind='bar')
        ax.set_xticklabels(comparison_table['Category'], rotation=0)
        plt.title('Comparison of Blood Pressure Categories between Men and Women')
        plt.xlabel('Category')
        plt.ylabel('Percentage (%)')
        plot_name = ' Overall_bollod_pressure_comparison'
        self.save_plot(plot_name)
        plt.show()
        
        print(comparison_table)

    
        women_elevated_bp = self.df[["State/UT", "Women age 15 years and above wih Elevated blood pressure (Systolic ≥140 mm of Hg and/or Diastolic ≥90 mm of Hg) or taking medicine to control blood pressure (%)"]]
        women_elevated_bp = women_elevated_bp.dropna() 
        mean_bp_by_state_women = women_elevated_bp.groupby('State/UT').agg(np.mean).reset_index()
        men_elevated_bp = self.df[["State/UT", "Men age 15 years and above wih Elevated blood pressure (Systolic ≥140 mm of Hg and/or Diastolic ≥90 mm of Hg) or taking medicine to control blood pressure (%)"]]
        men_elevated_bp = men_elevated_bp.dropna() 
        mean_bp_by_state_men = men_elevated_bp.groupby('State/UT').agg(np.mean).reset_index()
        top_states_men = mean_bp_by_state_men.nlargest(5, columns="Men age 15 years and above wih Elevated blood pressure (Systolic ≥140 mm of Hg and/or Diastolic ≥90 mm of Hg) or taking medicine to control blood pressure (%)")
        top_states_women = mean_bp_by_state_women.nlargest(5, columns="Women age 15 years and above wih Elevated blood pressure (Systolic ≥140 mm of Hg and/or Diastolic ≥90 mm of Hg) or taking medicine to control blood pressure (%)")

    
        colors_men = ['blue', 'green', 'orange', 'red', 'purple']
        colors_women = ['pink', 'lightgreen', 'lightblue', 'magenta', 'cyan']

       
        plt.figure(figsize=(12, 6))
        plt.subplot(121) 
        plt.bar(top_states_men["State/UT"], top_states_men["Men age 15 years and above wih Elevated blood pressure (Systolic ≥140 mm of Hg and/or Diastolic ≥90 mm of Hg) or taking medicine to control blood pressure (%)"], color=colors_men)
        plt.title('Top Five States for Men with Highest Elevated Blood Pressure')
        plt.xlabel('State/UT')
        plt.ylabel('Percentage of Men with Elevated Blood Pressure')
        plt.xticks(rotation=45)

        plt.subplot(122) 
        plt.bar(top_states_women["State/UT"], top_states_women["Women age 15 years and above wih Elevated blood pressure (Systolic ≥140 mm of Hg and/or Diastolic ≥90 mm of Hg) or taking medicine to control blood pressure (%)"], color=colors_women)
        plt.title('Top Five States for Women with Highest Elevated Blood Pressure')
        plt.xlabel('State/UT')
        plt.ylabel('Percentage of Women with Elevated Blood Pressure')
        plt.xticks(rotation=45)
        plt.tight_layout()       
        plt.show()


class ScatterPlotGenerator:
    def __init__(self, data_path):
        """Initialize ScatterPlotGenerator object."""
        self.df = pd.read_csv(data_path)
        self.df.iloc[:, 2:] = self.df.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')
        self.df = self.df.replace('*', pd.NA)  # Replacing '*' with NaN
        self.df.iloc[:, 2:] = self.df.iloc[:, 2:].abs()  #
        self.df.fillna(self.df.mean(), inplace=True)
        self.selected_columns = None

    def plot_scatter_plot(self, col1, col2):
        """Plot scatter plot for specific columns."""
        sns.set(style="whitegrid")
        scatter = sns.scatterplot(x=col1, y=col2, data=self.df, marker='o', color='blue', alpha=0.7)
        scatter.set(xlabel=col1, ylabel=col2)
        plt.title('Scatter Plot of Selected Coloumns', loc='center', pad=20)
        plt.tight_layout(pad=5)
        plt.show()


    def execute_scatter_plot(self):
        """Execute the scatter plot visualization."""
        print("Available columns for scatter plot:")
        for i, col in enumerate(self.df.columns[5:16]):
            print(f"{i + 1}. {col}")

        selected_column_indices = [int(input(f"Enter the index of the first column: ")) - 1,
                                   int(input(f"Enter the index of the second column: ")) - 1]

        col1, col2 = self.df.columns[5:16][selected_column_indices]
        self.plot_scatter_plot(col1, col2)

class ChoroplethMap:

    def __init__(self, data_path, shapefile_path):
        """Initialize ChoroplethMap object."""
        
        self.df = pd.read_csv(data_path)
        # Data Cleaning 
        self.df.iloc[:, 2:] = self.df.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')
        self.df = self.df.replace('*', pd.NA)  # Replacing '*' with NaN
        self.df.iloc[:, 2:] = self.df.iloc[:, 2:].abs()  #
        self.df.fillna(self.df.mean(), inplace=True)

        self.shapefile_path = shapefile_path
        self.gdf = gpd.read_file(self.shapefile_path)
        self.selected_feature = None
        self.short_column_names = None

    def replace_state_names(self, replace_dict):
        """Replace state names in the DataFrame."""
        self.df['State/UT'] = self.df['State/UT'].replace(replace_dict)

    def randomly_select_columns(self, num_columns=15):
        """Randomly select columns from the DataFrame."""

        all_columns = self.df.columns[5:]  # Exclude the first five coloums as they are noy survey data
        self.short_column_names = random.sample(all_columns.tolist(), num_columns)

    def group_and_merge_data(self):
        """Group and merge data based on selected feature."""

        grouped_data = self.df.groupby('State/UT')[self.selected_feature].mean().reset_index()
        self.gdf = pd.merge(self.gdf, grouped_data, left_on='ST_NAME', right_on='State/UT', how='left')
        self.gdf = self.gdf.dropna(subset=[self.selected_feature])

    def plot_choropleth_map(self):
        """Plot choropleth map with value annotations."""
        
        colors = [(0, 0, 1), (1, 1, 1), (1, 0, 0)] # Defining the color gradient 
        cmap = LinearSegmentedColormap.from_list('custom', colors, N=256)
        fig, ax = plt.subplots(1, 1, figsize=(15, 10))
        self.gdf.plot(column=self.selected_feature, cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)


        for idx, row in self.gdf.iterrows():
            plt.annotate(
                text=f'{row[self.selected_feature]:.2f}',
                xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                xytext=(3, 3),  # Adjust the text offset
                textcoords='offset points',
                ha='center',
                fontsize=8
            )

    
        plt.title(f'{self.selected_feature} by State')
        plt.show()

    def execute_choropleth(self):
        """Execute the choropleth map visualization."""

        # This replacement was done to make state name in dataframe consistent with those in shapefile
        state_replace_dict = {
            'Maharastra': 'Maharashtra',
            'Odisha': 'Orissa',
            'Jammu & Kashmir': 'Jammu And Kashmir',
            'Andaman & Nicobar Islands': 'ANDAMAN AND NICOBAR ISLANDS',
            'NCT of Delhi': 'Nct Of Delhi'
        }

        self.replace_state_names(state_replace_dict)
        # Randomly select 15 columns for the user to choose from, it may be implemented statically as well
        self.randomly_select_columns(num_columns=15)
        print("Select a feature from the following:")
        for i, col in enumerate(self.short_column_names):
            print(f"{i + 1}. {col}")

        selected_column_index = int(input("Enter the index of the feature you want to visualize: ")) - 1
        self.selected_feature = self.short_column_names[selected_column_index]
        self.group_and_merge_data()
        self.plot_choropleth_map()
