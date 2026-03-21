# Data Pipeline & AI Retrieval Assistant (RAG)

## Project Overview
This project is an end-to-end **ETL (Extract, Transform, Load)** data pipeline integrated with a **Large Language Model (LLM)**. It automatically ingests unstructured web data, structures it into a relational database, and serves it through an interactive web dashboard equipped with a natural language chat interface. 

This architecture allows users to bypass complex SQL queries and "chat" directly with the ingested dataset.

## Technical Stack
* **Data Ingestion/Web Scraping:** `requests`, `BeautifulSoup4`
* **Database Operations:** `SQLite3`, `pandas`
* **Frontend Application:** `Streamlit`
* **AI & NLP:** `OpenAI API (gpt-3.5-turbo)`

## System Architecture
1. **Extraction:** Python scripts systematically scrape target web sources for unstructured product and pricing data.
2. **Transformation:** The raw HTML is parsed and cleaned, formatting string variables into strict numerical data types for accurate analysis.
3. **Load:** The structured data is systematically inserted into a local SQLite database (`book_data.db`).
4. **Retrieval-Augmented Generation (RAG):** The Streamlit frontend queries the SQLite database and injects that real-time contextual data directly into the LLM's system prompt. This restricts the AI to answering analytical questions based *strictly* on the local dataset, preventing hallucinations.

## Quick Start Guide

**1. Clone the repository:**

git clone [https://github.com/69owens21/python-etl-pipeline.git](https://github.com/69owens21/python-etl-pipeline.git)

cd python-etl-pipeline
