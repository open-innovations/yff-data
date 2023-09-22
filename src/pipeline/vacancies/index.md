---
title: Vacancies data processing
url: /dashboard/vacancies/pipeline/
---

There are three stages to the [data processing pipeline](https://github.com/open-innovations/yff-data/tree/main/scripts/vacancies), each being written in Python:

* extract: where we get a copy of the file from an appropriate source
* transform: where we convert it into a simpler form by selecting rows and filtering columns, and transforming formats to meet what we need
* prepare: where we build files which will directly drive our visualisations. These may be summarised or transposed data, or in a completely different format (e.g. JSON).

## Data sources

The sources for this release are:

* [VACS01 SA: Vacancies and unemployment (seasonally adjusted)](https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/vacanciesandunemploymentvacs01)
* [VACS02 SA: Vacancies by industry (seasonally adjusted)](https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/vacanciesbyindustryvacs02)

These datasets are taken from our own Economic Data Dashboard (EDD) repository, created and managed by Christian Spence, that automatically extracts labour market statistics as they are released and processes them into a single CSV extract.

## VACS01 processing

For the VACS01 figures, the transform script extracts the following variable from the EDD extract:

* `AP2Y`: all vacancies (thousands), SA

We then we save a [CSV of estimated vacancies by quarter](https://github.com/open-innovations/yff-data/blob/main/src/_data/sources/vacancies/quarterly_vacancies.csv) and [another CSV by rolling 3-month period](https://github.com/open-innovations/yff-data/blob/main/src/_data/sources/vacancies/monthly_vacancies.csv) for visualisation on [the vacancies dashboard](https://data.youthfuturesfoundation.org/dashboard/vacancies/).

## VACS02 processing

VACS02 processing is similar, with the following alterations:

From the EDD extract, we query the following measures for each sector:

*   `JP9H`: mining and quarrying, SA 
*   `JP9J`: electricity gas steam and air conditioning supply, SA
*   `JP9K`: water supply sewerage waste and remediation services, SA
*   `JP9L`: construction, SA  
*   `JP9M`: wholesale and retail trade repair of motor vehicles and motor cycles, SA 
*   `JP9N`: transport and storage, SA  
*   `JP9O`: accommodation and food service activities, SA  
*   `JP9P`: information and communication, SA  
*   `JP9S`: professional scientific and technical activities, SA  
*   `JP9T`: administrative and support service activities, SA  
*   `JP9U`: public admin and defence compulsory social security, SA  
*   `JP9Q`: financial and insurance activities, SA  
*   `JP9V`: education, SA  
*   `JP9W`: human health and social work activities, SA  
*   `JP9X`: arts entertainment and recreation, SA  
*   `JP9Y`: other service activities, SA  
*   `JP9Z`: total services, SA  

Quarterly values are extracted for these measures and saved as a [CSV file of all vacancies by sector](https://github.com/open-innovations/yff-data/blob/main/data/vacancies/vacancies_by_sector.csv).  

In the Prepare script, these sectors are broken down further and saved as separate CSV files that are used to power the visualisations on [the vacancies dashboard](https://data.youthfuturesfoundation.org/dashboard/vacancies/). 

The sector groupings are below:

All sectors (as above)

Key sectors for young people (where young people are most likely to work): 

*   `JP9X`: arts entertainment and recreation, SA  
*   `JP9O`: accommodation and food service activities, SA  
*   `JP9W`: human health and social work activities, SA 
*   `JP9V`: education, SA  
*   `JP9M`: wholesale and retail trade repair of motor vehicles and motor cycles, SA 

Sectors targeted by young people (where young people want to work): 

*   `JP9S`: professional scientific and technical activities, SA  
*   `JP9Q`: financial and insurance activities, SA  

## Headline statistics 

The above datasets are summarised by the following methods. 

* Rolling 3-month vacancies estimates are taken from VACS01 
* Growth on previous quarter is calculated from AP2Y (VACS01) as the 'change on previous non-overlapping three month rolling average time period' for all sectors 



