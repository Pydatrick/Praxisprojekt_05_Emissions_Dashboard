# Global aviation demand, energy efficiency and CO₂ emissions - Data package

This data package contains the data that powers the chart ["Global aviation demand, energy efficiency and CO₂ emissions"](https://ourworldindata.org/grapher/aviation-demand-efficiency?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website.

## CSV Structure

The high level structure of the CSV file is that each row is an observation for an entity (usually a country or region) and a timepoint (usually a year).

The first two columns in the CSV file are "Entity" and "Code". "Entity" is the name of the entity (e.g. "United States"). "Code" is the OWID internal entity code that we use if the entity is a country or region. For normal countries, this is the same as the [iso alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) code of the entity (e.g. "USA") - for non-standard countries like historical countries these are custom codes.

The third column is either "Year" or "Day". If the data is annual, this is "Year" and contains only the year as an integer. If the column is "Day", the column contains a date string in the form "YYYY-MM-DD".

The remaining columns are the data columns, each of which is a time series. If the CSV data is downloaded using the "full data" option, then each column corresponds to one time series below. If the CSV data is downloaded using the "only selected data visible in the chart" option then the data columns are transformed depending on the chart type and thus the association with the time series might not be as straightforward.

## Metadata.json structure

The .metadata.json file contains metadata about the data package. The "charts" key contains information to recreate the chart, like the title, subtitle etc.. The "columns" key contains information about each of the columns in the csv, like the unit, timespan covered, citation for the data etc..

## About the data

Our World in Data is almost never the original producer of the data - almost all of the data we use has been compiled by others. If you want to re-use data, it is your responsibility to ensure that you adhere to the sources' license and to credit them correctly. Please note that a single time series may have more than one source - e.g. when we stich together data from different time periods by different producers or when we calculate per capita metrics using population data from a second source.

### How we process data at Our World In Data
All data and visualizations on Our World in Data rely on data sourced from one or several original data providers. Preparing this original data involves several processing steps. Depending on the data, this can include standardizing country names and world region definitions, converting units, calculating derived indicators such as per capita measures, as well as adding or adapting metadata such as the name or the description given to an indicator.
[Read about our data pipeline](https://docs.owid.io/projects/etl/)

## Detailed information about each time series


## Passenger demand (billion passenger-km)
Passenger demand for aviation, measured in billions passenger-kilometers.
Last updated: March 19, 2024  
Date range: 1990–2021  
Unit: billion-kilometers  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World in Data

#### Full citation
Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World in Data. “Passenger demand (billion passenger-km)” [dataset]. Bergero et al. (2023). Pathways to net-zero emissions from aviation., “aviation_emissions_bergero” [original data].
Source: Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World In Data

### What you should know about this data

### Source

#### Bergero et al. (2023). Pathways to net-zero emissions from aviation. – aviation_emissions_bergero
Retrieved on: 2024-03-19  
Retrieved from: https://www.nature.com/articles/s41893-022-01046-9  


## Freight demand (million-ton km)
Freight demand for aviation, measured in million-ton kilometers.
Last updated: March 19, 2024  
Date range: 1990–2021  
Unit: million-ton kilometers  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World in Data

#### Full citation
Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World in Data. “Freight demand (million-ton km)” [dataset]. Bergero et al. (2023). Pathways to net-zero emissions from aviation., “aviation_emissions_bergero” [original data].
Source: Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World In Data

### What you should know about this data

### Source

#### Bergero et al. (2023). Pathways to net-zero emissions from aviation. – aviation_emissions_bergero
Retrieved on: 2024-03-19  
Retrieved from: https://www.nature.com/articles/s41893-022-01046-9  


## Energy intensity (per passenger-km)
Energy intensity of aviation, measured as megajoules of energy per passenger-kilometer.
Last updated: March 19, 2024  
Date range: 1990–2021  
Unit: MJ per passenger-km  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World in Data

#### Full citation
Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World in Data. “Energy intensity (per passenger-km)” [dataset]. Bergero et al. (2023). Pathways to net-zero emissions from aviation., “aviation_emissions_bergero” [original data].
Source: Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World In Data

### What you should know about this data

### Source

#### Bergero et al. (2023). Pathways to net-zero emissions from aviation. – aviation_emissions_bergero
Retrieved on: 2024-03-19  
Retrieved from: https://www.nature.com/articles/s41893-022-01046-9  


## CO₂ per unit energy (gCO₂eq per MJ)
The amount of CO2 emitted per megajoule of energy used for aviation.
Last updated: March 19, 2024  
Date range: 1990–2021  
Unit: grams CO2e per MJ  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World in Data

#### Full citation
Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World in Data. “CO₂ per unit energy (gCO₂eq per MJ)” [dataset]. Bergero et al. (2023). Pathways to net-zero emissions from aviation., “aviation_emissions_bergero” [original data].
Source: Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World In Data

### What you should know about this data

### Source

#### Bergero et al. (2023). Pathways to net-zero emissions from aviation. – aviation_emissions_bergero
Retrieved on: 2024-03-19  
Retrieved from: https://www.nature.com/articles/s41893-022-01046-9  


## CO₂ intensity (gCO₂ per passenger-km)
The carbon intensity of aviation, measured as the amount of the CO2 emitted per passenger-kilometer.
Last updated: March 19, 2024  
Date range: 1990–2021  
Unit: grams CO2 per passenger-km  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World in Data

#### Full citation
Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World in Data. “CO₂ intensity (gCO₂ per passenger-km)” [dataset]. Bergero et al. (2023). Pathways to net-zero emissions from aviation., “aviation_emissions_bergero” [original data].
Source: Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World In Data

### What you should know about this data

### Source

#### Bergero et al. (2023). Pathways to net-zero emissions from aviation. – aviation_emissions_bergero
Retrieved on: 2024-03-19  
Retrieved from: https://www.nature.com/articles/s41893-022-01046-9  


## CO₂ emissions (billion tonnes)
Carbon dioxide emissions from aviation, without altitude impacts included.
Last updated: March 19, 2024  
Date range: 1990–2021  
Unit: billion tonnes  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World in Data

#### Full citation
Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World in Data. “CO₂ emissions (billion tonnes)” [dataset]. Bergero et al. (2023). Pathways to net-zero emissions from aviation., “aviation_emissions_bergero” [original data].
Source: Bergero et al. (2023). Pathways to net-zero emissions from aviation. – processed by Our World In Data

### What you should know about this data

### Source

#### Bergero et al. (2023). Pathways to net-zero emissions from aviation. – aviation_emissions_bergero
Retrieved on: 2024-03-19  
Retrieved from: https://www.nature.com/articles/s41893-022-01046-9  


    