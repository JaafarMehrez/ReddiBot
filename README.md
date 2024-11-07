# ReddiBot

ReddiBot is a simple [Chatbot](https://en.wikipedia.org/wiki/Chatbot) based on content from your chosen subreddits. 

Data is obtained with Python Reddit API Wrapper library [praw](https://praw.readthedocs.io/en/stable/)

The chatbot is built with local LLM and embedding models. In specific, [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) as embedding model and [Llama3](https://www.llama.com/docs/overview) through [Ollama](https://ollama.com).

Your directory structure should look like this:

    ├── Starter.py
    └── data
       └── SampleData.txt
    ├── src
       └── EDA.py
       └── FetchData.py

The src/ folder contains the Reddit API wrapper along with methods for building pre-processing the data. Starter.py builds an index over the documents in the data/ folder (which in this case consists of the posts and comments fetched from your chosen subreddits, and it could contain more than one document). The Starter.py would also create an engine for Q&A over your index and respond to your queries.
