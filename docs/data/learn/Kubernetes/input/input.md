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

 * image is an application (or set of applications) packaged with all of its dependencies as an immutable and isolated filesystem. The filesystem typically contains all dependencies required for the application(s) to run sealed at their correct version:
 
   * libraries (e.g. correct version of libssh),
   * applications (e.g. correct version bash and Python),
   * files (e.g. embedded SQLite databases)
   * etc.. 

   Images also typically include metadata describing its needs and operational standards. For example, the metadata may stipulate that the image ...
   
   * launches by running /opt/my_app/run.sh
   * requires 4gb of memory, 1.5 CPU cores
   * etc..

 * container is an instance of an image. A container creates an isolated copy of the image's filesystem, isolates the resources required for that image, and launches the entry point application for that image. That container can't see or access anything outside of the container unless explicitly allowed to by the user. For example, opening a port 8080 on a container won't open port 8080 on the host running it, but the user can explicitly ask that port 8080 in the container map to some port on the host.

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

OCIs and OCRs are also the basis for container engines. Container engines tools responsible for creating and running containers, creating images, and other high-level functionality such as local testing of containers. Docker Engine is an example of a container engine.

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

Kubernetes breaks down its orchestration as a set of objects. Each object is of a specific type, referred to as kind. The main kinds are ...

 * Node - A physical worker machine that runs containers.
 * Pod - A set of containers tightly coupled to run in unison on a single node.
 * Volume - A storage mechanism that lets pods persist and / or share data.
 * Service - A load balancer that routes traffic to pods.
 * Configuration Map - A configuration mechanism for applications running within pods (non-security related configurations).
 * Secret - A security configuration mechanism for applications running within pods (e.g. passwords as certificates).
 * Ingress - An access point in which traffic comes in from the outside world to the internal Kubernetes network.

Of these kinds, the two main ones are nodes and pods.

```{svgbob}
.----------------------------------------------------------.  .---------------------.
|                         node1                            |  |        node2        |
|                                                          |  |                     |
| .--------------------------------.   .----------------.  |  | .----------------.  |
| |               podA             |   |      podB      |  |  | |      podC      |  |
| |  .------------.                |   | .------------. |  |  | | .------------. |  |
| |  | containerA | .------------. |   | | containerD | |  |  | | | containerF | |  |
| |  '------------' | containerB | |   | '------------' |  |  | | '------------' |  |
| | .------------.  '------------' |   | .------------. |  |  | '----------------'  |
| | | containerC |                 |   | | containerE | |  |  '---------------------'
| | '------------'                 |   | '------------' |  |
| '--------------------------------'   '----------------'  |
'----------------------------------------------------------'
```

Nodes, pods, and other important kinds are discussed further on in this document.

```{seealso}
Kinds_TOPIC (Discussion of common kinds)
```

```{note}
The terminology here is a bit wishy-washy. Some places call them kinds, other places call them resources, other places call them classes, and yet other places call them straight-up objects (in this case, they mean kind but they're saying object). None of it seems consistent and sometimes terms are overloaded, which is why it's been difficult piecing together how Kubernetes works.

I'm using kind to refer to the different types of objects, and object to refer to an instance of a kind.
```

## Labels

`{bm} /(Introduction\/Labels)_TOPIC/i`

```{prereq}
Introduction/Objects_TOPIC
```

An object can have two types of key-value pairs associated with it:

 * Labels - These key-value pairs organize objects into logical groups, such that those groups can be targeted as a whole (e.g. give me all pods designed by the SRE team).
 * Annotations - These key-value pairs allow tools to gather and share information about an object (e.g. when was this object created).

Finding objects based on labels is done via label selectors, described in the following table.

| Operator                          | Description                                             |
|-----------------------------------|---------------------------------------------------------|
| `key=value`                       | `key` is set to `value`                                 |
| `key!=value`                      | `key` is not set to `value`                             |
| `key in (value1, value2, ...)`    | `key` is either `value1`, `value2`, ...                 |
| `key notin (value1, value2, ...)` | `key` is neither `value1`, `value2`, ...                |
| `key`                             | a value is set for `key`                                |
| `!key`                            | a value not set for `key`                               |
| `key1=value1,key2=value2`         | `key1` is set to `value1` and `key2` is set to `value2` |

Kubernetes uses labels to orchestrate. Labels allow objects to have loosely coupled linkages to each other as opposed to tightly coupled parent-child / hierarchy relationships. For example, a load balancer decides which pods it routes requests to by searching for pods using label selector.

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

If there are a large number of keys / annotations, either because the organization set them directly or because they're being set by external tools, the chance of a collision increases. To combat this, keys for labels and annotations can optionally include a prefix (separated by a slash) that maps to a DNS subdomain to help disambiguate it. For example, `company.com/my_key` rather than just having `my_key`.

```{note}
The book states that key name itself can be at most 63 chars. If a prefix is included, it doesn't get included in that limit. A prefix can be up to 253 chars.
```

## Configuration

`{bm} /(Introduction\/Configuration)_TOPIC/i`

Objects can either be accessed and mutated through a standard command-line interface called kubectl or a REST web interface. Manipulations come in two forms:

 * imperative configuration - the mutations to perform on the object (via kubectl invocations).

   ```
   kubectl run my_pod --image=my-image:1.0
   kubectl set pods my_pod --requests='cpu=500m,memory=128Mi'
   ```

 * declarative configuration - the overall description of the object, called a manifest (as YAML or JSON via either kubectl or REST).

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-pod
   spec:
     containers:
       - image: my-image:1.0
         name: my-container
         resources:
           requests:
             cpu: "500m"
             memory: "128Mi"
   ```

   ```
   kubectl apply -f obj.yaml
   kubectl delete -f obj.yaml
   ```

Generally, declarative configurations are preferred over imperative configurations. When a declarative configuration is submitted, Kubernetes runs a reconciliation loop in the background to automatically mutate the state of the object to the one in the manifest. Contrast this to the imperative configuration method, where the mutations have to be manually submitted by the user one by one.

# Kinds

`{bm} /(Kinds)_TOPIC/`

```{prereq}
Introduction_TOPIC
Introduction/Configuration_TOPIC
Introduction/Labels_TOPIC
```

The following subsections give an overview of the most-used kinds and example manifests for those kinds. All manifests, regardless of the kind, require the following fields ...

 * `apiVersion`: API version.
 * `kind`: Class of object (kind).
 * `metadata.name`: Name of object.

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

In addition, the `metadata.labels` and `metadata.annotations` contain the object's labels and annotations (respective).

## Pod

`{bm} /(Kinds\/Pod)_TOPIC/i`

Containers are deployed in Kubernetes via pods. A pod is a set of containers grouped together, often containers that are tightly coupled and / or are required to work in close proximity of each other (e.g. on the same host).

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

By default, containers within a pod are isolated from each other  (e.g. isolated process IDs) except for sharing the same ...

 * network (containers within a pod have the same IP, same host, and share the port space).
 * IPC bus (containers within a pod can communicate with each other over POSIX message queues / System V IPC channels).
 * volumes (containers within a pod may have shared storage assigned to them in addition to their isolated storage).

While the point of Kubernetes is to orchestrate containers over a set of nodes, the containers for a pod are all guaranteed to run on the same node. As such, pods are usually structured in a way where their containers are tightly coupled and uniformly scale together. For example, imagine a pod with comprised of a container running a WordPress server and a container running the MySQL database for that WordPress server. This would be a poor example of a pod because the two containers within it ...

 1. don't scale uniformly (e.g. you may need to scale the database up before the WordPress server, or vice versa).
 2. don't communicate over anything other than the network (e.g. they don't need a shared volume).
 3. are intended to be distributed (e.g. it's okay for them to be running on separate machines).

Contrast that to a pod with a container running a WordPress server and a container that pushes that WordPress server's logs to a monitoring service. This would be a good example of a pod because the two containers within ...

 1. communicate over the filesystem (e.g. application server is writing logs to a shared volume and the log watcher is tailing them).
 2. aren't intended to be distributed (e.g. log watcher is intended for locally produced logs).
 3. are written by different teams (e.g. SRE team wrote the log watcher image while another team wrote the application server image).

Example manifest:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - image: my-image:1.0
      name: my_container
      resources:
        requests:
          cpu: "500m"
          memory: "128Mi"
        limits:
          cpu: "1000m"
          memory: "256Mi"
      volumeMounts:
        - mountPath: "/data"
          name: "my_data"
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
      readinessProbe:
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
        path: "/var/lib/my_data"  # literally mounts a path from the worker node? not persistent if node modes
    - name: "my_data_nfs"
      nfs:
        server: nfs.server.location
        path: "/path/on/nfs"
```

### Images

`{bm} /(Kinds\/Pod\/Images)_TOPIC/`

Each container within a pod must have an image associated with. Images are specified in the Docker image specification format, where a name and a tag are separated by a colon (e.g. `my-image:1.0`).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container1
      image: my-image:1.0
    - name: my-container2
      image: my-image:2.4
```

#### Pull Policy

`{bm} /(Kinds\/Pod\/Images\/Pull Policy)_TOPIC/`

Each container in a pod has to reference an image to use. How Kubernetes loads a container's image is dependent on that container's image pull policy.

```yaml
apiVersion: v1
kind: Pod
metadata:F
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image:1.0
      imagePullPolicy: IfNotPresent  # Only download if the image isn't present
```

A value of ...

 * `IfNotPresent` only downloads the image if it's not already locally present on the node.
 * `Always` always downloads the image.
 * `Never` never downloads the image (will fail if image does not exist locally on the node).

If unset, the image pull policy differs based on the image tag. Not specifying a tag or specifying `latest` as the tag will always pull the image. Otherwise, the image will be pulled only if it isn't present.

#### Private Container Registries

`{bm} /(Kinds\/Pod\/Images\/Private Container Registries)_TOPIC/`

```{prereq}
Kinds/Secret_TOPIC
```

Images that sit in private container registries require credentials to pull. Private container registry credentials are stored in secret objects of type `kubernetes.io/dockerconfigjson` in the format of Docker's `config.json` file.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-docker-creds
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: ... # base64 encoded ~/.docker/config.json goes here
```

```{note}
If you don't want to supply the above manifest, you can also use `kubectl` to create a secret object with the appropriate credentials: `kubectl create secret docker-registry secret-tiger-docker --docker-email=tiger@acme.example --docker-username=tiger --docker-password=pass1234 --docker-server=my-registry.example:5000`.
```

Those secret objects are then referenced in the pod's image pull secrets list.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  # Place secret here. This is a list, so you can have many container registry credentials
  # here.
  imagePullSecrets:
    - name: my-docker-creds
  containers:
    - name: my-container
      image: my-registry.example/tiger/my-container:1.0  # Image references registry.
```

```{seealso}
Kinds/Service Account_TOPIC (Image pull secrets may be assigned to service accounts, where any pod using that service account inherits them)
```

### Resources

`{bm} /(Kinds\/Pod\/Resources)_TOPIC/`

Each container within a pod can optionally declare a ...

 * minimum set of resources that it needs to operate,
 * maximum set of resources that it will ever need to operate.
 
Setting these options allows Kubernetes to choose a node with enough available resources to run that pod.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image:1.0
      resources:
        requests:  # Minimum CPU and memory for this container
          cpu: "500m"
          memory: "128Mi"
        limits:    # Maximum CPU and memory for this container
          cpu: "1000m"
          memory: "256Mi"
```

`requests` are the minimum resources the container needs to operate while `limits` are the maximum resources the container can have. Some resources are dynamically adjustable while others require the pod to restart. For example, a pod ...

 * can have its CPU usage dynamically adjusted because Kubernetes can just ask the operating system's CPU scheduler to give it less/more time.
 * can't have its memory usage dynamically adjusted because if it loses access to a block of memory, the applications running within the pod won't know and will likely crash.

The example above lists out CPU and memory as viable resource types. The unit of measurement for ...

 * cpu is either in ...
   * whole cores: no suffix
   * millicpus: suffix of m (1 core is equivalent to 1000m -- e.g. 0.5 = 5000m).
 * memory is either in ...
   * bytes: no suffix
   * 1000 scale: suffix of k = 1000, M = 1,000,000, G = 1,000,000,000
   * power of two scale: suffix of k = 1024, M = 1,048,576, G = 1,073,741,824

### Ports

`{bm} /(Kinds\/Pod\/Ports)_TOPIC/`

Each container within a pod can expose ports to the cluster.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image:1.0
      ports:
        - containerPort: 8080
          name: http
          protocol: TCP
