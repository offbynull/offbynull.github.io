`{title} Kubernetes`

```{toc}
```

# Introduction

`{bm} /(Introduction)_TOPIC/i`

Kubernetes is a service orchestration framework that provides many of the plumbing pieces required for running services. These services include ...

 * DNS for naming and discovery of services,
 * Load balancer to distribute requests across many instances of a service,
 * Automatic recovery when a service crashes,
 * Automatic scaling when a service comes under load,
 * Password / certificate / secrets management for services,
 * etc..

## Containers

`{bm} /(Introduction\/Containers)_TOPIC/i`

Kubernetes is structured around containers.

```{svgbob}
.-----------.                .-------.
| container +----------------+ image |
'-----------' 1+           1 '-------'
```

In the context of containers, an ...

 * image is an application (or set of applications) packaged with all of its dependencies as an immutable and isolated filesystem. The filesystem typically contains all dependencies required for the application(s) run sealed at their correct version:
 
   * libraries (e.g. correct version of libssh),
   * applications (e.g. correct version bash and Python),
   * files (e.g. embedded SQLite databases)
   * etc.. 

   Images also typically include metadata describing its needs and operational standards. For example, the metadata may stipulate that the image ...
   
   * launches by running /opt/my_app/run.sh
   * stops by signalling SIGTERM
   * requires 4gb of memory, 1.5 CPU cores, etc..A container is an instance of an application requires that services be exposed as container images. An image is 

 * container is an instance of an image. A container creates an isolated copy of the image's filesystem, isolates the resources required for that image, and launches the entrypoint application for that image. That container can't see or access anything outside of the container unless explicitly allowed to by the user. For example, opening a port 8080 on a container won't open port 8080 on the host running it, but the user can explicitly ask that port 8080 in the container map to some port on the host.

As shown in the entity diagram above, each container is created from a single image, but that same image can be used for to create multiple containers. Another way to think about it is that an image is the blueprint of a factory and a container is the actual factory built from that blueprint. You can build multiple factories from the same blueprint.

Kubernetes requires two core components to run:

 * open container initiative (OCI) runtime - A runtime responsible for only creating and launching containers.
 * container runtime interface (CRI) - A runtime responsible for the high-level management of containers and images: image management, image distribution, container mounts / storage, container networking, etc..

Different vendors provide different implementations of each. For example, certain vendors provide an OCI runtime that use virtualization technology for isolation instead of standard Linux isolation (e.g. cgroups).

```{svgbob}
.---------------------.
|      Kubernetes     |
+---------------------+
+-----+    OCR        |
| OCI |               |
'-----+---------------'
```

OCIs and OCRs are also the basis for container engines, tools that are responsible for creating and running containers (similar in nature Kubernetes without the orchestration) as well as creating images and other high-level functionality such as local testing of containers. Docker Engine is an example of a container engine.

```{svgbob}
.---------------------.
|  "Container Engine" |
+---------------------+
+-----+    OCR        |
| OCI |               |
'-----+---------------'
```

## Objects

`{bm} /(Introduction\/Objects)_TOPIC/i`

Kubernetes breaks down its orchestration as a set of objects. Each object is of a specific type (referred to as resource) and those objects coordinate and manage each other through linkages (described in Introduction/Labels_TOPIC). For example, a load balancer object is an instance of resource Service and each copy of a running application it pipes requests to is an instance of resource Pod, and the load balancer is decides which pods it to route to by searching for pods with a specific label.

This is in contrast to a hierarchal setup where objects have ownership or are inherited from others. There is no ownership or parent-child relationship here, only loosely coupled linkages.

```{svgbob}
 .-------.
 | L     |                           .-------------.
 | o     | *-----------------------* | application |
 | a     |                           |     POD     |
 | d   S |                           '-------------'
 |     E |                                          
 | B   R |                           .-------------.
 | a   V | *-----------------------* | application |
 | l   I |                           |     POD     |
 | a   C |                           '-------------'
 | n   E |                           
 | c     |                           .-------------.
 | e     | *-----------------------* | application |
 | r     |                           |     POD     |
 '-------'                           '-------------'
```

## Labels

`{bm} /(Introduction\/Labels)_TOPIC/i`

Objects within Kubernetes may be assigned key-value pairs. Two types of key-value pair assignments exist:

 * Labels - key-value assignments for logical grouping of Kubernetes objects. These allow for organizing objects into groups, such that users can target a group as a whole (e.g. give me all pods designed by the SRE team).
 * Annotations - key-value assignments for metadata on Kubernetes objects. These allow tools and libraries to gather ancillary information about the object, such that they can perform some task.

In other words, labels are used to identity objects while annotations are not. For example if you have different classes of worker nodes in your cluster, it may be a good idea to label each node with its class. That way, if you wanted to deprecate a specific class, you'd be able to targe them as a group and shut them down.

Labels are targeted using a simple language called label selectors.

| Operator                          | Description                                             |
|-----------------------------------|---------------------------------------------------------|
| `key=value`                       | `key` is set to `value`                                 |
| `key!=value`                      | `key` is not set to `value`                             |
| `key in (value1, value2, ...)`    | `key` is either `value1`, `value2`, ...                 |
| `key notin (value1, value2, ...)` | `key` is neither `value1`, `value2`, ...                |
| `key`                             | a value is set for `key`                                |
| `!key`                            | a value not set for `key`                               |
| `key1=value1,key2=value2`         | `key1` is set to `value1` and `key2` is set to `value2` |

Kubernetes uses labels for many of its internal services. For example, label selectors are used for deciding ...

 * the pods which a service routes traffic to.
 * which pods are allowed to communicate with each other over the internal network.
 * the nodes which a pod can be scheduled on.
 * etc..

If there are a large number of keys / annotations, either because the organization set them directly or because they're being set by external tools, the chance of a collision increases. To combat this, keys for labels and annotations can optionally include a prefix (separated by a slash) that maps to a DNS subdomain to help disambiguate it. For example, `company.com/my_key` rather than just having `my_key`.

```{note}
The book states that key name itself can be at most 63 chars. If a prefix is included, it doesn't get included in that limit. A prefix can be up to 253 chars.
```

## Configuration

`{bm} /(Introduction\/Configuration)_TOPIC/i`

