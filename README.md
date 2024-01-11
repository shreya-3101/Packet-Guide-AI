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

## Screenshots
### Project Overview
![Project Overview](/screenshots/ProjectOverview.png)

### Initial Streamlit App Page
![Initial Streamlit App Page](/screenshots/wp-1.png)

### Entering the prompt after providing the name
![Entering the prompt after providing the name](/screenshots/wp-2.png)

### Displaying sniffed packets on the sidebar of the web-page
![Displaying sniffed packets on the sidebar of the web-page](/screenshots/wp-3.png)

### Expanding and searching inside the table containing sniffed packets
![Expanding and searching inside the table containing sniffed packets](/screenshots/wp-4.png)

### Prompt creating the table
![Prompt creating the table](/screenshots/wp-5.png)

### Prompt showing graphs
![Prompt showing graphs](/screenshots/wp-6.png)

## Initial Prompts to Try
The following list showcases the prompts available for users to initiate. There is no obligation to only utilize these specific prompts. Users have the ability to engage in experimentation and provide us with feedback.
- Hello
- What all things can you can do?
- Capture 50 network packets.
- give me a detailed summary of the UDP packets.
- Create a table of the 5 most used IP addresses and ports for the TCP protocol and sort them by time
- Can you visualize the captured packet data?
- Summarize the usage of transport protocols (TCP, UDP) in this capture, with a focus on any abnormal TCP flags or unusual UDP traffic.
- Are there any HTTPS packets?
- From the network packet capture, which IP address do you think is related to my machine by analyzing the IP packets?
- Identify the IP addresses which are internal and external in the network packet capture
- Capture network packets for 3 seconds.
- Give me a summary of DNS queries made during this network capture. Include the most frequently accessed domains
- Can you identify DNS servers from the packet capture?
- Review these packet timings and sizes to identify any potential network performance issues, such as bottlenecks or high latency periods.
- Analyze TCP handshake timings in this capture to identify any slow connection establishments.
- can you ping www.google.com
- ping fit.edu

## Additional Information

### Overview
The Packet Guide AI prototype is designed to simplify complex packet analysis using natural language discussions, tailored for non-technical audiences. It combines real-time network data analysis, deep knowledge of fundamental network protocols, and OpenAI’s natural language processing capabilities to offer an assistive tool that provides immediate, user-friendly responses.

### Current Capabilities and Limitations
- **Packet Analysis Limit**: The system is currently optimized for analyzing up to 100 packets effectively. 
- **Upper Limit Caution**: While the system can capture more than 100 packets, please note that processing over 850 packets may result in errors due to the limitations in the OpenAI function agent’s capacity.

### Usage Tips
- **Effective Queries**: For best results, include relevant keywords in your inquiries, such as specific protocols (e.g., TCP).
- **Avoid Complex Combinations**: Overly complex protocol combinations may reduce analysis quality.
- **Troubleshooting**: If you encounter issues, try resending your prompt. Should problems persist, consider capturing new packets or rephrasing your query.

### Future Developments
We are committed to enhancing the functionalities of PacketGuide AI. Stay tuned for future updates as we work towards making this tool even more beneficial for everyone.

## Contributing
Please read CONTRIBUTING.md for details on our [Code of Conduct](/CODE_OF_CONDUCT.md), and the process for submitting pull requests to us.

## License
This project is licensed under the MIT License - see the [License](/LICENSE.md) file for details.

## Contact
Contact
For questions or feedback, **Shreya Nandanwar** at shreya.nandanwar2001@gmail.com or **Tapas Joshi** at tapasjoshi.it@gmail.com.
