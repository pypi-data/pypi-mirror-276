# Agentic Reports
## A Comprehensive Python Library for Generating Research Reports

Welcome to Agentic Reports, a Python library designed to simplify the process of generating comprehensive research reports. This library leverages the power of FastAPI, Pydantic, Pandas, and Exa to provide users with an efficient and streamlined way to create detailed reports based on various data sources.

### Technical Overview

Agentic Reports uses a multi-step process to deliver detailed research reports from a variety of sources:

1. **User Query Submission**: Users start by submitting a topic they wish to research. This can be done through a simple API request.

2. **Subquery Generation**: The system automatically generates a set of subqueries related to the main topic. These subqueries break down the broad topic into specific areas of focus, ensuring a comprehensive analysis.

3. **Data Collection**: Using the generated subqueries, the system searches for relevant information across various sources, including databases, external APIs, and other repositories. This step ensures the gathering of extensive and pertinent data.

4. **Data Compilation**: The collected data is compiled into a cohesive and structured report. The system organizes the information, providing detailed analysis, insights, and findings based on the initial topic and subqueries.

5. **Report Delivery**: The final report, complete with citations and data sources, is delivered back to the user in a well-organized format. This ensures that users receive a thorough and reliable resource for their research needs.

By following these steps, Agentic Reports provides users with a streamlined and efficient way to generate comprehensive research reports, making it an invaluable tool for in-depth analysis and information gathering.

### How to Install

To install Agentic Reports, simply use pip:

```bash
pip install agentic-reports
```

This command will install the library and all its dependencies, making it ready for use in your projects.

### How `Agentic Reports` Works

`Agentic Reports` is designed to make the process of generating detailed research reports seamless and user-friendly.

#### Step 1: Submitting a Topic

1. **Submit a Topic**: The user starts by submitting a topic they want to research. This can be done through a simple API request, where the user provides the main topic of interest. For example, "Latest AI advancements".

#### Step 2: Generating Subqueries

2. **Automatic Subquery Generation**: Once the main topic is submitted, the system automatically generates a set of detailed subqueries related to the main topic. These subqueries help in breaking down the broad topic into specific areas of focus, ensuring a comprehensive analysis.

#### Step 3: Data Collection

3. **Data Gathering**: The system then uses these subqueries to search for relevant information across various sources. This includes fetching data from databases, external APIs, and other repositories. The goal is to gather as much pertinent information as possible.

#### Step 4: Compiling the Report

4. **Report Compilation**: After collecting the data, the system compiles all the gathered information into a cohesive and structured report. This report includes detailed analysis, insights, and findings based on the provided topic and its subqueries.

#### Step 5: Delivering the Report

5. **Report Delivery**: The final report is delivered back to the user in a well-organized format. The user can then review the comprehensive report, which includes citations, data sources, and detailed explanations, providing a thorough understanding of the topic.

### User Experience Highlights

- **Ease of Use**: Users only need to provide a single topic to get started. The rest of the process, including generating subqueries and gathering data, is handled automatically.
- **Comprehensive Analysis**: By breaking down the main topic into subqueries, the system ensures a deep and thorough exploration of the subject matter.
- **Time Efficiency**: Automating the research process saves users significant time and effort, providing them with detailed reports quickly.
- **Detailed Insights**: The final report includes citations and sources, offering users a reliable and informative resource for their research needs.

Agentic Reports, through `Agentic Reports`, streamlines the entire process of creating detailed research reports, making it an invaluable tool for anyone needing comprehensive and accurate information on a specific topic.

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
 