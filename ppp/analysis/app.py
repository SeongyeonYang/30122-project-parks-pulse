import webbrowser
import os
import pathlib

ana_filepath = pathlib.Path(__file__).parent
vis_filepath = pathlib.Path(__file__).parent.parent / "analysis/visualizations/"
print(ana_filepath)
print(vis_filepath)

def generate_html():
    regression_summary = f'{vis_filepath}/regression_summary.txt'
    with open(regression_summary, 'r') as file:
        regression_content = file.read()
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>[Capp30122 Project: Project-Parks-Pulse] - Analysis</title>
    </head>
    <body>
        <h1>[Capp30122 Project: Project-Parks-Pulse] - Analysis</h1>
        
        <section id="introduction">
            <h2>Introduction</h2>
            <p>
This project aims to analyze the U.S. National Parks System (NPS) and other open-sourced datasets to construct a composite measure of individual parks’ health status, 
called the Park Health Index (PHI). To compute PHI, we will examine and assign appropriate weight to different aspects of a park’s current state, including park usage, climate data, park management, and hazards. 
From individual time series data by parks unit, we are also interested in exploring trends in visitation and impact of climate change among parks over 10 years (2011-2022).
Our analysis unfolds in three main sections: </p> 
            <ol type=1>
                <li> Trend and Correlation Analysis: Providing a snapshot of park characteristics.</li> 
                <li> Regression Analysis: Exploring the relationship between DMR, visitation, and spending. </li> 
                <li> Factor Analysis: Identifying underlying factors that influence park health.</li> 
            </ol>
        </section>
        
        <section>
            <h2>1. Trend and Correlation Analysis</h2>
            <p>Some text for analysis...</p>
                <div style="display: flex; justify-content: center;">
                    <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                        <img src="{vis_filepath}/Total Fire Occurrences Trend Over the Years of All Parks.png" alt="Climate Spending and Visitation Graph" style="width: 50%; height: auto;">
                    <figcaption>Figure 1. Total Fire Occurrences Trend Over the Years</figcaption>
                    </figure>
                </div>
            <p>Some text for analysis...</p>
                <div style="display: flex; justify-content: center;">
                    <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                        <img src="{vis_filepath}/Average Temperature Over Years by Region.png" alt="Descriptive Statistics Graph" style="width: 60%; height: auto;">
                    <figcaption>Figure 2. Average Temperature Growth Rate Over the Years by Region</figcaption>
                    </figure>                
                </div>
            <p>Some text for analysis...</p>
                <div style="display: flex; justify-content: center;">
                    <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                        <img src="{vis_filepath}/Precipitation Sum Over Years for Each Park.png" alt="Descriptive Statistics Graph" style="width: 60%; height: auto;">
                    <figcaption>Figure 3. Precipitation Sum Over the Years for Each Park</figcaption>
                    </figure>                 
                </div>
            <p>Some text for analysis...</p>
                <div style="display: flex; justify-content: center;">
                    <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                        <img src="{vis_filepath}/Yearly Trends in National Park Visitation and Spending (2011-2022).png" alt="Descriptive Statistics Graph" style="width: 50%; height: auto;">
                    <figcaption>Figure 4. Yearly Trends in National Park Visitation and Spending</figcaption>
                    </figure> 
                </div>
            <p>Some text for analysis...</p>
                <div style="display: flex; justify-content: center;">
                    <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                        <img src="{vis_filepath}/Correlation Matrix of Visitation, Spending, and Climate Variables (2011-2022).png" alt="Descriptive Statistics Graph" style="width: 60%; height: auto;">
                    <figcaption>Figure 5. Correlation Matrix of Visitation, Spending, and Climate Variables</figcaption>
                    </figure> 
                </div>
        </section>
        
        <section>
            <h2>2. Regression Analysis</h2>

            <p>Some text for analysis...</p>
            <div style="display: flex; justify-content: center;">
                <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                    <pre>{regression_content}</pre>
                    <figcaption>Table 1. Regression Analysis Summary</figcaption>
                </figure> 
            </div>
            <p>Some text for analysis...</p>
            <div style="display: flex; justify-content: center;">
                <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                    <img src="{vis_filepath}/regression_plot.png" alt="Descriptive Statistics Graph" style="width: 70%; height: auto;">
                <figcaption>Figure 6. Partial Regression Plot: DMR, Visitation and Spending</figcaption>
                </figure> 
            </div>
        </section>
        
        <section>
            <h2>3. Factor Analysis</h2>
            <p>Here is the 5 national parks that have the highest index in 2015:</p>
            <table style="border-collapse: collapse; width: 60%; margin-left: auto; margin-right: auto;">
                <caption style="font-weight: bold; text-align: center; padding: 8px;">Table 2: Top 5 National Park by PHI in 2015</caption>
                <thead>
                    <tr>
                        <th style="border-bottom: 2px solid black; padding: 8px;">Park Name</th>
                        <th style="border-bottom: 2px solid black; padding: 8px;">Region</th>
                        <th style="border-bottom: 2px solid black; padding: 8px;">Factors 1</th>
                        <th style="border-bottom: 2px solid black; padding: 8px;">Factors 2</th>
                        <th style="border-bottom: 2px solid black; padding: 8px;">Factors 3</th>
                        <th style="border-bottom: 2px solid black; padding: 8px;">Factors 4</th>
                        <th style="border-bottom: 2px solid black; padding: 8px;">Factors 5</th>
                        <th style="border-bottom: 2px solid black; padding: 8px;">Composite Index</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Yellowstone</td>
                        <td>Intermountain</td>
                        <td>0.216</td>
                        <td>0.284</td>
                        <td>0.008</td>
                        <td>0.076</td>
                        <td>0.056</td>
                        <td>0.640</td>
                    </tr>
                    <tr>
                        <td>Grand Canyon</td>
                        <td>Intermountain</td>
                        <td>0.287</td>
                        <td>0.212</td>
                        <td>0.095</td>
                        <td>0.024</td>
                        <td>0.015</td>
                        <td>0.634</td>
                    </tr>
                    <tr>
                        <td>Glacier</td>
                        <td>Intermountain</td>
                        <td>0.323</td>
                        <td>0.096</td>
                        <td>0.146</td>
                        <td>0.000</td>
                        <td>0.011</td>
                        <td>0.575</td>
                    </tr>
                    <tr>
                        <td>Yosemite</td>
                        <td>Pacific West</td>
                        <td>0.178</td>
                        <td>0.271</td>
                        <td>0.014</td>
                        <td>0.067</td>
                        <td>0.041</td>
                        <td>0.571</td>
                    </tr>
                    <tr>
                        <td>Crater Lake</td>
                        <td>Pacific West</td>
                        <td>0.297</td>
                        <td>0.058</td>
                        <td>0.139</td>
                        <td>0.001</td>
                        <td>0.008</td>
                        <td>0.502</td>
                    </tr>
                </tbody>
                <tfoot>
                    <tr>
                        <td style="border-top: 2px solid black; padding: 8px;" colspan="8"></td>
                    </tr>
                </tfoot>
            </table>
            
            <div style="display: flex; justify-content: center;">
                <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                    <img src="{vis_filepath}/2015_Average Composite Index among Regions.png" alt="Factor Analysis Graph" style="width: 70%; height: auto;">
                    <figcaption>Figure 7. Average Composite Index among Regions in 2015</figcaption>
                </figure>
            </div>
            
            <p>Some text for analysis...</p>
            
        </section>
        
        <section>
        <h2>Conclusion</h2>
        <p>Some text for conclusion..</p>
        </section>

    </body>
    </html>
    """
    
    file_path = f'{ana_filepath}/analysis.html'
    # Writing HTML content to output.html
    with open(file_path, 'w') as html_file:
        html_file.write(html_content)
    print("HTML file has been generated successfully.")
    # Construct a file URI for the HTML file
    file_uri = f'file://{os.path.abspath(file_path)}'

    # Open the HTML file in the default web browser
    webbrowser.open(file_uri)
    
    
