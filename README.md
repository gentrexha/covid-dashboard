Covid Dashboard
==============================

## Introduction

- Dataset: COVID-19
  - Dataset sources:
  -COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University
  - ourworldindata.org/coronavirus - Data on COVID-19 (coronavirus) confirmed cases, deaths, and tests
- Preprocessing - only merging the data from both sources through iso3 country
codes.

## The Dashboard

![Picture of the dashboard](https://i.imgur.com/ad6hkPv.png)

Communication:
- Looking up COVID-19 Numbers on a Country/Region
- Dashboard can be used by anyone
- Dashboard is interactive

The dashboard was created using python framework Dash
- Easy to learn and use
- Flexible
- Open source
- Created and maintained by: Plotly

## Tasks

Based on date, type of case, continent, data transformation:
- Find country with highest cases/gdp per capita,
- Find out if this relationship changed over time

Also based on previous filters find out:

- Most cases in region/continent,
- historic data about country,
- top 20 countries with most cases, and
- see choropleth map of countries with most confirmed cases