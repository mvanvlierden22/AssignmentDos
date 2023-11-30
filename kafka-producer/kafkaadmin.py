from kafka.admin import KafkaAdminClient, NewTopic


def delete_topics(admin):
    admin.delete_topics(topics=["flights_results"])


def create_topics(admin, topic_list):
    admin.create_topics(new_topics=topic_list, validate_only=False)


if __name__ == "__main__":
    admin_client = KafkaAdminClient(
        bootstrap_servers="34.133.117.196:9092",
        client_id="streamer",
    )  # use your VM's external IP Here!
    topic_list = [
        NewTopic(name="flights", num_partitions=1, replication_factor=1),
        NewTopic(name="flights_results", num_partitions=1, replication_factor=1),
    ]
    create_topics(admin_client, topic_list)
