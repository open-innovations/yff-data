---
title: NEET data processing
url: /dashboard/neet/pipeline
---

There are three stages to the [data processing pipeline](https://github.com/open-innovations/yff-data/tree/main/scripts/neet), each being written in Python:

* extract: where we get a copy of the file from an appropriate source
* transform: where we convert it into a simpler form by selecting rows and filtering columns, and transforming formats to meet what we need
* prepare: where we build files which will directly drive our visualisations. These may be summarised or transposed data, or in a completely different format (e.g. JSON).

## Data sources

The sources for this are:

* [Young people not in education, employment or training (NEET)](https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/youngpeoplenotineducationemploymentortrainingneettable1)

The extract scripts find the latest Excel link from these pages and download them for transformation.

## Processing

We extract the following figures for 16-24 year olds:

* Young people who were NEET Total
* Young people who were NEET Unemployed
* Young people who were NEET Economically inactive
* Total people in relevant population group
* People who were NEET as a percentage of people in relevant population group

This processing is repeated for the `People - SA`, `Men - SA` and `Women - SA` sheets.

In each case we
* convert the quarter to a datetime object.
* renamed the columns

We then combine the three data sets into a single file, extract the most recent three years of data and save as a [NEET CSV file](https://github.com/open-innovations/yff-data/blob/main/data/neet/neet.csv).

