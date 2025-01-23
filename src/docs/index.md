---
title: Data site overview
---

This page outlines the process by which the [YFF Data Dashboard](/) site is built.

## Overview

There are three stages to the overall build:

1. Open data is retrieved from various sources and stored in a standardised format.
   Some automated data processing is also completed based on models created by YFF and
   their partners / suppliers.
2. The data is taken from this collection and prepared ready to build the visualisations.
3. The site is built based on this and other data, templates, assets and configuration.

![](/assets/images/yff-overview.png)

## Data pipelines

The first part of the data processing takes place in the
[`yff-data-pipelines` GitHub repo](https://github.com/open-innovations/yff-data-pipelines).
Data is ultimately written to appropriate directories in the
[`yff-data` GitHub repo](https://github.com/open-innovations/yff-data).

In either case, scripts are written in Python / Jupyter, and stored in the `/pipelines`
or `/scripts` folders.
The stages are orchestrated using [DVC](https://dvc.org), with pipeline defintions being
stored in dvc.yml files close to the source code.

### Extract

Data is automatically extracted from a series of open data source systems:

* ONS: LMS, CPI, Unemployment, Vacancy
* NOMIS: Census data, Population estimates
* Explore Education Statistics service: Education attainment at KS4, 16-18 destinations
* NEET analysis
* OECD: International comparison data

### Transform

These are transformed into a 'melted' format, comprising one value on each row, along with
any dimensions (e.g. geography, gender, age range, measurement, etc).

Some transformed data (e.g. NEET Factors analysis) is synthesised from a model combining
multiple datasets in a weighted matrix. These models have been automated from prior
analysis conducted by YFF or their partners / suppliers.

### Prepare

Data is then prepared for visualisation within the
[GitHub source code repository for this site](https://github.com/open-innovations/yff-data).
This is largely a case of extracting data from the large transformed datasets, potentially
filtering and summarising that data, and reshaping to a form that can be used to build
the visualisations.
The prepare stages are responsible for filtering and summarising the data stored in the top-level upstream repository. These scripts typically output data into [a _data folder](https://lume.land/docs/creating-pages/shared-data/#the-_data-directories) in the site source so that they can be made available as build context.

The data is structured in ways appropriate to drive site generation.

### Scheduling

Data pipelines run Monday to Friday at 7:50 AM (UTC)in the
`yff-data-pipelines` repository.
This means that whenever new data is published, it will be downloaded and transformed by
the pipeline processes.
Any change in the repository as a result of the pipeline processing will trigger a data
pipeline run in the `yff-data` (main site) repo, which will in turn prepare the data and
rebuild the site.
In that way, the site will be updated within a short period of an open data source being
published. Assuming data is live by 7:50, it _should_ be on the site by around 8:00 (9:00 during BST).

NB all times are expressed in UTC.
This will be the same as GMT, but jobs will run at 8:35 local time.

## Site build

The YFF data dashboard site has been created by combining data with templates and a library of visualisation components.
The build process is known as static site generation (SSG).
This means that the resulting site comprises simple HTML and CSS, with some Javascript optional progressive enhancement.
It is consequently easy to host, requiring only a simple web server, and is simpler to
manage than a site hosted on a CMS such as Wordpress.

The site is built using the [Lume static site generator](https://lume.land) software, with the site source comprising templates, components and other assets.

The resulting static HTML, CSS, JavaScript and assets are then deployed to a GitHub Pages site.

All prepared data, pipeline and site source code are tracked in the [`yff-data` GitHub repository](https://github.com/open-innovations/yff-data). Pipelines and site build execution uses GitHub Actions.

The content of the pages is derived directly from the templates. Any changes to this
content would need to be committed to the GitHub repository. This is typically coded in
Nunjucks templates, a templating language based on and which outputs HTML.
Some of the content is derived from data provided to the templates, so would need to be
updated in the data structures.