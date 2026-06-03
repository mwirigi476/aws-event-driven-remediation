# aws-event-driven-remediation
# Event-Driven Auto-Remediation and Observability System on AWS

## Project Architecture & Flow Description
1. **Detection Engine**: AWS Config monitors security configuration drift continuously. It instantly catches any open SSH security groups using the `restricted-ssh` managed baseline check.
2. **Event Router & Fan-out Engine**: Amazon EventBridge catches non-compliant rules changes and matches them via custom JSON filtering patterns. It triggers 3 isolated data consumers in parallel:
   * **Amazon SQS**: Logs raw event payloads asynchronously for compliance audit trails.
   * **Amazon Kinesis**: Streams real-time runtime configurations data for analytics parsing.
   * **AWS Step Functions**: Launches an automated structural repair engine.
3. **Remediation & Observability Engine**: The state machine runs an explicit conditional assessment via an AWS Lambda function before passing target variables to AWS Systems Manager (SSM) automation documents. AWS CloudWatch captures unified execution metrics, log streams, and X-Ray active workflow tracing.

## Production Code Artifacts
* Core Processing Code: Located under `src/lambda_evaluator.py`
* Automation Topology Orchestration JSON: Located under `templates/state_machine.json`

## Proof of Execution Logs & Status Verifications

### 1. AWS Config Compliance Event Identification
![Config Rule](./01_config_rule.png)

### 2. Step Functions Automated Success Tree Run
![Step Functions Run](./02_step_functions_success.png)

### 3. Lambda Core Event Broker Processing Logs (CloudWatch)
![CloudWatch Traces](./03_cloudwatch_logs.png)

### 4. Cleansed Architecture State Following Post-Remediation Check
![Remediated Environment State](./04_remediated_sg.png)
