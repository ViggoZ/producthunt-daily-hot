
# Product Hunt Daily Hot List

[English](README.en.md) | [中文](README.md)

![License](https://img.shields.io/github/license/ViggoZ/producthunt-daily-hot) ![Python](https://img.shields.io/badge/python-3.x-blue)

Product Hunt Daily Hot is a GitHub Action-based automation tool that generates a daily Markdown file summarizing the top products from Product Hunt and automatically commits it to a GitHub repository. The project aims to help users quickly view the daily Product Hunt leaderboard and provide more detailed product information.

 [🌐 View here](https://decohack.com/category/producthunt/https://decohack.com/category/producthunt/).

## Preview

![Preview](./preview.gif)

## Features

- **Automated Data Retrieval**: Automatically retrieves the top 30 products from Product Hunt from the previous day.
- **Keyword Generation**: Generates easy-to-understand Chinese keywords to help users better understand the product content.
- **High-Quality Translation**: Uses OpenAI's GPT-4 model to perform high-quality translations of product descriptions.
- **Markdown File Generation**: Generates Markdown files containing product data, keywords, and translated descriptions, which can be easily published on websites or other platforms.
- **Daily Automation**: Automatically generates and commits the daily Markdown file via GitHub Actions.
- **Configurable Workflow**: Supports manual triggering or scheduled generation via GitHub Actions.
- **Flexible Customization**: The script is easy to extend or modify to include additional product details or adjust the file format.

## Getting Started

### Prerequisites

- Python 3.x
- GitHub account and repository
- OpenAI API Key
- Product Hunt API credentials

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/ViggoZ/producthunt-daily-hot.git
cd producthunt-daily-hot
```

2. **Install Python dependencies:**

Ensure you have Python 3.x installed. Then, install the required packages:

```bash
pip install -r requirements.txt
```

### Setup

1. **GitHub Secrets:**

   Add the following secrets to your GitHub repository:

   - `OPENAI_API_KEY`: Your OpenAI API key.
   - `PRODUCTHUNT_CLIENT_ID`: Your Product Hunt API client ID.
   - `PRODUCTHUNT_CLIENT_SECRET`: Your Product Hunt API client secret.
   - `PAT`: Personal Access Token for pushing changes to the repository.

2. **GitHub Actions Workflow:**

   The workflow is defined in `.github/workflows/generate_markdown.yml`. It runs daily at 08:01 UTC (16:01 Beijing Time) and can also be manually triggered.

### Usage

Once set up, the GitHub Action will automatically generate and commit a Markdown file each day with the top products from Product Hunt. These files are stored in the `data/` directory.

### Customization

- Modify `scripts/product_hunt_list_to_md.py` to customize the format or add additional content.
- Adjust the schedule in `.github/workflows/generate_markdown.yml` if needed.

### Example Output

The generated files are stored in the `data/` directory. Each file is named in the format `PH-daily-YYYY-MM-DD.md`.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
