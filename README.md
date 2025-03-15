# LEGAL-ASSIST-AI
# LegalAssist AI 🏛️⚖️

![image]()

An AI-powered legal assistant application built with Streamlit and Google's Gemini API.

## Overview

LegalAssist AI is a comprehensive legal assistance tool designed for lawyers, law students, and legal professionals in India. It leverages Google's Gemini 2.0 Flash model to provide AI-powered legal services including document analysis, case law summarization, argument generation, and more.

## Features

- **Legal Advice**: Get AI-generated legal advice across multiple areas of law
- **Document Analysis**: Upload legal documents for AI analysis of contracts, risks, and compliance
- **Case Law Summarization**: Generate concise summaries of case laws with key principles
- **Argument Generator**: Create structured legal arguments for both sides of a case
- **Citation Generator**: Generate properly formatted legal citations for various sources
- **Bias Detection**: Analyze judgments for potential biases or prejudicial language
- **IPC Search**: Search and navigate the Indian Penal Code with AI assistance
- **Legal Research Assistant**: Get help with legal research questions and find relevant resources

![sample]

## Getting Started

### Prerequisites

- Python 3.7+
- Streamlit
- Google API key with Gemini API access

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/legalassist-ai.git
   cd legalassist-ai
   ```

2. Install required packages:
   ```
   pip install streamlit google-generativeai pypdf2 python-docx
   ```

3. Create a `.streamlit/secrets.toml` file with your Google API key:
   ```
   GOOGLE_API_KEY = "your-google-api-key"
   ```

4. Run the application:
   ```
   streamlit run app.py
   ```

## Usage

1. Start the application using the command above
2. Select a service from the sidebar menu
3. Enter your query or upload documents as required
4. View the AI-generated results

## Services Explained

### Legal Advice
Enter your legal situation to receive structured advice including applicable laws, potential courses of action, and recommended next steps.

### Document Analysis
Upload legal documents (PDF, DOCX, TXT) for AI analysis. Choose from multiple analysis types:
- Contract Review
- Legal Risk Assessment
- Plain Language Summary
- Legal Compliance Check

### Case Law Summarization
Get AI-powered summaries of case laws with structured breakdowns of facts, legal issues, decisions, and key principles.

### Argument Generator
Generate structured legal arguments for different positions (plaintiff/prosecution, defendant/defense, or both sides).

### Citation Generator
Create properly formatted legal citations for:
- Case Law
- Statutes/Acts
- Rules/Regulations
- Legal Journals/Articles
- Books
- Reports

### Bias Detection
Analyze judgments for potential biases related to gender, religion, socioeconomic status, caste, age, region, or language.

### IPC Search
Search and explore the Indian Penal Code by:
- Section Number
- Keyword Search
- Legal Concept

### Legal Research Assistant
Get comprehensive research on legal questions, including statutory frameworks, case law, and academic commentary.

## Important Notes

- This tool is intended to assist legal professionals and should not replace professional legal advice
- All AI-generated content should be reviewed by a qualified legal professional
- The application requires an internet connection to access Google's Gemini API

## Acknowledgements

- Streamlit for the app framework
- Google's Generative AI for the Gemini model
- Libraries: PyPDF2, python-docx
