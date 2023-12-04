from kafka.admin import KafkaAdminClient, NewTopic


def delete_topics(admin):
    admin.delete_topics(topics=["results"])


def create_topics(admin, topic_list):
    admin.create_topics(new_topics=topic_list, validate_only=False)


if __name__ == "__main__":
    admin_client = KafkaAdminClient(
        bootstrap_servers="34.172.3.9:9092",
        client_id="streamer",
    )  # use your VM's external IP Here!
    topic_list = [
        NewTopic(name="results", num_partitions=1, replication_factor=1),
        NewTopic(name="flight", num_partitions=1, replication_factor=1),
    ]
    # delete_topics(admin_client)
    create_topics(admin_client, topic_list)
