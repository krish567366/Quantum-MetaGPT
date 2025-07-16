### QuantumMetaGPT User Guide
1. Installation
bash
# Clone the repository
```bash
git clone https://github.com/yourusername/QuantumMetaGPT.git
cd QuantumMetaGPT


# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export IBMQ_TOKEN="your_ibm_quantum_token"  # Get from quantum-computing.ibm.com
export OPENAI_API_KEY="your_openai_key"     # Get from platform.openai.com

# Generate license
python -m qmetagpt.security_licensing.cli_license generate --customer "Your Name"
```
2. Basic Usage
```python
from QuantumMetaGPT import run_pipeline

# Run full research pipeline
report_path = run_pipeline(
    arxiv_id="quant-ph/2310.12345",  # Quantum paper ID
    use_hardware=False,               # Set True for real quantum computer
    rl_agent="PPO",                   # RL algorithm (PPO, A2C, SAC, DDPG)
    optimizer="COBYLA"                # Optimizer (COBYLA, SPSA, NELDER_MEAD)
)
print(f"Report generated at: {report_path}")
```
3. Command Line Interface
```bash
# Process a quantum research paper
python main.py quant-ph/2310.12345

# Options:
#   --hardware     Run on real quantum computer
#   --agent AGENT  RL agent (default: PPO)
#   --optimizer OPT  Optimizer (default: COBYLA)
#   --shots N      Number of executions (default: 1024)

# Example:
python main.py quant-ph/2310.12345 --hardware --agent SAC --optimizer SPSA --shots 5000
```
4. Web API Interface
```bash
# Start the API server
uvicorn qmetagpt.frontend_interface.app:app --reload

# Endpoints:
#   POST /run_pipeline?arxiv_id=quant-ph/2310.12345
#   GET  /task_status/{task_id}
#   GET  /task_result/{task_id}

# Example workflow:
curl -X POST "http://localhost:8000/run_pipeline?arxiv_id=quant-ph/2310.12345"
# Returns: {"task_id": "a1b2c3d4", "status": "processing"}

curl "http://localhost:8000/task_status/a1b2c3d4"
# Returns status until "completed"

curl "http://localhost:8000/task_result/a1b2c3d4"
# Returns full results and report path
```
5. Configuration
Edit config.yaml for advanced settings:

```yaml
quantum:
  backend: "ibmq_manila"   # Quantum hardware backend
  use_hardware: false       # Use real quantum computer
  shots: 1024               # Execution shots

llm:
  model_type: "openai"      # "openai" or "llama"
  model_name: "gpt-4"       # "gpt-3.5-turbo" or llama model path

rl:
  agent: "PPO"              # RL algorithm
  policy: "MlpPolicy"       # Neural network architecture
  learning_rate: 0.0003
  gamma: 0.99               # Discount factor
  timesteps: 50000          # Training steps

optimizer:
  type: "COBYLA"            # Optimization algorithm
  max_iter: 1000            # Max iterations

report:
  format: "pdf"             # "pdf" or "latex"
  template: "default"       # Report template
  ```
6. Security Management
```bash
# Generate new license
python -m qmetagpt.security_licensing.cli_license generate --customer "Lab Name" --duration 365

# Validate license
python -m qmetagpt.security_licensing.cli_license validate

# Show hardware ID
python -m qmetagpt.security_licensing.cli_license info
```
# Transfer license to new machine:
1. Run `license info` on new machine to get HW ID
2. On old machine: `license generate --hw-id NEW_HW_ID`
3. Copy license.key to new machine
Building QuantumMetaGPT
1. Building Python Package
bash
# Create distributable package
```pytho
python setup.py sdist bdist_wheel
```
# Install locally
pip install dist/QuantumMetaGPT-0.1.0-py3-none-any.whl

# Verify installation
python -c "from QuantumMetaGPT import run_pipeline; print(run_pipeline.__doc__)"
2. Docker Build
bash
# Build Docker image
docker build -t quantummetagpt .

# Run container
docker run -it --rm \
  -e IBMQ_TOKEN="your_token" \
  -e OPENAI_API_KEY="your_key" \
  -v $(pwd)/reports:/app/reports \
  quantummetagpt quant-ph/2310.12345

# Access reports in ./reports directory
3. Deployment Options
A. Cloud Deployment (AWS Example)

bash
# Push Docker image to ECR
aws ecr create-repository --repository-name quantummetagpt
docker tag quantummetagpt:latest 123456789.dkr.ecr.region.amazonaws.com/quantummetagpt:latest
aws ecr get-login-password | docker login --username AWS --password-stdin 123456789.dkr.ecr.region.amazonaws.com
docker push 123456789.dkr.ecr.region.amazonaws.com/quantummetagpt:latest

# Run on ECS/Fargate with environment variables:
# IBMQ_TOKEN, OPENAI_API_KEY
B. Kubernetes Deployment

```yaml
# quantummetagpt-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quantummetagpt
spec:
  replicas: 3
  selector:
    matchLabels:
      app: quantummetagpt
  template:
    metadata:
      labels:
        app: quantummetagpt
    spec:
      containers:
      - name: quantumai
        image: quantummetagpt:latest
        env:
        - name: IBMQ_TOKEN
          valueFrom:
            secretKeyRef:
              name: quantum-secrets
              key: ibmq_token
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: quantum-secrets
              key: openai_key
        volumeMounts:
        - name: reports
          mountPath: /app/reports
      volumes:
      - name: reports
        persistentVolumeClaim:
          claimName: reports-pvc

```

4. Development Build
bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest --cov=qmetagpt

# Generate coverage report
coverage html

# Run linter
pylint qmetagpt

# Build documentation (requires Sphinx)
cd docs
make html
Key Directories
├── data/           # Processed research data
├── reports/        # Generated PDF reports
├── trained_models/ # Saved RL agents
├── logs/           # System logs
└── licenses/       # License keys
Support
For issues and support:

GitHub Issues: https://github.com/yourusername/QuantumMetaGPT/issues

Documentation: https://quantummetagpt.readthedocs.io

Community Forum: https://forum.quantummetagpt.org

Citation
bibtex
@software{QuantumMetaGPT,
  author = {Your Name},
  title = {{QuantumMetaGPT: Autonomous Quantum-AI Research Agent}},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/yourusername/QuantumMetaGPT}}
}