```

The example above exposes port 8080 to the rest of the cluster (not to the outside world). Even with the port exposed, other entities on the cluster don't have a built-in way to discover the pod's IP / host or the fact that it has this specific port open. For that, services are required.

```{seealso}
Kinds/Service_TOPIC (Exposing pods to the outside world)
```

A pod can have many containers within it, and since all containers within a pod share the same IP, the ports exposed by those containers must be unique. For example, only one container within the pod expose port 8080.

```{note}
By default, network access is allowed to all pods within the cluster. You can change this using a special kind of pod called `NetworkPolicy` (as long as your Kubernetes environment supports it -- may or may not depending on the container networking interface used). `NetworkPolicy` lets you limit network access such that only pods that should talk together can talk together (a pod can't send a request to another random pod in the system). This is done via label selectors.

If you're aware of endpoints, service, and ingress kinds, I'm not sure how this network policy stuff plays with those kinds.
```

### Command-line Arguments

`{bm} /(Kinds\/Pod\/Command-line Arguments)_TOPIC/`

An image typically provides a default entry point (process that gets started) and default set of arguments to run with. Each container within a pod can override these defaults.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - image: my-image:1.0
      command: [/opt/app/my-app]
      args: [--no-logging, --dry-run]
```

```{note}
The Dockerfile used to create the image had an `ENTRYPOINT` and a `CMD`. `command` essentially overrides the Dockerfile `ENTRYPOINT` and `args` overrides the Dockerfile's `CMD`.
```

### Environment Variables

`{bm} /(Kinds\/Pod\/Environment Variables)_TOPIC/`

```{prereq}
Kinds/Pod/Command-line Arguments_TOPIC
```

Each container within a pod can be assigned a set of environment variables.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image:1.0
      env:
        - name: LOG_LEVEL
          value: "OFF"
        - name: DRY_RUN
          value: "true"
```

Once defined, an environment variables value can be used in other parts of the manifest using the syntax `$(VAR_NAME)`. For example, an environment variable's value may be placed directly within an argument.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image:1.0
      env:
        - name: LOG_LEVEL
          value: "OFF"
      args: [--logging_telemetry=$(LOG_LEVEL)]
```

```{seealso}
Kinds/Pod/Configuration_TOPIC (Set configurations to environment variables)
Kinds/Pod/Metadata_TOPIC (Set pod details to environment variables)
Kinds/Pod/Service Discovery/Environment Variables_TOPIC (Find services using environment variables)
```

### Configuration

`{bm} /(Kinds\/Pod\/Configuration)_TOPIC/`

```{prereq}
Kinds/Configuration Map_TOPIC
Kinds/Secret_TOPIC
Kinds/Pod/Environment Variables_TOPIC
Kinds/Pod/Command-line Arguments_TOPIC
Kinds/Pod/Volume Mounts_TOPIC
```

A container's configuration can come from both config maps and secrets. For config maps, a config map's key-value pairs can be accessed by a container via environment variables, command-line arguments, or volume mounts. To set a ...

 * environment variable:
 
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-pod
   spec:
     containers:
       - name: my-container
         image: my-image:1.0
         # Under each "env" entry to come from a config map, add a "valueFrom" that contains
         # the config map to pull an entry from and the key for the config map entry to pull.
         env:
           - name: ENV_VAR_NAME1  # Env var to assign value to.
             valueFrom:
               configMapKeyRef:
                 name: my-config       # Config map to pull from
                 key: CONFIG_MAP_KEY1  # Config map entry to get value from
           - name: ENV_VAR_NAME2
             valueFrom:
               configMapKeyRef:
                 name: my-config
                 key: CONFIG_MAP_KEY2
   ```

   In certain cases, you may want to map all entries within a config map directly as a set of environment variables. This is useful when many entries of a config map are required for configuration, so many that it becomes tedious and error-prone to map them all to environment variables manually.
   
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-pod
   spec:
     containers:
       - name: my-container
         image: my-image:1.0
         # "envFrom" maps all entries of a config map as env vars.
         envFrom:
           - prefix: CONFIG_    # Prefix to tack on to each config map entry (optional).
             configMapRef:
               name: my-config
   ```
   
   ```{note}
   If a config map name can't map to an environment variable, it's silently omitted. For example, env names can't contain dashes.
   ```

 * command-line argument:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-pod
   spec:
     containers:
       - name: my-container
         image: my-image:1.0
         # You can't pass in config map entries directly as command-line arguments, but what
         # you can do is load them up first as environment variables and then reference the
         # environment variables in the "command" (or "args") field.
         env:
           - name: ENV_VAR_NAME1
             valueFrom:
               configMapKeyRef:
                 name: my-config
                 key: CONFIG_MAP_KEY1
           - name: ENV_VAR_NAME2
             valueFrom:
               configMapKeyRef:
                 name: my-config
                 key: CONFIG_MAP_KEY2
         command:
           - "/my-app.sh"
           - "$(ENV_VAR_NAME1)"
           - "$(ENV_VAR_NAME2)"
   ```

 * volume mount:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-pod
   spec:
     # Place a "configMap" type volume into the pod.
     volumes:
       - name: config-volume
         configMap:
           name: my-config
           # "items" lists out specific config map entries to include and mounts each as
           # a specific filename. If you don't include this, all config map entries will
           # be included (filenames will map to config map entry names).
           items:
             - key: CONFIG_MAP_KEY1
               path: file1.cfg
             - key: CONFIG_MAP_KEY2
               path: file2.cfg
     # In the container, mount that volume to whichever containers you want.
     containers:
       - name: my-container
         image: my-image:1.0
         volumeMounts:
           - name: config-volume
             mountPath: /config
             readOnly: true       # Make the mount read-only (optional).
             defaultMode: "6600"  # File access permissions of mounted files (optional).
   ```

   If the directory you're mounting to already exists on the container, that existing directory is entirely replaced. In the example above, if the container already has a "/config" directory, it'll get replaced entirely with the config map mount (this is bad because the container's "/config" might have other necessary files required for the container to work). A workaround to this is to use the volume mount's "subPath" property, which allows you to mount a single file / directory from a volume.

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-pod
   spec:
     volumes:
       - name: config-volume
         configMap:
           name: my-config
     containers:
       - name: my-container
         image: my-image:1.0
         # The use of "subPath" here ensures that that original "/config" directory on the
         # container doesn't go away. It remains in place, and files / directories are just
         # added to it.
         volumeMounts:
           - name: config-volume
             mountPath: /config/file1.cfg  # Destination file to mount to.
             subPath: CONFIG_MAP_KEY1      # Source config map entry name.
           - name: config-volume
             mountPath: /config/file2.cfg  # Destination file to mount to.
             subPath: CONFIG_MAP_KEY2      # Source config map entry name.
   ```

For secrets, a secret object's key-value pairs can be accessed in almost exactly the same way as config maps with almost exactly the same set of options and restrictions. To set a ...

 * environment variable:
 
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-pod
   spec:
     containers:
       - name: my-container
         image: my-image:1.0
         env:
           - name: ENV_VAR_NAME1
             valueFrom:
               secretKeyRef:  # This has been changed from "configMapKeyRef" to "secretKeyRef".
                 name: my-secret
                 key: SECRET_KEY1
           - name: ENV_VAR_NAME2
             valueFrom:
               secretKeyRef:  # This has been changed from "configMapKeyRef" to "secretKeyRef".
                 name: my-secret
                 key: SECRET_KEY2
   ```

 * command-line argument:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-pod
   spec:
     containers:
       - name: my-container
         image: my-image:1.0
         env:
           - name: ENV_VAR_NAME1
             valueFrom:
               secretKeyRef:  # This has been changed from "configMapKeyRef" to "secretKeyRef".
                 name: my-secret
                 key: SECRET_KEY1
           - name: ENV_VAR_NAME2
             valueFrom:
               secretKeyRef:  # This has been changed from "configMapKeyRef" to "secretKeyRef".
                 name: my-secret
                 key: SECRET_KEY2
         command:
           - "/my-app.sh"
           - "$(ENV_VAR_NAME1)"
           - "$(ENV_VAR_NAME2)"
   ```

 * volume mount:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-pod
   spec:
     volumes:
       - name: secret-volume
         secret:  # This has been changed from "configMap" to "secret"
           name: my-secret
     containers:
       - name: my-container
         image: my-image:1.0
         volumeMounts:
           - name: secret-volume
             mountPath: /secrets
             readOnly: true
   ```

Both config maps and secrets can be dynamically updated. If a pod is running when an update gets issued, it may or may not receive those updates depending on the configurations are exposed to the container:

 * environment variables *don't* receive updates.
 * command-line arguments *don't* receive updates.
 * individual volume mounts *don't* receive updates.
 * whole volume mounts do receive updates.

Command-line arguments and environment variables don't update because an application's command-line arguments and environment variables can't be changed from the outside once a process launches. Individual files/directories mounted from a volume don't update because of technical limitations related to how Linux filesystems work (see [here](https://github.com/kubernetes/kubernetes/issues/50345#issuecomment-656947594])). Whole volume mounts *do* update files under the mount, but it's up to the application to detect and reload those changed files.

```{note}
All files in a volume mount get updated at once. This is possible because of symlinks. New directory get loaded in and the symlink is updated to use that new directory.
```

```{note}
For individual files/directories mounted from a volume, one workaround to receiving updates is to use symlinks. Essentially, mount the whole volume to a path that doesn't conflict with an existing path in the container. Then, as a part of the container's start-up process, add symlinks to the whole volume mount wherever needed.

For example, if the application requires a configuration file at /etc/my_config.conf, you can mount all configurations to /config and then symlink /etc/my_config.conf to /config/my_config.conf. That way, you can still receive updates.
```

The typical workaround to config map dynamic updates is to use deployments. In deployments, secrets / config maps and pods are bound together as a single unit, meaning that all pods restart automatically on any change.

```{seealso}
Kinds/Deployment_TOPIC
```

### Volume Mounts

`{bm} /(Kinds\/Pod\/Volume Mounts)_TOPIC/`

```{prereq}
Kinds/Volume_TOPIC
```

A pod is able to supply multiple volumes, where those volumes may be mounted to different containers within that pod.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  # Volumes supplied are listed here.
  volumes:
    - name: my-data1
      hostPath:
        path: "/var/lib/my_data1"
    - name: my-data2
      hostPath:
        path: "/var/lib/my_data2"
  # Each container in the pod can mount any of the above volumes by referencing its name.
  containers:
    - name: my-container
      image: my-image:1.0
      volumeMounts:
        # Mount "my-data1" volume to /data1 in the container's filesystem.
        - mountPath: /data1
          name: my-data1
        # Mount "my-data2" volume to /data2 in the container's filesystem.
        - mountPath: /data2
          name: my-data2
```

In the example above, the two volumes supplied by the pod are both of type `hostPath`. `hostPath` volume types reference a directory on the node that the pod is running on, meaning that if two containers within the same pod are assigned the same `hostPath` volume, they see each other's changes on that volume. The type of volume supplied defines the characteristics of that volume. Depending on the volume type, data on that volume ...

 * may be shared across pods, shared across containers within a single pod, or not shared at all
 * may be encrypted or unencrypted
 * if shared, may have delayed and / or unreliable read-write consistency
 * if not shared, may be transient or persistent across pod or container restarts
 * if not shared, may be transient or persistent when a pod is moved to a new node
 * etc..

Each supplied volume within a pod can either reference a direct piece of storage or it can reference a persistent volume claim. In most cases, directly referencing a piece of storage (as done in the above example) is discouraged because it tightly couples the pod to that storage and its parameters. The better way is to use persistent volume claims, where volumes are assigned from a pool (or dynamically created and assigned) to pods as required. Assuming that you have a persistent volume claim already created, it can be referenced by using `persistentVolumeClaim` as the volume type.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  volumes:
    - name: my-data
      persistentVolumeClaim:  # Volume type of "persistentVolumeClaim"
        claimName: my-data-pv-claim
  containers:
    - name: my-container
      image: my-image:1.0
      volumeMounts:
        - mountPath: /data
          name: my-data
```

### Lifecycle

`{bm} /(Kinds\/Pod\/Lifecycle)_TOPIC/`

A pod's lifecycle goes through several phases:

 * **Pending** - Pod is waiting to run. This could be either because it hasn't been scheduled on a node yet or because it has been scheduled on a node but some of its containers aren't ready to run yet (e.g. images for those containers are still being downloaded).
 * **Running** - Pod is running. It's been scheduled on a node, all of its containers are ready to run, and at least one of those containers is either running, starting, or restarting.
 * **Success** - Pod's containers all finished successfully.
 * **Failed** - Pod's container all finished, some unsuccessfully. This could be either because some containers terminated with an error or because Kubernetes itself terminated those containers for some reason.
 * **Unknown** - Special marker indicating that the state of a pod couldn't be obtained (e.g. from a network outage).

```{svgbob}
     Pending
        |
        |
        v
     Running
       / \
      /   \
     v     v
 Success  Failed
```

Each container in a pod can be in one of several states:

 * **Waiting** - Container is performing operations it needs to run (e.g. downloading image for the container).
 * **Running** - Container is running.
 * **Terminated** - Container has terminated.

The following subsections detail various lifecycle-related configurations of a pod and its containers.

#### Probes

`{bm} /(Kinds\/Pod\/Lifecycle\/Probes)_TOPIC/`

Probes are a way for Kubernetes to check the state of a pod. Containers within the pod expose interfaces which Kubernetes periodically pings to determine what actions to take (e.g. restarting a non-responsive pod).

Different types of probes exists. A ...

 * liveness probe is something that Kubernetes pings to check if a container is alive and responsive (typical action on failure: restart pod).
 * readiness probe is something that Kubernetes pings to check if a container is able to accept traffic (typical action on failure: stop traffic until readiness probes on all containers pass).
 * startup probe is something that Kubernetes pings to check if a container has started (typical action on failure: retry until startup probes on all containers pass before allowing liveness and readiness probes).

```{seealso}
Kinds/Service_TOPIC (Readiness probes are used by services for routing traffic).
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image:1.0
      # Probe to check if a container is alive or dead. Performs an HTTP GET with path
      # /healthy at port 8080.
      livenessProbe: 
        httpGet:
          path: /healthy
          port: 8080
        initialDelaySeconds: 5
        timeoutSeconds: 1
        periodSeconds: 10
        failureThreshold: 3
      # Probe to check if a container is able to service requests. Performs an HTTP GET
      # with path /ready at port 8080.
      readinessProbe:
        httpGet:
          path: /ready
          port: 8080
        initialDelaySeconds: 5
        timeoutSeconds: 1
        periodSeconds: 10
        failureThreshold: 3
```

In the example above, each of the probes check an HTTP server within the container at port 8080 but at different paths. The field ...

 * `initialDelaySeconds` is the number of seconds to wait before performing the first probe.
 * `timeoutSeconds` is the number of seconds to wait before timing out.
 * `periodSeconds` is the number of seconds to wait before performing a probe.
 * `failureThreshold` is the maximum number of successive failure before Kubernetes considers the probe failed.
 * `successThreshold` is the maximum number of successive successes before Kubernetes considers the probe passed.
 
There are types of probes other than `httpGet`. A probe of type ...

 * `httpGet` will perform an HTTP GET operation to a server on the container and fail it if it's non-responsive.
 * `tcpSocket` will attempt to connect a TCP socket to the container and fail if the container doesn't accept.
 * `exec` will run a command on the container and fail if it gets a non-zero exit code.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image:1.0
      readinessProbe:
        exec:
          command:
            - cat
            - /tmp/some_file_here
        initialDelaySeconds: 5
        timeoutSeconds: 1
        periodSeconds: 10
        failureThreshold: 3
```

#### Graceful Termination

`{bm} /(Kinds\/Pod\/Lifecycle\/Graceful Termination)_TOPIC/`

Kubernetes terminates pods by sending a `SIGTERM` to each container's main process, waiting a predefined amount of time, then forcefully sending a `SIGKILL` to that same process if the process hasn't shut itself down. The predefined waiting time is called the termination grace period, and it's provided so the application can perform cleanup tasks after it's received `SIGTERM` (e.g. emptying queues).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  restartPolicy: Always
  terminationGracePeriodSeconds: 60  # Default to 30
  containers:
    - name: my-container
      image: my-image:1.0
```

```{note}
If you have a pre-stop pod lifecycle hook (described in another section), note that this termination grace period starts as soon as the hook gets invoked (not after it finishes).
```

On termination (either via `SIGTERM` or voluntarily), a pod's container can write a message to a special file regarding the reason for its termination. The contents of this file be visible in the pod container's "last state" property.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  restartPolicy: Always
  containers:
    - name: my-container
      image: my-image:1.0
      terminationMessagePath: /var/exit-message  # Defaults to /dev/termination-log
```

```{note}
A pod container's "last state" property is visible when you describe the pod via `kubectl`.
```

#### Maximum Runtime

`{bm} /(Kinds\/Pod\/Lifecycle\/Maximum Runtime)_TOPIC/`

The runtime of a pod can be limited such that, if continues to run for more than some duration of time, Kubernetes will forcefully terminate it and mark it as failed.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  activeDeadlineSeconds: 3600  # When set, pod can't run for more than this many seconds
  containers:
    - name: my-container
      image: my-image:1.0
```

#### Lifecycle Hooks

`{bm} /(Kinds\/Pod\/Lifecycle\/Lifecycle Hooks)_TOPIC/`

```{prereq}
Kinds/Pod/Lifecycle/Probes_TOPIC
Kinds/Pod/Lifecycle/Graceful Termination_TOPIC
```

Lifecycle hooks are a way for Kubernetes to notify a container of when ...

* it's been brought up, called a post-start hook.
* it's about to be brought down, called a pre-stop hook.

Similar to probes, containers within the pod expose interfaces which Kubernetes invokes. A lifecycle hook interface is similar to a probe interface in that it can be one of multiple types: `httpGet`, `tcpSocket`, and `exec`.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image:1.0
      lifecycle:
        # Hook to invoke once the container's main process starts running. This hook runs
        # along-side the main process (not before it launches), but Kubernetes will treat
        # the container as if it's waiting for it to still be created until this hook
        # completes.
        #
        # A pod will be a "Pending" state until all each of its container post-start hooks
        # complete.
        postStart:
          exec:
            command: [sh, sleep 15]  # Artificial sleep
        # Hook to invoke just before the container is voluntarily terminated (e.g. its
        # moving to a new node). This hook runs first and once it's finished, a SIGTERM is
        # sent to the main container process, followed by a SIGKILL if the container's
        # main process hasn't terminated itself.
        #
        # It's important to note that the termination grace period begins as soon as the
        # pre-stop hook gets invoked, not after the pre-stop hook finishes.
        preStop:
          httpGet:
            path: /shutdown
            port: 8080
```

A post-start hook is useful when some form of initialization needs to occur but it's impossible to do that initialization within the container (e.g. initialization doesn't happen on container start and you don't have access to re-create / re-deploy the container image to add support for it). Likewise, a pre-stop hook is useful when some form of graceful shutdown needs to occur but it's impossible to do that shutdown within the container (e.g. shutdown procedures don't happen on `SIGTERM` and you don't have access to re-create / re-deploy the container image to add support for it).

```{note}
Recall that a container has three possible states: waiting, running, and terminated. The docs say that a container executing a post-start hook is still in the waiting state.
```

```{note}
According to the book, it's difficult to tell if / why a hook failed. Its output doesn't go anywhere. You'll just see something like `FailedPostStartHook` / `FailedPreStopHook` somewhere in the pod's event log.

According to the book, many applications use pre-stop hook to manually send a `SIGTERM` to their app because, even though `SIGTERM` is being sent by Kubernetes, it's getting gobbled up and discarded by some parent process (e.g. running your app via `sh`).
```

#### Init Containers

`{bm} /(Kinds\/Pod\/Lifecycle\/Init Containers)_TOPIC/`

```{prereq}
Kinds/Pod/Command-line Arguments
```

Init containers are pod containers that run prior to a pod's actual containers. Their purpose is to initialize the pod in some way (e.g. writing startup data to some shared volume) or delay the start of the pod until some other !!service!! is detected as being online (e.g. database).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  # Init containers are defined similarly to main containers, but they're run before main containers, one after the other in the order they're defined. After the last init container successfully completes, the main containers for the pod start.
  initContainers:
    - name: my-initA
      image: my-init-imageA:1.0
    - name: my-initB
      image: my-initB-image:1.0
      command: ['launchB', '--arg1']
  containers:
    - name: my-container
      image: my-image:1.0
```

```{note}
Important note from the docs:

> Because init containers can be restarted, retried, or re-executed, init container code should be idempotent. In particular, code that writes to files on EmptyDirs should be prepared for the possibility that an output file already exists.
```

#### Restart Policy

`{bm} /(Kinds\/Pod\/Lifecycle\/Restart Policy)_TOPIC/`

Restart policy is the policy Kubernetes uses for determining when a pod should be restarted.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  restartPolicy: Always
  containers:
    - name: my-container
      image: my-image:1.0
```

A value of ...

 * `Always` always restarts the pod regardless of how it exists (default).
 * `OnFailure` only restarts the pod if it failed execution.
 * `Never` never restarts the pod.

`Always` is typically used when running servers that should always be up (e.g. http server) while the others are typically used for one-off jobs.

When a container within a pod fails, that entire pod is marked as failed and may restart depending on this property. Kubernetes exponentially delays restarts so that, if the restart is happening due to an error, there's some time in between restarts for the error to get resolved (e.g. wait for some pending network resource required by the pod comes online). The delay increases exponentially (10 seconds, 20 seconds, 40 seconds, 80 seconds, etc..) until it caps out at 5 minutes. The delay resets once a restarted pod is executing for more than 10 minutes without issue.

```{note}
"When a container within a pod fails, that entire pod is marked as failed" -- Is this actually true?

The delay may also reset if the pod moves to another node. The documentation seems unclear.
```

```{seealso}
Kinds/Job_TOPIC
```

### Service Discovery

`{bm} /(Kinds\/Pod\/Service Discovery)_TOPIC/`

```{prereq}
Kinds/Service_TOPIC
```

For a pod to communicate with services, it needs to be able to discover the IP(s) of those services. The mechanisms for discovering services within a pod are environment variables and DNS.

These service discovery mechanisms are details in the subsections below.

#### Environment Variables

`{bm} /(Kinds\/Pod\/Service Discovery\/Environment Variables)_TOPIC/`

When a pod launches, all services within the same namespace have their IP and port combinations added as environment variables within the pod's containers. The environment variable names are in the format `{SVCNAME}_SERVICE_HOST` / `{SVCNAME}_SERVICE_PORT`, where `{SVCNAME}` is the service converted to uppercase and dashes swapped with underscores. For example, `service-a` would get converted to `SERVICE_A`.

```
SERVICE_A_SERVICE_HOST=10.111.240.1
SERVICE_A_SERVICE_PORT=443
SERVICE_B_SERVICE_HOST=10.111.249.153
SERVICE_B_SERVICE_PORT=80
```

If a service exposes multiple ports, only the first port goes in `{SVCNAME}_SERVICE_PORT`. When multiple ports are present, additional environment variables get created in the format `{SVCNAME}_SERVICE_PORT_{PORTNAME}`, where `{PORTNAME}` is the name of service's port modified the same way that `{SVCNAME}` is. For example, `service-c` with two exposed ports named `web-1` and `metrics-1` would get converted to `SERVICE_C_SERVICE_PORT_WEB_1` and `SERVICE_C_SERVICE_PORT_METRICS_1` respectively.

```
SERVICE_C_SERVICE_HOST=10.111.240.1
SERVICE_C_SERVICE_PORT=443
SERVICE_C_SERVICE_PORT_WEB_1=443
SERVICE_C_SERVICE_PORT_METRICS_1=8080
```

```{note}
Looking at the k8s code, it looks like for a service port needs to be named for it as an environment variable. Service ports that don't have a name won't show up as environment variables. See (here)[https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/envvars/envvars.go#L51-L55].
```

Using environment variables for service discovery has the following pitfalls:

 * Services outside the pod's namespace aren't provided.
 * Services added to the namespace after the pod launches won't be picked up (env vars can only be changed before the launch of a container process).
 * Services removed from the name after the pod launches won't be picked up (env vars can only be changed before the launch of a container process).
 * Service naming conflicts can happen during normalization (e.g. uppercase-ing and converting dashes to underscores can cause conflict: `My-name` and `my_namE` both end up as `MY_NAME`).

On the plus side, inspecting environment variables within a container essentially enumerates all services within the pod's namespace. Enumerating services isn't possible when using DNS for service discovery, discussed in the next section.

#### DNS

`{bm} /(Kinds\/Pod\/Service Discovery\/DNS)_TOPIC/`

```{prereq}
Kinds/Pod/Service Discovery/Environment Variables_TOPIC
```

Kubernetes provides a global DNS server which is used for service discovery. Each pod is automatically configured to use this DNS server and simply has to query it for a service's name. If the queried service is present, the DNS server will return the stable IP of that service.

```{note}
The DNS server runs as an internal Kubernetes application called 'coredns` or `kube-dns`. This is usually in the `kube-system` namespace. Recall that the IP of a service is stable for the entire lifetime of the service, meaning that service restarts and DNS caching by the application and / or OS isn't an issue here.
```

The general domain query format is `{SVCNAME}.{NAMESPACE}.svc.{CLUSTERDOMAIN}`, where ...

 * `{SVCNAME}` is the name of the service.
 * `{NAMESPACE}` is the name of the namespace that `{SVCNAME}` is in.
 * `{CLUSTERDOMAIN}` is the cluster domain suffix of the cluster that `{SVCNAME}` and `{NAMESPACE}` are in.

For example, to query for the IP of service `serviceA` in namespace `ns1` within a cluster that has the domain name suffix `cluster.local`, the domain name to query is `serviceA.ns1.svc.cluster.local`. Alternatively, if the pod doing the querying is ...

 * within the same cluster, the cluster domain suffix can be omitted: `serviceA.ns1`.
 * within the same cluster and namespace, both the namespace and the cluster domain suffix can be omitted: `serviceA`.

Using DNS for service discovery has the following pitfalls:

 * Service port information isn't included in queries.
 * Enumerating services isn't possible with DNS.

On the plus side, DNS queries can extend outside the pod's namespace and services started after a container launches are queryable. These aren't possible when using environment variables for service discovery, discussed in the previous section.

### Metadata

`{bm} /(Kinds\/Pod\/Metadata)_TOPIC/`

```{prereq}
Kinds/Pod/Resources_TOPIC
Kinds/Pod/Environment Variables_TOPIC
Kinds/Pod/Volume Mounts_TOPIC
```

Information about a pod and its containers such as ...

 * pod name,
 * pod labels and annotations,
 * pod IP,
 * pod namespace,
 * node running the pod,
 * container resource limits,
 * etc..

... can all be accessed within the container via either a file system mount or environment variables.

#### Environment Variables

`{bm} /(Kinds\/Pod\/Metadata Access\/Environment Variables)_TOPIC/`

All pod information except for labels and annotations can be assigned to environment variables. This is because a running pod can have its labels and annotations updated but the environment variables within a running container can't be updated once that container starts (updated labels / annotations won't show up to the container).

```{note}
CPU resources can also be dynamically updated without restarting the pod / container process. The environment variable for this likely won't update either, but it isn't restricted like labels / annotations are. There may be other reasons that labels / annotations aren't allowed. Maybe Linux has a cap on how large an environment variable can be, and there's a realistic possibility that labels / annotations can exceed that limit?
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - image: my-image:1.0
      name: my-container
      resources:
        requests:
          cpu: 15m
          memory: 100Ki
        limits:
          cpu: 100m
          memory: 4Mi
      env:
        # These entries reference values that would normal be "fields" under a running pod
        # in Kubernetes. That is, these entries reference paths that you would normally see
        # when you inspect a pod in Kubernetes by dumping out its YAML/JSON. For example,
        # by running "kubectl get pod my_pod -o yaml" -- it produces a manifest but with
        # many more fields (dynamically assigned fields and fields with default values
        # filled out).
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name  # Pulls in "my_pod".
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace  # Pulls in the default namespace supplied by Kubernetes.
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP  # Pulls in the pod's IP.
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName  # Pulls in the name of the node that the pod's running on.
        # When referencing resource requests / limits for a container, if you're requesting those
        # for a different container than the one the container you're assigning the env var to,
        # you'll need to supply a "containerName" field. Otherwise, you can omit the
        # "containerName" field.
        #
        # Resource requests / limits by optionally be provided a "divisor" field, which will
        # divide the value before assigning it.
        - name: CPU_REQUEST
          valueFrom:
            resourceFieldRef:
              resource: requests.cpu
              containerName: my-container  # If you omit this, it'll default to "my-container" anyways.
              divisor: 5m  # Divide by 5 millicores before assigning (15millicores/5millicores=3)
        - name: CPU_LIMIT
          valueFrom:
            resourceFieldRef:
              resource: limits.cpu
              containerName: my-container  # If you omit this, it'll default to "my-container" anyways.
              divisor: 5m  # Divide by 5 millicores before assigning (100millicores/5millicores=20)
        - name: MEM_REQUEST
          valueFrom:
            resourceFieldRef:
              resource: requests.memory
              containerName: my-container  # If you omit this, it'll default to "my-container" anyways.
              divisor: 1Ki  # Divide by 1 kibibyte before assigning (100Kebibytes/1Kibibyte=100)
        - name: MEM_LIMIT
          valueFrom:
            resourceFieldRef:
              resource: limits.memory
              containerName: my-container  # If you omit this, it'll default to "my-container" anyways.
              divisor: 1Ki  # Divide by 1 kibibyte before assigning (4Mebibytes/1Kibibyte=4096)
```

#### Volume Mount

`{bm} /(Kinds\/Pod\/Metadata Access\/Volume Mount)_TOPIC/`

```{prereq}
Kinds/Pod/Metadata Access/Environment Variables_TOPIC
```

All pod information can be exposed as a volume mount, where files in that mount map to pieces of information. Unlike with environment variables, a volume mount can contain labels and annotations. If those labels and annotations are updated, the relevant files within the mount update to reflect the changes. It's up to the application running within the container to detect and reload those updated files.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    drink: Pepsi
    car: Volvo
  annotations:
    key1: value1
    key2: |
      Good morning,
      Today is Sunday.
spec:
  volumes:
    # A volume of type downwardAPI will populate with files, where each file contains the
    # value for a specific field. Fields are specified in a similar manner to the
    # environment variable version above.
    #
    # Each "path" under "items" is file within the volume.
    - name: downward_vol
      downwardAPI:
        items:
          - path: podName
            fieldRef:
              fieldPath: metadata.name
          - path: podNamespace
            fieldRef:
              fieldPath: metadata.namespace
          - path: podIp
            fieldRef:
              fieldPath: status.podIP
          - path: nodeName
            fieldRef:
              fieldPath: spec.nodeName
          - path: cpuRequest
            resourceFieldRef:
              resource: requests.cpu
              containerName: my-container  # MUST BE INCLUDED, otherwise it's impossible to know which container.
              divisor: 5m
          - path: cpuLimit
            resourceFieldRef:
              resource: limits.cpu
              containerName: my-container  # MUST BE INCLUDED, otherwise it's impossible to know which container.
              divisor: 5m
          - path: memRequest
            resourceFieldRef:
              resource: requests.memory
              containerName: my-container  # MUST BE INCLUDED, otherwise it's impossible to know which container.
              divisor: 1Ki
          - path: memLimit
            resourceFieldRef:
              resource: limits.memory
              containerName: my-container  # MUST BE INCLUDED, otherwise it's impossible to know which container.
              divisor: 1Ki
          # The following two entries supplies labels and annotations. Note that, if labels
          # or annotations change for the pod, the files in this volume will be updated to
          # reflect those changes.
          #
          # Each file below will contain multiple key-value entries. One key-value entry per line, where
          # the key and value are delimited by an equal sign (=). Values are escaped, so the new lines in
          # the multiline example annotation in this pod (see key2, where the value is a good morning
          # message) will be appropriately escaped.
          - path: "labels"
            fieldRef:
              fieldPath: metadata.labels
          - path: "annotations"
            fieldRef:
              fieldPath: metadata.annotations
  containers:
    - image: my-image:1.0
      name: my-container
      resources:
        requests:
          cpu: 15m
          memory: 100Ki
        limits:
          cpu: 100m
          memory: 4Mi
      # Mount the volume declared above into the container. The application in the container
      # will be able to access the metadata as files within the volume mount.
      volumeMounts:
        - name: downward_vol
          mountPath: /metadata
```

### Node Placement

`{bm} /(Kinds\/Pod\/Node Placement)_TOPIC/`

A pod can have soft / hard requirements as to which nodes it can run on. It's common to segregate which nodes a pod can / can't run when dealing with...
 
 * multiple environments in the same cluster (e.g. testing nodes vs staging nodes vs production nodes)
 * multiple zones in the same cluster (e.g. eastern US vs western US).
 * specific hardware requirements (e.g. node that has a specific type of SSD, CPU, or GPU).
 * etc..

Three different mechanisms are used to define these requirements:

 * node selectors: hard requirements for which nodes a pod can run on.
 * node taints: hard and soft requirements for which nodes a pod *can't* run on.
 * node affinity: hard and soft requirements for which nodes a pod *can* and *can't* run on.

These mechanisms are documented in further detail in the subsections below. 

#### Node Selectors

`{bm} /(Kinds\/Pod\/Node Placement\/Node Selectors)_TOPIC/`

A node selector forces a pod to run on nodes that have a specific set of node labels.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  # This pod can only run on nodes that have the labels disk=ssd and cpu=IntelXeon.
  nodeSelector:
    disk: ssd
    cpu: IntelXeon
  containers:
    - name: my-container
      image: my-image:1.0
```

#### Taints and Tolerations

`{bm} /(Kinds\/Pod\/Node Placement\/Taints and Tolerations)_TOPIC/`

```{prereq}
Kinds/Node/Taints_TOPIC
```

A taint is a node property, structured as a key-value pair and effect, that repels pods. For a pod to be scheduled / executed on a node with taints, it needs tolerations for those taints. Specifically, that pod ... 

 * needs tolerations for any taints with effect `NoSchedule` or `NoExecute`.
 * can have tolerations for any taints with effect `PreferNoSchedule` (having tolerations increases odds that pod gets scheduled on that node).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  # This pod can only run on nodes that have the taints "environment=production:NoExecute" and
  # "environment=excess-capacity:NoExecute". The example below uses the "Equal" operator, but
  # there's also an "Exists" operator which will match any value ("value" field shouldn't be
  # set if "Exists" is used).
  tolerations:
    - key: environment
      operator: Equal
      value: production
      effect: NoSchedule
    - key: environment
      operator: Equal
      value: excess-capacity
      effect: NoSchedule
  containers:
    - name: my-container
      image: my-image:1.0
```

```{seealso}
Kinds/Pod Disruption Budget_TOPIC (Controls how quickly pods are evicted when `NoExecute` used)
```

#### Node Affinity

`{bm} /(Kinds\/Pod\/Node Placement\/Node Affinity)_TOPIC/`

```{prereq}
Kinds/Pod/Node Placement/Node Selectors_TOPIC
Kinds/Pod/Node Placement/Taints and Tolerations_TOPIC
```

Node affinity is a set of rules defined on a pod that repels / attracts it to nodes tagged with certain labels, either as soft or hard requirements. 

 * For hard requirements, a set of label selectors need to be specified.
 * For soft requirements, a set of label selectors need to be specified along with weights that define the desirability of those selectors.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  affinity:
    nodeAffinity:
      # This field lists the hard requirements for node labels. The possible operators
      # allowed are ...
      #
      #  * "In" / "NotIn" - Tests key has (or doesn't have) one of many possible values.
      #  * "Exists" / "DoesNotExist" - Tests key exists (or doesn't exist), value ignored.
      #  * "Gt" / "Lt" - Tests key's value is grater than / less than.
      #
      # Use "In" / "Exists" for attraction and "NotIn" / "DoesNotExist" for repulsion.
      #
      # In this example, it's requiring that the CPU be one of two specific Intel models and
      # the disk not be a hard-drive (e.g. it could be a solid-state drive instead).
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
            - key: cpu
              operator: In
              values: [intel-raptor-lake, intel-alder-lake]
            - key: disk-type
              operator: NotIn
              values: [hdd]
      # This field lists out the soft requirements for node labels and weights those
      # requirements. Each requirement uses the same types of expressions / operators as the
      # hard requirements shown above, but it also has a weight that defines the
      # desirability of that requirement. Each weight must be between 1 to 100.
      #
      # In this example, the first preference outweighs the second by a ratio of 10:2 (5x
      # more preferred).
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          preference:
            - matchExpressions:
              - key: ram-speed
                operator: gt
                values: [3600]
              - key: ram-type
                operator: In
                values: [ddr4]
        - weight: 20
          preference:
            - matchExpressions:
              - key: ram-speed
                operator: lt
                values: [3601]  # This is <, 3601 means speed needs to be <= 3600.
              - key: ram-type
                operator: In
                values: [ddr4]
  containers:
    - name: my-container
      image: my-image:1.0
```

```{note}
The scheduler will try to enforce these preferences, but it isn't guaranteed as there could be other competing scheduling requirements (e.g. the admin have set something up to spread out pods more / less across nodes).
```

```{note}
The "5x more preferred" comment above is speculation. I've tried to look online to see how weights work but haven't been able to find much. Does it scale by whatever the highest weight is? So if the example above's first preference was 10 instead of 100, would it be preferred 0.5x as much (10:20 ratio)?
```

Unlike ...

 * node selectors, ...
     * the requirements for node affinity can be soft requirements.
     * the requirements for node affinity can repel as well as attract.
     * the requirements for node affinity has more ways to specify label selection criteria (more expressive).
 * node taints,
     * the requirements for node affinity are attracting / repulsing based on node labels, not repulsing based on lack of pod tolerations.
     * node affinity can't evict running pods from a node whereas taints with a `NoExecute` effect which will cause evictions.

```{note}
Note that `requiredDuringSchedulingIgnoredDuringExecution` and `preferredDuringSchedulingIgnoredDuringExecution` both end with "ignored during execution". This basically says that a pod won't get scheduled on a node but it also won't get evicted if that pod is already running on that node. This is in contrast to node taints, where a taint having an effect of `NoExecute` will force evictions of running pods.

The book hints that the ability to evict running pods may be added sometime in the future.
```

#### Pod Affinity

`{bm} /(Kinds\/Pod\/Node Placement\/Pod Affinity)_TOPIC/`

```{prereq}
Kinds/Pod/Node Placement/Node Affinity_TOPIC
```

Pod affinity is a set of rules defined on a pod that repels / attracts it to the vicinity of other pods tagged with certain labels. Vicinity is determined via a topology key, which is a label placed on nodes to define where they live. For example, nodes within the same ...

 * rack can have a "rack" label (e.g. nodes on rack 15 have label `rack=15`, nodes on rack 16 have label `rack=16`, ...).
 * data center can have a "dc" label (e.g. nodes in data center 1 have label `dc=1`, nodes in data center 2 have label `dc=2`, ...).
 * geographic region can have a "geo" label (e.g. nodes in Texas have label `geo=Texas`, nodes in Ohio have label `geo=Ohio`, ...).

Pod affinity defines pod attraction / repulsion by looking for pod labels and a topology key. For example, it's possible to use pod affinity to ensure that a pod gets scheduled on the same rack (via topology key) as another pod with the label `app=api-server`. There could be multiple pods with the label `app=api-server`, in which case the scheduler will pick one, figure out which rack it lives on, and place the new pod on that same rack.

Similar to node affinity, pod affinity can have hard and soft requirements, where soft requirements have weights that define the desirability of attraction / repulsion. Selector expressions and weights for pod affinity are defined similarly to those for node affinity.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - image: my-image:1.0
      name: my-container
  affinity:
    # This field defines the rules specifically for **attraction**. Like with node affinity,
    # pod affinity uses ...
    #
    #  * "requiredDuringSchedulingIgnoredDuringExecution" for hard requirements.
    #  * "preferredDuringSchedulingIgnoredDuringExecution" for soft requirement.
    #  * the same selector operators as node affinity ("In", "NotIn", "Exists",
    #    "DoesNotExist", "Gt", and "Lt").
    #  * the same weight requirements as node affinity (range between 1 to 100 per soft
    #    requirement).
    #
    # Unlike with node affinity, the negation operators ("NotIn" / "DoesNotExist") don't
    # define repulsion, they just attract to pods that don't have something. For example,
    # here we're looking to have affinity to pods that don't have the labels
    # "stability-level=alpha" and "stability-level=alpha". In addition, it strongly
    # prefers to live on the same rack as pods with label "app=api-server" and less strongly
    # prefers to live on the same rack as pods with label "app=db-server".
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        - topologyKey: rack
          labelSelector:
            matchExpressions:
              - key: stability-level
                operator: NotIn
                values: [alpha, beta]
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            - topologyKey: rack
              labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values: [api-server]
        - weight: 20
          podAffinityTerm:
            - topologyKey: rack
              labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values: [db-server]
    # This field defines the rules specifically for **repulsion**. It set up exactly the
    # same way as the field for attraction shown above, but the criteria here repulses away.
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        - topologyKey: data-center
          labelSelector:
            matchExpressions:
              - key: security-context
                operator: NotIn
                values: [privileged-pod]
```

```{note}
The scheduler will try to enforce these preferences, but it isn't guaranteed as there could be other competing scheduling requirements (e.g. the admin have set something up to spread out pods more / less across nodes).
```

```{note}
I've tried to look online to see how weights work but haven't been able to find much. Does it scale by whatever the highest weight is? So if the example above's first preference was 10 instead of 100, would it be preferred 0.5x as much (10:20 ratio)?
```

Kubernetes comes with pre-define topology keys:

 * Same node: `kubernetes.io/hostname`
 * Same availability zone: `topology.kubernetes.io/zone`
 * Same geographical region: `topology.kubernetes.io/region`

### Container Isolation

`{bm} /(Kinds\/Pod\/Container Isolation)_TOPIC/`

The isolation guarantees of the containers within a pod can be modified. Specifically, a pod can ask that its containers get ...

 * access to parts of the node that it's running on (e.g. share node's network interfaces).
 * updated container isolation parameters, potentially giving it access to more / less / different features (e.g. change user ID running the main container process).

The following subsections document these mechanisms in further detail. 

```{seealso}
Security/Pod Security Admission_TOPIC (Everything discussed here may be disabled by the cluster admin)
```

#### Security Context

`{bm} /(Kinds\/Pod\/Container Isolation\/Security Context)_TOPIC/`

```{prereq}
Kinds/Pod/Container Isolation/Node Access_TOPIC
```

A pod and its containers can have security-related features configured via a security context.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - image: my-image:1.0
      name: my-container
      securityContext:
        # When set, the default user of the container is updated to use be this user ID
        # (note that this is a user ID, not a user name). This is useful if multiple
        # applications are reading / writing to the sane shared volume (no permission
        # problems if they're are read/writing as the same UID?).
        runAsUser: 99 
        # When set, the group of the default user of the container is updated to use be this
        # group ID (there are multiple group IDs here, 123 is the main one used when
        # creating files and directories). This is useful if multiple applications are
        # reading / writing to the sane shared volume (no permission problems if they're are
        # read/writing as the same GID? -- if file permissions allow).
        fsGroup: 123
        supplementalGroups: [456, 789]
        # When set to true, the container will run as a non-root user. This is useful if
        # the pod breaks isolation by exposing the internals of the node to some of its
        # containers.
        runAsNonRoot: true
        # When set to true, the container runs in "privileged mode" (full access to the
        # Linux kernel). This is useful in cases where the pod manages the node somehow
        # (e.g. modified iptables).
        privileged: true
        # An alternative to giving a container "privileged" access (shown above) is to
        # instead provide the container with fine-grained permissions to the kernel.
        # This can also be used to revoke fine-grained permissions that are provided
        # by default (e.g. remove the ability to change ownership of a dir).
        capabilities:
          add:
            - SYS_TIME
          drop:
            - CHOWN
        # When set to true, the container is unable to write to its own filesystem. It
        # can only read from it. Any writing it needs to do has to be done on a mounted
        # volume.
        readOnlyRootFilesystem: true
        #
        # Not all features are listed here. There are many others.
```

These security-related features can also be used at the pod-level rather than the container-level. When used at the pod level, the features are applied as defaults for all containers (containers can override them if needed).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  # Pod-level security context. This gets applied as a default for all container in the pod.
  securityContext:
    runAsUser: 99 
    runAsNonRoot: true
    privileged: true
    capabilities:
      add:
        - SYS_TIME
      drop:
        - CHOWN
    readOnlyRootFilesystem: true
  containers:
    - image: my-image1:1.0
      name: my-container1
    - image: my-image2:1.0
      name: my-container2
      securityContext:
        privileged: false  # Override the default "privileged" security context option.
```

#### Node Access

`{bm} /(Kinds\/Pod\/Container Isolation\/Node Access)_TOPIC/`

```{prereq}
Kinds/Pod/Ports_TOPIC
```

A pod's isolation guarantees can be relaxed so that it has access to the internals of the node it's running on. This is important for in certain system-level scenarios, such as pods that collect node performance metrics.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - image: my-image:1.0
      name: my-container
  # By default, all containers within a pod share the same IP and port space (unique to that
  # pod. However, when this property is set to true, the node's default "network namespace"
  # is shared with the containers of the pod (network interfaces are exposed to the pod).
  hostNetwork: true
  # By default, each container within a pod has its own isolated process ID space. However,
  # when this property is set to true, the node's default "process ID namespace" is used for
  # each pod container's processes.
  hostPID: true
  # By default, each container within a pod has its own isolated IPC space. However, when
  # this property is set to true, the node's default "IPC namespace" is used for each pod
  # container's processes.
  hostIPC: true
```

```{seealso}
Kinds/Daemon Set_TOPIC (Daemon sets are used for running a single instance of a pod across a set of nodes)
```

If the only requirement is that requests from a node's port get forwarded to a container's port, that node's network interfaces don't need to be exposed to the pod. Instead, a container can also simply ask that the node running it directly map a node port to it.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - image: my-image:1.0
      name: my-container
      ports:
        # Map port 9999 on the node that this pod runs to port 8080 on this pod's container.
        #
        # Note that the Kubernetes scheduler ensures that a node has port 9999 available
        # before scheduling this pod to run on it.
        - containerPort: 8080
          hostPort: 9999
          protocol: TCP
```

```{note}
If you already know about services, the `NodePort` service isn't the same thing as what's going on here. This is opening up a port on the node that the pod is running on and forwarding requests to the container. `NodePort` opens the same port on *all* nodes and forwards requests to a random pod (not necessarily the pod running on the same node that the request came in to).
```

```{seealso}
Kinds/Service/Exposure/Node Port_TOPIC
```

### API Access

`{bm} /(Kinds\/Pod\/API Access)_TOPIC/`

```{prereq}
Kinds/Pod/Service Discovery_TOPIC
Kinds/Pod/Configuration_TOPIC
```

Containers within a pod can access the Kubernetes API server via a service called `kubernetes`, typically found on the default namespace. Communicating with this service requires a certificate check (to verify the server isn't a man-in-the-middle box) as well as an access token (to authentication with the service). By default, containers have a secret object mounted as a volume at `/var/run/secrets/kubernetes.io/serviceaccount` that contains both these pieces of data as files:

 * `ca.crt` - certificate used for verifying the server's identity.
 * `token` - bearer token used for authenticating with the server.
 * `namespace` - namespace of the *pod* itself (not the namespace of the `kubernetes` service).

In most cases, the credentials provided likely won't provide unfettered access to the Kubernetes API.

```{note}
See [here](https://stackoverflow.com/a/25843058) for an explanation of bearer tokens. You typically just need to include an HTTP header with the token in it.

Third-party libraries that interface with Kubernetes are available for various languages (e.g. Python, Java, etc..), meaning you don't have to do direct HTTP requests and do things like fiddle with headers.
```

```{seealso}
Kinds/Service Account_TOPIC (Credentials map to a service account)
Security/API Access Control/Disable Credentials_TOPIC (Disable mounting of credentials within pod)
```

## Configuration Map

`{bm} /(Kinds\/Configuration Map)_TOPIC/`

A configuration map is a set of key-value pairs intended to configure the main application of a container (or many containers). By decoupling configurations from the containers themselves, the same configuration map (or parts of it) could be used to configure multiple containers within Kubernetes.

```{seealso}
Kinds/Secret_TOPIC (Do **NOT** use config maps for storing secrets such as tokens, certificates, or password).
```

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

The key-value pairs of a configuration map typically get exposed to a container either as environment variables, files, or command-line arguments. Keys are limited to certain characters: alphabet, numbers, dashes, underscores, and dots.

## Secret

`{bm} /(Kinds\/Secret)_TOPIC/`

```{prereq}
Kinds/Configuration Map_TOPIC
```

A secret object is a set of key-value pairs, similar to a config map, but oriented towards security rather than just configuration (e.g. for storing things like access tokens, passwords, certificates). As opposed to a config map, Kubernetes takes extra precautions to ensure that a secret object is stored and used securely.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque  # "Opaque" is the default type (can be omitted)
# Both text and binary data are supported. To insert a text entry, place it under
# "stringData". To insert a binary entry, base64 the value and place it under "data". 
stringData:
  username: admin
  password: pepsi_one
data:
  key_file: eWFiYmFkYWJiYWRvbw==  
```

Many types of secrets exist. Each type either does some level of verification on the entries and / or acts as a tag to convey what data is contained within (e.g. SSH data, TLS data, etc..). In general `Opaque` is the secret type used by most applications.

```{note}
Certain sources are claiming that a secret object can be 1 megabyte at most.
```

## Node

`{bm} /(Kinds\/Node)_TOPIC/i`

Nodes are the machines that pods run on. A Kubernetes environment often contains multiple nodes, each with a certain amount of resources. Pods get assigned to nodes based on their resource requirements. For example, if a pod A requires 2gb of memory and node C has 24 gigs available, that node may get assigned to run that pod.

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

Kubernetes has a leader-follower architecture, meaning that of the nodes, a small subset is chosen to lead / manage the others. The leaders are referred to as master nodes while the followers are referred to as worker nodes.

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

### Taints

`{bm} /(Kinds\/Node\/Taints)_TOPIC/i`

A taint is a node property that repels pods, either as a preference or as a hard requirement. Each taint defined as a key-value pair along with an effect that defines how it works (value can be null, leaving just a key and effect). An effect can be either ...

 * `NoSchedule`, which means pods won't be scheduled on the node but already running pods will keep running.
 * `NoExecute`, which means pod won't be scheduled on the node and already running pods will be evicted.
 * `PreferNoSchedule`, which means pod can be scheduled on the node but that node will be avoided if possible.

```{seealso}
Kinds/Pod/Node Placement/Taints and Tolerations_TOPIC (Running pods on nodes with taints)
```

Multiple taints on a node repel pods based on each taint.

```{note}
The multiple taints paragraph is speculation. I think this is how it works.
```

A taint is formatted as `key=value:effect` Node taints can be added and removed via command-line.

```sh
kubectl taint node my-staging-node-1 environment-type=production:NoExecute  # Add taint
kubectl taint node my-staging-node-1 environment-type=production:NoExecute- # Remove taint (note the - at the end)
```

```{note}
Can this be done via a manifest as well? Probably, but it seems like the primary way to handle this is either through kubectl or via whatever cloud provider's managed Kubernetes web interface.
```

## Volume

`{bm} /(Kinds\/Volume)_TOPIC/i`

Volumes are disks where data can be persisted across container restarts. Normally, Kubernetes resets a container's filesystem each time that container restarts (e.g. after a crash or a pod getting moved to a different node). While that works for some types of applications, other application types such as database servers need to retain state across restarts.

Volumes in Kubernetes are broken down into "persistent volumes" and "persistent volume claims". A ...

* persistent volume is the volume itself.
* persistent volume claim is the assignment of a volume.

The idea is that a persistent volume itself is just a floating block of disk space. Only when it's claimed does it have an assignment. Pods can then latch on to those assignments.

```{svgbob}
 .------.      .------.     .------.     .------. 
 | vol1 |      | vol2 |     | vol3 |     | vol4 | 
 '---+--'      '---+--'     '------'     '---+--' 
     |             |                         |     
     v             v                         v     
.--------.    .--------.                .--------.
| claim1 |    | claim2 |                | claim3 |
'--------'    '--------'                '--------'
    ^             ^ ^                        ^
    |             | |                        |
    |             | '----------------.       |
    |             |                  |       |
.---+-------------+----.         .---+-------+---.
|         podA         |         |      podB     |
'----------------------'         '---------------'
```

In the example above, there are 4 volumes in total but only 3 of those volumes are claimed. podA latches on to claim1 and claim2 while podB latches on to claim3 and claim2 (both pods can access the volume claimed in claim2).

```{note}
Persistent volumes themselves are cluster-level kinds while persistent volume claims are namespace-level kinds. All volumes are available for claims regardless of the namespace that claim is in. Maybe you can limit which volumes can be claimed by using labels / label selectors?
```

```{note}
Part of the reasoning for doing it like this is decoupling: volumes are independent from pods and a volume can be shared access across pods.

Another reason is that a developer should only be responsible for claiming a volume while the cluster administrator should be responsible for setting up those volumes and dealing with backend details like the specifics of the volume type and how large each volume is. As a developer, you only have to make a "claim" while the administrator is responsible for ensuring those resources exist.
```

Example persistent volume manifest:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-vol
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
    - ReadOnlyMany
  persistentVolumeReclaimPolicy: Recycle  # once a claim on this volume is given up, delete the files on disk
  awsElasticBlockStore:
    volumeID: volume-id
    fsType: ext4
```

Example persistent volume claim manifest:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-vol-claim
spec:
  resources:
    requests:
      storage: 1Gi  # volume must have at least this much space
  accessModes:
    - ReadWriteOnce  # volume must have this access mode
  storageClassName: ""  # MUST BE EMPTY STRING to claim test-vol described above (if set, uses dynamic provisioning)
```

```{note}
Why must `spec.storageClassName` be an empty string instead of being removed entirely? Being removed entirely would cause Kubernetes to use a default storage class name (if one exists), which is not what you want. Storage classes are described in the next few paragraphs below.
```

There are two types of volume provisioning available:

* static provisioning - a claim is assigned a pre-created persistent volume.
* dynamic provisioning - a claim triggers a new persistent volume to get created and is assigned to it.

Dynamic provisioning only requires that you make a persistent volume claim with a specific storage class name. The administrator is responsible for ensuring a provisioner exists for that storage class and that provisioner automatically creates a volume of that type when a claim comes in. Each storage class can have different characteristics such as volume type (e.g. HDD vs SSD), volume read/write speeds, backup policies, etc.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
```

### Capacity

`{bm} /(Kinds\/Volume\/Capacity)_TOPIC/i`

Each persistent volume has a storage capacity.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-vol
spec:
  capacity:
    storage: 10Gi  # Capacity of the persistent volume.
```

A persistent volume claim can then be set to a capacity within some range.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-vol-claim
spec:
  resources:
    requests:
      storage: 1Gi  # Minimum capacity that the persistent volume should have.
    limits:
      storage: 5Gi  # Maximum capacity that the persistent volume should have.
```

### Access Modes

`{bm} /(Kinds\/Volume\/Access Modes)_TOPIC/i`

A persistent volume can support multiple access modes:

* `ReadWriteOnce` - volume is mountable by a single node in read-write mode.
* `ReadWriteOncePod` - volume is mountable by a single pod in read-write mode.
* `ReadWriteMany` - volume is mountable by many nodes in read-write mode.
* `ReadOnlyMany` - volume is mountable by many nodes in read-only mode.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-vol
spec:
  # Access modes for the persistent volume listed here.
  accessModes:
    - ReadWriteOnce
    - ReadOnlyMany
  capacity:
    storage: 10Gi
```

A persistent volume claim can then be set to target one or more access modes.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-vol-claim
spec:
  # Persistent volume selected must have these access modes
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

```{note}
A claim takes a list of access modes, so is it that a claim needs to get a volume with all access modes present or just one of the access modes present?
```

```{note}
Not all persistent volume types support all access modes. Types are discussed further below.
```

### Reclaim Policy

`{bm} /(Kinds\/Volume\/Reclaim Policy)_TOPIC/i`

A persistent volume claim, once released, may or may not make the persistent volume claimable again depending on the volume reclaim policy. The options available are ...

* `Retain` - keep all existing data on the persistent volume and prevent a new persistent volume claim from claiming it again.
* `Recycle` - delete all existing data on the persistent volume and allow a new persistent volume claim to claim it again.
* `Delete` - delete the persistent volume object itself.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-vol-claim
spec:
  persistentVolumeReclaimPolicy: Recycle  # Recycle the persistent volume once released
  resources:
    requests:
      storage: 1Gi
```

If the data on disk is critical to operations, the option to choose will likely be `Retain`.

```{note}
For retain specifically, once the existing persistent volume claim is released, the persistent volume itself goes into "Released" status. If it were available for reclamation, it would go into "Available" status. The book mentions that there is no way to "recycle" a persistent volume that's in "Released" status without destroying and recreating it.

According to the k8s docs, this is the way it is so that users have a chance to manually pull out data considered precious before it gets destroyed.
```

```{note}
Not all persistent volume types support all reclaim policies. Types are discussed further below.
```

### Types

`{bm} /(Kinds\/Volume\/Types)_TOPIC/i`

A persistent volume needs to come from somewhere, either via a cloud provider or using some internally networked (or even local) disks. There are many volume types: AWS elastic block storage, Azure file, Azure Disk, GCE persistent disk, etc.. Each type has its own set of restrictions such as what access modes it supports or the types of nodes it can be mounted.

The configuration for each type is unique. The following are sample configurations for popular types...

```{note}
The documentation says that a lot of these types are deprecated and being moved over to something called CSI (container storage interface), so these examples may need to be updated in the future
```

```yaml
# Amazon Elastic Block Storage
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-vol
spec:
  awsElasticBlockStore:
    volumeID: volume-id  # a volume with this ID must already exist in AWS
    fsType: ext4
```

```yaml
# Google Compute Engine Persistent Disk
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-vol
spec:
  gcePersistentDisk:
    pdName: test-vol  # a disk with this name must already exist in GCE
    fsType: ext4
```

```yaml
# Azure Disk
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-vol
spec:
  azureDisk:
    # a volume with this name and URI must already exist in Azure
    diskName: test.vhd
    diskURI: https://someaccount.blob.microsoft.net/vhds/test.vhd
```

```yaml
# Host path
#   -- this is a path on the node that the pod gets scheduled on, useful
#      for debugging purposes.
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-vol
spec:
  hostPath:
    path: /data
```

### Storage Classes

`{bm} /(Kinds\/Volume\/Storage Classes)_TOPIC/i`

```{prereq}
Kinds/Volume/Reclaim Policy_TOPIC
Kinds/Volume/Types_TOPIC
```

Defining a storage class allows for dynamic provisioning of persistent volumes per persistent volume claim.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
# The two fields below ("provisioner" and "parameters" define how persistent volumes are to
# be created and are unique to each volume type. In this example, the storage class
# provisions new persistent volumes on AWS. Any persistent volume claim with storage class
# name set to `standard` will call out to this AWS elastic store provisioner to create a
# persistent volume of type "awsElasticBlockStore" which gets assigned to it.
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
# This field ("reclaimPolicy") maps to a persistent volume's
# "persistentVolumeReclaimPolicy", except that "Recycle" isn't one of the allowed options:
# Only "Delete" and "Retain" are allowed. This example uses "Retain". If unset, the reclaim
# policy of a dynamically provisioned persistent volume is "Delete". 
reclaimPolicy: Retain
# When this field ("allowVolumeExpansion") is set to true, the persistent volume can be
# resized by editing the persistent volume claim object. Only some volume types support
# volume expansion. This example will work because AWS elastic block store volume types do
# support volume expansion.
allowVolumeExpansion: true
```

To use a storage class in a persistent volume claim, supply the name of that storage class.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-vol-claim
spec:
  storageClassName: standard  # Use the storage class defined above for this claim
  resources:
    requests:
      storage: 1Gi
  accessModes:
    - ReadWriteOnce
```

```{note}
Since these persistent volumes are being dynamically provisioned, it doesn't make sense to have `Recycle`. You can just `Delete` and if a new claim comes in it'll automatically provision a new volume. It's essentially the same thing as `Recycle`.
```

If a persistent volume claim provides no storage class name, that persistent volume claim will use whatever storage class Kubernetes has set as its default. Recall that leaving the storage class name unset is *not* the same as leaving it as an empty string. To leave unset means to keep it out of the declaration entirely. If the storage class name is ...

* set to an empty string, it tells Kubernetes to find any _existing_ persistent volume for the persistent volume claim.
* set to a non-empty string, it tells Kubernetes to use that storage class to dynamically provision a persistent volume for the persistent volume claim.
* unset, it tells Kubernetes to use the default storage class to dynamically provision a persistent volume for the persistent volume claim.

Most Kubernetes installations have a default storage class available, identified by the storage class having the annotation `storageclass.kubernetes.io/is-default-class=true`.

````{note}
The following example shows the default storage class on microk8s.

```
# kubectl get sc
# Note how the name identifies it as the default.
NAME                          PROVISIONER            RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
microk8s-hostpath (default)   microk8s.io/hostpath   Delete          WaitForFirstConsumer   false                  6s
```

```yaml
# kubectl get sc microk8s-hostpath -o yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"storage.k8s.io/v1","kind":"StorageClass","metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"},"name":"microk8s-hostpath"},"provisioner":"microk8s.io/hostpath","volumeBindingMode":"WaitForFirstConsumer"}
    storageclass.kubernetes.io/is-default-class: "true"
  creationTimestamp: "2022-07-22T19:41:28Z"
  name: microk8s-hostpath
  resourceVersion: "2775"
  uid: 1df92cbc-6e2f-4726-a487-a81b1fcd8d2b
provisioner: microk8s.io/hostpath
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
```
````

## Endpoints

`{bm} /(Kinds\/Endpoints)_TOPIC/i`

Endpoints (plural) is a kind that simply holds a list of IP addresses and ports. It's used by higher-level kinds to simplify routing. For example, an endpoints object may direct to all the nodes that make up a sharded database server.

Example manifest:

```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: database
subsets: 
  - addresses:
      - ip: 10.10.1.1
      - ip: 10.10.1.2
      - ip: 10.10.1.3
    ports:
      - port: 5432 
        protocol: TCP  # TCP or UDP, default: TCP
        name: pg
  - addresses:
      - ip: 10.13.4.101
      - ip: 10.13.4.102
      - ip: 10.13.4.103
    ports:
      - port: 12345
        protocol: TCP  # TCP or UDP, default: TCP
        name: pg2
```

The endpoints example above points to ...

 * `10.10.1.1:5432`
 * `10.10.1.2:5432`
 * `10.10.1.3:5432`
 * `10.13.4.101:12345`
 * `10.13.4.102:12345`
 * `10.13.4.103:12345`

## Service

`{bm} /(Kinds\/Service)_TOPIC/i`

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
    - name: webapp-port
      protocol: TCP
      port: 80
      targetPort: 9376
```

```{note}
Internally, an endpoints object is used to track pods. When you create a service, Kubernetes automatically creates an accompanying endpoints object that the service makes use of.
```

### Routing

`{bm} /(Kinds\/Service\/Routing)_TOPIC/i`

```{prereq}
Introduction/Labels_TOPIC
Kinds/Endpoints_TOPIC
```

A service determines which pods it should route traffic to via label selectors.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  # Label selectors that pick out the pods this service routes to.
  selector:
    key1: value1
    key2: value2
    key3: value3
  ports:
    - name: webapp-port
      protocol: TCP
      port: 80
      targetPort: 9376
```

Internally, the service creates and manages an endpoints object containing the IP and port for each pod captured by the selector. If no selectors are present, the service expects an endpoints object with the same name to exist, where that endpoints object contains the list of IP and port pairs that the service should route to.

```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: database  # Must be same name as the service
subsets: 
  - addresses:
      - ip: 10.10.1.1
      - ip: 10.10.1.2
      - ip: 10.10.1.3
    ports:
      - port: 5432
```

If no label selectors are present but the service's type is set to `ExternalName`, the service will route to some user-defined host. This is useful for situations where you want to hide the destination, such as an external API that you also want to mock for development / testing.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ExternalName
  externalName: api.externalcompany.com  # Route to this host
  ports:
    - name: api-port
      protocol: TCP
      port: 8080
      targetPort: 5000
```

```{note}
If not set, `spec.type` defaults to `ClusterIP`. That's the type used when selectors are used to create an endpoints / a custom endpoints is used.
```

### Ports

`{bm} /(Kinds\/Service\/Ports)_TOPIC/i`

```{prereq}
Kinds/Pod/Ports_TOPIC
Kinds/Service/Routing_TOPIC
```

A service can listen on multiple ports.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  # In most cases, each port entry has ...
  #
  #  * "name", which is a friendly name to identify the port (optional)
  #  * "protocol", which is either `TCP` or `UDP` (defaults to `TCP`).
  #  * "port", which is the port that the service listens on.
  #  * "targetPort", which  is the port that requests are forwarded to on the pod (defaults
  #     to value set for "port").
  ports:
    - name: webapp-port
      protocol: TCP
      port: 80
      targetPort: 9376
    - name: api-port
      protocol: TCP
      port: 8080
      targetPort: 1111
```

```{note}
Not having a name makes it more difficult for pods to discover a service. Discussed further in the service discovery section.
```

The example above forwards requests on two ports. Requests on port ...

 * 80 of the service get forwarded to port 9376 of a pod assigned to that service.
 * 8080 of the service get forwarded to port 1111 of a pod assigned to that service.

Ports may also reference the names of ports in a pod. For example, the following pod provides names for its ports.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image:1.0
      ports:
        - name: my-http-port  # Name for the port
          containerPort: 8080
          protocol: TCP
```

In the service targeting that pod, you can use `my-http-port` as a target port.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - name: webapp-port
      protocol: TCP
      port: 80
      targetPort: my-http-port  # The name of the port in the pod
```

```{note}
Does this work for manual endpoints as well? When a selector isn't used with a service, it looks for an endpoints object of the same name as the service to figure out where the service should route to. That endpoints object can have names associated with its ports as well.
```

```{note}
A service decides which pods it routes to based key-value pairs in on `spec.selector`. What happens if the key-value pairs identify a set of pod instances where some of those instances don't have a port named `my-http-port`. For example, a service may be forwarding to two applications rather than a single application which just could be sharing the same set of key-value labels (pod instances are heterogenous).

Maybe this isn't possible with Kubernetes?
```

### Health

`{bm} /(Kinds\/Service\/Health)_TOPIC/i`

```{prereq}
Kinds/Pod/Lifecycle/Probes_TOPIC
Kinds/Service/Routing_TOPIC
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
Recall that, when a service has selectors assigned, Kubernetes internally maintains an endpoints object that contains the addresses of ready and healthy pods. The addresses in this endpoints object is what the service routes to.
```

### Headless

`{bm} /(Kinds\/Service\/Headless)_TOPIC/i`

```{prereq}
Kinds/Service/Routing_TOPIC
Kinds/Service/Health_TOPIC
```

A headless service is one in which there is no load balancer forwarding requests to pods / endpoints. Instead, the domain for the service will resolve a list of ready IPs for the pods (or endpoints) that the service is for. 

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  # When this field ("clusterIP") is set to "None", the service is a "headless service".
  clusterIP: None
  selector:
    app: MyApp
  ports:
    - name: webapp-port
      protocol: TCP
      port: 80
```

Generally, headless services shouldn't be used because DNS queries are typically cached by the operating system. If the IPs that a service forwards to change, apps that have recently queried the service's DNS will continue to use the old (cached) set of IPs until the operating system purges its DNS cache.

### Session Affinity

`{bm} /(Kinds\/Service\/Session Affinity)_TOPIC/i`

How a service decides to forward incoming requests to the pod instances assigned to it is controlled via a session affinity field. Assigning a value of ...

 * `None` forwards each request to a randomly selected pod instance (default behavior).
 * `ClientIP` forwards each request originating from the same IP to the same pod instance.

When using `ClientIP`, a maximum session "sticky time" may also be provided.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  # The two fields below ("sessionAffinity" and "sessionAffinityConfig") define how session
  # affinity works.
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10000  # Defaults value is 108300, which is around 3 hours
  selector:
    app: MyApp
  ports:
    - name: webapp-port
      protocol: TCP
      port: 80
```

```{note}
When using `ClientIP`? What happens when the service runs out of memory to track client IPs? LRU algorithm to decide which to keep / discard?
```

```{note}
The book mentions that because services work on the TCP/UDP level and not at HTTP/HTTPS level, forwarding requests by tracking session cookies isn't a thing.
```

### Exposure

`{bm} /(Kinds\/Service\/Exposure)_TOPIC/i`

The service type defines where and how a service gets exposed. For example, a service may only be accessible within the cluster, to specific parts of the cluster, to an external network, or to the public Internet.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP  # Service type
  selector:
    app: MyApp
  ports:
    - name: webapp-port
      protocol: TCP
      port: 80
```

If not specified, the type is `ClusterIP`, meaning that it's exposed only locally within the cluster.

#### Local

`{bm} /(Kinds\/Service\/Exposure\/Local)_TOPIC/i`

```{prereq}
Kinds/Service/Routing_TOPIC
```

Services of type `ClusterIP` / `ExternalName` are only accessible from within the cluster. The hostname of such services are broken down as follows: NAME.NAMESPACE.svc.CLUSTER

 * *NAME* is the name of the service.
 * *NAMESPACE* is the namespace the service is in (defaults to `default`).
 * svc is a constant that identifies the host is for a service.
 * *CLUSTER* is the name of the cluster (defaults to `cluster.local.`).

Depending on what level you're working in, a hostname may be shortened. For example, if the requestor and the service are within ...

 * the same namespace and cluster, hostname NAME is sufficient.
 * the same cluster but not the same namespace, hostname NAME.NAMESPACE is sufficient.
 * different clusters, the full hostname NAME.NAMESPACE.svc.CLUSTER is required.

The IP for a `ClusterIP` / `ExternalName` service is stable as well, just like the hostname.

```{note}
Internally, a `ClusterIP` service uses kube-proxy to route requests to relevant pods (endpoints).
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP  # ClusterIP service type
  selector:
    app: MyApp
  ports:
    - name: webapp-port
      protocol: TCP
      port: 80
```

#### Node Port

`{bm} /(Kinds\/Service\/Exposure\/Node Port)_TOPIC/i`

Services of type `NodePort` are accessible from outside the cluster. Every worker node opens a port (either user-defined or assigned by the system) that routes requests to the service. Since nodes are transient, there is no single point of access to the service.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort  # Nodeport service type
  selector:
    app: MyApp
  ports:
    # When "NodePor"` is used as the type, each port should have "nodePort" field that
    # defines the port on the worker nodes to open.
    - protocol: TCP
      port: 80
      targetPort: 9376
      nodePort: 8080
```

```{seealso}
Kinds/Pod/Container Isolation/Node Access_TOPIC (Somewhat similar `hostPort` feature of container port mapping)
```

#### Load Balancer

`{bm} /(Kinds\/Service\/Exposure\/Load Balancer)_TOPIC/i`

Services of type `LoadBalancer` are accessible from outside the cluster. When the `LoadBalancer` type is used, the cloud provider running the cluster assigns their version of a load balancer to route external HTTP requests to the Kubernetes ingress component. Ingress then determines what service that request should be routed to based on details within the HTTP parameters (e.g. Host).

There is no built-in Kubernetes implementation of ingress. Kubernetes provides the interface but someone must provide the implementation, called an ingress controller, for the functionality to be there. This is because load balancers come in multiple forms: software load balancers, cloud provider load balancers, and hardware load balancers. When used directly, each has a unique way it needs to be configured, but the ingress implementation abstracts that out.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
      nodePort: 8080
    ...
```

Once provisioned, the object will have the field `status.loadBalancer.ingress.ip` added to it, which states the IP of the load balancer forwarding requests to this service.

```yaml
# <REMOVED PREAMBLE>
spec:
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
      nodePort: 8080
status:
  loadBalancer:
    ingress:
      ip: 192.0.5.6
```

```{note}
You can also use `kubectl` to get a list of services and it'll also list out the public IP.
```

```{note}
The book says that a load balancer type is a special case of node port type.
```

## Ingress

`{bm} /(Kinds\/Ingress)_TOPIC/i`

```{prereq}
Kinds/Service_TOPIC
```

Similar to a service of type `LoadBalancer`, An ingress object is a load balancer with a publicly exposed IP. However, rather than load balancing at the TCP/UDP level, an ingress object acts as a load balancing HTTP proxy server. An HTTP request coming into an ingress object gets routed to one of many existing services based on host and path HTTP headers. This is useful because the cluster can expose several services under a single public IP address.

```{svgbob}
                                                                           +---------------------------------+
                                stats.myhost.com/graphana   .---------.    | .-----. .-----. .-----. .-----. |
                              .---------------------------->| Service |--->| | Pod | | Pod | | Pod | | Pod | |
                              |                             '---------'    | '-----' '-----' '-----' '-----' |
                              |                                            +---------------------------------+
                              |
                              |                                            +---------------------------------+
                              | api.myhost.com/v1           .---------.    | .-----. .-----. .-----. .-----. |
                              +---------------------------->| Service |--->| | Pod | | Pod | | Pod | | Pod | |
                              |                             '---------'    | '-----' '-----' '-----' '-----' |
.---------.    .---------.    |                                            +---------------------------------+
| Request |--->| Ingress |----+
'---------'    '---------'    |                                            +---------------------------------+
                              | api.myhost.com              .---------.    | .-----. .-----. .-----. .-----. |
                              +---------------------------->| Service |--->| | Pod | | Pod | | Pod | | Pod | |
                              |                             '---------'    | '-----' '-----' '-----' '-----' |
                              |                                 ^          +---------------------------------+
                              | api.myhost.com/v2               |
                              '---------------------------------'
```

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
  - host: stats.myhost.com
    http:
      paths:
      - path: /graphana
        pathType: Prefix
        backend:
          service:
            name: graphana-service
            port:
              number: 80
  - host: api.myhost.com
    http:
      paths:
      - path: /v2
        pathType: Prefix
        backend:
          service:
            name: api-service-v2
            port:
              number: 80
      - path: /v1
        pathType: Prefix
        backend:
          service:
            name: api-service-v1
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service-v2
            port:
              number: 80
```

```{note}
According to the book, most if not all implementations of ingress simply query the service for its endpoints and directly load balance across them vs forwarding the request through that service. Note that the port in the example above is still the port that the *service* is listening on, not the port of the pod is listening on.
```

### Hosts

`{bm} /(Kinds\/Ingress\/Hosts)_TOPIC/i`

The host in each rule can be either an exact host or it could contain wildcards (e.g. `*.api.myhost.com`). Each name in the host (split by dot) intended for a wildcard should explicitly have an asterisk in its place. The portion the asterisk is in must exist and it only covers that name. For example, the rule below will match `ONE.api.myhost.com`, but not `TWO.THREE.api.myhost.com` or `api.myhost.com`.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
  - host: "*.api.myhost.com"
    - path: /v2
      pathType: Prefix
      backend:
        service:
          name: api-service-v2
          port:
            number: 80
```

### Path Type

Each rule entry should have a path type associated with it. It can be set to any of the following values:

 * `Exact` - Matches the URL path exactly (case-sensitive).
 * `Prefix` - Matches the URL path prefix (case-sensitive).
 * `ImplementationSpecific` - Based on the class of the ingress object.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
  - host: api.myhost.com
    http:
      paths:
      - path: /my/prefix/path
        pathType: Prefix
        backend:
          service:
            name: api-service-v2
            port:
              number: 80
```

The most common path type is `Prefix`. A type of `Prefix` splits the path using `/` and matches the rule if the incoming request's path starts with the same path elements as the rule's path. Trailing slashes are ignored (e.g. `/p1/p2/p3/` and `/p1/p2/p3` are equivalent).

```{note}
What about `ImplementationSpecific`? There are different types of ingress controllers, each of which has its own configuration options. An ingress class is something you can put into your ingress object that contains "configuration including the name of the controller that should implement the class." It seems like an advanced topic and I don't know enough to write about it. Probably not something you have to pat attention to if you're doing basic cloud stuff.
```

### TLS Traffic

`{bm} /(Kinds\/Ingress\/TLS Traffic)_TOPIC/i`

```{prereq}
Kinds/Pod/Configuration_TOPIC
```

Assuming you have a TLS certificate and key files for the host configured on the ingress object, you can add those into Kubernetes as a secret and configure the ingress object to make use of it.

```yaml
# openssl genrsa -out tls.key 2048
# openssl req -new -x509 -key tls.key -out tls.cert -days 360 -subj /CN=api.myhost.com
# kubectl create secret tls my-api-tls --cert=tls.crt --key=tls.key
apiVersion: v1
kind: Secret
metadata:
  name: my-api-tls
type: kubernetes.io/tls
data:
  tls.crt: base64 encoded cert
  tls.key: base64 encoded key
```

Each certificate secret used by an ingress object has its own entry that contains the hosts it supports.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  # TLS certificates are listed here. Each entry has a certificate secret name under
  # "secretName" and the domain(s) supported by that certificate under "hosts". Hosts must
  # match hosts explicitly listed in the ingress object's rules.
  tls:
    - secretName: my-api-tls
      hosts:                
        - api.myhost.com
    - secretName: my-stats-tls
      hosts:
        - stats.myhost.com
      
```

Once an encrypted request comes in to the ingress controller, it's decrypted. That decrypted request then gets forwarded to the service it was intended for.

```{note}
From the k8s website: 

> You need to make sure the TLS secret you created came from a certificate that contains a Common Name (CN), also known as a Fully Qualified Domain Name (FQDN) for https-example.foo.com.

> Keep in mind that TLS will not work on the default rule because the certificates would have to be issued for all the possible sub-domains. Therefore, hosts in the tls section need to explicitly match the host in the rules section.
```

```{note}
The book mentions that `CertificateSigningRequest` is a special type of kind that will sign certificates for you, if it was set up. You can issue requests via `kubectl certificate approve csr_name` and it'll either automate it somehow or a human will process it? Not sure exactly what's going on here.
```

## Namespace

`{bm} /(Kinds\/Namespace)_TOPIC/i`

A namespace is a kind used to avoid naming conflicts. For example, it's typical for a Kubernetes cluster to be split up into development, testing, and production namespaces. Each namespace can have objects with the same names as those in the other two namespaces.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
```

Namespaces are cluster-level objects. This is contrary to most other kinds in Kubernetes, which are namespace-level objects, meaning that a namespace can be used to disambiguate objects of that type with the same name...

```yaml
# These are namespace-level objects
apiVersion: v1
kind: Pod
metadata:
  name: mypod
  namespace: testing  # put into the testing namespace
spec:
  containers:
  - name: mypod
    image: my_image:v2_alpha5
---
apiVersion: v1
kind: Pod
metadata:
  name: mypod
  namespace: production  # put into the production namespace
spec:
  containers:
  - name: mypod
    image: my_image:v1
```

If a namespace-level object doesn't set a namespace, the namespace defaults to `default`.

## Replica Set

`{bm} /(Kinds\/Replica Set)_TOPIC/i`

```{prereq}
Kinds/Pod_TOPIC
Kinds/Volume_TOPIC
```

```{note}
Replica sets deprecate a replication controllers.
```

A replica set is an abstraction that's used to ensure a certain number of copies of some pod are always up and running. Typical scenarios where replica sets are used include ...

 * sharding (e.g. workers that pull job out of a queue for processing).
 * scale (e.g. microservices that scale horizontally).
 * redundancy (e.g. leader-follower architectures such as Redis-style replica servers).

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: my-replicaset
spec:
  replicas: 2  # Number of pod copies to run.
  # Selectors are label selectors used to identify pods, which match the key-value pairs
  # used for pod template labels further down.
  selector:
    matchLabels:
      app: my-app
  # A template of the pod to launch when there aren't enough copies currently running.
  # Everything under "template" is essentially a pod manifest, except the "apiVersion" and
  # "kind" aren't included.
  template:
    metadata:
      name: my-pod
      # These labels are how this replicate set will determine how many copies are running. It
      # will look around for pods with this set of labels.
      labels:
        app: my-app
    spec:
      containers:
      - name: my-container
        image: nginx
```

Recall that, to link objects together, Kubernetes uses loosely coupled linkages via labels rather than hierarchical parent-child relationships. As such, the pod template should have a unique set of labels assigned that the replica set can look for to determine how many instances are running. Regardless of how those instances were launched (via the replica set or something else), the replica set will account for them. In the example above, the replica set determines pod instances it's responsible for by looking for the label named `app` and ensuring its set to `my-app`.

```{note}
According to the k8s docs, it may be a parent-child relationship. Apparently looking for labels is just an initial step to permanently bringing pods under the control of a specific replica set:

> A ReplicaSet is linked to its Pods via the Pods' metadata.ownerReferences field, which specifies what resource the current object is owned by. All Pods acquired by a ReplicaSet have their owning ReplicaSet's identifying information within their ownerReferences field. It's through this link that the ReplicaSet knows of the state of the Pods it is maintaining and plans accordingly.

What happens when two replica sets try "owning" the same pod?
```

A replica set's job is to ensure that a certain number of copies of a pod template are running. It won't retain state between its copies or do any advanced orchestration. Specifically, a replica set ...

 * won't retain pod IPs / hostnames across time. Each launched pod will have its own unique IP / hostname, even if it's replacing a downed pod (it won't inherit that downed pod's IP / hostname). 
 * will force all pods to use a single persistent volume claim (if one was specified in the pod template), meaning all pods will use a single volume. For horizontally scalable applications (e.g. microservices, databases, etc..), each running instance of an application typically needs its own persistent storage.

```{note}
If one of the replicas is in a loop where it's constantly crashing and restarting, that replica will stay as-is in the replica set. It won't automatically get moved to some other node / forcefully removed and re-added as a new replica.
```

```{note}
You can distinguish a pod created by a replica set vs one created manually by checking the annotation key `kubernetes.io/create-by` on the pod.

If deleting a replica set, use `--cascade=false` in `kubectl` if you don't want the pods created by the replica set to get deleted as well.
```

```{seealso}
Kinds/Deployment_TOPIC (Like replica sets but supports rolling updates of an application)
Kinds/Stateful Set_TOPIC (Like replica sets but supports individual persistent volume claims)
```

## Deployment

`{bm} /(Kinds\/Deployment)_TOPIC/i`

```{prereq}
Kinds/Replica Set_TOPIC
```

Deployment are similar to replica sets but make it easy to do rolling updates, where the update happens while the application remains online and still services requests. Old pods are transitioned to new pods as a stream instead of all at once, ensuring that the application is responsive throughout the upgrade process. Likewise, they allow for rolling back should an update encounter any problems.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
# The manifest for a deployment builds off the manifest for a replica set. Most replica set
# fields are present: Number of copies, label selectors, pod template, etc... In addition,
# it supports several other fields specific to doing updates.
spec: 
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
      labels:
        app: my-app
    spec:
      containers:
        - name: my_container
          image: my-image:1.0
  strategy: RollingUpdate  # How the deployment should perform updates (default value)
```

A deployment provides mechanisms to control how an update happens (e.g. all at once vs gradual), if an update is deemed successful (e.g. maximum amount of time a rollout can take), fail-fast for bad updates, and rollbacks to revert to previous versions. These features are discussed in the subsections below. 

```{note}
If one of the replicas is in a loop where it's constantly crashing and restarting, that replica will stay as-is in the deployment. It won't automatically get moved to some other node / forcefully removed and re-added as a new replica.
```

```{note}
The same gotchas with replica sets also apply to deployments: all pods will use the same persistent volume claim and IPs / hosts aren't retained when pods are replaced.

Like with replica set, you might have to use `--cascade=false` in `kubectl` if you don't want the pods created by the deployment to get deleted as well (unsure about this).
```

```{seealso}
Kinds/Stateful Set_TOPIC (Like replica sets but supports individual persistent volume claims)
```

### Updates

`{bm} /(Kinds\/Deployment\/Updates)_TOPIC/i`

```{prereq}
Kinds/Pod/Lifecycle/Probes_TOPIC
```

A deployment can support one of the two update strategies:

 * `RollingUpdate` - updates pods piecemeal (default).
 * `Recreate` - updates by first bringing down all old pods then bringing up all the new pods.

`Recreate` is simple but results in down (a period of time where no pods are running). Most enterprise applications have up-time guarantees and as such require `RollingUpdate`. `RollingUpdate` has several options that control the flow and timing of how pods go down and come up, documented in the example below.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 10
  selector:
    matchLabels:
      app: my-app
  template:
      labels:
        app: my-app
    spec:
      containers:
        - name: my_container
          image: my-image:1.0
  strategy:
    type: RollingUpdate
    rollingUpdate:
      # "maxUnavailable" - During an update, this is the number (or percentage) of pods
      # that can be unavailable relative to the number of replicas. Since this deployment
      # has 10 replicas, the parameter below is instructing that the number of replicas
      # can't go below 8 during an update (at most 2 pods may be unavailable).
      #
      # If between 0 and 1, this is treated as a percentage of pods (e.g. 0.25 means 25
      # percent of pods may be unavailable during an update). 
      maxUnavailable: 2
      # "maxSurge" - During an update, this is the number (or percentage) of excess pods
      # that can be available relative to the number of replicas. Since this deployment
      # has 10 replicas, the parameter below is instructing that the number of replicas
      # can't go above 12 during an update (at most 2 pods extra pods may be running).
      #
      # If between 0 and 1, this is treated as a percentage of pods (e.g. 0.25 means 25
      # percent of pods may be unavailable during an update). 
      maxSurge: 2
      # "minReadySeconds" - Once all of the readiness probes of a new pod succeed, this
      # is the number of seconds to wait before the deployment deems that the pod has
      # been successfully brought up. If any readiness probes within the pod fail during
      # this wait, the update is blocked.
      #
      # This is useful to prevent scenarios where pods initially report as ready but
      # revert to un-ready soon after receiving traffic.
      minReadySeconds: 10
      # "progressDeadlineSeconds" - This is the maximum number of seconds that is allowed
      # before progress is made. If this is exceeded, the deployment is considered stalled.
      #
      # Default value is 600 (10 minutes).
      progressDeadlineSeconds: 300
```

It's common for deployments to fail or get stuck for several reasons:

* Insufficient node resources.
* Problems pulling images.
* Probe failures (startup probes / readiness probes).
* etc..

### Rollbacks

`{bm} /(Kinds\/Deployment\/Rollbacks)_TOPIC/i`

A deployment retains update history in case it needs to rollback. The mechanism used for this is replica sets: For each update, a deployment launches a new replica set. The replica set for the old version ramps down the number of pods while the replica set for the new version ramps up the number of pods. Once all pods have been transitioned to the new version, the old replica set (now empty of pods) is kept online.

It's good practice to limit the number of revisions kept in a deployments update history because it limits the number of replica sets kept alive.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  revisionHistoryLimit: 5  # Keep the 5 latest revisions
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
      labels:
        app: my-app
    spec:
      containers:
        - name: my_container
          image: my-image:1.0
```

```{note}
You can inspect previous versions via `kubectl rollout history deployment my-deployment`. For each update, it's good practice to set the `kubernetes.io/change-cause` annotation a custom message describing what was updated / why it was updated -- this shows up in the history.

You can rollback via `kubectl rollout undo deployments my-deployment --to-revision=12345`.
```

## Stateful Set

`{bm} /(Kinds\/Stateful Set)_TOPIC/i`

```{prereq}
Kinds/Replica Set_TOPIC
Kinds/Deployment_TOPIC
Kinds/Volume_TOPIC
Kinds/Service/Headless_TOPIC
```

A stateful set is similar to a deployment but the pods it creates are guaranteed to have a stable identity and each pod can have its own dedicated storage volumes. In the context of stateful sets, ...

 * stable identity means that if a pod goes down, the stateful set responsible for it will replace it with a new pod has the exact same identification information (same name, IP, etc..). Contrast that to deployments, where replacement pods have entirely new identities.
 * dedicated storage volume means that each stable identity can have its own unique persistent volume claims. Contrast that to deployments, where persistent volume claims are shared across all pods.

```{note}
"Stable identity" doesn't imply that a replacement pod will be scheduled on the same node. The replacement may end up on another node.
```

A stateful set requires three separate pieces of information:

 1. a headless service, which acts as a gateway to a stateful set's pods (referred to as a governing service).
 2. a volume claim template, which templates persistent volume claims for a stateful set's pods.
 3. a pod template, which templates pods similar to pod template for a deployment.

These three pieces are represented as two separate objects: the governing service and the stateful set itself.

```yaml
# Manifest #1: Headless service for the stateful set's pods (governing service).
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  clusterIP: None
  # Routes traffic to pods based on the following label selectors, which are the same
  # key-value pairs used for pod template labels of the stateful set further down.
  selector:
    app: my-app
  ports:
    - name: http
      port: 80
----
# Manifest #2: The stateful set itself, which contains both the pod template and the
# volume claim template.
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: my-stateful-set
spec:
  # Selectors are label selectors used to identify pods, which match the key-value pairs
  # used for pod template labels further down.
  selector:
    matchLabels:
      app: my-app
  serviceName: my-service  # Name of headless service for stateful set (governing service).
  replicas: 3              # Number of replicas for the stateful set.
  # Persistent volume claims will be created based on the following template.
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        resources:
          requests:
             storage: 1Mi
        accessModes:
          - ReadWriteOnce
  # Pod's will be created based on the following template. Note that the volume mount
  # references the persistent volume claim template described above.
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-container
          image: my-image:1.0
          ports:
            - name: http
              containerPort: 8080
          volumeMounts:
            - name: data
              mountPath: /var/data
  # Similar to deployments, stateful sets also support updating / rollback mechanisms exist,
  # but not exactly the same ones.
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
   # Once all of the readiness probes of a new pod succeed, this is the number of seconds to
   # wait before the stateful set deems the pod to be available. No readiness probes within
   # the pod can fail during this wait.
  minReadySeconds: 10
```

The example above creates a stateful set that manages three pod replicas and a governing service for those pods. The pods created by the stateful set are numbered starting from 0: `my-stateful-set-0`, `my-stateful-set-1`, and `my-stateful-set-2`. In addition, each pod gets its own persistent volume claim mounted at `/data` containing a modest amount of storage space. That persistent volume claim will have the format `data-my-stateful-set-N` (where `N` is the ordinal suffix)

```{svgbob}
                    .--> "my-stateful-set-0 with PVC data-my-stateful-set-0"
                    |
my-stateful-set ----+--> "my-stateful-set-1 with PVC data-my-stateful-set-1"
                    |
                    '--> "my-stateful-set-2 with PVC data-my-stateful-set-2"
```

The ordinal suffixes of a stateful set's pods are part of their stable identity. If a pod were to die, the volume for that stable identity will be re-bound to its replacement. Stateful sets take great care to ensure that no more than one pod will ever be running with the same stable identity so as to prevent race conditions (e.g. conflicts regarding IP / host, multiple pods using the same volume, etc..). In many cases, that means a pod won't be replaced until the stateful set is absolutely sure that it has died.

```{note}
If one of the replicas is an a loop where its constantly crashing and restarting, that replica will stay as-is in the stateful set. It won't automatically get moved to some other node / forcefully removed and re-added as a new replica.
```

```{seealso}
Kinds/Stateful Set/Scaling_TOPIC (Scaling via ordinal suffixes and race condition prevention)
Kinds/Stateful Set/Updates_TOPIC (Race condition prevention on pod updates)
```

### Scaling

`{bm} /(Kinds\/Stateful Set\/Scaling)_TOPIC/i`

Because of stable identity guarantees and the fact that each stable identity can have its own distinct volumes, stateful sets have different scaling behavior than deployments. A stateful set scales pods based on the ordinal suffix of its pod names. When the number of replicas is ...

 * decreased, the stateful set brings down the pods with the highest ordinal suffixes first (decrementing).
 * increased, the stateful set brings up new pods with the next unused ordinal suffixes (incrementing).

For example, given the stateful set `my-stateful-set` with 3 replicas (those replicas being pods `my-stateful-set-0`, `my-stateful-set-1`, and `my-stateful-set-2`), ...

 * decrementing the replica count to 1 is guaranteed to shut down pods `my-stateful-set-2` and `my-stateful-set-1` (in that order).
 * incrementing the replica count to 5 is guaranteed to spin up pods `my-stateful-set-4` and `my-stateful-set-5` (in that order).

The scaling behavior makes the stable identities of the pods being removed / added known beforehand. In contrast, a deployment's scaling behavior makes no guarantees as to which replicas get removed / added and in what order.

```{svgbob}
                    .--> "my-stateful-set-0 with PVC data-my-stateful-set-0"
                    |
my-stateful-set ----+--> "my-stateful-set-1 with PVC data-my-stateful-set-1"
                    |
                    '--> "my-stateful-set-2 with PVC data-my-stateful-set-2 (scale from here)"
```

Stateful sets scale one pod at a time to avoid race conditions that are sometimes present in distributed applications (e.g. which database server is the primary vs which database server is the replica). When scaling down, the persistent volumes for a pod won't be removed along with the pod. This is to avoid permanently deleting data in the event of an accidental scale down. Likewise, when scaling up, if a volume for that stable identity is already present, that volume gets attached instead of creating a new volume.

For example, given the same 3 replica `my-stateful-set` example above, changing the number of replicas to 1 will leave the volumes for `my-stateful-set-1` and `my-stateful-set-2` lingering undeleted.

```{svgbob}
                    .--> "my-stateful-set-0 with PVC data-my-stateful-set-0"
                    |
my-stateful-set ----+    "unassigned PVC data-my-stateful-set-1"
                    
                         "unassigned PVC data-my-stateful-set-2"
```

Changing the number of replicas back to 3 will then recreate `my-stateful-set-1` and `my-stateful-set-2`, but those new pods will be assigned the lingering undeleted volumes from before rather than being assigned new volumes (all previous data will be present).

```{svgbob}
                    .--> "my-stateful-set-0 with PVC data-my-stateful-set-0"
                    |
my-stateful-set ----+--> "my-stateful-set-1 with PVC data-my-stateful-set-1 (PVC contains previous data)"
                    |
                    '--> "my-stateful-set-2 with PVC data-my-stateful-set-2 (PVC contains previous data)"
```

A stateful set will not proceed with scaling until all preceding pods (ordinal suffix) are in a healthy running state. This is because, if a pod is unhealthy and the stateful set gets scaled down, it's effectively lost two members at once. This goes against the "only one pod can go down at a time" stateful set scaling behavior.

For example, given the same 3 replica `my-stateful-set` example above, scaling down to 1 replica will first shut down pod `my-stateful-set-2` and then pod `my-stateful-set-1`. If `my-stateful-set-2` shuts down but then `my-stateful-set-0` enters into an unhealthy state, `my-stateful-set-1` won't shut down until `my-stateful-set-0` recovers. Likewise, if `my-stateful-set-0` enters into an unknown state (e.g. the node running it temporarily lost communication with the control plane), `my-stateful-set-1` won't shut down until `my-stateful-set-0` is known and healthy.

```{note}
The scaling guarantees described here can be relaxed through `spec.podManagementPolicy`. By default, this value is set to `OrderedReady`, which enables the behavior described in this section. If it were instead set to `Parallel`, the stateful set's scaling will launch / terminate pods in parallel and won't wait for preceding pods to be healthy.
```

### Updates

`{bm} /(Kinds\/Stateful Set\/Updates)_TOPIC/i`

```{prereq}
Kinds/Deployment/Updates_TOPIC
Kinds/Volume/Storage Classes_TOPIC
Kinds/Stateful Set/Scaling_TOPIC
```

There are two templates in a stable set: a pod template and a volume claim template.

A pod template has two different update strategies:

 * `RollingUpdate` - updates pods piecemeal (default).
 * `OnDelete` - user must manually bring down each pod and the stateful set will replace it with updated version.

`OnDelete` is simple but requires user intervention to shutdown pods. `RollingUpdate` is similar to the `RollingUpdate` strategy for deployments, but it supports fewer parameters and its behavior is slightly different. Specifically, rolling updates for stateful sets support two parameters.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: my-ss
spec:
  selector:
    matchLabels:
      app: my-app
  serviceName: my-service
  replicas: 10
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-container
          image: my-image:1.0
  # Rolling update strategy.
  strategy:
    type: RollingUpdate
    rollingUpdate:
      # "maxUnavailable" - During an update, this is the number (or percentage) of pods
      # that can be unavailable relative to the number of replicas. Since this deployment
      # has 10 replicas, the parameter below is instructing that the number of replicas
      # can't go below 8 during an update (at most 2 pods may be unavailable).
      #
      # If between 0 and 1, this is treated as a percentage of pods (e.g. 0.25 means 25
      # percent of pods may be unavailable during an update). 
      maxUnavailable: 1
      # "partition" - Only pods with suffix ordinals that are >= to this number will
      # receive updates. All other pods will remain un-updated. For this stateful set,
      # that means only "my-ss-5", "my-ss-6", "my-ss-7", "my-ss-8", "my-ss-9", and
      # "my-ss-10" get updated. 
      #
      # This is a useful feature for gradual / phased roll outs.
      partition: 5
```

```{note}
Deployments also supported the rolling update parameter `minReadySeconds`. There's a similar feature for stateful sets but it goes under the field `spec.minReadySeconds` (it isn't specific to rolling updates).
```

Rolling updates performed with a pod management policy of `OrderedReady` (the default) may get into a broken state which requires manual intervention to roll back. If an update results in a pod entering into an unhealthy state, the rolling update will pause. Reverting the pod template won't work because it goes against the "only one pod can go down at a time" behavior of stateful sets.

```{seealso}
Kinds/Stateful Set/Scaling_TOPIC (Discussion of pod management policy and "only one pod can go down at a time" behavior)
```

A volume claim template cannot be updated. The system will reject an updated stateful set if its volume claim template differs from the original. As such, users have devised various manual strategies for modifying volumes in a stateful set:
 
 * Expanding the volumes for a stateful set's pods is documented [here](https://serverfault.com/a/989665). The idea is to manually edit each persistent volume claim then re-create the stateful set without deleting any of its pods.

   ```sh
   kubectl edit pvc <name> # for each PVC in the StatefulSet, to increase its capacity.
   kubectl delete sts --cascade=orphan <name> # to delete the StatefulSet and leave its pods.
   kubectl apply -f <name> # to recreate the StatefulSet.
   kubectl rollout restart sts <name> # to restart the pods, one at a time. During restart, the pod's PVC will be resized.
   ```

   ```{note}
   For this to work, I think the volume type / storage class needs to support expanding volumes (`allowVolumeExpansion` is `true`)?
   ```

```{note}
What about shrinking a volume? I imagine what you need to do is, starting with the last ordinal to the first (current pod denoted N), ...

1. delete stateful set without deleting its pods (`kubectl delete sts --cascade=orphan <name>`).
1. delete pod N.
1. create a temporary volume with the new desired size.
1. create a temporary pod with both the pod N's volume and the temporary volume attached.
1. use the temporary pod to copy pod N's volume to the temporary volume.
1. delete the temporary pod.
1. delete pod N's volume.
1. re-create pod N's volume with the new desired size (same name).
1. create a temporary pod with both the pod N's volume and the temporary volume attached.
1. use the temporary pod to copy the temporary volume to pod N's volume.
1. re-create the stateful set (`kubectl apply -f <name>`).
1. trigger the stateful set to restart pods one at a time (`kubectl rollout restart sts <name>`).

The last step should restart the deleted pod, and that deleted pod will attach the updated volume.

These same steps may work for expanding volumes when `allowVolumeExpansion` isn't set to `true`.
```

### Peer Discovery

`{bm} /(Kinds\/Stateful Set\/Peer Discovery)_TOPIC/i`

A stateful set's governing service allows for its pods to discover each other (peer discovery). For each pod in a stateful set, that pod will have a sub-domain within that stateful set's governing service. For example, a stateful set with the name `my-ss` in the namespace `apple` within the cluster will expose its pods as ...

 * `my-ss-0.my-ss.apple.svc.cluster.local`
 * `my-ss-1.my-ss.apple.svc.cluster.local`
 * `my-ss-2.my-ss.apple.svc.cluster.local`
 * ...

... , where each sub-domain points to one of the stable identities.

A governing service allows for enumerating all pods within its stateful set via DNS service records (SRV). In the example above, performing an SRV lookup on `my-ss.apple.svc.cluster.local` will list out the sub-domains and IPs for all `my-ss` pods.

```{note}
If you have access to `dig`, you can do `dig SRV my-ss.apple.svc.cluster.local` and it'll list out all available sub-domains and their IPs for you.
```

```{note}
If polling for the IP of a peer that hasn't come up yet, DNS negative caching might cause a small delay to discovering the IP when that peer actually comes up.
```

## Job

`{bm} /(Kinds\/Job)_TOPIC/i`

```{prereq}
Kinds/Pod_TOPIC
Kinds/Pod/Lifecycle/Restart Policy_TOPIC
Kinds/Stateful Set_TOPIC
```

A job launches one or more pods to perform one-off tasks. Once those one-off tasks complete, the job is effectively over. Typical job use-cases include ...

 * database migration
 * database compaction
 * log file removal

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: my-job
spec:
  parallelism: 5  # Num of pods that can run at the same time (default is 1).
  completions: 10 # Num of pods that must successfully finish for job to end (default is 1).
  backoffLimit: 4 # Max num of retries of a failed pod before failing job (default is 6).
  activeDeadlineSeconds: 99 # Max secs before job forcibly fails, killing all pods.
  # Completion mode, when set to "Indexed", provides an ordinal suffix / stable identity to
  # each launched pod, similar to how a stateful set provides its pods with a stable identity.
  # This is useful in cases where the pods of a job need to communicate with each other (e.g.
  # distributed work-queue processing), but a service will likely also need to be provided.
  #
  # In most cases, this should be set to "NonIndexed" (default value).
  completionMode: NonIndexed
  # Pod template describing job's pods.
  template:
    spec:
      containers:
        - name: my-container
          image: my-image:1.0
      # Restart policy of the launched pods. For jobs, this must be set to either
      # "OnFailure" or "Never".
      restartPolicy: OnFailure
```

The example job  10 pods to successful completion, keeping up to 5 concurrently running at any one time. If a pod fails, the job will retry it up to 4 times before failing the job entirely. Similarly, the job itself runs no more than 99 seconds before failing entirely.

Common gotchas with jobs:

 * *`activeDeadlineSeconds` confusion*: There's an `activeDeadlineSeconds` that can go in the pod template as well which is different from the job's `activeDeadlineSeconds`. Don't confuse the two.

   ```{seealso}
   Kinds/Pod/Lifecycle/Maximum Runtime_TOPIC
   ```

 * *Lingering finished jobs*: By default, neither a job nor its pods are cleaned up after the job ends (regardless of success or failure). This can end up cluttering the Kubernetes servers.

   ```{seealso}
   Kinds/Job/Cleanup (Job cleanup strategies)
   ```

 * *No communication between pods*: By default, a job will automatically pick pod labels and set its label selectors so as not to conflict with other pods in the system. Without consistent labels, the pods of a job can't communicate with each other.

   ```{seealso}
   Kinds/Job/User-defined Labels (Job cleanup strategies)
   ```

 * *Unexpected concurrency*: Even if `concurrency` and `completions` fields are both set to 1, there are cases where a job may launch more than once. As such, a job's pods should be tolerant of concurrency.

### Cleanup

`{bm} /(Kinds\/Job\/Cleanup)_TOPIC/i`

One common problem with jobs is resource cleanup. Except for failed pods that have been retried (`backoffLimit` field), a completed job won't delete its pods by default. Those pods are kept around in a non-running state so that their logs can be examined if needed. Likewise, the job itself isn't deleted on completion either.

```{note}
This became a problem for me when using Amazon EKS with Amazon Fargate to run the job's pods. The Fargate nodes were never removed from the cluster because the job's pods were never deleted?
```

The problem with letting jobs and pods linger around in the system is that it causes clutter, putting pressure on the Kubernetes servers. Typically, it's up to the user to delete a job (deleting a job will also deletes any lingering pods). However, there are other mechanisms that can automate the deletion of jobs:

 * There's a higher-level kind called cron job that has cleanup policies for ended jobs.

   ```{seealso}
   Kinds/Cron Job_TOPIC ("Job history limit" fields)
   ```

 * There's a time-to-live mechanism that can be used to automatically deletes jobs that have ended (regardless of success or failure) after some duration.

   ```yaml
   apiVersion: batch/v1
   kind: Job
   metadata:
     name: my-job
   spec:
     # The number of seconds have the job has ended before the job is eligible to be
     # deleted. If this is 0, the job will be deleted immediately after ending.
     ttlSecondsAfterFinished: 100
     template:
       spec:
         containers:
           - name: my-container
             image: my-image:1.0
     restartPolicy: Never
   ```

### User-defined Labels

`{bm} /(Kinds\/Job\/User-defined Labels)_TOPIC/`

```{prereq}
Kinds/Stateful Set/Peer Discovery_TOPIC
```

By default, a job automatically picks out a unique label to identify its pods (such that it definitively knows which pods in the system belong to it). However, it's possible to give custom labels to a job's pods / give custom label selectors to a job. This is useful is cases where a job's pods need to communicate with each other: A headless service can target a job's pods based on its labels, which is similar to how a stateful set's pods can communicate with and discover each other (governing service).

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: my-job
spec:
  parallelism: 5  # Num of pods that can run at the same time (default is 1).
  completions: 10 # Num of pods that must successfully finish for job to end (default is 1).
  backoffLimit: 4 # Max num of retries of a failed pod before failing job (default is 6).
  activeDeadlineSeconds: 99 # Max secs before job forcibly fails, killing all pods.
  # Completion mode, when set to "Indexed", provides an ordinal suffix / stable identity to
  # each launched pod, similar to how a stateful set provides its pods with a stable identity.
  # This is useful in cases where the pods of a job need to communicate with each other (e.g.
  # distributed work-queue processing), but a service will likely also need to be provided.
  #
  # In most cases, this should be set to "NonIndexed" (default value).
  completionMode: NonIndexed
  # Selectors are label selectors used to identify pods, which match the key-value pairs
  # used for pod template labels further down.
  #
  # In most cases, you shouldn't need to specify this (or the labels in the pod template
  # below). When not present, the system will automatically pick labels / label selectors
  # that won't conflict with other jobs / pods.
  selector:
    matchLabels:
      app: my-app
  # Pod template describing job's pods.
  template:
    spec:
      containers:
        - name: my-container
          image: my-image:1.0
      # Restart policy of the launched pods. For jobs, this must be set to either
      # "OnFailure" or "Never".
      restartPolicy: OnFailure
```

## Cron Job

`{bm} /(Kinds\/Cron Job)_TOPIC/i`

```{prereq}
Kinds/Job_TOPIC
```

A cron job launches a job periodically on a schedule, defined in [cron format](https://en.wikipedia.org/wiki/Cron#Overview).

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: my-cronjob
spec:
  schedule: "0 * * * *"  # Schedule of the job in cron format (launches every hour)
  # How much tolerance to have (in seconds) for a scheduled run of a job that's been missed.
  # If a scheduled run gets missed for any reason but is identified within this window,
  # it'll run anyways. If it's past the window, it'll count as a failed job.
  #
  # This is an optional field. If not set, there is no deadline (infinite tolerance).
  startingDeadlineSeconds: 200
  # How should a job launch be treated if the previously launched job is still running.
  # If this is set to ...
  #  * "Allow", it allows the jobs to run concurrently (default value).
  #  * "Forbid", it skips the new job launch, meaning concurrently running jobs not allowed.
  #  * "Replace", it replaces the previously running job with the new job.
  concurrencyPolicy: Forbid
  # How many ended successful/failed jobs should remain in Kubernetes. If set to 0, a job and
  # its corresponding pods are removed immediately after ending. If  > 0, the last N jobs and
  # their pods will remain in Kubernetes (useful for inspection of logs).
  successfulJobsHistoryLimit: 0
  failedJobsHistoryLimit: 0
  # Job template that describes the job that a cron job launches. This is effectively a job
  # definition without "apiVersion", "kind", and "metadata" fields.
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: my-container
              image: my-image:1.0
          restartPolicy: OnFailure
```

```{note}
There is no stable support for timezones. The timezone used by all cron jobs is whatever the timezone of the controller manager is (other parts of the doc say unspecified timezone). There currently is a beta feature that's gated off that lets you specify a timezone by setting `spec.timeZone` (e.g. setting it to `Etc/UTC` will use UTC time).
```

Common gotchas with cron jobs:

 * *Unexpected concurrency*: There are cases where a cron job may launch more than once. As such, a job's pods should be tolerant of concurrency.

 * *Unexpected misses*: There are cases where a cron job may not launch even though it's supposed to.

## Daemon Set

`{bm} /(Kinds\/Daemon Set)_TOPIC/i`

```{prereq}
Kinds/Replica Set_TOPIC
Kinds/Deployment_TOPIC
Kinds/Stateful Set_TOPIC
```

A daemon set ensures that a set of nodes each have a copy of some pod always up and running. Typical scenarios where a daemon set is used include ...

 * node log collection (e.g. logstash agent).
 * node monitoring (e.g. zabbix agent).

The above scenarios are ones which break container / pod isolation. That is, a daemon set is intended to run pods that are coupled to nodes and sometimes those pods will do things such as mount the node's root filesystem and run commands to either install software or gather information.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: my-ds
spec:
  # Selectors are label selectors used to identify pods, which match the key-value pairs
  # used for pod template labels further down.
  selector:
    matchLabels:
      app: my-app
  # Pod template describing daemon set's pods.
  template:
    metadata:
      name: my-pod
      # These labels are how this daemon set will determine if the pod is running on a node.
      # It will look around for pods with this set of labels.
      labels:
        app: my-app
    spec:
      # Put copies of this pod only on nodes that have these labels. There is also a
      # "nodeAffinity" field and "tolerations" field, which allow for more elaborate logic
      # / soft logic for node selection (too vast to cover here).
      #
      # If neither "nodeSelector" nor "nodeAffinity" is set, copies of this pod will run on
      # all nodes.
      nodeSelector:
        type: my-node-type
      containers:
        - name: my-container
          image: my-image:1.0
          resources:
            limits:
              cpu: 100m
              memory: 200Mi
          volumeMounts:
            - name: varlog
              mountPath: /host_log
              readOnly: true
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
```

The example above runs a copy of the pod template on each node that has the label `type=my-node-type` and mounts the host's `/var/log` directory to `/host_log` in the container. Most daemon sets are used for some form of monitoring or manipulation of nodes, so it's common to have volumes of the type `hostPath`, which mounts a directory that's directly on the node itself.

Unlike deployments and stateful sets, daemon sets don't have support for rolling updates. On any change to a daemon set's pod template on node selection criteria, old pods are deleted and updated pods are brought up in their place.

## Service Account

`{bm} /(Kinds\/Service Account)_TOPIC/i`

```{prereq}
Kinds/Namespace_TOPIC
Kinds/Secret_TOPIC
Kinds/Pod/API Access_TOPIC
Kinds/Pod/Images/Private Container Registries_TOPIC
```

A service account is a set of credentials that applications within a pod use to communicate with the Kubernetes API server. Service accounts also provide an aggregation point for image pull secrets and other security-related features.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service-account
# A list of image pull secrets to use with private container registries. When this service
# account is applied to a pod, all image pull secrets in the service account get added to
# the pod.
imagePullSecrets:
  - name: my-dockerhub-secret
  - name: my-aws-ecr-secret
# API access credentials will never be mounted to any pod that uses this service account.
automountServiceAccountToken: false
```

By default, each namespace comes with its own service account which pods in that namespace automatically use. The service account used by a pod can be overridden to another service account.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  # Custom service account to use. This can't be changed once the pod's been creatd.
  serviceAccountName: my-service-account
  containers:
    - name: my-container
      image: my-registry.example/tiger/my-image:1.0
```

```{seealso}
Security/API Access Control_TOPIC (Role-based access control to limit a service account's access to the Kubernetes API)
```

## Horizontal Pod Autoscaler

`{bm} /(Kinds\/Horizontal Pod Autoscaler)_TOPIC/i`

```{prereq}
Kinds/Replica Set_TOPIC
Kinds/Deployment_TOPIC
Kinds/Stateful Set_TOPIC
Kinds/Ingress_TOPIC
```

A horizontal pod autoscaler (HPA) periodically measures how much work a set of pod replicas are doing so that it can appropriately adjust the number of replicas on that replica set, deployment, or stateful set. If the pod replicas ...

* aren't doing enough work, the numbers of replicas is decreased.
* are doing too much work, the number of replicas is increased.

```{note}
This feature depends on a "metrics server" that should be running on Kubernetes by default.
```

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-hpa
spec:
  # What kind and name are being targeted for autoscaling? Is it a replica set, deployment,
  # stateful set, or something else?
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: my-ss
  # What are the minimum and maximum replicas that this HPA will scale to? At the time of
  # writing, the minimum number of replicas must be 1 or more (it can't be 0).
  minReplicas: 2
  maxReplicas: 10
  # What type of metrics are being collected? In this example, on average across all active
  # pod replicas, we want the CPU load to be 50%. If the average is more than 50%, scale
  # down the number of replicas. If it's more, scale up the number of replicas.
  #
  # The average utilization is referring to the amount of resource requested by the pod. In
  # this example, this is 50% of the CPU resource AS REQUESTED BY THE POD (via the pod's
  # spec.containers[].resources.requests for CPU).
  #
  # Instead of doing average percentage, you can also do absolute values by changing
  # target.type to AverageValue and replacing target.averageUtilization with
  # target.averageValue.
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

```{seealso}
Kinds/Pod/Resources_TOPIC (Refresher on resource requests)
```

In the example above, if the average CPU usage of the stateful set `my-ss` replicas is 

* less than 50% that of the CPU resource requested, the replicas will scale down until there are 2 replicas or until the CPU usage reaches 50%.
* more than 50% that of the CPU resource requested, the replicas will scale up until there are 10 replicas or until the CPU usage reaches 50%.

The HPA will at-most double the number of replicas on each iteration. Each scaling iteration has an intentional waiting period. Specifically, scaling ...

 * up will only occur if no previous scaling has occurred in the past 3 mins.
 * down will only occur if no previous scaling has occurred in the past 5 mins.

Common gotchas with HPAs:

 * *Scale to zero*: Setting the number of minimum replicas to zero isn't supported. See [here](https://github.com/kubernetes/kubernetes/issues/69687).

 * *Scaling memory*: It's easy to autoscale based on CPU, but be careful with autoscaling based on memory. If the number of replicas scale up, the existing replicas need to somehow "release" memory, which can't really be done without killing the pods and starting them back up again.

 * *Scaling on non-linear scaling metrics*: Be careful with scaling based on metrics that don't linearly scale. For example, if you double the number of pods, the value of that metric should cut in half. This may end up becoming an issue when scaling based off poorly designed custom user-defined metrics.

```{note}
In addition to horizontal pod autoscaler, there's a vertical pod autoscaler (VPA). A VPA will scale a single pod based on metrics and its resource requests / resource limits.

The VPA kind doesn't come built-in with Kubernetes. It's provided as an add-on package found [here](https://github.com/kubernetes/autoscaler).
```

### Scaling Behavior

`{bm} /(Kinds\/Horizontal Pod Autoscaler\/Scaling Behavior)_TOPIC/i`

How an HPA scales up / down can be controlled through policies. It's common to control scaling behavior to reduce problems such as trashing of replicas (constantly introducing and evicting replicas).

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: my-ss
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
  # Scaling behavior is defined through policies. Both scaling up and scaling down have
  # their own list of policies to select from. When a list contains more than one policy,
  # the one selected is defined by "spec.selectPolicy" (next field after this one).
  #
  # In addition to policies, scaling up and scaling down both have their own "stabilization
  # window" which is used to prevent thrasing of replicas (constantly introducing / evicting
  # replicas). The window tracks the highest replica count in the past n seconds and won't
  # let policies go through with setting it to a smaller value (e.g. use the highest
  # computed replica count over the past 5 mins).
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Pods # Allow at most 4 pod replicas to be added in a span of 1 min
          value: 4
          periodSeconds: 60 
        - type: Percent # Allow at most a 10% increase of pod replicas in a span of 1 min
          value: 10
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Pods  # Allow at most 3 pod replicas to be removed in a span of 2 mins
          value: 3
          periodSeconds: 120
        - type: Percent  # Allow at most a 10% decrease of pod replicas in a span of 5 mins
          value: 10
          periodSeconds: 300
  # When many policies are present for a scale up / down, the policy chosen can be either
  # the one causing the ...
  #
  #  * most change (e.g. most pods added), set by using "Max" as the value.
  #  * least change (e.g. least pods removed), set by using "Min" as the value.
  selectPolicy: Max
```

```{note}
Default scaling behavior is defined [here](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#default-behavior).
```

### Metric Types

`{bm} /(Kinds\/Horizontal Pod Autoscaler\/Metric Types)_TOPIC/i`

Metrics can be one of the following types types:

 * `Resource` metrics cover CPU and memory metrics of the replicas.
 * `Pods` metrics cover other metrics of the replicas.
 * `Object` are metrics related to some other object in the same namespace.
 * `External` are metrics related to something other than Kubernetes.

`Resource` is set directly by Kubernetes while `Pods`, `Object`, and `External` are for custom / user-defined metrics.

If multiple metrics being tracked by an HPA, as in the example below, that HPA calculates the replica counts for each metric and then chooses the one with the highest.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: my-ss
  minReplicas: 2
  maxReplicas: 10
  metrics:
    # Target an average of 50% CPU utilization across all replicas
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
    # Target an average of 1000 queries-per-second across all replicas.
    - type: Pods
      pods:
        metric:
          name: queries-per-second
        target:
          type: AverageValue
          averageValue: 1000
    # Target an average of 1000 queries-per-second across all replicas.
    - type: Object
      object:
        metric:
          name: requests-per-second
        describedObject:
          apiVersion: extensions/v1
          kind: Ingress
          name: my-ingress
        target:
          type: Value
          averageValue: 2000
```

```{note}
I've spent hours trying to figure out how replicas can send custom metrics that an HPA can scale on. There is barely any documentation on this and zero examples online. The closest thing I could find to a source is [here](https://medium.com/swlh/building-your-own-custom-metrics-api-for-kubernetes-horizontal-pod-autoscaler-277473dea2c1).

The simplest solution here seems to be to use a third-party software package called Prometheus.
```

```{seealso}
Extensions/Prometheus_TOPIC (Scaling replicas based on user-defined metrics)
```

## Cluster Autoscaler

`{bm} /(Kinds\/Cluster Autoscaler)_TOPIC/i`

```{prereq}
Kinds/Pod_TOPIC
Kinds/Node_TOPIC
```

A cluster autoscaler is a component that scales a Kubernetes cluster on a public cloud by adding and removing nodes as needed. Each public could has its own implementation of a cluster autoscaler. In some clouds, the implementation is exposed as a kind / set of kinds. In other clouds, the implementation is exposed as a web interface or a command-line interface.

In most cases, nodes and added and removed to predefined groups called node pools. Each node pool has nodes of the same type (same resources and features). For example, a specific node pool of machines with the same CPU, networking gear, and same amount and type of RAM.

If a pod is scheduled to run but none of the nodes have enough resources to run it, the cluster autoscaler will increase the number of nodes in one of the node pools that has the capability to run the pod. Likewise, the cluster autoscaler will decrease the number of nodes if nodes aren't being utilized enough by actively running pods.

```{note}
It doesn't seem to be consistent so there isn't much else to put about cluster autoscaling. See the cluster autoscaler section on [this website](https://github.com/kubernetes/autoscaler) and navigate to whatever public cloud you're using.
```

```{seealso}
Kinds/Pod Disruption Budget_TOPIC (Prevent rapid killing of pods on cluster autoscaler scale down)
```

## Pod Disruption Budget

`{bm} /(Kinds\/Pod Disruption Budget)_TOPIC/i`

```{prereq}
Kinds/Cluster Autoscaler_TOPIC
Kinds/Replica Set_TOPIC
Kinds/Deployment_TOPIC
Kinds/Stateful Set_TOPIC
Kinds/Pod/Node Placement_TOPIC
```

A pod disruption budget (PDB) specifies the number of downed pod replicas that a replica set, deployment, or stateful set can tolerate relative to its expected replica count. In this case, a disrupted pod is one that's brought down via ...

 * voluntary disruptions (e.g. manually removing a node from the cluster).
 * involuntary disruptions (e.g. kernel panic on a node).
 * rolling updates (deployments and stateful set).

Once a PDB has reached its downed pod replica limit, it prevents further downing of pod replicas via voluntary disruptions. It cannot prevent further downing of pod replicas via involuntary disruptions or rolling updates (these downed pods will still be accounted for within the PDB).

```{note}
This has something to do with an "Eviction API". Haven't had a chance to read about this yet.
```

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-pdb
spec:
  # Selector for pod replicas within the stateful set.
  selector:
    matchLabels:
      app: my-ss-pods
  # Max number of pods that can be unavailable at one time.
  #
  # Instead of "maxUnavailable", this can also be "minAvailable", which is the min number of
  # pods must be available at all times.
  maxUnavailable: 3
```

```{note}
The manifest is using label selectors are being used to identify pods. How does it know what the replica count is for the replica set / deployment / or stateful set? According to the docs:

> The "intended" number of pods is computed from the spec.replicas of the workload resource that is managing those pods. The control plane discovers the owning workload resource by examining the metadata.ownerReferences of the Pod.
```

# Security

`{bm} /(Security)_TOPIC/i`

Kubernetes comes with several features to enhance cluster security. These include gating off inter-cluster networking, gating off how containers can break isolation, and providing access control mechanisms to the API.

The subsections below detail various security related topics.

## Network Policy

`{bm} /(Security\/Network Policy)_TOPIC/i`

```{prereq}
Kinds/Pod/API Access_TOPIC
Kinds/Service Account_TOPIC
```

```{note}
For this feature to work, Kubernetes needs to be using a network plugin that supports it.
```

Network policies restrict pods from communicating with other network entities (e.g. services, endpoints, other pods, etc..). Restrictions can be for either inbound connections, outbound connections, or both.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: my-np
  namespace: my-ns
spec:
  # Which pods this network policy applies to is defined via pod labels. The pods have to be
  # in the same namespace as the network policy.
  podSelector:
    matchLabels:
      app: backend
  # Which directions is this network policy? Possible options include "Ingress" is for
  # inbound connections, "Egress" is for outbound connections, or both. If empty, it'll
  # default to just "Ingress" and "Egress" will also be set if there are any egress rules
  # below.
  policyTypes: [Ingress, Egress]
  # Inbound connection rules go here. Rules can be for IP blocks (CIDR), namespaces
  # (identified via labels), or pods (identified via labels). Each rule is for a specific
  # port.
  ingress:
    - from:
        # Allow all pods from another namespace.
        - namespaceSelector:
            matchLabels:
              project: my-company
        # Allow all pods in this namespace that have a particular set of labels.
        - podSelector:
            matchLabels:
              app: frontend
        # Allow all pods from another namespace that have a particular set of labels. Note
        # that this is a SINGLE ENTRY, not two separate entries (there is no dash before
        # "podSelector" like the "podSelector" above has).
        - namespaceSelector:
            matchLabels:
              project: my-company
          podSelector:
            matchLabels:
              app: frontend
        # Allow all pods from an IP block (with exceptions).
        - ipBlock:
            cidr: 172.17.0.0/16
            except:
              - 172.17.99.0/24
      ports:
        - protocol: TCP
          port: 8080
  # Outbound connection rules go here. This is specified in exactly the same way as the
  # rules for inbound connections, but the rules apply to outbound connections.
  egress:
    - to:
        - ipBlock:
            cidr: 10.0.0.0/24
      ports:
        - protocol: TCP
          port: 8888
```

```{note}
The pod selectors should still apply when communicating to pods over a service. Will they still apply when communicating to pods without using a service (e.g. raw)?
```

The following are commonly used patterns for network policies.

```yaml
# DENY ALL INGRESS TRAFFIC
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes: [Ingress]
----
# ALLOW ALL INGRESS TRAFFIC
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-ingress
spec:
  podSelector: {}
  ingress:
  - {}
  policyTypes: [Ingress]
----
# DENY ALL EGRESS TRAFFIC
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
spec:
  podSelector: {}
  policyTypes: [Egress]
----
# ALLOW ALL EGRESS TRAFFIC
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-egress
spec:
  podSelector: {}
  ingress:
  - {}
  policyTypes: [Egress]
----
# DENY ALL INGRESS AND EGRESS TRAFFIC
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

## Pod Security Admission

`{bm} /(Security\/Pod Security Admission)_TOPIC/i`

```{prereq}
Kinds/Pod/Container Isolation_TOPIC
```

```{note}
There was a feature called pod security policy that this deprecates. Pod security policies are no longer a thing.
```

Pod security admissions are used to restrict the security context of pods using policy groups that define up-to-date best practices. Restricting requires two pieces of information: policy and mode. Specifically, ...

 * policy defines the level of privileges to grant to pods, which can be either ...

   * `privileged`: Unrestricted usage (default).
   * `baseline`: Minimally restricted usage, based on known privilege escalations.
   * `restricted`: Maximally restricted usage, based on best practices of hardening pods.

   Note that the description above doesn't explicitly define what it is that's being restricted (it just says minimally restricted / maximally restricted). The definition of minimal / maximal are based on up-to-date best practices and update with different releases of Kubernetes. As such, to help keep things consistent, a policy can be pinned to use the definitions from a specific version of Kubernetes (e.g. apply definitions from Kubernetes v1.22 even though the version of Kubernetes being run is v1.25).

 * mode defines what to do when a policy violation is detected, which can be either ...

   * `enforce`: Violating pods are rejected.
   * `audit`: Violating pods are not rejected, but a message will be recorded in the audit logs.
   * `warn`: Violating pods are not rejected, but a warning message will be shown to the user.

For example, setting ...

 * `warn` to `baseline` means that pods will run but also warn if they're breaking the minimal set of restrictions.
 * `enforce` to `privileged` means that pods won't run if they're unrestricted.

To apply to all pods cluster-wide, use the following object.

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
  - name: PodSecurity
    configuration:
      apiVersion: pod-security.admission.config.k8s.io/v1
      kind: PodSecurityConfiguration
      defaults:
        enforce: privileged
        enforce-version: latest
        audit: restricted
        audit-version: "1.25"
        warn: baseline
        warn-version: "1.22"
      exemptions:
        usernames: []             # Usernames to exempt
        runtimeClasses: []        # Runtime class names to exempt
        namespaces: [kube-system] # Namespaces to exempt
```

```{seealso}
Security/API Access Control_TOPIC (Usernames and groups)
```

To apply to all pods in a specific namespace, use the following namespace label templates.

 * policy, use `pod-security.kubernetes.io/<MODE>:<POLICY>`.
 * version, use `pod-security.kubernetes.io/<MODE>-version:<VERSION>` (defaults to `latest` if omitted).

```
pod-security.kubernetes.io/warn=baseline
pod-security.kubernetes.io/warn-version=1.22
pod-security.kubernetes.io/audit=restricted
pod-security.kubernetes.io/audit-version=1.25
pod-security.kubernetes.io/enforce=privileged
pod-security.kubernetes.io/enforce-version=latest
```

## API Access Control

`{bm} /(Security\/API Access Control)_TOPIC/i`

```{prereq}
Kinds/Pod/API Access_TOPIC
Kinds/Service Account_TOPIC
```

Access control to the Kubernetes API is modeled using accounts and groups, where an account can be associated with many groups and each group grants a certain set of permissions to its users. Two types of accounts are provided:

 * users, which are accounts for human access.
 * service accounts, which are accounts for programmatic access.

```{svgbob}
groupA
     '-----.
           +-- userA
     .-----'
groupB
     '-----.
           +-- serviceAccountA
     .-----'
groupC

* "userA is both in groupA and groupB"
* "serviceAccountA is both in groupB and groupC"
```

Service accounts are what get used when a pod needs access to the Kubernetes API. Containers within that pod have a volume mounted with certificates and credentials that the applications within can use to authenticate and communicate with the API server.

Each namespace gets created with a default service account (named `default`). By default, pods created under a namespace will be assigned the default service account for that namespace. A pod can be configured to use a custom service account that has more or less access rights than the default service account. A pod can also forgo volume mounting the credentials of a service account entirely if the applications within it don't need access to the Kubernetes API.

```{svgbob}
             .----- "my-service-account"
namespaceA --+----- "my-other-service-account"
             '----- "default"

             .----- "yet-another-service-account"
namespaceB --+----- "default"

* "two namespaces, both have a default service account"
```

```{seealso}
Kinds/Service Account_TOPIC (Creating service accounts)
Security/API Access Control/Disable Credentials_TOPIC (Disable volume mounting service account credentials)
```

How access rights are defined depends on how Kubernetes has been set up. By default, Kubernetes is set up to use role-based access control (RBAC), which tightly maps to the REST semantics of the Kubernetes API server. RBAC limits what actions can be performed on which objects: Objects map to REST resources (paths on the REST server) and manipulations of objects map to REST actions (verbs such as `DELETE`, `GET`, `PUT`, etc.. on those REST server paths).

The subsections below detail RBAC as well as other API security related topics.

```{note}
Other types of access control mechanisms exist as well, such as attribute-based access control (ABAC).
```

### Role-based Access Control

`{bm} /(Security\/API Access Control\/Role-based Access Control)_TOPIC/i`

RBAC tightly maps to the REST semantics of the Kubernetes API server by limiting what actions can be performed on which objects: Objects map to REST resources (paths on the REST server) and manipulations of objects map to REST actions (verbs such as `DELETE`, `GET`, `PUT`, etc.. on those REST server paths). RBAC is configured using two sets of kinds:

 * `Role` and `ClusterRole` specify which actions can be performed on which kinds / in which namespace.
 * `RoleBinding` and `ClusterRoleBinding` specify which roles bind to which users, groups, or service accounts.

A role binding always maps a single role to many users, groups, and service accounts.

```{svgbob}
RoleA ---- RoleBinding1 ----- userA
                              | |
RoleB ---- RoleBinding2 ------' |
                           .----'
RoleC ---- RoleBinding3 ---+
                           '--.
RoleD ---- RoleBinding4 ----- serviceAccountB
```

```{note}
Recall that a ...

* namespace-level object / kind is one that comes under the umbrella of a namespace: Services, pods, config maps, etc..
* cluster-level object / kind is one that comes under the umbrella of the entire cluster (it's cluster-wide, not tied to a namespace): Nodes, persistent volumes, etc...
```

`ClusterRole` and `ClusterRoleBinding` are cluster-level kinds while `Role` and `RoleBinding` are namespace-level kinds. RBAC provides different permissions based on which role variant (`ClusterRole` vs `Role`) gets used with which role binding variant (`ClusterRoleBinding` vs `RoleBinding`):

| Role          | Binding              | Permission Granted |
|---------------|----------------------|--------------------|
| `Role`        | `RoleBinding`        | Allow access to namespace-level kinds in that role / role binding's namespace. |
| `ClusterRole` | `ClusterRoleBinding` | Allows access to namespace-level kinds in all namespaces, cluster-level kinds, and arbitrary URL paths on the Kubernetes API server. |
| `ClusterRole` | `RoleBinding`        | Allow access to namespace-level kinds in all namespaces, cluster-level kinds, and arbitrary URL paths on the Kubernetes API server. But, that access is only permitted from within the namespace of the role binding. |
| `Role`        | `ClusterRoleBinding` | Invalid. It's allowed but it *does nothing* (it won't cause an error). |


 * `Role` and `RoleBinding`: Allow access to namespace-level kinds in that role / role binding's namespace.

   ```yaml
   apiVersion: rbac.authorization.k8s.io/v1
   kind: Role
   metadata:
     name: my-role
     # Namespace of this role. Permissions are for THIS namespace only. If omitted, the current
     # namespace is used.
     namespace: my-ns
   rules:  # List of kinds and actions go here
     - apiGroups: [""]
       resources: [services]
       verbs: [get, list]
   ----
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: my-role-binding
     # Namespace of this role binding. This must be the same as the role being bound (otherwise,
     # the role binding won't be able to see the role as its in another namespace?). If omitted,
     # the current namespace is used.
     namespace:  my-ns
   # The role that's being bound.
   roleRef:
     apiGroup: rbac.authorization.k8s.io
     kind: Role
     name: my-role
   # The users/groups/service accounts that the role is being bound to.
   subjects:
     - kind: ServiceAccount
       namespace: my-other-ns
       name: default
     - apiGroup: rbac.authorization.k8s.io
       kind: Group
       name: system:authenticated
   ```

 * `ClusterRole` and `ClusterRoleBinding`: Allow access to namespace-level kinds in all namespaces, cluster-level kinds, and arbitrary URL paths on the Kubernetes API server.

   ```yaml
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRole
   metadata:
     name: my-cluster-role
   rules:  # List of kinds and actions go here
     - apiGroups: [""]
       resources: [nodes]
       verbs: [get, list]
     - nonResourceURLs:  # List of server paths to allow go under here.
       - /api
       - /api/*
       - /apis
       - /apis/*
   ----
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRoleBinding
   metadata:
     name: my-cluster-role-binding
   # The role that's being bound.
   roleRef:
     apiGroup: rbac.authorization.k8s.io
     kind: ClusterRole
     name: my-cluster-role
   # The users/groups/service accounts that the role is being bound to.
   subjects:
     - kind: ServiceAccount
       namespace: my-ns
       name: default
     - apiGroup: rbac.authorization.k8s.io
       kind: Group
       name: system:authenticated
   ```

 * `ClusterRole` and `RoleBinding`: Allow access to namespace-level kinds in all namespaces, cluster-level kinds, and arbitrary URL paths on the Kubernetes API server. But, that access is only permitted from within the namespace of the role binding.

   ```yaml
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRole
   metadata:
     name: my-cluster-role
   rules:  # List of kinds and actions go here
     - apiGroups: [""]
       resources: [services]
       verbs: [get, list]
   ----
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: my-role-binding
     # Namespace of this role binding. Although the cluster role being bound to this role binding
     # allows access to everything (all namespaces and at the cluster-level), access must happen
     # from within this namespace.
     namespace:  my-ns
   # The role that's being bound.
   roleRef:
     apiGroup: rbac.authorization.k8s.io
     kind: Role
     name: my-role
   # The users/groups/service accounts that the role is being bound to. If the group is pointing
   # to a service account, is that service account required to be in the same namespace as this
   # role binding for access to be allowed? (Unsure at this point)
   subjects:
     - kind: ServiceAccount
       namespace: my-other-ns
       name: default
     - apiGroup: rbac.authorization.k8s.io
       kind: Group
       name: system:authenticated
   ```

   ```{note}
   I'm still confused as to what this actually does. The example above gives permissions to the default service account in the `my-other-ns` namespace, but the `RoleBinding` is in the `my-ns` namespace. Does that mean the service account won't get permissions because it's in another namespace?
   ```

 * `Role` and `ClusterRoleBinding`: Invalid. It's allowed but it *does nothing* (it won't cause an error).

   ```yaml
   apiVersion: rbac.authorization.k8s.io/v1
   kind: Role
   metadata:
     name: my-role
     namespace: my-ns
   rules:
     - apiGroups: [""]
       resources: [services]
       verbs: [get, list]
   ----
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRoleBinding
   metadata:
     name: my-cluster-role-binding
   roleRef:
     apiGroup: rbac.authorization.k8s.io
     kind: Role
     name: my-role
   subjects:
     - kind: ServiceAccount
       namespace: my-ns
       name: default
   ```

Roles / cluster roles define a set of rules, where each rule grants access to a specific part of the API. Each rule requires three pieces of information:

 * `resources`: The kinds to allow (e.g. pods, services, nodes, etc.., note these are plurals).
 * `verbs`: The actions to allow (e.g. `GET`, `DELETE`, etc..).
 * `apiGroups`: The APIs of the kinds, which roughly maps to the `apiVersion` field used within a manifest for that kind. For core APIs such as services and pods, this should be an empty string.

In addition, cluster roles take in a set of paths, where each path grants access to a specific path on the API server. This is useful in scenarios where the path being accessed doesn't represent a kind (meaning it can't be represented with rules as described above -- e.g. querying the health information of the cluster).

All of the fields discussed above can use wildcards via `*`.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: my-cluster-role
rules:
  - apiGroups: ["*"]
    resources: ["*"]
    verbs: ["*"]
  - nonResourceURLs: ["/api/*", "/apis/*"]
```

Role bindings / cluster role bindings associate a set of subjects (users, groups, and / or service accounts) with a role / cluster role with, granting each subject the permissions defined by that role / cluster role. Each subject needs to be either a ...

 * service account, requiring that service account's name and namespace.
 * group, requiring that group's name.
 * user, requiring that user's name.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: my-cluster-role-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: my-role
subjects:
  - kind: ServiceAccount
    namespace: my-ns
    name: default
  - apiGroup: rbac.authorization.k8s.io
    kind: Group
    name: system:authenticated  # case-sensitive
  - apiGroup: rbac.authorization.k8s.io
    kind: User
    name: dave  # case-sensitive
```

```{note}
I suspect that users and groups are cluster-level kinds, hence the lack of namespace. Haven't been able to verify this.
```

```{note}
What exactly is the `system:authenticated` group in the examples above? According to the book, there are several groups internal to Kubernetes that help identify an account:

 * `system:unauthenticated` - Group assigned when authentication failed.
 * `system:authenticated` - Group assigned when authentication succeeded.
 * `system:serviceaccounts` - Group assigned to service accounts.
 * `system:serviceaccounts:<NAMESPACE>` - Group assigned to service accounts under a specific namespace.
```

Kubernetes comes with several predefined cluster roles that can be used as needed:

 * `cluster-admin`: Full-access to everything in the cluster.
 * `admin`: Access to almost everything in the cluster (resource quotas and namespaces excluded).
 * `view`: Access to view most objects in the cluster (roles and role bindings excluded).
 * `edit`: Access to edit most objects in the cluster (roles and role bindings excluded).

```{note}
`edit` also excludes access to resource quotes and namespaces? Unsure.
```

### Disable Credentials

`{bm} /(Security\/API Access Control\/Disable Credentials)_TOPIC/i`

By default, a pod will mount its service account's credentials to `/var/run/secrets/kubernetes.io/serviceaccount` within its containers. Unless access to the API is required, it's good practice to disable the mounting of credentials entirely. This can be done via the service account object or the pod object.

```yaml
# Disable on service account
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service-account
  automountServiceAccountToken: false # Don't mount creds into pods using this service account
----
# Disable on pod
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  serviceAccountName: my-service-account
  automountServiceAccountToken: false  # Prevent auth details from mounting to containers in pod
  containers:
    - name: my-container
      image: my-image:1.0
```

```{note}
Recall that it's also possible to disable auto-mounting on individual pods. Auto-mounting can't be disabled on individual containers, but it is possible to override the `/var/run/secrets/kubernetes.io/serviceaccount` mount on those containers with something like `tmpfs` (empty directory).
```

# Extensions

`{bm} /(Extensions)_TOPIC/i`

```{prereq}
Kinds_TOPIC
Security_TOPIC
```

Kubernetes can be automated / extended through user supplied code and third-party software packages. The subsections below detail various automation related topics.

## Custom Kinds

`{bm} /(Extensions\/Custom Kinds)_TOPIC/i`

```{prereq}
Kinds/Pod/API Access_TOPIC
Kinds/Deployment_TOPIC
Kinds/Service Account_TOPIC
Security/API Access Control_TOPIC
```

Kubernetes allows user-defined kinds. User-defined kinds typically build on existing kinds, either to ...

 * wrap them (e.g. multiple objects of different kinds under a single umbrella, where that umbrella controls and manages those objects).
 * automate them (e.g. take care of custom maintenance tasks on objects or automate audits of objects).
 * extend them (e.g. wrap an existing kind and add new features on-top of it, like how cron job does with job).

Each user-defined kind first requires a custom resource definition (CRD), which tells Kubernetes how a user-defined kind is defined. Given a CRD for a user-defined kind, the Kubernetes API server will store, allow access, and perform basic validation on objects of that kind.

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: cars.my-corp.com  # Must be set to <spec.names.plural>.<spec.group>.
spec:
  # The different naming variations of the kind that this CRD is adding.
  names:
    plural: cars     # Plural variant, used for API path (discussed further below).
    singular: car    # Singular variant, used as alias for kubectl and for display.
    kind: Car        # CamelCased singular variant, used by manifests.
    shortNames: [cr] # Shorter variants, used by kubectl.
  # Is this a namespace-level kind (objects associated with a namespace) or a cluster-level
  # kind (objects are cluster-wide). Use either "Namespaced" or "Cluster".
  scope: Namespaced
  # The REST API path is specified using the two fields below ("group" and "version") along
  # with the plural name defined above. There's only one group but there can be multiple
  # versions for that group. Each version gets its own REST API path in the format
  # /apis/<group>/<version>/<plural>. 
  #
  # In this example, only one version exists. Its REST API path is /api/my-corp.com/v1/vars.
  group: my-corp.com
  versions:
    - name: v1
      served: true  # Setting this to false disables this version.
      storage: true # Given multiple version, exactly one must be marked for storage.
      # Each version can have some validation performed via a schema. The following OpenAPI
      # schema ensures several fields exist on the object and those objects are of the
      # correct type.
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                model: {type: string}
                year: {type: integer}
                doorCount: {type: integer}
----
# An example object created using the definition above
apiVersion: cars.my-corp.com/v1
kind: Car
metadata:
  name: my-car
spec:
  model: Jetta
  year: 2005
  doorCount: 4
```

To process objects of a user-defined kind, a special pod needs to be written with access to the Kubernetes API. This pod, called a controller, needs to use the Kubernetes API to watch for object events and process those events in whatever way is appropriate. To provide redundancy, it's common for multiple instances of such a pod to be running at once (e.g. deployment), possibly coordinating with each other (e.g. shared database).

```python
# This is a naive implementation of a controller. It shouldn't have multiple instances
# running on the cluster because those instances get into race conditions and trip over each
# other.

# Import Kubernetes API client for Python.
import kubernetes.config
from kubernetes.client import V1Pod
from kubernetes.client import V1PodSpec
from kubernetes.client import V1Container
from kubernetes.client import V1ObjectMeta
from kubernetes.client import V1Service
from kubernetes.client import V1ServiceSpec
from kubernetes.client import V1ServicePort

# Load the credentials mounted within the pod. Make sure a service account is associated
# with the pod and that service account has the necessary permissions to watch, add/delete
# pods, and add/delete services.
#
# If this is running locally rather than within a pod, use load_kube_config() instead.
kubernetes.config.load_incluster_config()

v1 = kubernetes.client.CoreV1Api()
custom_v1 = kubernetes.client.CustomObjectsApi()

# An added car should result in a new pod and a new service for that pod.
def create_car(car_name):
    pod_name = car_name + '-pod'
    pod_labels = {'app': 'car'}
    pod_spec = V1PodSpec(containers=[V1Container(name='car', image='my-image:1.0')])
    pod = V1Pod(metadata=V1ObjectMeta(name=pod_name, labels=pod_labels), spec=pod_spec)
    v1.create_namespaced_pod(namespace='default', body=pod)
    
    service_name = car_name + '-service'
    service_labels = {'app': 'car'}
    service_spec = V1ServiceSpec(selector=pod_labels, ports=[V1ServicePort(protocol='TCP', port=80)])
    service = V1Service(metadata=V1ObjectMeta(name=service_name, labels=service_labels), spec=service_spec)
    v1.create_namespaced_service(namespace='default', body=service)

# A deleted car should result in pod and service associated with it to be deleted as well.
def delete_car(car_name):
    pod_name = car_name + '-pod'
    v1.delete_namespaced_pod(name=pod_name, namespace='default')
    
    service_name = car_name + '-service'
    v1.delete_namespaced_service(name=service_name, namespace='default')

# Watch the API server for changes to "cars"
w = kubernetes.watch.Watch()
for event in w.stream(custom_v1.list_cluster_custom_object, 'my-corp.com', 'v1', 'cars', watch=True):
    car = event['object']
    if event['type'] == 'ADDED':
        create_car(car['metadata']['name'])
    elif event['type'] == 'DELETED':
        delete_car(car['metadata']['name'])
```

Note that, when a CRD is deleted, all of its objects are deleted as well. Those deleted objects will cause `DELETED` events. For example, deleting the CRD example above will cause the controller example above to receive `DELETED` events for objects that were taken out by that CRD's deletion.

```{note}
In addition to doing it manually like this, there's also a handy framework to take a lot of the boilerplate out called Kubernetes Operators Framework (Kopf).
```

```{note}
There's also another much more complicated mechanism of adding your own kind called: API server aggregation. In this method, you create your own API server that handles requests, storage, and management of your kind. The Kubernetes API sever then proxies to your API server via an aggregation layer.
```

## Helm

```{prereq}
Kinds_TOPIC
Extensions/Custom Kinds_TOPIC
Security_TOPIC
```

`{bm} /(Extensions\/Helm)_TOPIC/i`

Helm is an application installer for Kubernetes, similar to package managers on Linux distributions (e.g. apt on Ubuntu). It installs, upgrades, and uninstalls software, taking care of configuration details and applying all the necessary manifests into Kubernetes. This could be software that's internal to Kubernetes (e.g. helps manage or extend Kubernetes in some way) or software that runs on top of Kubernetes (e.g. install a cluster of Redis pods for your application to use).

A chart is a recipe that details how Helm should install a piece of software. Each chart is made up of ...

 1. manifest templates that render based on user-supplied configurations.
 2. default configurations for those manifest templates.
 3. dependencies to other charts.

```{svgbob}
.----------------------------------------.
|             "MyApp's Chart"            |
|                                        |
| "Manifest Templates"                   |
|   "deployment template"                |
|   "service template"                   |
|   "ingress template"                   |
|   "horizontal pod autoscaler template" |
|                                        |
| "Default Configs"                      |
|   "app.port=8080"                      |
|   "app.log-retention-size=100mb"       |
|                                        |
| "Chart Dependencies"                   |
|   "postgres"                           |
|   "redis"                              |
'----------------------------------------'
```

Helm can access charts from either ...

 * a chart repository, which is an HTTP server somewhere on the internet that distributes charts.
 * a container registry, where charts are stored and distributed as if they were containers.
 * the local file system.

Publicly available charts / chart repositories are commonly listed on [ArtifactHub](https://artifacthub.io/).

```{svgbob}
             .---------------------------.
             |     "Chart repository"    |
.------.     |                           |
| Helm |<--->| .----------. .----------. |
'------'     | | Postgres | | WordPres | |
             | | chart    | | chart    | |
             | '----------' '----------' |
             |         .-------.         |
             |         | MySQL |         |
             |         | chart |         |
             |         '-------'         |
             '---------------------------'
```

Each chart can be installed multiple times, where each installation has a different name and / or namespace. Helm can update installations in one of two ways: An installation can be updated to ...

 * a newer / older version of a chart.
 * use a different set of configurations.

Each change to an installation is called a revision. For example, an installation of a Redis chart may go through the following revisions:

 1. Installed Redis 5 with default configurations.
 2. Updated configurations to listen on port 3333.
 3. Upgraded Redis 5 to Redis 6.
 4. Upgraded Redis 6 to Redis 7 and updated configurations to listen on port 7777.
 5. Rolled back to revision 2 (Redis 5 configured to listen on port 3333).

```{svgbob}
.-------.                .--------------.               .-----------.
| Chart |----------------| Installation |---------------| Revisions |
'-------' 1           1+ '--------------' 1          1+ '-----------'
```

Each revision has a lifecycle, which is stored inside of Kubernetes as a secret of a type `helm.sh/release.v1`.  The steps of that lifecycle are ...

 * `pending-install` - this revision is pending, it's for an installation.
 * `pending-upgrade` - this revision is pending, it's for an update.
 * `pending-rollback` - this revision is pending, it's for a rollback.
 * `deployed` - this revision has deployed.
 * `superseded` - this revision has been superseded by a new revision.
 * `failed` - this revision failed to deploy.

```{svgbob}
                              *
                              |
             .----------------+----------------.
             |                |                |
             v                v                v
.-----------------.  .-----------------.   .------------------.
| pending-install |  | pending-upgrade |   | pending-rollback |
'-----------+--+--'  '-+------+--------'   '--+--+------------'
            |  |       |      |               |  |
            |  |       |      v               |  |
            |  |       \   .--------.         |  |
            |  '--------]->| failed |<--------'  |
            |          /   '--------'            |
            |          |                         |
            |          v                         |
            |      .----------.                  |
            '----->| deployed |<-----------------'
                   '---+------'
                       |                    
                       v
                  .------------.
                  | superseded |
                  '------------'
```

Helm is used via a CLI of the same name. By default, the Helm CLI uses the same configuration as kubectl to access the cluster, meaning Helm's CLI should work if kubectl works.

```sh
helm repo add bitnami https://charts.bitnami.com/bitnami  # Add bitnami's repo as "bitnami"
helm repo update                                          # Update list of charts from repos
helm install my-db bitnami/mysql                          # Install bitnami's mysql as "my-db"
```

### Repository References

`{bm} /(Extensions\/Helm\/Repository References)_TOPIC/i`

To add a reference to a chart repository, use `helm repo add`. Each added chart repository is given a local name, such that whenever that chart repository needs to be accessed in the CLI, the local name is used instead of the full URL.

```sh
# Add a repo as "bitnami".
helm repo add bitnami https://charts.bitnami.com/bitnami
# Add a repo as "my-private" using username and password authentication.
helm repo add my-private https://my-org/repo --username $USERNAME --password $PASSWORD
# Add a repo as "my-private" using SSL key file.
helm repo add my-private https://my-org/repo --key-file $SSL_KEY_FILE
# Add a repo as "my-private" using SSL certificate file.
helm repo add my-private https://my-org/repo --cert-file $SSL_CERT_FILE
# Add a repo as "my-private" but skip certificate checks for the server.
helm repo add my-private https://my-org/repo --insecure-skip-tls-verify
# Add a repo as "my-private" but use custom CA file to verify server's certificate.
helm repo add my-private https://my-org/repo --ca-file $CA_FILE
```

To list all chart repository references, use `helm repo list`.

```sh
# List all chart repositories.
helm repo list
# List all chart repositories as YAML.
helm repo list --output yaml
# List all chart repositories as JSON.
helm repo list --output json
```

To remove a chart repository reference, use `helm repo remove`.

```sh
# Remove the repo "bitnami".
helm repo remove bitnami
# Update only the repos "bitnami" and "my-private".
helm repo remove bitnami my-private
```

Helm caches a chart repository once it's been added. To update an added chart repository's cache, use `helm repo update`.

```sh
# Update all repos.
helm repo update
# Update only the repos "bitnami" and "my-private".
helm repo update bitnami my-private
```

To search added chart repositories for charts containing a specific keyword, use `helm search repo`.

```sh
# Search all repos for charts containing "redis".
helm search repo redis
# Search all repos for charts containing "redis", including pre-release versions.
helm search repo redis --devel
# Search all repos for charts containing "redis", including prior versions of charts.
helm search repo redis --versions
```

```{note}
Rather than searching just added repositories for "redis", it's possible to search all repositories in [ArtifactHub](https://artifacthub.io/) (or your own instance of it) via `helm search hub redis`.
```

### Installation Management

`{bm} /(Extensions\/Helm\/Installation Management)_TOPIC/i`

```{prereq}
Extensions/Helm/Repository References_TOPIC
```

To install a chart, use `helm install`. Installing a chart requires the chart's name (e.g. `redis`), where to find the chart (e.g. locally vs chart repository), and what to name the installation (e.g. `my-redis-install`). Depending on the chart, some configuration parameters will likely be needed during installation as well.

```{note}
If installing / upgrading from a chart repository that's been added to Helm, you should update Helm's cache of that chart repository first: `helm repo update`.
```

```sh
# Install "my-app" from the directory "./web-server".
helm install my-app ./web-server
# Install "redis" from the repo at https://charts.bitnami.com/bitnami.
helm install my-app https://charts.bitnami.com/bitnami/redis
# Install "redis" from the repo added as "bitnami".
helm install my-redis-install bitnami/redis \
  --namespace $NAMESPACE \  # Namespace to install under (optional, default if omitted)
  --version $VERSION \      # Version of chart to install (optional, latest if omitted)
  --values $YAML_FILE       # YAML containing overrides for chart's config defaults (optional)
# Install "redis" from the repo added as "bitnami" using multiple config files.
#
#  * When multiple "--values" exist, the latter's values override former's values.
helm install my-redis-install bitnami/redis \
  --namespace $NAMESPACE \  # Namespace to install under (optional, default if omitted)
  --version $VERSION \      # Version of chart to install (optional, latest if omitted)
  --values $YAML_FILE_1 \   # YAML file containing config overrides (optional)
  --values $YAML_FILE_2 \   # YAML file containing config overrides (optional)
  --values $YAML_FILE_2     # YAML file containing config overrides (optional)
# Install "redis" from the repo added as "bitnami" using individual configs.
#
#  * Individual configs reference paths in a object, similar to YAML/JSON keys.
helm install my-redis-install bitnami/redis \
  --namespace $NAMESPACE \  # Namespace to install under (optional, default if omitted)
  --version $VERSION \      # Version of chart to install (optional, latest if omitted)
  --set app.port=80 \       # YAML file containing config overrides (optional)
  --set app.name=app \      # YAML file containing config overrides (optional)
  --set app.replicas=5      # YAML file containing config overrides (optional)
# Install "redis" from the repo added as "bitnami" and force creation of namespace if it doesn't
# exist.
#
#  * Forcing namespace creation can result in security issues because the namespace won't have RBAC
#    set up.
helm install my-redis-install bitnami/redis \
  --namespace $NAMESPACE \  # Namespace to install under (optional, default if omitted)
  --create-namespace        # Create namespace if missing (optional)
# Install "redis" from the repo added as "bitnami" using a uniquely generated name.
#
#  * Generated name will be based on chart's name.
helm install my-redis-install bitnami/redis --generate-name
# Install "my-app" but wait until specific objects are in a ready state before marking as success.
#
#  * By default, the install command will block only until manifests are submitted to Kubernetes.
#    It's possible to force the install command to block until certain success criteria have bee
#    met: pods, persistent vol claims, services, and min pods for deployments/stateful sets/etc..).
helm install my-app ./web-server --wait \
  --wait-for-jobs \    # Wait until all jobs have completed as well (optional)
  --atomic \           # Delete the installation on failure  (optional)
  --timeout $DURATION  # Max duration to wait before marking as failed (optional, 5m0s if omitted)
# Simulate install "redis" from the repo added as "bitnami".
#
#  * Won't install, but will give the set of changes to be applied.
helm install my-app ./web-server --dry-run
```

To list installations, use `helm list`.

```sh
# List installations.
helm list \
  --namespace $NAMESPACE \  # Namespace of installations (optional, default if omitted)
  --max $MAX_ITEMS \        # Max installations to list (256 is set to 0 -- optional, 256 if omitted)
  --filter $REGEX           # Perl compatible regex (optional, all listed if omitted)
# List installations in all namespaces.
helm list --all-namespaces
```

To update an installation, use `helm upgrade`. Updating works very similarly to installing, supporting many of the same options. The difference between the two is that, with `helm upgrade`, Helm diffs the current installation's objects with the objects created by the chart to see what it should update. Only objects that have changes will get submitted to Kubernetes.

When using `helm upgrade`, the configuration values used by the installation aren't re-applied by default. If the previous configuration values aren't supplied by the user or the `--reuse-values` flag isn't set, the upgrade will revert all configurations back to the chart's default values.

```{note}
The book recommends that you not use `--reuse-values` and instead supply the configurations each time via YAML. It's recommended that you store the YAML somewhere in git (unless it has sensitive information, in which case you should partition out the sensitive info into another YAML and keep it secure somewhere).
```

```sh
# Update "my-app" from the directory "./web-server" with existing config.
helm upgrade my-app ./web-server --reuse-values \
  --force                   # Replace object manifests instead of updating them (optional)
# Update "redis" from the repo added as "bitnami" with existing config.
helm upgrade my-redis-install bitnami/redis --reuse-values \
  --force                   # Replace object manifests instead of updating them (optional)
  --namespace $NAMESPACE \  # Namespace installed under (optional, default if omitted)
  --version $VERSION \      # Version of chart to update to (optional, latest if omitted)
# Update "redis" from the repo added as "bitnami" with new YAML config.
helm upgrade my-redis-install bitnami/redis \
  --force                   # Replace object manifests instead of updating them (optional)
  --namespace $NAMESPACE \  # Namespace installed under (optional, default if omitted)
  --version $VERSION \      # Version of chart to update to (optional, latest if omitted)
  --values $YAML_FILE       # YAML containing overrides for chart's config defaults (optional)
# Update "my-app" with existing config, but wait until specific objects are in a ready state before
# marking as success.
#
#  * By default, the install command will block only until manifests are submitted to Kubernetes.
#    It's possible to force the install command to block until certain success criteria have bee
#    met: pods, persistent vol claims, services, and min pods for deployments/stateful sets/etc..).
helm upgrade my-app ./web-server --reuse-values --wait \
  --cleanup-on-fail \  # Delete new resources inserted by the upgrade on failure (optional)
  --wait-for-jobs \    # Wait until all jobs have completed as well (optional)
  --atomic \           # Rollback the update on failure  (optional)
  --timeout $DURATION  # Max duration to wait before marking as failed (optional, 5m0s if omitted)
# Simulate update "redis" (with existing config) from the repo added as "bitnami".
#
#  * Won't update, but will give the set of changes to be applied.
helm upgrade my-app ./web-server --reuse-values --dry-run
```

To update or install (update if it exists / install if it doesn't exist), use `helm upgrade` just as before but also set the `--install` flag.

```sh
# Update or install "redis" from the repo added as "bitnami".
helm upgrade my-redis-install bitnami/redis \
  --install                 # Install rather than upgrade if "my-app" doesn't exist (optional)
  --namespace $NAMESPACE \  # Namespace installed under (optional, default if omitted)
  --version $VERSION \      # Version of chart to update to (optional, latest if omitted)
  --values $YAML_FILE       # YAML containing overrides for chart's config defaults (optional)
# Update or install "redis" from the repo added as "bitnami", and if installing, force creation of
# namespace if it doesn't exist.
#
#  * Forcing namespace creation can result in security issues because the namespace won't have RBAC
#    set up.
helm upgrade my-redis-install bitnami/redis \
  --install                 # Install rather than upgrade if "my-app" doesn't exist (optional)
  --namespace $NAMESPACE \  # Namespace installed under (optional, default if omitted)
  --create-namespace        # Create namespace if missing (optional)
```

```{note}
`helm template` will do similar work to `helm upgrade`, but instead of applying updated / created objects to Kuberentes, it simply shows you the manifests for those objects.
```

Helm retains an installation's update history directly within Kubernetes (stored as secrets). To access the update history of an installation, use `helm history`.

```sh
# Get revision history for "redis".
helm history redis
# Get revision history for "redis" as YAML.
helm history redis --output yaml
# Get revision history for "redis" as JSON.
helm history redis --output json
```

To rollback to a previous revision of an installation, use `helm rollback`.

```sh
# Rollback "redis" to revision 3.
helm rollback redis 3
# Simulate rollback "redis" to revision 3.
#
#  * Won't rollback, but will give the set of changes to be applied.
helm rollback redis 3 --dry-run
```

To remove an installation, use `helm uninstall`.

```sh
# Uninstall "redis".
helm uninstall redis
# Uninstall "redis" but keep it's history.
helm uninstall redis --keep-history
```

### Custom Charts

`{bm} /(Extensions\/Helm\/Custom Charts)_TOPIC/i`

To create a custom chart, use `helm create $NAME` to first create a skeleton. The directory structure created should have pieces to it:

 * Configurations: The files `Chart.yaml` and `values.yaml` are configurations for the chart.
 * Templates: The `templates` directory contains manifest templates (and other templates) for the chart.
 * Tests: The `templates/test` directory contains manifest templates for automated tests of the chart.
 * Dependencies: The `charts` directory contains other charts that the chart depends on.

The subsections below detail the particulars of each file / directory.

#### Configurations

`{bm} /(Extensions\/Helm\/Custom Charts\/Configurations)_TOPIC/i`

In a chart directory, the files `Chart.yaml` and `values.yaml` make up the configurations for the chart.

`Chart.yaml` contains metadata about the chart (e.g. what it's called, who maintains it, etc..) as well as some control flags.

```yaml
# [REQUIRED] The chart specification being targeted by this chart. Set this value to "v2" ("v2"
# charts targets version 3 of Helm, while "v1" targets version 2 of Helm).
apiVersion: v2
# [REQUIRED] The name of this chart. This is the name people use when they install / update this
# chart. This name must conform to the specifications of names for Kubernetes objects (lowercase
# characters, numbers, dashes, and dots only).
name: my-app  
# [OPTIONAL] The annotations associated with this chart. Similar to annotations for Kubernetes
# objects.
annotations:
  development-os: Windows95
# [OPTIONAL] The description, project URL, source URLs, icons, maintainers, and keywords associated
# with this chart.
description: Some text here.
home: https://chart.github.io
sources: [https://github.com/organization/chart]
icon: https://github.com/some_user/chart_home/icon.svg  # This can be a data URL (if you want)
maintainers:
  - name: Steve
    email: steve@gmail.com
    url: https://steve.com
  - name: Josh
    url: https://josh.com
  - name: George
keywords: [apple, cars, pepsi]
# [OPTIONAL] This can be set to either "application" or "library" (default is "application"). An
# "application" is a chart that installs an application for some user, while a "library" is
# essentially a chart that provides helper functionality for other charts (it can't be
# installed).
type: application
# [REQUIRED] This is the version of this chart. This should be incremented whenever a change is
# made to the chart.
version: 1.0.1
# [OPTIONAL] This is the version of the application being installed by this chart (must be set if
# type of this chart is "application"?).
appVersion: 7.0.1
```

`values.yaml` contains default configuration values for the chart, which are overridable by the user during installs / updates.

```yaml
app.port: 8080
app.service-type: LoadBalancer
```

#### Templates

`{bm} /(Extensions\/Helm\/Custom Charts\/Templates)_TOPIC/i`

```{prereq}
Extensions/Helm/Custom Charts/Configurations_TOPIC
```

In a chart directory, the files inside of the `templates/` directory consist of templates. These templates are mostly for manifests, but can also include macros and templates for other aspects of the chart (e.g. `NOTES.txt` is displayed to the user once it installs).

Helm's templating functionality leverages [Go's text template package](https://pkg.go.dev/text/template). Rendering a template requires an object, where that object's fields are evaluated to fill in various sections of the template. Helm provides this object. The object has ...

 * configuration values under `.Values`.
 * revision information under `.Release`.
 * chart information under `.Chart`.
 * template information under `.Template`.
 * Kubernetes cluster capabilities under `.Capabilities`.
 * file access methods under `.Files`.

The object's most commonly accessed fields are...

 * `.Values` - Configuration values. These are from `values.yaml`, where some or all values are overridden by the user.
 * `.Chart.Name` - Chart's name. Maps to `name` in `Config.yaml`.
 * `.Chart.Version` - Chart's version.  Maps to `version` in `Config.yaml`.
 * `.Chart.AppVersion` - Chart's application version.  Maps to `appVersion` in `Config.yaml`.
 * `.Chart.Annotations` - Chart's annotations.  Maps to `annotations` in `Config.yaml`.
 * `.Release.Name` - Release name.
 * `.Release.Namespace` - Release namespace.
 * `.Release.IsInstall` - `true` if installing.
 * `.Release.IsUpgrade` - `true` if upgrading or rolling back.
 * `.Release.Service` - !!Service!! performing the release. Usually, it's Helm doing it.
 * `.Template.Name` - Template file path (relative to chart directory's parent - e.g. `/my-chart/templates/service.yaml`).
 * `.Template.BaseName` - Template directory path (relative to chart directory's parent - e.g. `/my-chart/templates`).
 * `.Capabilities.APIVersions` - Supported API versions and kinds.
 * `.Capabilities.KubeVersion.Version.Major` - Kubernetes major version.
 * `.Capabilities.KubeVersion.Version.Minor` - Kubernetes minor version.

```{note}
For `.Chart`, the `Config.yaml` has keys with lowercase first characters. When accessed through the object, you need to uppercase that first character (e.g. `name` becomes `.Chart.Name`).
```

In the template, evaluations are encapsulated by double squiggly brackets, where inside the brackets are field accesses and control structures. The object provided by Helm is referenced simply with a preceding dot (e.g. `{{.Values.app.name}}`).

```yaml
# Define template macros
{{define "name"}}
name: {{.Values.app.name}}
{{end}}
{{define "labels"}}
app: backend
version: 3.4.1
{{end}}
# Define template
apiVersion: v1
kind: Pod
metadata:
  {{include "name" . | nident 2}}
  labels:
    {{include labels | nident 4}}
spec:
  containers:
    - image: my-image:1.0
      name: my-container
```

The rest of this section gives a brief but incomplete overview of templating in Helm. A complete overview of templating is available at the documentation for [Go's template package](https://pkg.go.dev/text/template) and [Helm's templating functions](https://helm.sh/docs/chart_template_guide/function_list/).

Common template evaluations are listed below (e.g. accessing fields, calling functions, if-else, variables, etc..).

 * `{{.Values.app.name}}` - Field access.
 * `{{printf "%s-%s" "my-app" "v1.0}}` - Function invocation.
 * `{{trimSuffix "-" (trunc 63 (printf "%s-%s" "my-app" "v1.0))}}` - Chain function invocation.
 * `{{trimSuffix "-" (trunc 63 (printf "%s-%s" .Values.app.name .Values.app.version))}}` - Chained function invocations and field accesses together.
 * `{{printf "%s-%s" .Values.app.name .Values.app.version | trunc 63 | trimSuffix "-"}}` - Chained function invocations and field accesses together *as a pipeline*. The result of each command is passed as *last* argument of the next.
 * `{{$var := .Values.app.name}}` - Variable declaration. Produces no output, but variable may be used further on in the template.
 * `{{if $var}} not empty {{end}}` - If block. Tests if whatever passed in is truthy (e.g. true if bool, >0 if integer, not null if object, non-empty if collection). The condition passed may be a compound (e.g. chained method invocations).
 * `{{if $var}} not empty {{else}} empty {{end}}` - If-else block. Similar to above, but with an else block.
 * `{{if $var1}} not empty1 {{else if $var2}} not empty2 {{else}} empty {{end}}` - If-else block. Similar to above, but with extra conditional checks.
 * `{{range .Values.my_list}} item={{.}} {{end}}` - Loop over the elements of a list. The current list item is placed in `.`.
 * `{{range $i,$v := .Values.my_list}} idx={{i}}, idx={{v}} {{end}}` - Loop over the elements of a list using variables. The current list item and its index are placed into variables.
 * `{{range $k,$v := .Values.my_dict}} key={{k}}, val={{v}} {{end}}` - Loop over the elements of a dict using variables. The current dict key and value are placed into variables.
 * `{{- .Values.app.name}}` - Ignore preceding whitespace of this block during evaluation. Dash must be followed by whitespace.
 * `{{.Values.app.name -}}` - Ignore trailing whitespace of this block during evaluation. Whitespace must be before dash.
 * `{{/* comment here */}}` - Comment (nothing gets rendered). May span multiple lines.

Common template functions are categorized are listed below. Some of these come directly from Go while others are provided by Helm.

```{note}
Many of these functions have `must` variants (e.g. `toYaml` vs `mustToYaml`) which error out in case it can't perform the expected function.
```

 * Common
   * `eq arg1 arg2` - Equals (`arg1 == arg2`).
   * `ne arg1 arg2` - Not equals (`arg1 != arg2`).
   * `lt arg1 arg2` - Less than (`arg1 < arg2`).
   * `le arg1 arg2` - Less than or equal (`arg1 <= arg2`).
   * `gt arg1 arg2` - Greater than (`arg1 > arg2`).
   * `ge arg1 arg2` - Greater than or equal (`arg1 >= arg2`).
   * `and arg1 arg2` - Logical AND (`arg1 and arg2`).
   * `or arg1 arg2` - Logical OR (`arg1 or arg2`).
   * `not arg1` - Logical NOT (`not arg1`).
   * `len arg1` - Length of string, collection, etc..
   * `print args...` - Go's print function.
   * `printf args...` - Go's printf function.
 * Collections
   * `index arg1 dims...` - Access some index (e.g. `index my_matrix 5 2` is equivalent to `my_matrix[5][2]`).
   * `list args...` - Create list of arguments (e.g. `list 1 2 3`).
   * `prepend l1 val` - Prepend value to a list (e.g. `prepend (list 1 2 3) 4`).
   * `append l1 val` - Prepend value to a list (e.g. `append (list 1 2 3) 4`).
   * `first l1` - Return first element of list.
   * `rest l1` - Return all but the first element of list.
   * `last l1` - Return last element of list.
   * `initial l1` - Return all but the last element of list.
   * `concat args...` - Concatenate lists into a single list (e.g. `concat (list 1 2 3) (list 4 5)`).
   * `dict args...` - Create dict of argument paris (e.g. `dict "key1" "value1" "key2" "value2"`).
   * `keys d1` - Get all dictionary keys (e.g. `keys (dict "k1" "v1" "k2" "v2")`).
   * `values d1` - Get all dictionary values (e.g. `keys (dict "k1" "v1" "k2" "v2")`).
   * `get d1 k` - Get dictionary entry (e.g. `get (dict "k1" "v1" "k2" "v2") "k2"`).
   * `set d1 k v` - Set dictionary entry (e.g. `set (dict "k1" "v1" "k2" "v2") "k3" "v3"`).
   * `unset d1 k` - Unset dictionary entry (e.g. `unset (dict "k1" "v1" "k2" "v2") "k2"`).
   * `hasKey d1 k` - Test if dictionary has key (e.g. `hasKey (dict "k1" "v1" "k2" "v2") "k2"`).
   * `deepEqual arg1 arg2` - Deep object equality (e.g. `deepEqual (list $obj1, obj2, obj3)  (list $obj4, obj5, obj7)`).
   * `deepCopy arg1` - Deep object copy (e.g. `deepEqual (list $obj1, obj2, obj3)`).
 * String
   * `trim arg` / `trimSuffix arg` / `trimPrefix arg` - Remove whitespace from start and / or end of function.
   * `nospace arg` - Remove all whitespace.
   * `contains arg1 arg2` - Test if 1st string is in 2nd string (e.g. `contains "app" "apple"`).
   * `hasPrefix arg1 arg2` / `hasSuffix arg1 arg2` - Test if 1st string starts / sends with 2nd string (e.g. `hasPrefix "app" "apple"`).
   * `replace arg1 arg2 arg3` - In the 3rd string, replace all instances of 1st string with the 2nd string (e.g. `replace "p" "t" "happy"`).
   * `lower arg` / `upper arg` - Convert to lowercase / uppercase.
   * `title arg` / `untitle arg` - Convert to / from title case.
   * `snakecase arg` - Convert from camel case to snake case (e.g. `snakecase "HelloWorld"`).
   * `camelcase arg` - Convert from snake case to camel case (e.g. `camelcase "hello_world"`).
   * `kebabcase arg` - Convert from camel case to kebab case (e.g. `kebabcase "HelloWorld"`).
   * `indent num str` - Indent each line by a certain number of spaces (e.g. `indent 4 "hello\nworld"`).
   * `nindent num str` - Same as above but adds a new line character before indenting (e.g. `nindent 4 "hello\nworld"`).
 * Regex (FYI: Regex needs to be escaped when used in a string literal, similar to how you have to quote it in Java or Python.)
   * `regexMatch regex str` - Match regex against a string (e.g. `regexMatch "\\d{5}" "12345"`).
   * `regexFind regex str` - Find first match of a regex within a string (e.g. `regexFind "[2,4]" "12345"`).
   * `regexFindAll regex str max` - Find matches of a regex within a string (e.g. `regexFindAll "[1,3,5]" "12345" -1`). Set `max` to the maximum number of matches to return, where -1 means unlimited.
   * `regexReplaceAll regex str replace` - Replace matches of a regex within a string (e.g. `regexReplaceAll "([1,3,5])" "12345" "!${1}!"`). Set `replace` to the replacement string, where that replacement string uses dollar sign to reference capture groups (similar to Java's regex replacement). The expression `regexReplaceAll "([1,3,5])" "12345" "!${1}!"` generates the replacement `"!1!2!3!4!5!"`.
   * `regexReplaceAllLiteral regex str replace` - Similar to above, but doesn't replace with capture groups. The expression `regexReplaceAllLiteral "([1,3,5])" "12345" "!${1}!"` generates the replacement `"!${1}!2!${1}!4!${1}!"`.
   * `regexSplit regex str max` - Split a string using a regex delimiter (e.g. `regexSplit "[1,3,5]" "12345" -1`). Set `max` to the maximum number of substrings to return, where -1 means unlimited.
 * Random
   * `shuffle arg` - Shuffles the characters in a string.
   * `randAlpha c` / `randNumeric c` / `randAlphaNum c` / `randAscii c` - Generate random string of a certain size, containing only letters / numbers / alphanumeric characters / ASCII characters (e.g. `randAlpha 5`).
   * `uuidv4` - Generate a UUID v4.
* Utility
   * `default def arg` - Return a default value if argument is unset.
   * `semver ver` - Parse semantic version into an object. Object has fields `Major`, `Minor`, `Patch`, `Prerelease`, and `Metadata`.
   * `semverCompare format ver` - Test if semantic version matches a version constraint (version constraints documented [here](https://github.com/Masterminds/semver#basic-comparisons)).
   * `toYaml arg` - Dump as YAML.
   * `toJson arg` - Dump as JSON.
   * `toPrettyJson arg` - Dump as JSON but pretty-printed.
   * `b32enc arg` / `b64enc arg` - Encode with Base 32 / 64.
   * `b32dec arg` / `b64dec arg` - Decode with Base 32 / 64.
 * Date
   * `unixEpoch` - Number of seconds since Unix epoch.
   * `now` / `date fmt` / `dateInZone fmt` - Current time as object. Typically formatted to string via `date` / `dateInZone` (e.g. `now | date`).
 * Kubernetes
   * `lookup apiVersion kind namespace name` - Get Kubernetes object. Set `name` to empty string to get all. Set `namespace` to empty string for cluster-level kinds.
   * `.Capabilities.APIVersions.Has api` - Test if a version and / or kind exists in Kubernetes (e.g. `.Capabilities.APIVersions.Has "apps/v1/Deployment` or `.Capabilities.APIVersions.Has "apps/v1`).
 * File-access
   * `.Files.Get path` - Read a file into a string. `path` is a path relative to the chart directory.
   * `.Files.Lines path` - Read a file as an array of lines. `path` is a path relative to the chart directory.
   * `.Files.GetBytes path` - Read a file into an array of bytes. `path` is a path relative to the chart directory.

A template can define a set of macros that act similarly to functions. To define a macro, wrap template text in `{{define name}}` and `{{end}}`.

```
{{define "name"}}
  name: {{.Values.app.name}}
{{end}}
{{define "labels"}}
    app: backend
    version: 3.4.1
{{end}}
```

To use a macro, use `{{template name scope}}`, where `name` is the name of the template and `scope` is whatever object that template uses when accessing fields and functions. If `scope` is omitted, the render may not be able to access necessary fields or functions to render. For example, in the last macro defined above, `scope` needs to contain the path `app.name`.

```yaml
# PRE-RENDER
{{define "name"}}
  name: {{.Values.app.name}}
{{end}}
{{define "labels"}}
    app: backend
    version: 3.4.1
{{end}}
apiVersion: v1
kind: Pod
metadata:
{{template "name" .}}
  labels:
{{template labels}}
spec:
  containers:
    - image: my-image:1.0
      name: my-container
----
# POST-RENDER
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
    app: backend
    version: 3.4.1
spec:
  containers:
    - image: my-image:1.0
      name: my-container
```

One issue with `{{template name scope}}` is inability to control whitespace in the render. For the macros to truly be reusable, they need to appropriately be indented to align with the section of YAML they're being rendered in. For example, imagine wanting to modify the example above to include the name as label as well. The YAML produced would be incorrect.

```yaml
# PRE-RENDER
{{define "name"}}
  name: {{.Values.app.name}}
{{end}}
{{define "labels"}}
    app: backend
    version: 3.4.1
{{end}}
apiVersion: v1
kind: Pod
metadata:
{{template "name" .}}
  labels:
app-{{template "name" .}}
{{template labels}}
spec:
  containers:
    - image: my-image:1.0
      name: my-container
----
# POST-RENDER
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
app-  name: my-app  # WRONG - should be "app-name: my-app" and indented to be child of "labels:.
    app: backend
    version: 3.4.1
spec:
  containers:
    - image: my-image:1.0
      name: my-container
```

The typical workaround to this is to use `{{include name scope}}`, which is a special function provided by Helm that, unlike `{{template name scope}}`, can be used in pipeline method invocations. Being usable in a pipeline means that you can pass the macro output to the `indent` / `nindent` function to properly align output.
 
```yaml
# PRE-RENDER
{{define "name"}}
name: {{.Values.app.name}}
{{end}}
{{define "labels"}}
app: backend
version: 3.4.1
{{end}}
apiVersion: v1
kind: Pod
metadata:
  {{include "name" . | nident 2}}
  labels:
    # Trim preceding/trailing whitespace from "name" macro output, then add "app- to it, then
    # indent add a new line to the beginning of it and indent all lines by 4.
    {{printf "app-%s" trim (include "name" .) | nident 4}}
    {{include labels | nident 4}}
spec:
  containers:
    - image: my-image:1.0
      name: my-container
----
# POST-RENDER
apiVersion: v1
kind: Pod
metadata:

  name: my-app
  labels:
    # Trim preceding/trailing whitespace from "name" macro output, then add "app- to it, then
    # indent add a new line to the beginning of it and indent all lines by 4.

    app-name: my-app

    app: backend
    version: 3.4.1
spec:
  containers:
    - image: my-image:1.0
      name: my-container
```

#### Tests

`{bm} /(Extensions\/Helm\/Custom Charts\/Tests)_TOPIC/i`

```{prereq}
Extensions/Helm/Custom Charts/Templates_TOPIC
```

TODO: TALK ABOUT TESTS HERE

TODO: TALK ABOUT TESTS HERE

TODO: TALK ABOUT TESTS HERE

TODO: TALK ABOUT TESTS HERE


#### Dependencies

`{bm} /(Extensions\/Helm\/Custom Charts\/Dependencies)_TOPIC/i`

```{prereq}
Extensions/Helm/Custom Charts/Templates_TOPIC
```

TODO: TALK ABOUT CHART DEPS HERE

TODO: TALK ABOUT CHART DEPS HERE

TODO: TALK ABOUT CHART DEPS HERE

TODO: TALK ABOUT CHART DEPS HERE

#### Packaging

To package a chart for distribution, use `helm package $NAME`. Based on the configuration of the chart, Helm will generate an archive with filename `$CHART_NAME-$VERSION.tgz` which encompasses the entire chart. Others can use this file to install the chart.

```sh
# Package "my-chart".
helm package my-chart
# Package "my-chart" but update chart dependencies first.
helm package my-chart --dependency-update
# Package "my-chart" to a the directory "/home/user".
helm package my-chart --destination /home/user
# Package "my-chart" but automatically update the chart version and the app version.
helm package my-chart \
  --app-version $APPVER \ # Override chart's app version (optional, config value used if omitted)
  --version $CHARTVER     # Override chart's version (optional, config value used if omitted)
```

The packaging process reads a special file that instructs it on which files and directories to ignore, named `.helmignore`. Files and directories are ignored using glob patterns, similar to `.gitignore` for git and `.Dockerignore` for Docker.

```
# Patterns to ignore when building packages.
.git/
.gitignore
.vscode/
*.tmp
**/temp/
```

Prior to packaging a chart, it's common to run it through Helm's built-in linter to see if it has any issues (e.g. invalid YAML generated). To link a chart, use `helm lint $NAME`. The linter supports three levels of feedback: informational, warning, and error. Only error causes the process to exit with a non-zero return code.

```sh
# Lint "my-chart".
helm lint my-chart
# Lint "my-chart" but treat warnings as errors.
helm lint my-chart --strict
```

## Prometheus

`{bm} /(Extensions\/Prometheus)_TOPIC/i`

```{prereq}
Kinds/Horizontal Pod Autoscaler_TOPIC
Extensions/Helm_TOPIC
```

Prometheus is a monitoring system that can integrate with Kubernetes to support custom metrics. These custom metrics, which Prometheus grabs by scraping files and querying servers, provide better visibility into the system and can be used to scale replicas via an HPA / VPA.

Any HPA can scale by using an object's values as metrics.

TODO: discuss installing through helm

TODO: discuss exposing endpoints to scrape metrics, and scale on those metrics

# Guides

`{bm} /(Guides)/`

The following subsections are guides to various aspects of Kubernetes.

## Pod Design

`{bm} /(Guides\/Pod Design)/`

```{prereq}
Kinds_TOPIC
Security_TOPIC
Extensions_TOPIC
```

Designing a pod appropriately requires ...

 * benchmarking and performance metrics.
 * mapping out what resources the pod needs access to and how it accesses those shared volume (e.g. read-only access to shared volumes)
 * mapping out what network entities it can communicate with and how it communicates with those network entities.

The following subsections detail various aspects of pod design.

### Security

`{bm} /(Guides\/Pod Design\/Security)/`

```{prereq}
Kinds/Pod_TOPIC
Kinds/Volume_TOPIC
Kinds/Service Account_TOPIC
Kinds/Secret_TOPIC
Kinds/Configuration Map_TOPIC
Security_TOPIC
```

There are several aspects to hardening the security of a pod.

 * **Harden container isolation** 
 
   Unless a container explicitly requires it, ...

   * turn off access to kernel capabilities. Bugs in the kernel are discovered from time-to-time, and when the container has privileged access to the kernel / has certain kernel capabilities enabled, it could lead to an attacker breaking out of container isolation and compromising the node itself.

   ```{note}
   How would you know which kernel capabilities you need? Can you stress test and log which capabilities were used? Then restrict the pod to just those capabilities?
   ```
    
   * don't run container processes as the root user (UID 0). For example, imagine a container running as root that has a volume mounted to a directory on the node that's running it. If that container were comprised by an attacker, the attacker could write to files with executable permissions as root, potentially leading to the node itself being compromised.

   ```{note}
   How would you know if the application won't crash if you used a user other than root? Stress test with a non-root user and see what happens?
   ```

   * don't expose aspects of the node to the container. Exposing aspects such as the node's networking interfaces, file system, incoming ports, or process IDs can leak information to an attacker as well as provide vectors of attack to the node.

   ```{seealso}
   Kinds/Pod/Container Isolation/Security Context_TOPIC (Pod isolation configurations)
   Kinds/Pod/Container Isolation/Node Access_TOPIC (Pod isolation configurations)
   Security/Pod Security Admission_TOPIC (Pod isolation restrictions)
   ```

 * **Harden network isolation**
    
   A pod typically doesn't require unrestricted network access to pods / endpoints across the entire cluster. For example, imagine an application broken up into three sets of pods: frontend, backend, and database. The ...

   * frontend pods receive requests from the outside world and send requests to the backend pods.
   * backend pods receive requests from the frontend pods and send requests to the database pods.
   * database pods receive requests from the backend pods.

   The three sets of pods above can have their networking restricted based on the expected flow of requests. That way, an attacker that compromises a frontend pod doesn't immediately have network access to a database pod (or some other unknown pod in the cluster).

   ```{seealso}
   Security/Network Policy_TOPIC (Pod network isolation)
   ```

 * **Harden API access**
 
   Unless a container explicitly requires it, turn off the mounting of credentials for the Kubernetes API server. For example, if an attacker compromises a container that has these credentials mounted, it gives them a leg up to compromising the Kubernetes API server itself.
 
   If access to the Kubernetes API server is required by the container, the credentials mounted should be for a service account that's restricted to only the required parts of the API (e.g. via RBAC).

   ```{seealso}
   Kinds/Pod/API Access_TOPIC (Pod credential mounting)
   Security/API Access Control/Role-based Access Control_TOPIC (Restricting API access via service accounts)
   Security/API Access Control/Disable Credentials_TOPIC (Preventing API credentials from being mounted to pod)
   ```

 * **Harden volume access**
 
   Unless a container explicitly requires write access to a volume, mount that volume in read-only mode. For example, imagine a pod containing a sidecar which collects the main container's logs. The sidecar gets access to the main container's log files via a volume, where that shared volume is used by the main container to store logs, configurations, and data.
 
   If the sidecar isn't restricted to just reading that shared volume, an attacker could first compromise the sidecar and use it to compromise the main container by writing malicious configurations and data on that shared volume.

   ```{seealso}
   Kinds/Volume/Access Modes_TOPIC (Access modes of volumes)
   ```

 * **Sensitive credential storage**

   All security-related configurations should be stored using secrets rather than config maps. Secrets are encrypted by default and extra care is taken to ensure they don't leak.

   When using secrets, mount as a volume if possible rather than dumping into environment variables. The volumes used for secrets are similar to a RAM disk in that no bits are actually being written to disk, providing an extra level of security against leaks. For example, if secrets were being written to disk, an attacker could look through blocks on the disk and potentially extract the contents of the deleted files (even if those deleted -- deleting a file doesn't necessarily wipe the data used by that file).

   ```{seealso}
   Kinds/Secret_TOPIC (Secret should be used for sensitive configurations)
   ```

### Configuration

`{bm} /(Guides\/Pod Design\/Configuration)/`

```{prereq}
Kinds/Pod/Images_TOPIC
Kinds/Pod/Environment Variables_TOPIC
Kinds/Pod/Metadata_TOPIC
Kinds/Pod/Service Discovery_TOPIC
```

A pod's configuration can make use of several features to ensure that it functions well.

 * **Image**

   * Should not use `latest`: Containers using `latest` may encounter inconsistent behavior across the cluster due to the fact that `latest` is a tag that constantly updates.
   * Should not update non-`latest`: Kubernetes caches images, meaning that if an image is cached but then updated again, nodes may run inconsistent images.

 * **Metadata**

   * Should declare sensitive configurations in secrets: Containers needing sensitive configurations (e.g. passwords, certificates, etc..) should use secrets to access those credentials instead of config maps.
   * Should declare non-sensitive configurations in config maps: Containers needing sensitive configurations (e.g. passwords, certificates, etc..) should use secrets instead of config maps.
   * Should use volume mounts for metadata: Containers access various metadata and configurations via either environment variables or volumes (e.g. service IPs, pod labels, config map entries, etc..). Volumes are preferred over environment variables because, as data gets updated, volumes will reflect the updated data while environment variables won't.

 * **Resources**

   * Should declare resource requirements: Containers should declare resource requests and resource limits.
   * May declare hardware requirements: Pods can use node selectors, node affinity, and taints / tolerations to direct pods towards preferred hardware (e.g. prefer Intel CPUs over AMD CPUs).

### Lifecycle

`{bm} /(Guides\/Pod Design\/Lifecycle)/`

```{prereq}
Kinds/Pod/Lifecycle_TOPIC
```

A pod's lifecycle can make use of several features to ensure that it functions well.

 * **Startup**
 
   * Should define startup probes: Startup probes signal to Kubernetes that the pod has correctly started.
   * May define startup tasks: Init containers and post-start hooks can be used to do certain initialization tasks when the pod designer doesn't have the ability to change up the main containers in a pod (e.g. it isn't possible to re-create the main container so that it performs the initialization tasks itself). 

 * **Shutdown**
 
   * Should gracefully shutdown: A container that receives `SIGTERM` should begin gracefully shutting itself down (e.g. clearing queues) but *should not stop processing incoming requests*.
   * Should define a termination grace period: A container's graceful shutdown process must complete within the pod's `terminationGraceSeconds`, otherwise the container will be forcefully killed via `SIGKILL`.
   * May define shutdown tasks: Pre-stop hooks can be used to do certain shutdown tasks when the pod designer doesn't have the ability to change up the main containers in a pod (e.g. write something to a database).

   ```{note}
   As to the first point -- why should not stop accepting requests? See [here](https://twitter.com/thockin/status/1560398974929973248?t=aDSdlxfgH_ijhmJWH6c_Qg&s=19). The book also mentioned that you should have a delay before you stop accepting requests so things can sync up (via pre-stop hooks).
   ```

 * **Running**

   * Should define readiness probes: Readiness probes signal to Kubernetes that a pod is currently not ready to receive requests (e.g. some required resource has temporarily locked up).
   * Should define liveness probes: Liveness probes signal to Kubernetes that a pod is no longer operational (e.g. something unrecoverable has happened).
   * May define a maximum lifetime: A container's lifetime can't exceed the pod's `activeDeadlineSeconds`, otherwise the container will be forcefully killed.
   * Should define a restart policy: Pods that are running servers should always restart when their main process terminates, while pods that are running under jobs should likely only restart on failure.

### Performance

`{bm} /(Guides\/Pod Design\/Performance)/`

```{prereq}
Kinds/Pod/Node Placement_TOPIC
Kinds/Horizontal Pod Autoscaler_TOPIC
Kinds/Cluster Autoscaler_TOPIC
Extensions/Prometheus_TOPIC
```

There are several aspects to ensure that pods perform well and pod replicas scale well. Before applying performance features, a bare-bones pod should be placed on a staging environment and load tested to determine its performance characteristics.

 * **Scaling**

   * Should use pod replicas: Pods that scale horizontally should use replica sets, deployments, or stateful sets.
   * Should scale pod replicas: Pods under a replica sets, deployments, or stateful sets can automatically scale up/down their replicas based on metrics (e.g. CPU utilization) via a horizontal pod autoscaler.
   * Should scale nodes: A cluster can scale up/down the number of nodes it has based on the number of scheduled pods via a cluster autoscaler.
   * May use custom scaling metrics: Pods under a replica sets, deployments, or stateful sets can first be stress tested in a staging environment to measure performance characteristics. For example, certain pods will encounter bottleneck on IO rather than CPU utilization. In these cases, pods may define their own metrics (e.g. IO rate) and horizontal pod autoscalers can make use of them to scale.

 * **Node Placement**

   * May use pod affinity: Pods that perform better when in the vicinity of each other (e.g. faster communication if on the same data center rack) can request to be placed in that same vicinity using pod affinity.
   * May use node affinity: Pods that perform better when on specific hardware (e.g. optimized for Intel Xeon) can request to be placed on nodes with that hardware using node affinity.

## Command-line Interface

`{bm} /(Guides\/Command-line Interface)/`

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

Kubernetes API is exposed as a RESTful interface, meaning everything is represented as an object and accessed / mutated using standard REST verbs (GET, PUT, DELETE, etc..). kubectl uses this interface to access the cluster. For example, accessing https://cluster/api/v1/namespaces/default/pods/obn_pod is equivalent to running `kubectl get pod obj_pod`. The difference between the two is that, by default, kubectl formats the output in a human friendly manner, often omitting or shortening certain details. That output can be controlled using flags. Specifically, to ...

 * get more detail, use `-o wide`.
 * remove headers such that the output can be more easily piped to other tools like `wc`, use `--no-headers`.
 * get JSON output `-o json`
 * get YAML output `-o yaml`
 * get JSON output isolated to a specific field or fields `-o jsonpath --template={TEMPLATE}`, where the template is a JSONPath expression.

### CRUD

`{bm} /(Guides\/Command-line Interface\/CRUD)/`

`get` / `describe` allows you to get details on a specific objects and kinds. To get an overview of a ...

 * list of all objects of a specific kind using `kubectl get {KIND}`.
 * a specific object of a specific kind using `kubectl get {KIND} {OBJ}`.

`describe` provides more in-depth information vs `get`.

Examples of object access:

 * `kubectl get componentstatuses` - basic cluster diagnostics
 * `kubectl get nodes` - list nodes
 * `kubectl get nodes --selector='class=high-mem'` - list nodes that have label class set to `high-mem` (label selector)
 * `kubectl get nodes --selector='class=high-mem,!gpu'` - list nodes that have label class set to `high-mem` but label` gpu` unset (label selector)
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

### Deployment

`{bm} /(Guides\/Command-line Interface\/Deployment)/`

`rollout` allows you to monitor and control deployment rollouts.

 * `kubectl rollout status deployments {DEPLOYMENT}` - monitor rollout
 * `kubectl rollout pause deployments {DEPLOYMENT}` - pause rollout
 * `kubectl rollout resume deployments {DEPLOYMENT}` - resume rollout
 * `kubectl rollout history deployments {DEPLOYMENT}` - view rollout history
 * `kubectl rollout undo deployments {DEPLOYMENT}` - undo rollout (works regardless state -- e.g. if a rollout is currently in progress or not)
 * `kubectl rollout undo deployments {DEPLOYMENT} --to-revision={REV}` - undo rollout to a previous revision (see rollout history command)

`configmap` allows you to create a configuration for applications running in pods.

 * `kubectl create configmap {CONFIGMAP} --from-file=my-config.txt --from-literal=key1=value1 --from-literal=key2=value2`

```{note}
The option `--from-file` can also point to a directory, in which case an entry will get created for each file in the directory provided that the filenames don't have any disallowed characters.
```

`secret` allows you to create a security related configuration for applications running in pods.

 * `kubectl create secret generic my-tls-cert --from-file=a.crt --from-file=a.key`

### Proxy

`{bm} /(Guides\/Command-line Interface\/Proxy)/`

`proxy` allows you to launch a proxy that lets you talk internally with the Kubernetes API server.

 * `kubectl proxy`

### Debug

`{bm} /(Guides\/Command-line Interface\/Debug)/`

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

 * `{bm} kind/(\bkind)s?\b/i/true/true` - A class of object within Kubernetes (e.g. pod, service, secret, replica set, deployment, etc..).

 * `{bm} object` - An entity orchestrated / managed by Kubernetes, such as a running pod or service.

 * `{bm} manifest` - A declarative configuration (either YAML or JSON) that describes an object. This is effectively a blueprint for an object, similar to how an image is a blueprint for a container.

 * `{bm} image` - An application packaged as an immutable and isolated filesystem. The filesystem typically contains all library dependencies required for the application to run in an isolated and reproducible manner (e.g. library dependencies are the versions expected by the application).

   Images also typically include metadata describing its needs and operational standards (e.g. memory requirements for the application).

 * `{bm} container` - An instance of an image. A container creates an isolated copy of the image's filesystem, isolates the resources required for that image, and launches the entry point application for that image. That container can't see or access anything outside the container unless explicitly allowed to by the user. For example, opening a port 8080 on a container won't open port 8080 on the host running it, but the user can explicitly ask that port 8080 in the container map to some port on the host.

 * `{bm} registry/(registry|registries)/i` - A server that stores and distributes images.

 * `{bm} multistage image/(multistage build|multistage image|multistage container image)/i` - A container image produced by merging portions of other container images together. For example, to build a multistage image that contains Java as well as compiled C++ binaries, ...

   1. an image containing the JVM has its Java directory pulled out.
   2. an image containing the GNU Compiler toolchain compiles some C++ code, then those compiled binaries are pulled out.

   The result is that the multistage build only contains the relevant portions of its "stages" (previous images), leading to a more focused image with smaller size.

 * `{bm} open container initiative runtime/(Open Container Initiative runtime|Open Container Initiative)/i`  `{bm} /\b(OCI runtime|OCI)s?\b//false/true`- A runtime responsible for only creating and launching containers. Examples include runC, rkt, runV, gviso, etc.. Some of these use Linux isolation technology (cgroups and namespaces) while others use virtualization technology.

 * `{bm} container runtime interface` `{bm} /\b(CRI)s?\b//false/true` - A runtime responsible for the high-level management of containers and images: image management, image distribution, container mounts / storage, container networking, etc..
 
   CRIs are also responsible for running containers, but typically do so by delegating to an OCI runtime. Examples of CRIs include containerd, and cri-o.

 * `{bm} container engine` - A high-level application / cohesive set of applications used for all the things OCI runtimes and CRIs are used for as well as building images, signing images, and several other extra features. Container engines typically delegate to OCI runtimes and CRIs for most of their functionality.
 
   Examples include Docker Engine and Container Tools (podman for running containers, buildah for building images, and skopeo for image distribution).

 * `{bm} Kubernetes` - A tool for orchestrating multiple containers across a set machines. Provides features such as load balancing, service naming, service discovery, automated service scaling, and automated service recovery.

 * `{bm} node` - A host that Kubernetes uses to run the containers it's orchestrating.

 * `{bm} master node` - A node responsible for the managing the cluster (control plane).

 * `{bm} worker node` - A node responsible for running application containers.

 * `{bm} pod/\b(pod)s?\b/i/false/true` - A set of containers all bundled together as a single unit, where all containers in that bundle are intended to run on the same node.

 * `{bm} pod template` - The blueprint for creating pods.

 * `{bm} namespace` - A user-defined category for objects in a cluster (e.g. pods), similar to a folder on a filesystem. Namespaces allow Kubernetes to do things such as apply isolation and access control.

 * `{bm} kube-system` - A namespace for internal cluster components (pods) that Kubernetes runs for itself. For example, Kubernetes's DNS service, Kubernetes's proxy service, etc.. all run under the kube-system namespace.

 * `{bm} kube-proxy/(kube-proxy|Kubernetes proxy|Kubernetes's proxy)/i` - An internal Kubernetes proxy service responsible for routing traffic to the correct services and load balancing between a service's pods. Runs on every node in the cluster.

 * `{bm} core-dns/(core-dns|kube-dns|Kubernetes DNS|Kubernetes's DNS)/i` - An internal Kubernetes DNS service responsible for naming and discovery of the services running on the cluster. Older versions of Kubernetes call this kube-dns instead of core-dns.

 * `{bm} kubernetes-dashboard/(kubernetes-dashboard|Kubernetes Dashboard|Kubernetes UI|Kubernetes GUI|Kubernetes's Dashboard|Kubernetes's UI|Kubernetes's GUI)/i` - An internal Kubernetes service responsible for providing a GUI to interface with and explore the cluster.

 * `{bm} kubectl` - The standard command-line client for Kubernetes.

 * `{bm} context` - In reference to kubectl, context refers to default cluster access settings kubectl applies when running some command: cluster location, cluster authentication, and default namespace.

 * `{bm} label` - User-defined key-value pairs assigned to Kubernetes objects to group those objects together. Labeling objects makes it so they can be accessed as a set (e.g. target all pods with authoring team set to SRE). Unlike annotations, labels aren't for assigning metadata to objects.

 * `{bm} label selector` - An expression language used to find objects with labels (e.g. `key=value`, `key!=value`, and `key in (value1, value2)`).

 * `{bm} annotation/(annotation|annotate)/i` - User-defined key-value pairs assigned to Kubernetes objects that acts as metadata for other tools and libraries. Unlike labels, annotations aren't for grouping objects together.

 * `{bm} declarative configuration` - A form of configuring where the configuration is submitted as a state and the system adjusts itself to match that state.

 * `{bm} imperative configuration` - A form of configuring where the configuration is submitted as a set of instructions and the system runs those instructions.

 * `{bm} health check` - A Kubernetes mechanism that checks the state of pods and performs corrective action if it deems necessary. This includes both ensuring that the main container process is running, liveness probes, and readiness probes.

 * `{bm} liveness probe` - A user-defined task that Kubernetes runs to ensure that a pod is running correctly. For example, an HTTP server that stalls when for more than 15 seconds before returning a response may be deemed as no longer live.

   Kubernetes restarts a pod if it deems it as no longer alive.

 * `{bm} readiness probe` - A user-defined task that Kubernetes runs to ensure that a pod is in a position to accept requests. For example, an HTTP server that has all of its worker threads busy processing requests may be deemed as not ready.

   Kubernetes stops routing requests to a pod if it's no longer ready (removed from load balancer).

 * `{bm} utilization` - A metric that tracks the amount of resources in use vs the amount of resources available.

 * `{bm} resource request` - The minimum amount of resources required to run an image (not a pod).

 * `{bm} resource limit` - The maximum amount of resources that an image (not a pod) may take up.
 
   If Kubernetes needs to scale down a resource for a container that isn't dynamic (e.g. a running process can have its CPU usage reduced but you can't force a running process to give up memory its holding on to), the pod gets restarted with that resource scaled down.

 * `{bm} service` - A set of pods exposed under a single named network service. Requests coming in to the service and are load balanced across the set of pods.

 * `{bm} endpoints` - A low-level kind that's used to map a service to the pods it routes to. In other words, an endpoints (note the plural) object is an abstraction that references a pod.

 * `{bm} ingress` - A kind that acts as an HTTP-based frontend that routes and load balances incoming external requests to the correct service. This kind is an interface without an implementation, meaning that Kubernetes doesn't have anything built-in to handle ingress. Implementations of these interfaces are referred to as ingress controllers and are provided by third-parties.

 * `{bm} replica set` - A kind that ensures a certain number of pod replicas are running at any time.

 * `{bm} deployment` - A kind that has the same functionality as a replica set but also provides functionality for updating pods to a new version and rolling them back to previous versions.

 * `{bm} stateful set/(stateful set|stable identity)/i` - A kind that has similar functionality to a deployment but also allows its pods to retain a stable identity and dedicated persistent storage.
   
   * Stable identity means that, if a pod dies, it gets replaced with a new pod that has the same identity information (same name, same IP, etc..)
   * Dedicated persistent storage means that each stable identity can have persistent volume claims unique to it (not shared between other pods within the stateful set).

 * `{bm} reconciliation loop/(reconciliation loop|control loop)/i` - A loop that continually observes state and attempts to reconcile it to some desired state if it deviates. See declarative configuration.

 * `{bm} daemon set` - A kind that ensures a set of nodes always have an instance of some pod running.

 * `{bm} replica/(pod replica|replica)/i` - A pod under a replica set, deployment, or stateful set. Replicas typically created using the replica set, deployment, or stateful set's pod template.

 * `{bm} job` - A kind that launches as a pod to perform some one-off task.

 * `{bm} cron job` - A kind that launches jobs on a repeating schedule.

 * `{bm} configuration map/(config map|configuration map)/i` - A kind for configuring the containers running in a pod.

 * `{bm} secret` - A kind for security-related configurations of the containers running in a pod.

 * `{bm} millicpu/(millicpu|millicore)/i` - A millicpu is 0.001 CPU cores (e.g. 1000 millicpu = 1 core).

 * `{bm} persistent volume` - A kind that represents non-ephemeral disk space.

 * `{bm} persistent volume claim` - A kind that claims a persistent volume, essentially acting as a marker that the persistent volume is claimed and ready to use by containers within the cluster.

 * `{bm} governing service` - A headless service for a stateful set that lets the pods of that stateful set to discover each other (peer discovery).

 * `{bm} control plane` - The distributed software that controls and makes up the functionality of a Kubernetes cluster, including the API server and scheduler used for assigning pods to worker nodes.

 * `{bm} controller` - Software that implements a control loop. Kinds such as pods, stateful sets, nodes, etc.. all have controllers backing them. Custom controllers can be written and deployed by for user-defined kinds as well.

 * `{bm} service account` - A kind used for authenticating pods with the control plane.

 * `{bm} role-based access control/(role[-\s]based access control)/i` `{bm} /(RBAC)/` - The default security mechanism in Kubernetes, which uses roles to limit what users (and service accounts) can access via the Kubernetes API.

 * `{bm} role/(cluster role|role)/i` - A kind specific to RBAC that defines a set of permissions.

 * `{bm} role binding/(role binding|cluster role binding)/i` - A kind specific to RBAC that binds a role to a set of users, groups, and / or service accounts.

* `{bm} horizontal pod autoscaler/(horizontal pod autoscaler|horizontal pod autoscaling)/i` `{bm} /\b(HPA)s?\b//false/true` - A kind that automatically scales the number of replicas in a deployment, stateful set, or replica set based on how much load existing replicas are under.

 * `{bm} vertical pod autoscaler/(vertical pod autoscaler|vertical pod autoscaling)/i` `{bm} /\b(VPA)s?\b//false/true` - A kind that automatically scales the resource requirements for some pod based on how much load existing replicas are under.

 * `{bm} cluster autoscaler/(cluster autoscaler|cluster autoscaling)/i` - A component that automatically scales the number of nodes in a cluster based on need.

 * `{bm} pod disruption budget` `{bm} /\b(PDB)s?\b//false/true` - A kind that defines the minimum number of available pods / maximum number of unavailable pods can be during a cluster resizing event (e.g. when cluster autoscaler is scaling up or down nodes).

 * `{bm} node selector` - A property of pods that forces them to be scheduled on a specific set of nodes.

 * `{bm} node affinity` - A property of pods that attracts them to or repels them from a set of nodes, either as a preference or as a hard requirement.

 * `{bm} node taint/(node taint|taint)/i` - A property of nodes that repels a set of pods, either as a preference or as a hard requirement.

 * `{bm} pod toleration/(pod toleration|toleration)/i` - A property of pods that defines a set of acceptable node taints, where those pods are allowed to be scheduled on nodes with those taints.

 * `{bm} pod affinity/(pod affinity|pod anti-affinity)/i` - A property of pods that attracts them to or repels them from the vicinity of other pods (e.g. pods on the same node, same rack, etc..), either as a preference or as a hard requirement.

 * `{bm} topology key` - A label placed on nodes that defines their vicinity. For example, nodes can define which rack they're on via a label with the key `rack`, where the value would be the same for all nodes on the same rack (e.g. nodes on rack 15 would have the label `rack=15`, nodes on rack 16 would have the label `rack=16`, etc..).

 * `{bm} image pull secret` - A special type of secret used for storing the credentials of a private container registry.

 * `{bm} container network interface/(container network interface|container networking interface|network plugin)/i` `{bm} /\b(CNI)s?\b//false/true` - A Kubernetes plugin responsible for inserting a network interface into the container (e.g. virtual ethernet) and making necessary changes on the node to bridge that network interface to the rest of the cluster.

 * `{bm} network policy/(network policy|network policies)/i` - A kind that restricts how pods can communicate with each other and with other network entities.

 * `{bm} namespace-level kind/(namespace-level kind|namespace-level object)/i` - A kind that comes under the umbrella of a namespace (e.g. service, pod, config map, etc..).

 * `{bm} cluster-level kind/(cluster-level kind|cluster-level object)/i` - A kind is one that comes under the umbrella of the entire cluster rather than a specific namespace (e.g. node, persistent volume, etc...).

 * `{bm} custom resource definition` `{bm} /\b(CRD)s?\b//false/true` - A kind that defines another user-defined kind.

 * `{bm} init container` - A container within a pod that performs initialization tasks for that pod (e.g. writing some files required by the main containers to run).

 * `{bm} sidecar container/(sidecar container|sidecar)/i` - A container within a pod that performs helper tasks for the other more important containers in that pod (e.g. collecting application logs and sending them to a database).

 * `{bm} custom metrics adapter/(custom metrics? adapter)/i` - A pod (or pod replicas) that accesses some other pod's metrics via a shared resource (e.g. shared volume) and places it into Kubernetes via CRDs for the purpose of scaling replicas via an HPA.

 * `{bm} Helm` - A tool to define, install, and upgrade applications on Kubernetes. Similar to a package manager for Linux distributions (e.g. apt is used to install, upgrade, and remove software on Ubuntu).

 * `{bm} chart` - A set of files that instructs Helm on how to install, manage, and upgrade some application(s). Each chart is comprised of a set of configurations, templated manifests, and dependencies to other charts.

 * `{bm} chart repository/(chart repository|chart repositories)/i` - A server that stores and distributes charts.

`{bm-ignore} !!([\w\-]+?)!!/i`

`{bm-error} Did you mean endpoints?/(endpoint)/i`

`{bm-error} Did you mean sidecar?/(side-car|side car)/i`

`{bm-error} Use the proper version (e.g. DaemonSet should be Daemon set)/(ConfigMap|ReplicaSetStatefulSet|CronJob|ServiceAccount)/`

`{bm-error} Missing topic reference/(_TOPIC)/i`