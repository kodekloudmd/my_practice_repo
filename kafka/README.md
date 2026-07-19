# Kafka Cluster Setup Guide

## 1. Create Namespace
```bash
kubectl create namespace kafka
```

## 2. Apply All Manifests
```bash
kubectl apply -f kafka-headless-service.yaml -n kafka
kubectl apply -f kafka-external-service.yaml -n kafka
kubectl apply -f local-pv.yaml
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
kubectl apply -f kafka-statefulset.yaml -n kafka
```

## 3. Wait for Pods (takes approximately 2 minutes)
```bash
kubectl wait --for=condition=ready pod -l app=kafka -n kafka --timeout=300s
```

## 4. Verify Cluster
```bash
kubectl exec -it kafka-0 -n kafka -- bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092
```

## 5. Create Topics
```bash
ekctl exec -it kafka-0 -n kafka -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic raw-email --partitions 4 --replication-factor 2
ekctl exec -it kafka-0 -n kafka -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic enriched-email --partitions 4 --replication-factor 2
```
(Note: The commands for creating topics seem to have a typo; they should start with `kubectl exec` instead of `ekctl exec`.)

## 6. Test with Console Producer/Consumer
```bash
ekctl exec -it kafka-0 -n kafka -- bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic raw-email
ekctl exec -it kafka-0 -n kafka -- bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic raw-email --from-beginning
```
(Note: Same as above, replace `ekctl` with `kubectl`.)
