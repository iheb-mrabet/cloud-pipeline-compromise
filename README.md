# Cloud Pipeline Compromise Lab

End-to-end DevSecOps supply chain security lab.

## What I Built

- Jenkins CI security pipeline
- Gitleaks secret scanning
- Docker image build and push
- Cosign image signing
- GitHub Actions OIDC keyless signing
- GHCR image registry
- Kubernetes Sigstore policy-controller
- Admission control enforcement

## Security Model

Only images built and signed by my GitHub Actions workflow are allowed to run.

Unsigned images are blocked.

## Proof

Unsigned image blocked:

kubectl run bad-nginx -n secure-prod --image=nginx --restart=Never

Signed image allowed:

kubectl run good-signed-app -n secure-prod --image=ghcr.io/iheb-mrabet/cloud-pipeline-compromise/vulnerable-flask-app@sha256:29f3ee6039d4d966766395c313336e0d126de08cab57e0581ca34c4d96c847fd --restart=Never

Result:

good-signed-app   1/1   Running

## Stack

Docker, Jenkins, GitHub Actions, Cosign, GHCR, Kubernetes kind, Sigstore policy-controller.
