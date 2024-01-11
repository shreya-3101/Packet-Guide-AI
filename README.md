# Packet-Guide-AI
The goal of this project is to create an intelligent conversational assistant that can capture and analyze network packets. Packet analysis involves examining and understanding network traffic data at the level of each individual packet. It is to streamline this procedure for students and experts by developing an intelligent assistant that comprehends natural language inquiries regarding packets.

Packet Guide AI utilizes OpenAI’s Large Language Models (LLM) for natural language processing, together with a Python back-end module that incorporates the Scapy packet manipulation framework. Users have the ability to capture real-time network packets and provide comprehensive information on the actual network traffic, clear explanations of the network packet fields and data through conversation. 

## Getting Started
### Installation
Make sure to install all the packages using the following command on the terminal when you are inside this project folder.
```bash
pip install -r requirements.txt
```

### Environment Configuration
To set up your environment:

1. Create a `.env` file in the root directory.
2. Add the following environment variables to the `.env` file:

    ```plaintext
    OPENAI_API_KEY=<Your OpenAI API Key>
    AWS_ACCESS_KEY_ID=<Your AWS Access Key ID>
    AWS_SECRET_ACCESS_KEY=<Your AWS Secret Access Key>
    AWS_DEFAULT_REGION=<Your AWS Default Region>
    ```

    Replace the placeholders with your actual credentials.

#### :lock: Security Notice

Please ensure that your `.env` file is never committed to version control or shared publicly. This file contains sensitive information that must remain confidential. Always verify your `.gitignore` file includes `.env` to prevent accidental commits.

### Running the App
After installing the requirements and making sure everything is present in the .env file as stated, you can run this streamlit app using the following command.
```python
streamlit run streamlit-webpage.py
```
## Features
The features that are currently present in our project are listed below.
- Conversational Interface
- Processes natural language queries without requiring specialized knowledge
- Efficiently adjusts and incorporates specific terms and language
- Graphical depiction of selected packet data information
- Ability to see the packets captured in real-time and search IP addresses or any other terms present in the packet through the local website.
- Capture a specific number of network packets
- Capture packets for a specific duration in seconds.
- Send ICMP packets (pings) to a target IP address to check connectivity and latency.
- Provide general summaries of the traffic captured
- Provide detailed examination of protocols, packet sizes, source and destination IPs, ports, and more
- Provide example prompts for the user to start or whenever it is not able to understand.
- Provide recommendations for further investigation based on identified knowledge deficiencies of the user.

