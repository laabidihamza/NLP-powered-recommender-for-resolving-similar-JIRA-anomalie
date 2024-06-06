# JIRA Solution Recommender

## Project Overview

The JIRA Solution Recommender is a Natural Language Processing (NLP) powered system designed to enhance developers' efficiency by recommending solutions for JIRA tickets. This project leverages advanced NLP techniques, including Sentence-BERT (SBERT), to capture semantic similarity between user queries and existing tickets in the dataset. The project follows the CRISP-DM methodology, ensuring a structured and comprehensive approach to development.

![Screenshot of the GUI](WebApp/assets/Home%20page.png)

## Features

- **Semantic Similarity Matching**: Utilizes SBERT to find semantically similar JIRA tickets based on user input.
- **Streamlit GUI**: Provides an intuitive and interactive user interface for developers to input queries and view recommendations.
- **Real-Time Processing**: Delivers instant feedback and recommendations to enhance productivity.
- **Data Integration**: Aggregates and preprocesses JIRA ticket data from multiple sources to ensure a robust dataset.

## Project Structure

1. **Data Collection**: Aggregation of JIRA ticket data from various websites.
2. **Data Preprocessing**: Cleaning, integrating, and formatting data to ensure consistency and quality.
3. **Model Exploration**: Evaluation of various NLP models, including SBERT and Universal Sentence Encoder (USE).
4. **Evaluation**: Benchmarking models using metrics like cosine similarity, spearmn rank correlation and computational efficiency to determine the best fit for the project.
5. **Model Deployment**: Selection and deployment of the optimal model (SBERT) using Streamlit for user accessibility.

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python Package Installer)
- Git

### Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/laabidihamza/NLP-powered-recommender-for-resolving-similar-JIRA-anomalie.git
    cd WebApp
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**:
    ```bash
    streamlit run app.py
    ```

## Usage

1. **Launch the Streamlit App**:
    - Open a terminal and navigate to the project directory.
    - Run `streamlit run app.py`.
    - The app will open in your default web browser.

2. **Input Query**:
    - Enter your query or issue in the input field.
    - Click on the "Search" button.

3. **View Recommendations**:
    - The app will display a list of JIRA tickets that are semantically similar to the input query.
    - Each recommendation includes the ticket summary, description, status, and comments.

## Evaluation

The project evaluates the performance of SBERT and USE models using various metrics. SBERT was chosen for its superior performance in capturing semantic similarity, making it the best fit for this project.

## Contributions

Contributions to this project are welcome. Please follow the guidelines below:

1. **Fork the Repository**.
2. **Create a Feature Branch**.
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Commit Your Changes**.
    ```bash
    git commit -m 'Add some feature'
    ```
4. **Push to the Branch**.
    ```bash
    git push origin feature/your-feature-name
    ```
5. **Open a Pull Request**.

## Acknowledgements

- **Supervisors**: Nader Kolsi and Akram Anaya for their invaluable guidance and support.
- **Vermeg Factory**: For providing the opportunity and resources to complete this project.
- **Higher Institute of Multimedia Arts of Manouba**: For academic support and resources.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or inquiries, please contact me **Hamza Laabidi** at laaabidihamza@gmail.com.
