# Python DevOps Lab

A Python version of the DevOps lab using Flask, pytest, Docker, Kubernetes, GitHub Actions, Postman and Terraform.

## 1. Project structure

```text
x/
├── app.py
├── test_app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── .github/workflows/
│   ├── environment.yml
│   └── ci.yml
├── postman/
│   └── student_api.postman_collection.json
└── terraform/
    └── main.tf
```

## 2. Local setup

```bash
git clone https://github.com/LonelyDreamer005/x.git
cd x

python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

## 3. Run Flask API

```bash
python app.py
```

The API runs at `http://localhost:5000`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API status |
| GET | `/health` | Health check |
| GET | `/students` | List students |
| GET | `/students/<id>` | Get one student |
| POST | `/students` | Add student |
| PUT | `/students/<id>` | Update student |
| DELETE | `/students/<id>` | Delete student |

Example:

```bash
curl http://localhost:5000/students

curl -X POST http://localhost:5000/students \\
  -H "Content-Type: application/json" \\
  -d '{"name":"Vinay","age":20,"department":"CSE"}'
```

## 4. Run tests

```bash
pytest -v
```

## 5. Git commands

```bash
git status
git add .
git commit -m "Update DevOps lab"
git push origin main
```

## 6. Docker

Build and run the Flask application:

```bash
docker build -t vinay1030/night:latest .

docker run -d --name night-app -p 5000:5000 vinay1030/night:latest

docker images
docker ps
docker ps -a
docker logs night-app
curl http://localhost:5000/health
```

Container management:

```bash
docker stop night-app
docker start night-app
docker restart night-app
docker rm -f night-app
```

Push the image to Docker Hub:

```bash
docker login
docker push vinay1030/night:latest
```

## 7. Kubernetes with Minikube

Start the cluster:

```bash
minikube start --driver=docker
kubectl config use-context minikube
kubectl get nodes
```

Deploy the YAML files:

```bash
kubectl apply -f k8s/
kubectl get deployments
kubectl get pods
kubectl get services
kubectl rollout status deployment/night-app
```

Access the application in GitHub Codespaces:

```bash
kubectl port-forward service/night-service 5000:5000 --address 0.0.0.0
```

Open port `5000` in the Codespaces Ports tab.

Scale and clean up:

```bash
kubectl scale deployment night-app --replicas=3
kubectl get pods
kubectl logs deployment/night-app
kubectl delete -f k8s/
minikube stop
```

## 8. GitHub Actions

- `.github/workflows/environment.yml`: explores the GitHub Actions runner environment.
- `.github/workflows/ci.yml`: installs Python dependencies, runs pytest and builds the Docker image.

If using a Docker Hub publishing workflow, add these repository secrets:

- `DOCKER_USERNAME`
- `DOCKER_TOKEN`

A Docker publishing workflow pushes the image to Docker Hub. It does not automatically deploy to the Minikube cluster in Codespaces.

## 9. Postman

Import `postman/student_api.postman_collection.json` into Postman.

Use base URL:

```text
http://localhost:5000
```

Test the GET, POST, PUT and DELETE student endpoints, plus the health endpoint.

## 10. Monitoring and logging

```bash
# Docker
docker logs night-app
docker stats night-app

# Kubernetes
kubectl get pods
kubectl logs deployment/night-app
kubectl describe deployment night-app
kubectl describe service night-service
```

## 11. Terraform

```bash
cd terraform

terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
terraform show
terraform destroy
```

The local provider example creates a local text file. It is a basic Terraform lifecycle exercise, not cloud infrastructure provisioning.

## Notes

- Keep the Flask app, Dockerfile and Kubernetes container port aligned on port `5000`.
- Kubernetes image: `vinay1030/night:latest`. Change it if you publish under another Docker Hub repository.
- Student records are stored in memory. They reset when the Flask process restarts and are not shared between multiple Kubernetes replicas.
- This is a learning project, not a production deployment.
