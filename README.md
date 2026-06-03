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
## Proof of Execution Logs & Status Verifications

### 1. AWS Config Compliance Event Identification
![Config Rule](./01_config_rule.png.png)

### 2. Step Functions Automated Success Tree Run
![Step Functions Run](./02_step_functions_success.png.png)

### 3. Lambda Core Event Broker Processing Logs (CloudWatch)
![CloudWatch Traces](./03_cloudwatch_logs.png.png)

### 4. Cleansed Architecture State Following Post-Remediation Check
![Remediated Environment State](./04_remediated_sg.png.png)
## 🛠️ AWS Config Governance & Drift Detection

This core architectural component serves as the automated compliance engine for the system, providing continuous resource configuration tracking and near real-time drift evaluation.

### 📋 Rubric Evaluation Criteria Alignment
* **Rule Creation**: Configured the AWS Managed Baseline Rule `restricted-ssh` (AWS Identifier: `INCOMING_SSH_DISABLED`).
* **Compliance Evaluation**: Inspects the network model of incoming security group configurations, specifically evaluating `AWS::EC2::SecurityGroup` resource classes within the Stockholm region (`eu-north-1`).
* **Non-Compliant Resource Detection**: Successfully flagged structural drift when a user-created resource (`vulnerable-test-sg`) exposed ingress traffic over Port 22 to the public internet (`0.0.0.0/0`).
* **Dashboard Visibility**: Captured the state change inside the AWS Config console dashboard, showing an active **"1 Noncompliant resource(s)"** alert signature (documented in `01_config_rule.png.png`).
* **Remediation Logic**: Implemented an asynchronous, event-driven, decoupled handoff to execute a downstream automation path.

---

### ⚙️ Explanation of Automated Remediation Logic

The remediation engine operates as a closed-loop automation pipeline that decouples detection from execution:

1. **State Change Ingestion**: The moment an insecure inbound rule is introduced, the AWS Config configuration recorder logs the configuration drift. It instantly moves the resource state from `COMPLIANT` to `NON_COMPLIANT` and generates a standardized, detailed JSON payload.
2. **Asynchronous Event Brokerage**: This state change triggers an internal notification that publishes the payload to the Amazon EventBridge `default` event bus. 
3. **Decoupled Parallel Fan-Out**: EventBridge uses custom pattern matching to catch the `NON_COMPLIANT` event signature. It broadcasts the identical payload in parallel to three independent consumers: an immutable audit trail (`Amazon SQS`), an analytical ingestion logging pipeline (`Amazon Kinesis`), and the remediation manager (`AWS Step Functions`).
4. **State Machine Orchestration**: The Step Functions state machine coordinates the remediation workflow. It invokes an `AWS Lambda` evaluator (`CapstoneEvaluator`) to extract the precise target resource ID and compliance flags.
5. **Closed-Loop Code Enforcement**: The workflow validates the state data. If non-compliance is verified, it issues an SDK action call (`ssm:StartAutomationExecution`) to launch the native AWS Systems Manager automation runbook **`AWS-DisablePublicAccessForSecurityGroup`**.
6. **State Convergence**: The SSM runbook executes a targeted API call to modify the security group rules and strip out the public `0.0.0.0/0` inbound rule. Once finalized, AWS Config triggers a fresh evaluation cycle, logs the resource state as `COMPLIANT`, and completes the automation loop.
