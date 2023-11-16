from my_module import DataAnalysis, ScatterPlotGenerator, ChoroplethMap
import os


def project_heading():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clearing the screen
    print("*" * 130)
    print("*" + " " * 40 + "National Health Data Analysis Project" + " " * 40)
    print("*" + " " * 40 + "Made By: Major Vaibhav Mishra" + " " * 40)
    print("*" * 130)


if __name__ == "__main__":
    csv_path = './Data/datafile.csv'
    output_folder = './output'

    data_analysis = DataAnalysis(csv_path, output_folder)
    choropleth_map = ChoroplethMap(csv_path, './Data/INDIA.shp')
    scatter_plot_generator = ScatterPlotGenerator(csv_path)  # Create an instance of ScatterPlotGenerator

    while True:
        project_heading()

        user_input = input("Enter Respective Digits to Analyze \n\n"
                           "\n1 Sex Ratios Analysis\n"
                           "\n2 Alcohol Consumption Analysis\n"
                           "\n3 Blood Pressure Analysis\n"
                           "\n4 Data on Choropleth Map With 15 Options\n"
                           "\n5 Scatter Plot : Select your own coloumn\n"  # Add an option for Scatter Plot
                           "\nEnter 'Exit' to quit: \n")

        if user_input.lower() == 'exit':
            print("Thank You")
            break

        if user_input == '1':
            data_analysis.analyze_sex_ratios()
        elif user_input == '2':
            data_analysis.analyze_alcohol_consumption()
        elif user_input == '3':
            data_analysis.analyze_blood_pressure()
        elif user_input == '4':
            choropleth_map.execute_choropleth()
        elif user_input == '5':  # Handle scatter plot option
            scatter_plot_generator.execute_scatter_plot()
        else:
            print("Invalid input. Please enter either 1, 2, 3, 4, or 5.")
