# NETW.BROKER: Message Broker / Pub-Sub

## Description

Communicates via message brokers and publish-subscribe systems: MQTT, AMQP (RabbitMQ), Apache Kafka, Redis pub/sub, AWS SQS/SNS, Google Pub/Sub, or similar message queuing services. Communication is asynchronous and decoupled: the sender publishes to a topic or queue, and the receiver subscribes independently. The sender and receiver never communicate directly; the broker intermediary handles routing and delivery.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Message broker client library imports (`paho-mqtt`, `amqplib`, `kafkajs`, `redis`), broker connection strings, topic/queue names, publish/subscribe calls |
| Static Binary | Partial | Broker library imports, connection string literals, topic/queue name strings |
| Runtime/Dynamic | Yes | MQTT connections (port 1883/8883), AMQP connections (port 5672), Kafka connections (port 9092), broker protocol handshakes, message publish/subscribe traffic |

## Disambiguation

- **vs NETW.HTTP**: Some brokers support HTTP interfaces (SQS, SNS, Kafka REST Proxy). If the code uses a broker-specific client library or protocol (MQTT, AMQP wire protocol), it's `NETW.BROKER`. If it uses HTTP to interact with a broker's REST API, it's both `NETW.HTTP` and `NETW.BROKER`.
- **vs NETW.WS**: Both can maintain persistent connections. MQTT over WebSocket uses `NETW.WS` as transport but the message semantics are pub/sub (`NETW.BROKER`). If broker semantics are present, classify as `NETW.BROKER` (with `NETW.WS` if WebSocket transport is used).

## Structural Relationships

- **Often co-occurs with**: `ARTF.URL` / `ARTF.IP` (broker connection strings), `CRED.*` (broker authentication credentials), `EXEC.*` (commands received from a subscribed topic and executed)
- **May imply**: A message broker service is running somewhere (cloud-managed or self-hosted)

## Notes

The decoupled nature of pub/sub means the sender and receiver have no direct network connection to each other. The broker handles all routing. Topic/queue names and broker addresses are the key structural data points. MQTT is particularly common in IoT environments. Kafka is standard in event-driven architectures. Redis pub/sub is common for real-time features.
