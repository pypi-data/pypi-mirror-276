# XeedChatBot

## How to Use
- Load the dataframe
- initialize the XeedChatBot Class

## XeedChatBot
Initializes the Chat Bot

**Args**
>**df**:&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp; Pandas DataFrame object of the data to be analyzed. Also accepts a list of DataFrame  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&ensp; Only supports .csv, .xlsx, .parquet, and .orc file formats.  
>**db**:&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp; Database Object that can be analyzed. If df is used, db should be empty  
>**llm**: &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *Optional*. Name of the Large Language Model to be used.  
>**prompt**:&emsp;&emsp;&emsp;&emsp;&nbsp; *Optional*. Instructions for the model.  

**Returns**
> Chatbot Agent


## Sample Usage using pandas DataFrame
```python
import os
import pandas as pd

from xeedchatbot import XeedChatBot

#set the API KEY
os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

df = pd.read_csv('sample_data/financial_data.csv')
prompt = f"You are an expert on the company's finances. By default the company you will provide information for is Xurpas.\
        Please make sure you complete the objective above with the following rules:\
        1/ Your job is to first breakdown the topic into relevant questions for understanding the topic in detail. You should have at max only 3 questions not more than that, in case there are more than 3 questions consider only the first 3 questions and ignore the others.\
        2/ You should use finance_tool to get more information about the topic. You are allowed to use the search tool only 3 times in this process.\
        3/ If asked for multiple items, query them one by one using the tools provided.\
        4/ If not asked for a specific time period, assume the year 2024.\
        5/ Aggregate all the answers that you can get on this topic.\
        6/ Ouput DataFrame data as an HTML table."

chatbot = XeedChatBot(df=df, prompt=prompt)
agent = chatbot.initialize_chatbot()

msg = agent.invoke("What is the EBITDA for Xurpas for the year 2024")

print(msg['output'])

*The EBITDA for Xurpas is $50 million.*

```