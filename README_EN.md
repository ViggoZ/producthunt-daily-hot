
# PH Daily Hot List - PH今日热榜

[中文版](README.md)

## Project Overview

PH Daily Hot List is an automated Python tool that leverages OpenAI's GPT-4 model to extract, generate keywords, and translate descriptions for the Top 30 products from Product Hunt of the previous day. This project aims to help users quickly view the daily Product Hunt hot list and provides more detailed product information.

## Features

- Automatically fetches the Top 30 products from Product Hunt of the previous day
- Generates concise and understandable Chinese keywords
- High-quality product description translation using OpenAI
- Generates daily hot list files in Markdown format, ready for publication on websites or other platforms

## How to Use

1. Clone this project locally
2. Create a `.env` file in the root directory of the project and add the following content:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   PRODUCTHUNT_CLIENT_ID=your_producthunt_client_id
   PRODUCTHUNT_CLIENT_SECRET=your_producthunt_client_secret
   ```
3. Run `python scripts/product_hunt_list_to_md.py` to generate the daily hot list file.

## Notes

- This project depends on the OpenAI API and Product Hunt API. You need to configure the relevant API keys.
- The generated Markdown files will be automatically saved to the `data` directory, with filenames in the format `PH-daily-YYYY-MM-DD.md`.

## Contribution

Feel free to submit issues and pull requests to improve this project.
