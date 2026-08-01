# Real-Time Transaction Processing Platform

## Cel projektu

Celem projektu jest zbudowanie kompletnej platformy Data Engineering do przetwarzania danych transakcyjnych w czasie rzeczywistym oraz wsadowo.

Projekt pokazuje praktyczne wykorzystanie:

- stream processing
- batch processing
- ETL
- data modeling
- konteneryzacji
- deploymentu na Kubernetes

Projekt nie skupia się na Machine Learningu. Głównym celem jest pokazanie architektury danych wykorzystywanej w nowoczesnych systemach finansowych.


# Architektura


                Transaction Generator
                        |
                        |
                        v

                  Apache Kafka
                transactions topic

                        |
          +-------------+-------------+
          |                           |
          v                           v

   Apache Flink                 Apache Spark
   Streaming                    Batch Processing

          |                           |
          |                           |
          v                           v

 PostgreSQL                  PostgreSQL
 Streaming Data             Analytics Data

                                      |
                                      |
                                      v

                                     dbt

                                      |
                                      |
                                      v

                              Analytics Models



# Technologie


## Data Engineering

- Python
- Apache Kafka
- Apache Flink (PyFlink)
- Apache Spark (PySpark)
- PostgreSQL
- dbt


## Infrastructure

- Docker
- Docker Compose
- Kubernetes


## Monitoring (opcjonalnie)

- Prometheus
- Grafana



# Funkcjonalności projektu

Platforma obsługuje:

- generowanie danych transakcyjnych
- streaming danych przez Kafka
- real-time processing przez Flink
- batch processing przez Spark
- transformacje danych
- modelowanie danych przez dbt
- przechowywanie danych analitycznych w PostgreSQL
- deployment komponentów na Kubernetes



# Data Generator

Projekt posiada prosty generator danych napisany w Pythonie.

Generator symuluje ruch transakcyjny.

Przykładowy rekord:


{
  "transaction_id": "abc123",
  "timestamp": "2026-01-01T12:00:00",
  "customer_id": 123,
  "merchant_id": 55,
  "amount": 250.50,
  "currency": "PLN",
  "country": "Poland",
  "payment_method": "card"
}


Dane wysyłane są do Kafka topic:


transactions



# Apache Kafka

Kafka pełni rolę message brokera.


Przepływ danych:


Python Generator

        |

        v

Kafka Topic

        |

        v

Flink / Spark



Topic:


transactions



# Apache Flink

Flink odpowiada za przetwarzanie danych w czasie rzeczywistym.


Zadania:

- Kafka Source
- walidacja danych
- transformacje
- filtrowanie
- window functions
- agregacje czasowe
- zapis wyników do PostgreSQL


Przykładowe operacje:


## Liczba transakcji na minutę


window = 60 seconds



## Podejrzane transakcje


Prosta reguła:


amount > 5000


wynik:


is_suspicious = true



Przykład:


{
  "transaction_id": "123",
  "amount": 15000,
  "is_suspicious": true
}



# Apache Spark

Spark odpowiada za batch processing.


Proces:


Raw Data

   |

   v

Spark ETL

   |

   v

Analytics Tables



Spark wykonuje:

- cleaning
- schema validation
- deduplication
- transformacje
- agregacje biznesowe


Przykładowe agregacje:


daily_transaction_summary

merchant_statistics

country_statistics

customer_activity



# dbt

dbt odpowiada za warstwę modelowania danych.


Tworzone modele:


## Dimensions


dim_customer

dim_merchant

dim_date



## Facts


fact_transactions

fact_suspicious_transactions



## Analytics Marts


daily_transaction_summary

merchant_statistics

country_statistics

customer_activity



# PostgreSQL

PostgreSQL przechowuje dane projektu.


Schemat:


postgres

├── raw

├── streaming

└── analytics



## Streaming tables


transactions_stream

suspicious_transactions



## Analytics tables


daily_transaction_summary

merchant_statistics

customer_activity



# Docker

Każdy komponent działa jako osobny kontener.


Kontenery:


generator

kafka

flink-jobmanager

flink-taskmanager

spark

postgres

dbt



Uruchomienie:


docker-compose up



# Kubernetes

Deployment aplikacji na Kubernetes.


Struktura:


kubernetes/

├── kafka/

├── flink/

├── spark/

├── postgres/

├── generator/

└── dbt/


Uruchomienie:


kubectl apply -f kubernetes/



# Monitoring

Opcjonalny moduł obserwowalności.


Prometheus zbiera:

- Kafka throughput
- Flink metrics
- Spark jobs
- CPU
- RAM


Grafana dashboard:


- Transactions per second
- Processed records
- Suspicious transactions
- System resources



# Struktura projektu


transaction-platform/

│

├── generator/

│   └── producer.py

│

├── kafka/

│

├── flink/

│   └── streaming_job.py

│

├── spark/

│   └── etl_job.py

│

├── dbt/

│   ├── models/

│   └── dbt_project.yml

│

├── postgres/

│   └── init.sql

│

├── docker/

│

├── kubernetes/

│

├── monitoring/

│

├── tests/

│

└── README.md



# Plan budowy projektu


## Etap 1 - Local Environment

- Docker Compose
- PostgreSQL
- Kafka
- Python Generator


## Etap 2 - Streaming

- Kafka Producer
- PyFlink Streaming Job
- PostgreSQL Sink


## Etap 3 - Batch Processing

- PySpark ETL
- Transformacje danych
- Agregacje


## Etap 4 - Data Modeling

- dbt models
- fact tables
- dimension tables
- analytics marts


## Etap 5 - Kubernetes

- Kubernetes manifests
- Deployments
- Services


## Etap 6 - Monitoring

- Prometheus
- Grafana dashboards



# Cel końcowy

Projekt ma pokazać pełny workflow Data Engineering:


Python

↓

Kafka

↓

Flink Streaming

↓

PostgreSQL

↓

Spark ETL

↓

dbt

↓

Analytics Layer

↓

Docker

↓

Kubernetes



Projekt demonstruje budowę nowoczesnej platformy danych wykorzystującej streaming, batch processing oraz cloud-native deployment.