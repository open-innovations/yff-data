---
title: QLFS data processing
url: /dashboard/qlfs/pipeline
---

There are three stages to the [data processing pipeline](https://github.com/open-innovations/yff-data/tree/main/scripts/qlfs), each being written in Python:

* extract: where we get a copy of the file from an appropriate source
* transform: where we convert it into a simpler form by selecting rows and filtering columns, and transforming formats to meet what we need
* prepare: where we build files which will directly drive our visualisations. These may be summarised or transposed data, or in a completely different format (e.g. JSON).

## Data sources

The sources for this are:

* [A06 SA: Educational status and labour market status for people aged from 16 to 24 (seasonally adjusted)](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/educationalstatusandlabourmarketstatusforpeopleagedfrom16to24seasonallyadjusteda06sa)
* [UNEM01 SA: Unemployment by age and duration (seasonally adjusted)](https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/unemploymentbyageanddurationseasonallyadjustedunem01sa)

The extract scripts find the latest Excel link from these pages and download them for transformation.

## A06 processing

For the A06 figures, the transform script extracts the following measures from the 'People' sheet (i.e. not split by Gender)

* `JN6B`: Total not in full-time education, 16-24, SA
* `AGNJ`: Employed level not in fte, 16-24, SA
* `AGOL`: Unemployed level not in fte, 16-24, SA
* `AGPM`: Economically inactive level not in fte, 16-24, SA
* `AIWI`: Employed rate not in fte, 16-24, SA
* `AIXT`: Unemployed rate not in fte, 16-24, SA
* `AIYU`: Economically inactive rate not in fte, 16-24, SA

We then discard quarters that do not start with Jan, Apr, Jul and Oct. The selected quarters are based on alignment with NEET stats, but could also take the most recent months figures as a baseline and work back from there. We also convert the quarter from a string to the date representing the start of the quarter (e.g. Jan-Mar 2023 is converted to a proper datetime object at 1-Jan-2023)

Finally, we filter to the latest 3 years (easily configurable) values, before saving to a [CSV of unemployment for people not in full-time education](https://github.com/open-innovations/yff-data/blob/main/data/qlfs/not_in_education.csv) file for further processing.

## UNEM01 processing

UNEM01 processing is similar, with the following alterations:

We extract the levels of unemployment and unemployment over 12 months as well as the rate for both ages 16-17 and age 18-24.

* `YBVH`: Age 16 to 17 unemployed level, SA
* `YBXJ`: Age 16 to 17 unemployed over 12 months level, SA
* `YBXM`: Age 16 to 17 unemployed over 12 months rate, SA
* `YBVN`: Age 18 to 24 unemployed level, SA
* `YBXY`: Age 18 to 24 unemployed over 12 months level, SA
* `YBYB`: Age 18 to 24 unemployed over 12 months rate, SA

We extract and convert the quarters as described above, and then combine the unemployment total and over 12 months levels across the two age ranges to come up with an aggregated figure from 16-24. We then calculate the resulting rate by simple division.

Finally, we save the last three years to a [CSV of long-term unemployment data](https://github.com/open-innovations/yff-data/blob/main/data/qlfs/not_in_education.csv) as before.
