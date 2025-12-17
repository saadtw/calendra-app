# Kubernetes Deployment Files

## Files Overview

- **namespace.yaml** - Creates the `calendra` namespace
- **database-deployment.yaml** - PostgreSQL database deployment, service, and PVC
- **app-deployment.yaml** - Next.js application deployment and LoadBalancer service
- **app-secrets.yaml** - Application secrets (DO NOT commit with real values!)
- **app-secrets.example.yaml** - Template for secrets

## Deployment Steps

### 1. Create Namespace

```bash
kubectl apply -f namespace.yaml
```

### 2. Create Secrets

Copy the example and fill in real values:

```bash
cp app-secrets.example.yaml app-secrets.yaml
# Edit app-secrets.yaml with real credentials
kubectl apply -f app-secrets.yaml
```

### 3. Deploy Database

```bash
kubectl apply -f database-deployment.yaml
```

Wait for PostgreSQL to be ready:

```bash
kubectl wait --for=condition=ready pod -l app=postgres -n calendra --timeout=120s
```

### 4. Run Database Migrations

```bash
# Copy migration SQL to the pod
kubectl cp ../drizzle/migrations/0000_careful_mesmero.sql calendra/postgres-0:/tmp/migration.sql

# Execute migration
kubectl exec -n calendra -it deployment/postgres -- psql -U postgres -d calendra -f /tmp/migration.sql
```

### 5. Deploy Application

```bash
kubectl apply -f app-deployment.yaml
```

### 6. Get LoadBalancer IP

```bash
kubectl get svc -n calendra calendra-app-service
```

## Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n calendra

# Check logs
kubectl logs -n calendra -l app=calendra-app --tail=50

# Check database logs
kubectl logs -n calendra -l app=postgres --tail=50
```

## Update Deployment

After pushing a new image to Docker Hub:

```bash
# Restart deployment to pull latest image
kubectl rollout restart deployment/calendra-app -n calendra

# Check rollout status
kubectl rollout status deployment/calendra-app -n calendra
```

## Troubleshooting

```bash
# Describe pod for issues
kubectl describe pod -n calendra <pod-name>

# Access pod shell
kubectl exec -n calendra -it <pod-name> -- /bin/sh

# Port forward for local testing
kubectl port-forward -n calendra svc/calendra-app-service 3000:80
```

## Clean Up

```bash
# Delete all resources
kubectl delete -f app-deployment.yaml
kubectl delete -f database-deployment.yaml
kubectl delete -f app-secrets.yaml
kubectl delete -f namespace.yaml
```
