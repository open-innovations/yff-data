---
title: CPI data processing
url: /dashboard/cpi/pipeline/
---

There are four stages to the [data processing pipeline](https://github.com/open-innovations/yff-data/tree/main/scripts/cpi), each being written in Python:

* extract: where we get a copy of the file from an appropriate source
* transform: where we convert it into a simpler form by selecting rows and filtering columns, and transforming formats to meet what we need
* prepare: where we build files which will directly drive our visualisations. These may be summarised or transposed data, or in a completely different format (e.g. JSON).
* vis: where we update the axis labels and minimum/maximum values to fit the data nicely.
## Data sources

The source for this is:

* [MM23: Consumer Price Inflation Time Series](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/consumerpriceindices)

The extract scripts find the latest Excel link from these pages and download them for transformation. However, increasingly we are moving to using
[EDD](https://github.com/economic-analytics/edd/tree/main/data/csv) to source the datasets (since they have been transformed into a consitent format) and DVC remote url to download them. In the CPI pipeline, the extract script is no longer used, and will be removed in the near future.

## CPI processing

For the CPI figures, the transform script extracts the following measures:

* `D7BT`: All CPI Categories
* `D7BU`: Food and non-alcoholic beverages
* `D7BV`: Alcoholic beverages and tobacco
* `D7BW`: Clothing and footwear
* `D7BX`: Housing, water, electricity, gas and other fuels
* `D7BY`: Furniture, household equipment and maintenance
* `D7BZ`: Health
* `D7C2`: Transport
* `D7C3`: Communication
* `D7C4`: Recreation and culture
* `D7C5`: Education
* `D7C6`: Restaurants and hotels
* `D7C7`: Miscellaneous goods and services 

Here, percentage change shows by how much the cosumer price index has increased relative to the price last month, quarter and year. To calculate percentage changes we take the most recent month's index value (the last line in the file), subtract the previous month/quarter/year's value, divide by that same value, and multiply by 100. As an equation this can be written as (current-previous / previous)*100. The result is rounded to one decimal place. 

Separately, we also compare this to the same set of values from the previous update (usually last month) to determine whether it has increased or decreased relative to the last update.

We explicitly indicate the sign to show if the percentage change is an positive or negative. A positive percentage change means the cost of goods is rising, and negative change means the cost of goods is falling.

&dagger;The youth-focused average is a mean average of the index for four categories most-affecting young people: Food and Non-Alcoholic Beverages (D7BU), Housing and fuels (D7BX), Transport (D7C2), and Recreation and Culture (D7C4). These are the top 4 categories which people under 30 spend their money on weekly, calculated from the ONS dataset <a href="https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/familyspendingworkbook1detailedexpenditureandtrends">Family spending workbook 1: detailed expenditure and trends</a>. 

For the line chart, we take monthly data for the past 10 years from the most recent release date. 

Finally, we save [CSV files](https://github.com/open-innovations/yff-data/blob/main/data/cpi/) to drive our visualisations.