Objects can either be accessed and mutated through a standard command-line interface called kubectl or a REST web interface. Manipulations come in two forms:

 * imperative configuration - the mutations to perform on the object (via kubectl invocations).

   ```
   kubectl run my_pod --image=gcr.io/my_company/my_pod:v1
   kubectl set pods my_pod --requests='cpu=500m,memory=128Mi'
   ```

 * declarative configuration - the overall description of the object, called a manifest (as YAML or JSON via either kubectl or REST).

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my_pod
   spec:
     containers:
       - image: gcr.io/my_company/my_pod:v1
         name: my_pod
         resources:
           requests:
             cpu: "500m"
             memory: "128Mi"
   ```

   ```
   kubectl apply -f obj.yaml
   ```

Generally, declarative configurations are preferred over imperative configurations. When a declarative configuration is submitted, Kubernetes runs a reconciliation loop in the background to automatically mutate the state of the object to the one in the manifest. Contrast this to the imperative configuration method, where the mutations have to be manually submitted by the user one by one.

# Resources

`{bm} /(Resources)_TOPIC/`

```{prereq}
Introduction_TOPIC
Introduction/Configuration_TOPIC
Introduction/Labels_TOPIC
```

The following sub-sections gives a overview of the main Kubernetes resources and example manifests. All manifests, regardless of the resource require the following fields...

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-name
  annotations:
    author: "Jimbo D."
    created_on: "Aug 20 2021"
  labels:
    app_server: jetty
```

... where `version` is the API version, `kind` is the resource (e.g. `Pod`), and `metadata.name` is the name of the object. In addition, the `metadata` section can contain labels and annotations to assign to the object via the `metadata.labels` and `metadata.annotations` manifest paths respectively.

## Pods

`{bm} /(Resources\/Pods)_TOPIC/i`

Containers are deployed in Kubernetes via pods. A pod is is a set of containers grouped together, often containers that are so tightly coupled or are required to work in close proximity of each other (e.g. on the same host).

```{svgbob}
.--------------------------------.
|               podA             |
|                                |
|  .------------.                |
|  | containerA | .------------. |
|  '------------' | containerB | |
| .------------.  '------------' |
| | containerC |                 |
| '------------'                 |
'--------------------------------'
```

Many copies of a pod may be running on the cluster at the same time, often in an effort to distribute load and / or provide redundancy.

```{svgbob}
.-----.                .--------------.
| pod +----------------+ pod template |
'-----' 1+           1 '--------------'
```

```{svgbob}
                      .---------.
                      |  podA   |
                      +---------+
                      | imageA  |    pod template
                      | imageB  |
                      | imageC  |
                      '----+----'
                           |
      .--------------------+-------------------.
      |                    |                   |
      v                    v                   v
.------------.      .------------.      .------------.
|    podA    |      |    podA    |      |    podA    |
+------------+      +------------+      +------------+
| containerA |      | containerA |      | containerA |     "running instances"
| containerB |      | containerB |      | containerB |
| containerC |      | containerC |      | containerC |
'------------'      '------------'      '------------'
```

Containers within a pod are isolated in terms of their resource requirements (e.g. CPU, memory, and disk), but they share the same ...

 * network (containers within a pod have the same IP, same host, and share the port space).
 * IPC bus (containers within a pod can communicate with each other over POSIX message queues / System V IPC channels).
 * volumes (containers within a pod may have shared storage assigned to them in addition to their isolated storage).

