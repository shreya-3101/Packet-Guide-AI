import boto3
import os
from dotenv import load_dotenv
# from langchain.memory import BaseMemory


# Load AWS credentials from .env file
load_dotenv()

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PacketGuideHistory')


# Function to retrieve all items from a DynamoDB table
def get_history(user_name, input_text):
    # Check if a history record exists for the given user and scene
    response = table.get_item(Key={"Username": user_name})
    db_record = response.get("Item")

    if db_record:
        return db_record["History"]
    else:
        return [{"role": "user", "content": input_text}]


def write_history(user_name, history):
    # Check if a history record exists for the given user and scene
    response = table.get_item(Key={"Username": user_name})
    db_record = response.get("Item")

    if db_record:
        # Append the new history to the existing history
        new_history = db_record["History"]
        new_history.extend(history)
        # Update the history record
        response = table.update_item(
            Key={"Username": user_name},
            UpdateExpression="set History=:h",
            ExpressionAttributeValues={":h": new_history},
            ReturnValues="UPDATED_NEW"
        )
    else:
        # Create a new history record
        response = table.put_item(
            Item={
                "Username": user_name,
                "History": history
            }
        )


# def write_packets_in_batches(dynamodb_user_packet):
#     table.put_item(Item=dynamodb_user_packet.to_dict())

def write_packets(user_name, packets):
    # Check if a history record exists for the given user and scene
    response = table.get_item(Key={"Username": user_name})
    db_record = response.get("Item")

    if db_record:
        # Append the new packets to the existing packets
        # if "Packets" in db_record:
        #     new_packets = db_record["Packets"]
        #     print(type(new_packets))
        #     print(type(packets))
        #     new_packets = bytes(new_packets)
        #     packets = bytes(packets)
        #     new_packets += packets
        #     # new_bytes_packets = bytes(new_packets, "utf-8")
        # else:
        #     new_packets = packets
        # Update the packets record
        response = table.update_item(
            Key={"Username": user_name},
            UpdateExpression="set Packets=:p",
            ExpressionAttributeValues={":p": packets},
            ReturnValues="UPDATED_NEW"
        )
    else:
        packets_bytes = packets
        # Create a new packet record
        response = table.put_item(
            Item={
                "Username": user_name,
                "Packets": packets_bytes,
                "History": []
            }
        )


def retrieve_packets(user_name):
    # Check if a history record exists for the given user and scene
    response = table.get_item(Key={"Username": user_name})
    db_record = response.get("Item")

    if db_record:
        return db_record["Packets"]
    else:
        return "No packets found."


def delete_packets(user_name):
    # Check if a history record exists for the given user and scene
    response = table.get_item(Key={"Username": user_name})
    db_record = response.get("Item")

    if db_record:
        # Update the packets record
        response = table.update_item(
            Key={"Username": user_name},
            UpdateExpression="set Packets=:p",
            ExpressionAttributeValues={":p": ""},
            ReturnValues="UPDATED_OLD"
        )
    else:
        return None
