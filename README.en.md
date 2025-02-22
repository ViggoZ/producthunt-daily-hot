# Product Hunt Daily Hot List

[English](README.en.md) | [中文](README.md)

![License](https://img.shields.io/github/license/ViggoZ/producthunt-daily-hot) ![Python](https://img.shields.io/badge/python-3.x-blue)

Product Hunt Daily Hot is a GitHub Action-based automation tool that generates a daily Markdown file summarizing the top products from Product Hunt and automatically commits it to a GitHub repository. The project aims to help users quickly view the daily Product Hunt leaderboard and provide more detailed product information.

[🌐 View here](https://decohack.com/category/producthunt/).

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
- **Automatic Publishing to WordPress**: The generated Markdown files can be automatically published to a WordPress website.

## Getting Started

### Prerequisites

- Python 3.x
- GitHub account and repository
- OpenAI API Key
- Product Hunt Developer Token (obtained from Product Hunt Developer Settings)
- WordPress website and credentials (for automatic publishing)

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

   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PRODUCTHUNT_DEVELOPER_TOKEN`: Your Product Hunt Developer Token
   - `PAT`: Personal Access Token for pushing changes to the repository
   - `WORDPRESS_URL`: Your WordPress website URL
   - `WORDPRESS_USERNAME`: Your WordPress username
   - `WORDPRESS_PASSWORD`: Your WordPress password

2. **Get Product Hunt Developer Token:**

   1. Visit [Product Hunt Developer Settings](https://www.producthunt.com/v2/oauth/applications)
   2. Log in to your account
   3. Create a new application in the developer settings
   4. Obtain the Developer Token

3. **GitHub Actions Workflow:**

   The workflow is defined in `.github/workflows/generate_markdown.yml` and `.github/workflows/publish_to_wordpress.yml`. It runs daily at 07:01 UTC (15:01 Beijing Time) and can also be manually triggered.

### Usage

Once set up, the GitHub Action will automatically generate and commit a Markdown file each day with the top products from Product Hunt, and automatically publish it to your WordPress website. These files are stored in the `data/` directory.

### Customization

- Modify `scripts/product_hunt_list_to_md.py` to customize the format or add additional content.
- Adjust the schedule in `.github/workflows/generate_markdown.yml` if needed.

### Example Output

The generated files are stored in the `data/` directory. Each file is named in the format `PH-daily-YYYY-MM-DD.md`.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