Kubernetes orchestrates containers over a cluster of machines. The containers for a pod are guaranteed to all be running on the same machine. As such, pods are usually structured in a way that their containers are tightly coupled and scale together. For example, a pod with two containers, a WordPress server and its required MySQL database server, is a bad usage example because those two ...

 1. don't scale uniformly (e.g. you'll likely need to scale the database up before the WordPress server).
 2. don't communicate over anything other than the network (e.g. they don't need a shared volume).
 3. are intended to be distributed (e.g. it's okay for them to be running on separate machines).

Contrast that to an example of a pod with two containers, an application server and an associated log watcher. This is a good example because the two containers ...

 1. communicate over the filesystem (e.g. application server is writing logs to a shared volume and the log watcher is tailing them).
 2. aren't intended to be distributed (e.g. log watcher is intended for locally produced logs).
 3. are written by different teams (e.g. SRE team wrote the log watcher image while another team wrote the application server image).

Example manifest:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my_pod
spec:
  containers:
    - image: gcr.io/my_company/my_pod:v1
      name: my_pod
      resources:
        requests:
          cpu: "500m"
          memory: "128Mi"
        limits:
          cpu: "1000m"
          memory: "256Mi"
      volumeMounts:
        - mountPath: "/data"
          name: "kuard-data"
      ports:
        - containerPort: 8080
          name: http
          protocol: TCP
      livenessProbe:
        httpGet:
          path: /healthy
          port: 8080
        initialDelaySeconds: 5
        timeoutSeconds: 1
        periodSeconds: 10
        failureThreshold: 3
      livenessProbe:
        httpGet:
          path: /ready
          port: 8080
        initialDelaySeconds: 5
        timeoutSeconds: 1
        periodSeconds: 10
        failureThreshold: 3
  volumes:
    - name: "my_data"
      hostPath:
        path: "/var/lib/my_data"  # literally mounts a path from the worker node? not persistant if node modes
    - name: "my_data_nfs"
      nfs:
        server: nfs.server.location
        path: "/path/on/nfs"
```

### Resources

`{bm} /(Resources\/Pods\/Resources)_TOPIC/`

`{bm-disable} resource`

Pod resources are controlled via the `spec.containers[].resources` manifest path.

```yaml
spec:
  containers:
    - ...
      resources:
        requests:
          cpu: "500m"
          memory: "128Mi"
        limits:
          cpu: "1000m"
          memory: "256Mi"
    ...
```

`requests` are the minimum resources the pod needs to operate while `limits` are the maximum it can have. Some resources are dynamically adjustable while others require the pod to restart. For example, a pod ...

 * can have its CPU usage dynamically adjusted because Kubernetes can just ask the operating system's CPU scheduler to give it less/more timer.
 * can't have its memory usage dynamically adjusted because if it loses access to a block of memory the applications running within the pod won't know and will likely crash.

The example above lists out CPU and memory as viable resource types. The unit of measurement for ...

 * cpu is either in ...
   * whole cores: no suffix
   * millicpus: suffix of m (1 core is equivalent to 1000m -- e.g. 0.5 = 5000m).
 * memory is either in ...
   * bytes: no suffix
   * 1000 scale: suffix of k = 1000, M = 1,000,000, G = 1,000,000,000
   * power of two scale: suffix of k = 1024, M = 1,048,576, G = 1,073,741,824

`{bm-enable} resource`

### Ports

`{bm} /(Resources\/Pods\/Ports)_TOPIC/`

Pod port exposures are controlled via the `spec.containers[].ports[]` manifest path.

```yaml
spec:
  containers:
    - ...
      ports:
        - containerPort: 8080
          name: http
          protocol: TCP
    ...
```

The example above exposes port 8080 to the rest of the cluster (not the outside world). Even with the port exposed, other entities on the cluster don't have a built-in way to discover the pod's IP / host or the fact that it has this specific port open. For that, services are required (see Resources/Services_TOPIC).

### Probes

`{bm} /(Resources\/Pods\/Probes)_TOPIC/`

Probes are a way for Kubernetes to check the state of a pod (e.g. alive, ready, started, etc..). The pod exposes some interfaces to determine state. Kubernetes periodically pings those interfaces to determine what actions to take (e.g. restarting a downed service.

Probes are controlled via the `spec.containers[].livenessProbe` and `spec.containers[].readinessProbe` manifest paths.

```yaml
spec:
  containers:
    - ...
      livenessProbe:
        httpGet:
          path: /healthy
          port: 8080
        initialDelaySeconds: 5
        timeoutSeconds: 1
        periodSeconds: 10
        failureThreshold: 3
      livenessProbe:
        httpGet:
          path: /ready
          port: 8080
        initialDelaySeconds: 5
        timeoutSeconds: 1
        periodSeconds: 10
        failureThreshold: 3
  ...
```

Different types of probes exists. A ...

 * liveness probe is something that Kubernetes pings to check if a pod is alive and responsive. If the pod fails to respond to such checks, Kubernetes deems it dead and restarts it.
 * readiness probe is something that Kubernetes pings to check if the pod is ready to process requests. When a pod initially comes online, before routing requests to it Kubernetes waits for its readiness probe to respond successfully.

In the example above, each of the probes check a HTTP server within the pod at port 8080 but at different paths. Other types of probes exist as well (e.g. `tcpSocket` instead of `httpGet`). The field ...

 * `initialDelaySeconds` is the number of seconds to wait before performing the first probe.
 * `timeoutSeconds` is the number of seconds to wait before timing out.
 * `periodSeconds` is the number of seconds to wait before performing a probe.
 * `failureThreshold` is the maximum number of successive failure before Kubernetes considers the probe failed.
 * `successThreshold` is the maximum number of successive successes before Kubernetes considers the probe passed.

### Volumes

`{bm} /(Resources\/Pods\/Volumes)_TOPIC/`

Volumes are controlled via the `spec.volumes[]` and `spec.containers[].volumneMounts` manifest paths ...

```yaml
spec:
  containers:
    - ...
      volumeMounts:
        - mountPath: "/data"
          name: "m_data"
      ...
  volumes:
    - name: "my_data"
      hostPath:
        path: "/var/lib/my_data"
```

`spec.volumes[]` defines a list of volumes, and those volumes can then go on to be mounted on the individual containers that make up the pod using `spec.containers[].volumneMounts`. In the example above, a volume is mounted on the container that points to a directory on the host machine. If other containers in that pod had that volume mounted, the directory on the host machine would be shared across all of them.

Multiple types of volumes exist. The volume type of ...

 * `hostPath` is a directory directly on the host machine running the pod (shared dir across containers in a pod).
 * `emptyDir` is a directory directly on the host machine running the pod (unshared temp dir per containers in a pod, guaranteed to be empty).
 * `nfs` is backed by NFS.
 * `cephfs` is backed by CephFS.
 * `awsElasticBlockStorage` is backed by AWS.
 * `azureDisk` is backed by Azure.

Others exist as well. Volume types are added / removed as Kubernetes updates between versions.

### Image Pull Policy

`{bm} /(Resource\/Pods\/Image Pull Policy)_TOPIC/`

Image pull policy is the policy Kubernetes uses for downloading a pod's images. It's controlled via the `spec.containers[].imagePullPolicy` manifest paths ...

```yaml
spec:
  containers:
  - ...
    imagePullPolicy: IfNotPresent
  ...
```

A value of ...

 * `IfNotPresent` only downloads the image if its not already locally present.
 * `Always` always downloads the image.
 * `Never` never downloads the image (will fail if image does not exist locally).

If unset, the pull policy differs based on the image tag. Not specifying a tag or specifying `latest` as the tag will always pull the image. Otherwise, the image will be pulled only if it isn't present.

### Restart Policy

`{bm} /(Resources\/Pods\/Restart Policy)_TOPIC/`

Restart policy is the policy Kubernetes uses for determining when a pod should be restarted. Its controlled via the `spec.containers[].restartPolicy` manifest paths ...

```yaml
spec:
  containers:
  - ...
    restartPolicy: Always
  ...
```

A value of ...

 * `Always` always restarts the pod regardless of how it exists (default).
 * `OnFailure` only restarts the pod only if it failed execution.
 * `Never` never restarts the pod.

The top one is typically used when running servers that should always be up (e.g. http server) while the latter two are typically used for one-off jobs.

### Configuration

`{bm} /(Resources\/Pods\/Configuration)_TOPIC/`

```{prereq}
Resources/Pods/Volumes_TOPIC
Configuration Map_TOPIC
```

```{note}
Do **NOT** use this for storing secrets such as tokens, certificates, or passwords. See Pods/Secrets_TOPIC.
```

Configuring the applications running under a pod is done through either command-line arguments, environment variables, files, or a mix of the three. Each has a different configuration method.

```yaml
spec:
  containers:
    - ...
      command:
        - "/my-app.sh"
        - "$(PARAM1)"
      env:
        - name: PARAM2
          valueFrom:
            configMapKeyRef:
              name: my-config
              key: key1
        - name: PARAM3
          valueFrom:
            configMapKeyRef:
              name: my-config
              key: key2
      volumeMounts:
        - name: config-volume
          mountPath: /config
  volumes:
    - name: config-volume
      configMap:
        name: my-config
```

To set a ...

 * environment variable to a ConfigMap key, use the following `valueFrom` stanza in `spec.containers[].env[]` ...
 
   ```yaml
   name: ENV_VAR_NAME
   valueFrom:
     configMapKeyRef:
     name: my-config
     key: CONFIG_MAP_KEY_HERE
   ```

 * command-line argument to a ConfigMap key, first set ito an environment variable, then set the argument to that environment variable by setting in `spec.containers[].command[]` using `${ENV_VAR_NAME}`.

 * file to a ConfigMap key (value is file's contents), create a `configMap` type volume and mount it to the container ...

   ```yaml
   spec:
     containers:
       - ...
         volumeMounts:
           - name: config-volume
             mountPath: /config
     volumes:
       - name: config-volume
         configMap:
           name: CONFIG_MAP_KEY_HERE
   ```

### Secrets

`{bm} /(Pods\/Secrets)_TOPIC/`

```{prereq}
Resources/Pods/Configuration_TOPIC
Resources/Pods/Volumes_TOPIC
```

Secrets are the standard way of storing application configurations related to security in Kubernetes (e.g. access tokens, passwords, certificates). Secrets can't be added through manifests or configuration maps. Instead, they must be added using kubectl. For example, ...

```
kubectl create secret generic my-tls-cert --from-file=a.crt --from-file=a.key
```

To use secrets in a pod, a specialized `secret` volume type must be used and mounted. For example, the following volume mounts the secrets created in the example command above ..

```yaml
spec:
  containers:
    - ...
      volumeMounts:
      - name: my-secrets
        mountPath: "/tls"
        readOnly: true
  volumes:
    - name: my-secrets
      secret:
        secretName: my-tls-cert
```

```{note}
Why not use ConfigMaps for secrets? Apparently there's some extra work going on to make sure this secrets volume is secure / transient.
```

## Nodes

`{bm} /(Resources\/Nodes)_TOPIC/i`

```{prereq}
Resources/Pods_TOPIC
```

Nodes are the machines that pods run on. A Kubernetes cluster often contains multiple nodes, each with a certain amount of resources. Pods get assigned to nodes based on their resource requirements. For example, if a pod A requires 2gb of memory and node C has 24 gigs available, that node may get assigned to run that pod.

```{svgbob}
.-------.    .-------.    .-------.
| nodeA |    | nodeB |    | nodeC |
+-------+    +-------+    +-------+
| podA  |    | podA  |    | podA  |
| podB  |    | podB  |    | podC  |
|       |    | podC  |    |       |
|       |    |       |    |       |
'-------'    '-------'    '-------'

* "nodeA running an instance of podA and podB"
* "nodeB running an instance of podA, podB, and podC"
* "nodeC running an instance of podA and podC"
```

Kubernetes typically attempts to schedule multiple instances of the same pod on different nodes, such that a downed node won't take out all instances of the service that pod runs. In the example above, pod instances of the same type are spread out across the 3 nodes.

Kubernetes has a leader-follower architecture, meaning that of the nodes a small subset is chosen to lead / manage the others. The leaders are referred to as master nodes while the followers are referred to as worker nodes.

```{svgbob}
.---------.      .---------.
| master1 |      | master2 |
'----+----'      '----+----'
     |                |
     | .------------. |
     +-|   worker1  |-+
     | '------------' |
     | .------------. |
     +-|   worker2  |-+
     | '------------' |
     | .------------. |
     +-|   worker3  |-+
     | '------------' |
     | .------------. |
     +-|   worker4  |-+
     | '------------' |
     | .------------. |
     +-|   worker5  |-+
       '------------'
```

A master node can still run pods just like the worker nodes, but some of its resources will be tied up for the purpose of managing worker nodes.

## Services

`{bm} /(Resources\/Services)_TOPIC/i`

```{prereq}
Resources/Pods_TOPIC
Resources/Nodes_TOPIC
```

Services are a discovery and load balancing mechanism. A service exposes a set of pods under a single fixed unified hostname and IP, routing traffic to that set by load balancing incoming requests across the set. Any external application would need to use a service's hostname because the IP / host of the single pod instances aren't fixed, exposed, or known. That is, pods are transient and aren't guaranteed to always reside on the same node. As they shutdown, come up, restart, move between nodes, etc.., there's no implicit mechanism that requestors can use to route their requests accordingly.

A service fixes this my internally tracking such changes and providing a single unified point of access.

```{svgbob}
.--------------------------------------.
|               serviceA               |
'--+---------------+---------------+---'
   |               |               |
   v               v               v
.------.        .------.        .------.
| podA |        | podA |        | podA |
'------'        '------'        '------'
```

```{note}
The book mentions why DNS can't be used directly. For example, having a basic DNS service which returns a list of all up-and-running pod IPs won't work because ...

1. applications and operating systems often cache DNS results, meaning that changes won't be visible immediately.
2. applications often only use the first IP given back by a DNS result, meaning that requests won't balance.

The service fixes this because it acts as a load balancing proxy and its IP / host never changes (DNS caching won't break anything).
```

Example manifest:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

### Routing

```{prereq}
Introduction/Labels_TOPIC
```

A service determines which pods it should route traffic to via the `spec/selector` manifest path. This manifest path contains key-value mappings, where these key-value mappings are labels that a pod needs before being considered for this service's traffic ...

```yaml
spec:
  selector:
    key1: value1
    key2: value2
    key3: value3
```

### Ports

```{prereq}
Resources/Pods/Ports_TOPIC
```

Requests are load balanced across the determined set of pods using ports defined via the `spec/ports` manifest path.

```yaml
spec:
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
    ...
```

`port` defines the port that the service listens on, while `targetPort` is the port requests are forwarded to on the pod. If `targetPort` is omitted, the value of `port` is assigned to it automatically.

### Health

```{prereq}
Resources/Pods/Probes_TOPIC
```

The service periodically probes the status of each pod to determine if it can handle requests or not. Two types of probes are performed:

 * liveness probes - When an existing instance of a pod fails a user-defined test that checks if it's still running, the service stops routing traffic to it.
 * readiness probes - When a new instance of a pod comes up, the service won't route traffic to it until it passes a user-defined test that says it's ready.

These probes are defined directly in the pod manifest.

```{svgbob}
.-------------------------------------------------------------.
|                             serviceA                        |
'------+-------------------------------+----------------------'
       |                               |                 
       v                               v
 .-----------.   .-----------.   .-----------.   .-----------.
 |   podA    |   |    podA   |   |   podA    |   |    podA   |
 |    OK     |   |  NOT LIVE |   |    OK     |   | NOT READY |
 '-----------'   '-----------'   '-----------'   '-----------'
```

```{note}
Internally, an EndPoints object is used to track pods. When you create a service, Kubernetes automatically creates an accompanying EndPoints object that the service makes use of.
```

### Exposure

TODO: CONTINUE FROM HERE
TODO: CONTINUE FROM HERE
TODO: CONTINUE FROM HERE
TODO: CONTINUE FROM HERE
TODO: CONTINUE FROM HERE
TODO: CONTINUE FROM HERE
TODO: CONTINUE FROM HERE
TODO: CONTINUE FROM HERE

The service type defines where and how a service gets exposed. For example, a service may only be accessible within the cluster, to specific parts of the cluster, to an external network, to the Internet, etc...

Services of type ClusterIP are only accessible from within the cluster. The hostname for a ClusterIP service is broken down as follows: NAME.NAMESPACE.svc.CLUSTER

 * *NAME* is the name of the service.
 * *NAMESPACE* is the namespace the service is in (defaults to `default`).
 * svc is a constant that identifies the host is for a service.
 * *CLUSTER* is the name of the cluster (defaults to `cluster.local.`).

Depending on what level you're working in, a hostname may be shortened. For example, if the requestor and the service are within ...

 * the same namespace and cluster, hostname NAME is sufficient.
 * the same cluster but not the same namespace, hostname NAME.NAMESPACE is sufficient.
 * different clusters, the full hostname NAME.NAMESPACE.svc.CLUSTER is required.

The IP for a ClusterIP service is stable as well, just like the hostname.

```{note}
Internally, a ClusterIP service uses kube-proxy to route requests to relevant pods (EndPoints).
```

TODO: Add sample YAML

Services of type NodePort are accessible from outside the cluster. Every worker node opens a port (either user-defined or assigned by the system) that routes requests to the service. Since nodes are transient, there is no single point of access to the service.

TODO: Add sample YAML

Services of type LoadBalancer are accessible from outside the cluster. When the LoadBalancer type is used, the cloud provider running the cluster assigning their version of a load balancer to route external HTTP requests to the Kubernetes Ingress component. Ingress then determines what service that request should be routed to based on details within the HTTP parameters (e.g. Host).

There is no built-in Kubernetes implementation of Ingress. Kubernetes provides the interface but someone must provide the implementation, called an Ingress controller, for the functionality to be there. The reason for this is that load balancers come in multiple forms: software load balancers, cloud provider load balancers, and hardware load balancers. When used directly, each has a unique way it needs to be configured, but the Ingress implementation abstracts that out.

TODO: Add sample YAML

## Replica Sets

`{bm} /(Resources\/Replica Sets)_TOPIC/i`

```{prereq}
Resources/Pods_TOPIC
```

A replica set is an abstraction that's used to ensure a certain number of copies of some pod are always up and running. Typical scenarios where replica sets are used include ...

 * sharding (e.g. workers that pull job out of a queue for processing).
 * scale (e.g. microservices that scale horizontally).
 * redundancy (e.g. leader-follower architectures such as Redis-style replica servers).

## Deployments

`{bm} /(Resources\/Deployments)_TOPIC/i`

```{prereq}
Resources/Services_TOPIC
Resources/Replica Sets_TOPIC
```

A deployment is an abstraction used to bring together pods, replica sets, and services under a single umbrella. It's intended to represent a single version of some application being deployed on Kubernetes. All of the pieces required for that application to run are housed under one roof.

Deployments make it easy to upgrade between versions of the applications they represent via a rolling upgrade that keeps the application online during the upgrade. Old pods are transitioned to new pods as a stream instead of all at once, ensuring that the application is responsive throughout the upgrade process. Likewise, they allow for rolling back an update should it have any problems.

## Daemon Sets

`{bm} /(Resources\/Daemon Sets)_TOPIC/i`

```{prereq}
Resources/Replica Sets_TOPIC
Resources/Deployments_TOPIC
```

A daemon set is an abstraction that's used to ensure that a set of nodes each have a copy of some pod always up and running. Typical scenarios where a daemon set is used include ...

 * node log collection (e.g. logstash agent).
 * node monitoring (e.g. zabbix agent).

The above scenarios are ones which break container / pod isolation. That is, a daemon set is intended to run pods that are coupled to nodes and sometimes those pods will do things such as mount the node's root filesystem and run commands to either install software or gather information.

Similar to how a replica set has a corresponding deployment that helps with upgrades, a daemon set has a daemon sets object that helps manage its upgrades.

## Jobs

`{bm} /(Resources\/Jobs)_TOPIC/i`

```{prereq}
Resources/Pods_TOPIC
Resources/Deployments_TOPIC
```

A job is an abstraction that's used to run a set of pods performing a one-off task. Unlike a deployment, the pods running under a job don't need the same level of management (e.g. multiple replicas, upgrade strategies, etc..). Once a job completes, it's over.

Typical scenarios where a job is used include ...

 * database migration
 * database compaction
 * log file removal

Jobs can also be scheduled to run at specific intervals / times.


# Replica Set

```yaml
apiVersion: v1
kind: ReplicaSet
metadata:
  name: my-rs
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: my-app
        version: "2"
    spec:
      containers:
        - name: my_container
          image: "gcr.io/my_container:v1"
```

The number of replicas the replica set should aim for is controlled by `spec/replicas`.

Note that the manifest for the replica set includes the manifest of the pods it should create. This is called a pod template.

You can distinguish a pod created by a replica set vs one created manually by checking the annotation key `kubernetes.io/create-by` on the pod.

```{note}
If deleting a replica set, use `--cascade=false` in kubectl if you don't want the pods created by the replica set to get deleted as well.
```

## Autoscaling

TODO: TALK ABOUT HORIZONTAL AUTOSCALING + yaml

The number of replicas in a replica set can be automatically scaled up an down through Kubernetes's horizontal pod autoscaling component. Replicas are scaled based on some user-defined criteria (e.g. high cpu usage).

```{note}
This feature depends on a pod called heapster that tracks metrics. Most Kubernetes installations include it by default.
```

```{note}
The book warns about setting replicas manual and setting replicas using HPA -- they fight with each other.
```

TODO: talk about vertical autoscaling + yaml -- it looks like this is in beta?

# Deployment

```yaml
apiVersion: v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: my_container
          image: "gcr.io/my_container:v1"
```

Note that the manifest for the deployment includes the manifest of the replicaset.

Add `kubernetes.io/change-cause` annotation to add a custom message for the deployment, viewable when browing the history of the rollout

## Strategy

TODO: `spec/strategy` defines the way rollouts should occur.

TODO: discuss the recreate strategy + add yaml -- one-shot update, everything shuts down and restarts

TODO: discuss the rolling update strategy + add yaml --

maxUnavailable (num or percent of pods that can be down during rollout) / maxSurge (num or percent of EXTRA pods that can be running during the rollout) -- so if you set unavail to 0% and surge to >0% (it'll bring up x% new pods first then shut down x% old pods, repeat until all updated), it'll rollout faster vs if you set unavail to > 0% and surge to 0% (it'll shutdown x% old pods first then bring up x% new pods, repeat until all updated)

for rolling, it'll always wait till the current iterations new pods probes report healthy + ready before moving to next iteration -- you should have defined these probes otherwise deployments are blind

minReadySeconds -- waits at least n seconds till the readiness probe reports okay before continuing -- an extra wait to make sure nothing's immediately crashing

progressDeadlineSeconds -- if any stage of the rollout waits for this long, the rollout is marked as failed. each time pods are brought down / up, it's a stage



## Undo

TODO: discuss kubectl rollout undo deployments {DEPLOYMENT} command to roll back

TODO: set spec/revisionHistoryLimit to limit the number of revisions kept for undo -- useful when many frequent updates are happening

# Daemon Set

```yaml
apiVersion: v1
kind: DaemonSet
metadata:
  name: my-ds
spec:
  template:
    spec:
      nodeSelector:
        node_label_key1: value1
        node_label_key1: value2
      containers:
      - name: my-app
        image: my-app/my-app:v1
        resources:
          limits:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
          readOnly: true
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
```

TODO: spec/template/spec/nodeSelector defines the node labels to target

TODO: notice how volumes are using hostPath, which goes into the node directly

# Daemon Sets

TODO: this is the equivalent of deployment for daemon set, it has rollingupdates just like a deployment does

# Job

```yaml
apiVersion: v1
kind: Job
metadata:
  name: my-job
spec:
  parallelism: 5
  completions: 10
  template:
    spec:
      containers:
      - name: my-app
        image: gcr.io/my-app:v1
        imagePullPolicy: Always
        args:
        - "--arg1"
        - "--arg2"
      restartPolicy: OnFailure   # restart pod if it didn't complete successfully, can also be Never
```

TODO: for one-off tasks, defined using pod templates

TODO: parallelism defines how many of the pods run at once, completion is how many need to complete

TODO: kubectl is the easiest way to run jobs? looks confusing see ch12. job needs to be explicitly deleted once it's finished

TODO: don't use labels, because people create lots of jobs and if you start labeling pods and there's a naming conflict bad/unexpected things happen (ch12)

TODO: don't set restartPolicy to never, because what happens is that the internal component responsible for restarts won't restart it and as such the job will see it hasn't restarted and restart it itself. this causes a lot of junk in the cluster.

TODO: liveness probes can be used to detect if the a pod is dead in a job as well

TODO: use CronJob type to have it be scheduled by time

# Configuration Map

`{bm} /(Configuration Map)_TOPIC/`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  param1: another-value
  param2: extra-value
  my-config.ini: |
    # This is a sample config file that I might use to configure an application
    key1 = value1
    ket1 = value2
```

# Cluster Autoscaler

TODO: it looks like this is an external component? if not enough resources to run a pod, provision more nodes from the cloud provider

# Kubectl Cheatsheet

kubectl commands are typically organized into contexts, where each context is defines contextual information about the cluster: cluster location, cluster authentication, and default namespace. To ...

 * set location, `kubectl config set-context {CTX} --cluster={VAL}`
 * set user, `kubectl config set-context {CTX} --user={VAL}`
 * set namespace, `kubectl config set-context {CTX} --namespace={VAL}`
 * use a context, `kubectl config use-context {CTX}`

Context information is usually stored in `$HOME/.kube/config`.

kubectl commands that target an object require a namespace. That namespace can either be supplied via ...

 * `--namespace={NS}` argument to target a specific namespace,
 * `--all-namespaces` argument to target all namespaces,

, ... or through the default namespace set for the current context. If not set explicitly in the context, the namespace will be `default`.

Kubernetes API is exposed as a RESTful interface, meaning everything is represented as an object and accessed / mutated using standard REST verbs (GET, PUT, DELETE, etc..). kubectl uses this interface to access the cluster. For example, accessing https://cluster/api/v1/namespaces/default/pods/obn_pod is equivalent to running `kubectl get pod obj_pod`. The difference between the two is that by default kubectl formats the output in a human friendly manner, often omitting or shortening certain details. That output can be controlled using flags. Specifically, to ...

 * get more detail, use `-o wide`.
 * remove headers such that the output can be more easily piped to other tools like `wc`, use `--no-headers`.
 * get JSON output `-o json`
 * get YAML output `-o yaml`
 * get JSON output isolated to a specific field or fields `-o jsonpath --template={TEMPLATE}`, where the template is a JSONPath expression.

## CRUD

`get` / `describe` allows you to get details on a specific objects and resources. To get an overview of a ...

 * list of all objects of a specific resource type using `kubectl get {RES}`.
 * a specific object of a specific resource type using `kubectl get {RES} {OBJ}`.

`describe` provides more in-depth information vs `get`.

Examples of object access:

 * `kubectl get componentstatuses` - basic cluster diagnostics
 * `kubectl get nodes` - list nodes
 * `kubectl get nodes --selector='class=high-mem'` - list nodes that have label class set to high-mem (label selector)
 * `kubectl get nodes --selector='class=high-mem,!gpu'` - list nodes that have label class set to high-mem but label gpu unset (label selector)
 * `kubectl describe nodes {NAME}` - node information
 * `kubectl get daemonSets --namespace={NAMESPACE} {NAME}`
 * `kubectl get deployments --namespace={NAMESPACE} {NAME}`
 * `kubectl get services --namespace={NAMESPACE} {NAME}`

Add `--watch` flag to have kubectl continually provide updates.

`apply` allows you to create and update objects. To create or update using ...

 * a YAML file, `kubectl apply -f obj.yaml`.
 * a JSON file, `kubectl apply -f obj.json`.
 * STDIN, `kubectl apply -f -`.

It will not allow you to delete objects.

```{note}
Is this true? See `kubectl apply` with prune flag.
```

`edit` is shorthand for `get` and `apply` in that it'll open the YAML in an editor and allow you to make changes directly.

 * `kubectl edit deployment {NAME}`
 * `kubectl edit service {NAME}`

`delete` allows you to delete an object. To delete using ...

 * a YAML file, `kubectl delete -f obj.yaml`.
 * a JSON file, `kubectl delete -f obj.json`.
 * STDIN, `kubectl apply -f -`.
 * command line, `kubectl delete {RES} {OBJ}`

In certain cases, the object being deleted has parental links to other objects. For example, a replica set is the parent of the pods it creates and watches. If you delete these parent objects, by default their children go with it unless the `--cascade=false` flag is used.

`label` / `annotate` allows you to label / annotate an object.

 * `kubectl label pods {POD} mark=55a` - set label mark to value 55a on a pod (no overwrite).
 * `kubectl label --overwrite pods {POD} mark=77a` - overwrite label mark to value 77a on a pod.
 * `kubectl label --overwrite pods {POD} mark=77a,end=fff` - overwrite label mark to value 77a and end to value fff on a pod.
 * `kubectl label pods {POD} mark-` - remove label mark from a pod.

When referencing objects, the ...

 * `--selector` flag can be fed in a label selector that filters those objects.
 * `--all` flag can target everything.

## Deployment

`rollout` allows you to monitor and control deployment rollouts.

 * `kubectl rollout status deployments {DEPLOYMENT}` - monitor rollout
 * `kubectl rollout pause deployments {DEPLOYMENT}` - pause rollout
 * `kubectl rollout resume deployments {DEPLOYMENT}` - resume rollout
 * `kubectl rollout history deployments {DEPLOYMENT}` - view rollout history
 * `kubectl rollout undo deployments {DEPLOYMENT}` - undo rollout (works regardless state -- e.g. if a rollout is currently in progress or not)
 * `kubectl rollout undo deployments {DEPLOYMENT} --to-revision={REV}` - undo rollout to a previous revision (see rollout history command)

`configmap` allows you to create a configuration for applications running in pods.

 * `kubectl create configmap {CONFIGMAP} --from-file=my-config.txt --from-literal=key1=value1 --from-literal=key2=value2`

`secret` allows you to create a security related configuration for applications running in pods.

 * `kubectl create secret generic my-tls-cert --from-file=a.crt --from-file=a.key`

## Proxy

`proxy` allows you to launch a proxy that lets you talk internally with the Kubernetes API server.

 * `kubectl proxy`

## Debug

`logs` allows you to view outputs of a container.

 * `kubectl logs {POD}` - get logs for a single container pod.
 * `kubectl logs {POD} -c {CONTAINER}` - get logs for a container within a pod.
 * `kubectl logs {POD} -c {CONTAINER} -f` - tail logs for a container within a pod.

`exec` allows you to run a command on a container.

 * `kubectl exec -it {POD} -- ps uax` - execute ps on a single container pod.
 * `kubectl exec -it {POD} -- bash` - execute bash on a single container pod and interact with it.
 * `kubectl exec -it {POD} -c {CONTAINER} -- bash` - execute bash on a container within pod and interact with it.

`attach` allows you to attach to a container's main running process.

 * `kubectl attach -it {POD}` - attach to main process on a single container pod.
 * `kubectl attach -it {POD} -c {CONTAINER}` - attach to main process on a container within a pod.

```{note}
`attach` is similar to `logs` with the tailing flag but also allows you pipe into stdin.
```

`cp` allows you to copy files between your machine and a container.

 * `kubetctl cp {POD}:{POD_PATH} {LOCAL_PATH}` - copy from single container pod to local path.
 * `kubetctl cp {LOCAL_PATH} {POD}:{POD_PATH}` - copy from local path to a single container pod.
 * `kubetctl cp {POD}:{POD_PATH} {LOCAL_PATH} -c {CONTAINER}` - copy from a container within a pod to local path.

`port-forward` allows you to connect to a open port on a container or connect to a service.

 * `kubectl port-forward {POD} 8080:80` - forward port 8080 locally to port 80 on a single container pod.
 * `kubectl port-forward {POD} 8080:80 -c {CONTAINER}` - forward port 8080 locally to port 80 on a container within a pod.
 * `kubectl port-forward services/{SERVICE} 8080:80` - forward port 8080 locally to port 80 for some service.

`top` allows you to see cluster usage.

 * `kubectl top nodes` - view node resource usages.
 * `kubectl top pods` - view pod resource usages.

# Terminology

 * `{bm} resource` - A class of Kubernetes object (e.g. pod, replica set, deployment, etc..). 

 * `{bm} image` - An application (or set of applications) packaged with all of its dependencies as an immutable and isolated filesystem. The filesystem typically contains all dependencies required for the application(s) run sealed at their correct version.

   Images also typically include metadata describing its needs and operational standards (e.g. memory requirements).

 * `{bm} container` - An instance of an image. A container creates an isolated copy of the image's filesystem, isolates the resources required for that image, and launches the entrypoint application for that image. That container can't see or access anything outside of the container unless explicitly allowed to by the user. For example, opening a port 8080 on a container won't open port 8080 on the host running it, but the user can explicitly ask that port 8080 in the container map to some port on the host.

 * `{bm} registry` - A service for storing and retrieving images.

 * `{bm} multistage image/(multistage build|multistage image|multistage container image)/i` - A container image produced by merging portions of other container images together. For example, to build a multistage image that contains Java as well as compiled C++ binaries, ...

   1. an image containing the JVM has its Java directory pulled out.
   2. an image containing the GNU Compiler toolchain compiles some C++ code, then those compiled binaries are pulled out.

   The end result is that the multistage build only contains the relevant portions of its "stages" (previous images), leading to a more focused image with smaller size.

 * `{bm} open container initiative runtime/(Open Container Initiative runtime|Open Container Initiative)/i`  `{bm} /\b(OCI runtime|OCI)s?\b//false/true`- A runtime responsible for only creating and launching containers. Examples include runC, rkt, runV, gviso, etc.. Some of these use Linux isolation technology (cgroups and namespaces) while others use virtualization technology.

 * `{bm} container runtime interface` `{bm} /\b(CRI)s?\b//false/true` - A runtime responsible for the high-level management of containers and images: image management, image distribution, container mounts / storage, container networking, etc..
 
   CRIs are also responsible for running containers, but typically do so by delegating to an OCI runtime. Examples of CRIs include containerd, and cri-o.

 * `{bm} container engine` - A high-level application / cohesive set of applications used for all the things OCI runtimes and CRIs are used for as well as building images, signing images, and several other extra features. Container engines typically delegate to OCI runtimes and CRIs for most of their functionality.
 
   Examples include Docker Engine and Container Tools (podman for running containers, buildah for building images, and skopeo for image distribution).

 * `{bm} Kubernetes` - A tool for orchestrating multiple containers across a set machines. Provides features such as load balancing, service naming, service discovery, automated service scaling, and automated service recovery.

 * `{bm} node` - A host that Kubernetes uses to run the containers its orchestrating.

 * `{bm} master node` - A node responsible for the managing the cluster (scheduling, API server, etc..).

 * `{bm} worker node` - A node responsible for running application containers.

 * `{bm} pod/\b(pod)s?\b/i` - A set of containers all bundled together as a single unit, where all containers in that bundle are intended to run on the same node.

 * `{bm} pod template` - The blueprint for creating pods.

 * `{bm} namespace` - A user-defined category for objects in a cluster (e.g. pods), allowing Kubernetes do things such as apply isolation and access control. By default, the kubectl command uses the namespace `default` if no namespace is specified.

   ```{note}
   The book tells you to think of it like it's a folder.
   ```

 * `{bm} kube-system` - A namespace for internal cluster components (pods) that Kubernetes runs for itself. For example, Kubernetes's DNS service, Kubernetes's proxy service, etc.. all run under the kube-system namespace.

 * `{bm} kube-proxy/(kube-proxy|Kubernetes proxy|Kubernetes's proxy)/i` - An internal Kubernetes proxy service responsible for routing traffic to the correct services and load balancing between a service's pods. Runs on every node in the cluster.

 * `{bm} core-dns/(core-dns|kube-dns|Kubernetes DNS|Kubernetes's DNS)/i` - An internal Kubernetes DNS service responsible for naming and discovery of the services running on the cluster. Older versions of Kubernetes call this kube-dns instead of core-dns.

 * `{bm} kubernetes-dashboard/(kubernetes-dashboard|Kubernetes Dashboard|Kubernetes UI|Kubernetes GUI|Kubernetes's Dashboard|Kubernetes's UI|Kubernetes's GUI)/i` - An internal Kubernetes service responsible for providing a GUI to interface with and explore the cluster.

 * `{bm} kubectl` - The standard command-line client for Kubernetes.

 * `{bm} context` - In reference to kubectl, context refers to default cluster access settings kubectl applies when running some command: cluster location, cluster authentication, and default namespace.

 * `{bm} label` - User-defined key-value pairs assigned to Kubernetes objects to group those objects together. Labeling objects makes it so they can be accessed as a set (e.g. target all pods with authoring team set to SRE). Unlike annotations, labels aren't for assigning metadata to objects.

 * `{bm} label selector` - An expression language used to find objects with labels. For example...

   * `key=value`
   * `key!=value`
   * `key in (value1, value2)`

 * `{bm} annotation/(annotation|annotate)/i` - User-defined key-value pairs assigned to Kubernetes objects that acts as metadata for other tools and libraries. Unlike labels, annotations aren't for grouping objects together.

 * `{bm} declarative configuration` - A form of configuring where the configuration is submitted as a state and the system adjusts itself to match that state.

 * `{bm} imperative configuration` - A form of configuring where the configuration is submitted as a set of instructions and the system runs those instructions.

 * `{bm} pod manifest` - A declarative configuration for a pod, listing out things like images required and resource mappings (e.g. ports). This is effectively a blueprint for a pod, similar to how an image is a blueprint for a container.

 * `{bm} health check` - A Kubernetes mechanism that checks the state of pods and performs corrective action if it deems necessary. This includes both ensuring that the main container process is running, liveness probes, and readiness probes.

 * `{bm} liveness probe` - A user-defined task that Kubernetes runs to ensure that a pod is running correctly. For example, an HTTP server that stalls when for more than 15 seconds before returning a response may be deemed as no longer live.

   Kubernetes restarts a pod if it deems it as no longer alive.

 * `{bm} readiness probe` - A user-defined task that Kubernetes runs to ensure that a pod is in a position to accept requests. For example, an HTTP server that has all of its worker threads busy processing requests may be deemed as not ready.

   Kubernetes stops routing requests to a pod if its no longer ready (removed from load balancer).

 * `{bm} utilization` - A metric that tracks the amount of resources in use vs the amount of resources available.

 * `{bm} resource request` - The minimum amount of resources required to run an image (not a pod).

 * `{bm} resource limit` - The maximum amount of resources that an image (not a pod) may take up.
 
   If Kubernetes needs to scale down a resource for a container that isn't dynamic (e.g. a running process can have its CPU usage reduced but you can't force a running process to give up memory its holding on to), the pod gets restarted with that resource scaled down.

 * `{bm} service` - A set of pods exposed under a single named network service. Requests coming in to the service and are load balanced across the set of pods.

 * `{bm} endpoints` - A low-level object that's used by Kubernetes to map a service to the pods it routes to. In other words, an endpoints (note the plural) object is an abstraction that references a pod.

 * `{bm} ingress` - A Kubernetes resource that acts as an HTTP-based frontend that routes and load balances incoming external requests to the correct service. This resource is an interface without an implementation, meaning that Kubernetes doesn't have anything built-in to handle ingress. Implementations of this interfaces are referred to as Ingress controllers and are provided by third-parties.

 * `{bm} replica set` `{bm} /(ReplicaSet)/` - A Kubernetes resource that ensures a pod has a certain number of instances running at any time.

 * `{bm} reconciliation loop` - A loop that continually observes state and attempts to reconcile it to some desired state if it deviates. See declarative configuration.

 * `{bm} horizontal pod autoscaling` `{bm} /\b(HPA)\b/` - A feature that automatically scales the number of replicas in a replica sets based on user-defined criteria.

 * `{bm} vertical pod autoscaling` `{bm} /\b(VPA)\b/` - A feature that automatically scales up the resource requirements for some pod based on user-defined criteria.

 * `{bm} cluster autoscaler` - A component that automatically scales the number of nodes in a cluster based on need.

 * `{bm} deployment` - A Kubernetes resource that groups together all objects required for some application (e.g. pods, services, ...).

 * `{bm} daemon set` `{bm} /(DaemonSet)/` - A Kubernetes resource that ensures a set of nodes always have an instance of some pod running.

 * `{bm} job` - A Kubernetes resource that launches as a pod to perform some one-of task.

 * `{bm} ConfigMap` - A Kubernetes resource for configuring the applications running in a pod.

 * `{bm} millicpu/(millicpu|millicore)/i` - A millicpu is 0.001 CPU cores (e.g. 1000 millicpu = 1 core).

`{bm-error} Did you mean endpoints?/(endpoint)/i`

`{bm-error} Missing topic reference/(_TOPIC)/i`