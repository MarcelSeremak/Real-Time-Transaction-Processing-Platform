#!/bin/bash

set -e

BOOTSTRAP_SERVER="kafka_broker_1:19092"

echo "Waiting for Kafka..."

until /opt/kafka/bin/kafka-topics.sh \
    --bootstrap-server $BOOTSTRAP_SERVER \
    --list > /dev/null 2>&1
do
    echo "Kafka not ready yet..."
    sleep 5
done


echo "Kafka is ready"


create_topic() {
    TOPIC=$1
    PARTITIONS=$2

    if /opt/kafka/bin/kafka-topics.sh \
        --bootstrap-server $BOOTSTRAP_SERVER \
        --describe \
        --topic $TOPIC > /tmp/topic-description.txt 2> /dev/null
    then
        CURRENT_PARTITIONS=$(grep -m 1 -oE 'PartitionCount: [0-9]+' /tmp/topic-description.txt | awk '{print $2}')

        if [ "$CURRENT_PARTITIONS" -lt "$PARTITIONS" ]; then
            /opt/kafka/bin/kafka-topics.sh \
                --alter \
                --topic $TOPIC \
                --bootstrap-server $BOOTSTRAP_SERVER \
                --partitions $PARTITIONS

            echo "Updated topic partitions: $TOPIC ($CURRENT_PARTITIONS -> $PARTITIONS)"
        else
            echo "Topic already exists: $TOPIC ($CURRENT_PARTITIONS partitions)"
        fi
    else
        /opt/kafka/bin/kafka-topics.sh \
            --create \
            --topic $TOPIC \
            --bootstrap-server $BOOTSTRAP_SERVER \
            --partitions $PARTITIONS \
            --replication-factor 3

        echo "Created topic: $TOPIC"
    fi

    /opt/kafka/bin/kafka-configs.sh \
        --bootstrap-server $BOOTSTRAP_SERVER \
        --alter \
        --entity-type topics \
        --entity-name $TOPIC \
        --add-config min.insync.replicas=1
}


create_topic customers 3
create_topic merchants 3
create_topic accounts 3
create_topic transactions 6


echo "Kafka initialization completed"
