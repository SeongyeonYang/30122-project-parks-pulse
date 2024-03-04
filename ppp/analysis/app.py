import webbrowser
import os
import pathlib

ana_filepath = pathlib.Path(__file__).parent
vis_filepath = pathlib.Path(__file__).parent.parent / "analysis/visualizations/"


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
                <div style="display: flex; justify-content: center;">
                    <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                        <img src="{vis_filepath}/Total Fire Occurrences Trend Over the Years of All Parks.png" alt="Climate Spending and Visitation Graph" style="width: 50%; height: auto;">
                    <figcaption>Figure 1. Total Fire Occurrences Trend Over the Years</figcaption>
                    </figure>
                </div>
            <p>Fire occurrences see an overall declining trend over the 10-year period (2011-2022), peaking in 2014 with roughly 120 fires occurred in national parks before decreasing to 77 fires in 2022. 
            While not shown on this graph, we find that while the size of fires does not necessarily trace this trend, fluctuating with no clear patterns, the overall acres burnt across all parks did take on a downward turn from 2011 to 2022. 
            These patterns seem to be tracing the global trends of declining global areas burned by wildfire. It is difficult to quantify whether this is good or bad however, considering how fires could have mixed impact on parks, its inhabitants, and the local communities that surround them.</p>
                <div style="display: flex; justify-content: center;">
                    <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                        <img src="{vis_filepath}/Average Temperature Over Years by Region.png" alt="Descriptive Statistics Graph" style="width: 60%; height: auto;">
                    <figcaption>Figure 2. Average Temperature Growth Rate Over the Years by Region</figcaption>
                    </figure>                
                </div>
            <p>Region-wise, while there is no clear pattern for the most part (attributable to too short a timeframe of observation), we could see a general increase in temperature in parks across different regions. 
            Most notably, Alaska shows significant increase of almost 10% since 2011 (most pronounced is Denali National Park, though not shown in the figure). 
            This suggests how geographical properties could lead to parks being affected disproportionately by climate change, how Alaska stands at the forefront of global warming, and how parks are especially sensitive to it.</p>
                <div style="display: flex; justify-content: center;">
                    <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                        <img src="{vis_filepath}/Precipitation Sum Over Years for Each Park.png" alt="Descriptive Statistics Graph" style="width: 60%; height: auto;">
                    <figcaption>Figure 3. Precipitation Sum Over the Years for Each Park</figcaption>
                    </figure>                 
                </div>
            <p>American Samoa National Park experiences a surge in precipitation/rainfall throughout the period observed of just 10 years. 
            This radical change in rain patterns within national parks are especially indicative of how the area as a whole is impacted by climate change, and has great implications on how the communities in it could be put at risk (in this case: rising sea level, flooding… that affect coastal resilience of the park and its inhabitants alike).</p>
                <div style="display: flex; justify-content: center;">
                    <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                        <img src="{vis_filepath}/Yearly Trends in National Park Visitation and Spending (2011-2022).png" alt="Descriptive Statistics Graph" style="width: 50%; height: auto;">
                    <figcaption>Figure 4. Yearly Trends in National Park Visitation and Spending</figcaption>
                    </figure> 
                </div>

                <div style="display: flex; justify-content: center;">
                    <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                        <img src="{vis_filepath}/Correlation Matrix of Visitation, Spending, and Climate Variables (2011-2022).png" alt="Descriptive Statistics Graph" style="width: 60%; height: auto;">
                    <figcaption>Figure 5. Correlation Matrix of Visitation, Spending, and Climate Variables</figcaption>
                    </figure> 
                </div>
            <p>The graph shows the changes in the number of visitors to national parks from 2011 to 2022 seems to follow budget spent on parks for corresponding years. 
            There appears to be a general upward trend in visitation, suggesting an increasing interest in national parks. This could be due to various factors, such as the rising popularity of outdoor activities, improvements in park accessibility, or enhanced awareness and promotion of national parks. Like visitation trend, spending also shows an upward trajectory, which likely correlates with the increase in visitors, which is shown in the correlation heatmap.
            When comparing the averages from 2020-2022 with those before 2020, we see a post-pandemic surge in visitation never seen before at national parks, peaking in 2021 with over 9.1 million visits across all parks.</p>            
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
            <div style="display: flex; justify-content: center;">
                <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                    <img src="{vis_filepath}/regression_plot.png" alt="Descriptive Statistics Graph" style="width: 70%; height: auto;">
                <figcaption>Figure 6. Partial Regression Plot: DMR, Visitation and Spending</figcaption>
                </figure> 
            </div>
            <p>Noticing an interesting correlation between deferred maintenance and repairs (DMR) and visitation, we ran a regression analysis of DMR on visitation across parks, controlling for spending. The model’s variables are able to explain 66.2% of the variation in DMR in parks. Using log-log regression, we are able to interpret the result such that an increase of 1% in visitation is associated with an 0.38% increase in DMR, controlling for spending (statistically significant). 
            Because DMR is closely tied with visits to parks and can have important implications to parks’ state (for example, surges in visit can expose parks to downgraded facilities and impairment that could interfere with its ecosystem), this could be useful in assessing the problem of overcrowding at parks, how park infrastructures could be put at risk, and how budget allocation could be calibrated based on individual parks’ rate of increase in visitation.</p>
            
        </section>
        
        <section>
            <h2>3. Factor Analysis</h2>
            <p>The index was constructed using factor analysis method, where variables’ common variance is examined to identify the optimally weighted linear combination of factors. 
            As dimensions/variables are reduced, an aggregate score is produced based on these weighted factors to describe different aspects of the dataset.</p>
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
            <p>The table outlines the index assigned to each park, as determined by the combination of nine out of twelve variables that we deem indicative of parks’ health, such as average temperature increase, acres burned from wildfire, wildfire count, proportion of water waste system over total facilities, deferred maintenance, etc. 
            The model’s five factors that come out of these variables is able to explain 61.25% of variability in the original dataset.</p>
            <div style="display: flex; justify-content: center;">
                <figure style="text-align: center; margin-left: auto; margin-right: auto;">
                    <img src="{vis_filepath}/2015_Average Composite Index among Regions.png" alt="Factor Analysis Graph" style="width: 70%; height: auto;">
                    <figcaption>Figure 7. Average Composite Index among Regions in 2015</figcaption>
                </figure>
            </div>
            
            <p>A few interesting observations: Highest score average goes to the Pacific West region where most of the well-known and well-funded parks are. Alaska has the lowest average composite scores across parks, most likely due to significant climate change impact. 
            In addition, parks with high popularity seem to have high scores (which we know to be typically associated with more budget).</p>
            
        </section>
        
        <section>
        <h2>Conclusion</h2>
        <p>We see that how overcrowding and downgraded infrastructure have considerable implication to parks’ wellbeing and not just visitors’ enjoyment, all caused by DMR.</p>
        <p>Climate change generally not reflected per parks over short period of time, but we see that some parks located at certain areas are impacted more severely than others. 
        More attention should be drawn to these, as it not only affects parks’ well-being, but also the local community that surrounds it.</p>
        <p>Parks scores are fairly distributed across regions. We see lowest score for Alaska (though not by a significant amount of difference with other regions). 
        More analysis can be done to identify potential issues other than climate change there.</p>
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
    
    
