# Agentic Reports

## A Comprehensive Python Library for Generating Research Reports

Welcome to Agentic Reports, a Python library designed to simplify the process of generating comprehensive research reports. This library leverages the power of FastAPI, Pydantic, Pandas, and Exa to provide users with an efficient and streamlined way to create detailed reports based on various data sources.

### Technical Overview

Agentic Reports utilizes `report_generator.py` in conjunction with `endpoints.py` to facilitate the generation of detailed reports. The `report_generator.py` module is responsible for processing user queries and generating subqueries, which are then passed to `endpoints.py`. This module interacts with external APIs and databases to gather the necessary data, which is then compiled into a comprehensive report.

### How to Install

To install Agentic Reports, simply use pip:

```bash
pip install agentic-reports
```

This command will install the library and all its dependencies, making it ready for use in your projects.

### API Reference

Agentic Reports provides several endpoints for generating reports and processing data:

- **/generate-report**: Generates a comprehensive report based on a given topic.
  - Parameters: `topic` (string)
  - Example Request: `{"topic": "Latest AI advancements"}`
  
- **/generate-subqueries**: Generates subqueries from a given topic for detailed analysis.
  - Parameters: `topic` (string), `num_subqueries` (int)
  - Example Request: `{"topic": "Latest AI advancements", "num_subqueries": 5}`
  
- **/search-subqueries**: Searches for information based on provided subqueries.
  - Parameters: `subqueries` (list of strings)
  - Example Request: `{"subqueries": ["AI in healthcare", "AI in finance"]}`
  
- **/advanced-search**: Performs an advanced search with customizable parameters.
  - Parameters: `query` (string), `start_published_date` (string), `end_published_date` (string), etc.
  - Example Request: `{"query": "AI", "start_published_date": "2021-01-01", "end_published_date": "2021-12-31"}`
  
- **/find-similar-links**: Finds similar links to a provided URL.
  - Parameters: `url` (string), `num_results` (int)
  - Example Request: `{"url": "https://cnn.com", "num_results": 10}`

### Advanced Uses

Agentic Reports can be used in a variety of advanced scenarios, such as:

- Automated generation of research papers and articles.
- Data analysis and visualization for business intelligence.
- Custom report generation for specific industries or topics.

### Features

- **AI-Driven Report Generation**: Utilizes advanced AI models to generate detailed and accurate reports.
- **Comprehensive Data Analysis**: Leverages Exa's search capabilities and Pandas for data manipulation.
- **Customizable Reports**: Offers flexibility in report generation to meet specific user needs.

For more information on how to use Agentic Reports and its capabilities, please refer to the official documentation.