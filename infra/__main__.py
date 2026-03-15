import pulumi
import pulumi_kubernetes as k8s

app_labels = {"app": "holidays-api"}

config = pulumi.Config()
app_env = config.get("appEnv")
image = config.get("image")
cpu_request = config.require("cpuRequest")
cpu_limit = config.require("cpuLimit")
memory_request = config.require("memoryRequest")
memory_limit = config.require("memoryLimit")

deployment = k8s.apps.v1.Deployment(
    "holidays-api",
    spec={
        "selector": {"matchLabels": app_labels},
        "replicas": 1,
        "template": {
            "metadata": {"labels": app_labels},
            "spec": {
                "containers": [{
                    "name": "holidays-api",
                    "image": image,
                    "ports": [{"containerPort": 5000}],
                    "resources": {
                        "requests": {
                            "cpu": cpu_request,
                            "memory": memory_request
                        },
                        "limits": {
                            "cpu": cpu_limit,
                            "memory": memory_limit
                        }
                    },
                    "env": [{
                        "name": "APP_ENV",
                        "value": app_env
                    }]
                }]
            },
        },
    })

service = k8s.core.v1.Service(
    "holidays-api-service",
    spec={
        "selector": app_labels,
        "ports": [{
            "port": 80,
            "targetPort": 5000
        }],
    })

ingress = k8s.networking.v1.Ingress(
    "holidays-api-ingress",
    spec={
        "rules": [{
            "host": "holidays.local",
            "http": {
                "paths": [{
                    "path": "/",
                    "pathType": "Prefix",
                    "backend": {
                        "service": {
                            "name": service.metadata["name"],
                            "port": {"number": 80}
                        }
                    }
                }]
            }
        }]
    })


pulumi.export("service_name", service.metadata["name"])
