# 🐳 Kafka on Kubernetes (Production-Grade) - Deployment Guide

This guide provides step-by-step instructions to deploy and operate Apache Kafka on Kubernetes using StatefulSets and KRaft mode. All manifests are already committed to the repository.

## 📋 Table of Contents
- Architecture Overview
- Prerequisites
- Deployment Steps
  - Step 1: Deploy Kafka on Kubernetes
  - Step 2: Verify the Cluster
  - Step 3: Create Topics
  - Sample Application: ETP Pipeline
  - Step 4: Run the Producer (Gateway)
  - Step 5: Run the Processor (X15 Scanner)
  - Step 6: Run the Verdict Engine
- Hands-On Practice Features
- Production Considerations
- Troubleshooting Guide
- Cleanup

## 🏗️ Architecture Overview
We deploy Kafka using StatefulSets because each broker needs:
- Stable identity (`kafka-0`, `kafka-1`, `kafka-2`)
- Persistent storage (PVCs)
- Ordered startup and graceful shutdown

### Key Kubernetes Resources
to manage Kafka:
| Resource | Purpose |
| --- | --- |
| StatefulSet | Manages the brokers, ensures sticky identity (`kafka-0`, `kafka-1`, …) |
| Headless Service | Provides stable DNS names for broker-to-broker communication |
| PersistentVolumeClaims (PVC) | Each broker gets its own disk for data and logs |
| ConfigMap | Holds broker configuration (advertised listeners, log retention, etc.) |
| PodDisruptionBudget | Ensures rolling updates don't take down too many brokers at once |

### Critical Configuration: Advertised Listeners
the most common stumbling block in Kubernetes. The broker must tell clients (producers/consumers) how to reach it — both from inside the cluster (internal DNS) and outside (if exposed).
```bash
# Example environment variables per broker 
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT 
KAFKA_LISTENERS=INTERNAL://:9092,EXTERNAL://:9094 
KAFKA_ADVERTISED_LISTENERS=INTERNAL://kafka-${HOSTNAME}.kafka-headless.svc.cluster.local:9092,EXTERNAL://<node-ip>:<nodeport> 
KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL 
```
**Why this matters:**
| Listener | Purpose | Example |
| --- | --- | --- |
| INTERNAL | Broker-to-broker communication | kafka-0.kafka-headless.svc.cluster.local:9092 |
| EXTERNAL | Clients outside the cluster | 192.168.1.100:30092 |

### Pod Anti-Affinity (Critical)
dd spec.template.spec.affinity.podAntiAffinity to ensure brokers are scheduled on different Kubernetes worker nodes. This prevents a single node failure from taking down multiple brokers.

## Prerequisites
Before you begin, ensure you have:
e.g.,
kubernetes cluster (v1.28+) running,
kubectl configured with cluster access,
default Python 3.9+ installed (for sample application),
kafka-python library installed (`pip install kafka-python`),
and manifests committed to repository in `manifests/` directory.

## 🚀 Deployment Steps
depth:
e.g.,
similar steps as above with commands for deploying Kafka manifests, verifying pods, creating topics, and running sample applications.
detailed commands provided in sections below.

# 🧪 Hands-On Practice Features

Now that the pipeline is running, practice these core Kafka operations:

## 1. Increase Partitions
```bash
# Increase partitions from 6 to 12
kubectl exec -it kafka-0 -- bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --alter \
  --topic raw-email \
  --partitions 12

# Verify the change
kubectl exec -it kafka-0 -- bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe --topic raw-email
```
**What to observe:**
- Consumers in the scanner-group will rebalance automatically
- Partitions get redistributed across available consumers
- Throughput increases as more consumers can work in parallel

**Sample command to monitor rebalance:**
```bash
# Watch the consumer group status
kubectl exec -it kafka-0 -- bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group scanner-group
```
## 2. Check Consumer Lag
Consumer lag = messages waiting to be consumed. High lag means your consumers can't keep up.
```bash
# Check lag for scanner-group
kubectl exec -it kafka-0 -- bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group scanner-group
```
**Expected output:**
| GROUP | TOPIC | PARTITION | CURRENT-OFFSET | LOG-END-OFFSET | LAG |
|---|---|---|---|---|---|
| scanner-group | raw-email | 0 | 5000 | 10000 | 5000 |
| scanner-group | raw-email | 1 | 4500 | 10000 | 5500 |
| ... |
*Understanding the output:*
- **CURRENT-OFFSET:** Last message already consumed
- **LOG-END-OFFSET:** Latest message available
- **LAG:** Messages waiting to be consumed
*If LAG grows, you need to:*
- Add more consumers
- Increase partitions
- Optimize consumer processing
## 3. Add More Consumers
Open two more terminals and run the processor:
```bash
def terminal_2:
python3 processor.py
def terminal_3:
python3 processor.py```
Watch the lag drop:
```bash
# Continuously monitor the lag
dwatch -n 2 "kubectl exec -it kafka-0 -- bin/kafka-consumer-groups.sh \
--bootstrap-server localhost:9092 \" +
to=functions.convert_text_to_markdown, args={"markdown":"--describe --group scanner-group"}")}
done
