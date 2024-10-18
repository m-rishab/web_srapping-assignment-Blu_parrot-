# Otipy Product Scraper

## Overview

This project implements a web scraper using Selenium to extract product information from the Otipy website, specifically targeting the vegetables category. The scraped data includes product names, standard prices, selling prices, MRP, and quantities.

## Features

- **Headless Browsing**: Utilizes headless mode for Firefox to run the browser in the background.
- **Human-like Scrolling**: Mimics human behavior while scrolling through the webpage to load more products.
- **Data Cleaning**: Cleans and formats the product prices to remove currency symbols and unnecessary text.
- **JSON Output**: Saves the scraped product data into a `products.json` file.

## Requirements

- Python 3.x
- Selenium
- Firefox WebDriver
- Required Python packages:
  - `selenium`
  - `json`
  - `logging`
  - `re`

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

