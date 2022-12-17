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

Kubernetes breaks down its orchestration as a set of objects. Each object is of a specific type, referred to as kind. The main kinds are ...

 * Node: A physical worker machine that runs containers.
 * Pod: A set of containers tightly coupled to run in unison on a single node.
 * Volume: A storage mechanism that lets pods persist and / or share data.
 * Service: A load balancer that routes traffic to pods.
 * Configuration Map - A configuration mechanism for applications running within pods (non-security related configurations).
 * Secret - A security configuration mechanism for applications running within pods (e.g. passwords as certificates).
 * Ingress - A access point in which traffic comes in from the outside world to the internal Kubernetes network.

Of these kinds, the two main ones are nodes and pods. Nodes, pods, and other important kinds are discussed in this document.

```{note}
The terminology here is a bit wishy-washy. Some places call them kinds, other places call them resources, other places call them classes, and yet other places call them straight-up objects (in this case, they mean kind but they're saying object). None of it seems consistent, which is why it's been difficult piecing together how Kubernetes works.

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

Kubernetes uses labels to orchestrate. Labels allow objects to have loosely-coupled linkages to each other as opposed to tightly-coupled parent-child / hierarchy relationships. For example, a load balancer decides which pods it routes requests to by searching for pods using label selector.

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

The following sub-sections gives a overview of kinds and example manifests. All manifests, regardless of the kind, require the following fields ...

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

In addition, the `metadata.labels` and `metadata.annotations` manifest paths contain the object's labels and annotations (respective).

## Pod

`{bm} /(Kinds\/Pod)_TOPIC/i`

Containers are deployed in Kubernetes via pods. A pod is is a set of containers grouped together, often containers that are tightly coupled and / or are required to work in close proximity of each other (e.g. on the same host).

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

Containers within a pod are isolated in terms of their resource requirements (e.g. CPU, memory, and disk), but they share the same ...

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

Each container within a pod must have an image associated with. Images are specified in the Docker image specification format, where a name and a tag are separated by a colon (e.g. `my-image:1.0.1`).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container1
      image: my-image:1.0.1
    - name: my-container2
      image: my-image:2.4
```

#### Pull Policy

`{bm} /(Kinds\/Pod\/Images\/Pull Policy)_TOPIC/`

Each container in a pod has to reference an image to use. How Kubernetes loads a container's image is dependent on that container's image pull policy.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image:1.0.1
      imagePullPolicy: IfNotPresent  # Only download if the image isn't present
```

A value of ...

 * `IfNotPresent` only downloads the image if its not already locally present on the node.
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
      image: my-registry.example/tiger/my-container:1.0.1  # Image references registry.
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
      image: my-image:1.0.1
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
      image: my-image:1.0.1
      ports:
        - containerPort: 8080
          name: http
          protocol: TCP
```

The example above exposes port 8080 to the rest of the cluster (not to the outside world). Even with the port exposed, other entities on the cluster don't have a built-in way to discover the pod's IP / host or the fact that it has this specific port open. For that, services are required.

```{seealso}
Kinds/Service_TOPIC (Exposing pods to the outside world)
```

A pod can have many containers within it, and since all containers within a pod share the same IP, the ports exposed by those containers can't conflict. For example, only one container within the pod expose port 8080.

### Command-line Arguments

`{bm} /(Kinds\/Pod\/Command-line Arguments)_TOPIC/`

An image typically provides a default entrypoint (process that gets started) and default set of arguments to run with. Each container within a pod can override these defaults.

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
      image: my-image:1.0.1
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
      image: my-image:1.0.1
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
         image: my-image:1.0.1
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

   In certain cases, you may want to map all entries within a config map directly as a set of environment variables. This is useful when many entries of a config map are required for configuration, so many that becomes tedious and error-prone to map them all to environment variables by hand.
   
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-pod
   spec:
     containers:
       - name: my-container
         image: my-image:1.0.1
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
         image: my-image:1.0.1
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
         image: my-image:1.0.1
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
         image: my-image:1.0.1
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
         image: my-image:1.0.1
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
         image: my-image:1.0.1
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
         image: my-image:1.0.1
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
For individual files/directories mounted from a volume, one workaround to receiving updates is to use symlinks. Essentially, mount the whole volume to path that doesn't conflict with an existing path in the container. Then, as a part of the container's start-up process, add symlinks to the whole volume mount wherever needed.

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
      image: my-image:1.0.1
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
      image: my-image:1.0.1
      volumeMounts:
        - mountPath: /data
          name: my-data
```

### Probes

`{bm} /(Kinds\/Pod\/Probes)_TOPIC/`

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
      image: my-image:1.0.1
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
  ...
```

In the example above, each of the probes check a HTTP server within the container at port 8080 but at different paths. The field ...

 * `initialDelaySeconds` is the number of seconds to wait before performing the first probe.
 * `timeoutSeconds` is the number of seconds to wait before timing out.
 * `periodSeconds` is the number of seconds to wait before performing a probe.
 * `failureThreshold` is the maximum number of successive failure before Kubernetes considers the probe failed.
 * `successThreshold` is the maximum number of successive successes before Kubernetes considers the probe passed.
 
There are types of probes other than `httpGet`. A probe of type ...

 * `httpGet` will perform an HTTP GET operation to a server on the container and fail it its non-responsive.
 * `tcpSocket` will attempt to connect a TCP socket to the container and  fail if the container doesn't accept.
 * `exec` will run a command on the container and fail if it gets a non-zero exit code.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image:1.0.1
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

### Restart Policy

`{bm} /(Kinds\/Pod\/Restart Policy)_TOPIC/`

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
      image: my-image:1.0.1
```

A value of ...

 * `Always` always restarts the pod regardless of how it exists (default).
 * `OnFailure` only restarts the pod only if it failed execution.
 * `Never` never restarts the pod.

`Always` is typically used when running servers that should always be up (e.g. http server) while the others are typically used for one-off jobs.

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

 * Services outside of the pod's namespace aren't provided.
 * Services added to the namespace after the pod launches won't be picked up (env vars can only be changed prior to the launch of a container process).
 * Services removed from the name after the pod launches won't be picked up (env vars can only be changed prior to the launch of a container process).
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

`{bm} /(Pods\/Metadata Access\/Environment Variables)_TOPIC/`

All pod information except for labels and annotations can be assigned to environment variables. The reason for this is that a running pod can have its labels and annotations updated but the environment variables within a running container can't be updated once that container starts (updated labels / annotations won't show up to the container).

```{note}
CPU resources can also be dynamically updated without restarting the pod / container process. The environment variable for this likely won't update either, but it isn't restricted like labels / annotations are. There may be other reasons that labels / annotations aren't allowed. Maybe Linux has a cap on how large a environment variable can be, and there's a realistic possibility that labels / annotations can exceed that limit?
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

`{bm} /(Pods\/Metadata Access\/Volume Mount)_TOPIC/`

```{prereq}
Pods/Metadata Access/Environment Variables_TOPIC
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

### API Access

`{bm} /(Kinds\/Pod\/API Access)_TOPIC/`

```{prereq}
Kinds/Pod/Service Discovery_TOPIC
Kinds/Pod/Configuration_TOPIC
```

Containers within a pod can access the Kubernetes API server via a service called `kubernetes`, typically found on the default namespace. Communicating with this service requires a certificate check (to verify server isn't a man-in-the-middle box) as well as an access token (to authentication with the service). By default, containers have a secret object mounted as a volume at `/var/run/secrets/kubernetes.io/serviceaccount` that contains both these pieces of data as files:

 * `ca.crt` - certificate used for verifying the server's identity.
 * `token` - bearer token used for authenticating with the server.
 * `namespace` - namespace of the *pod* itself (not the namespace of the `kubernetes` service).

In most cases, the credentials provided likely won't provide unfettered access to the Kubernetes API.

```{note}
See [here](https://stackoverflow.com/a/25843058) for an explanation of bearer tokens. You typically just need to include a HTTP header with the token in it.

Third-party libraries that interface with Kubernetes are available for various languages (e.g. Python, Java, etc..), meaning you don't have to do direct HTTP requests and do things like fiddle with headers.
```

```{seealso}
Kinds/Service Account_TOPIC (Credentials map to a service account)
Kinds/API Security/Disable Credentials_TOPIC (Disable mounting of credentials within pod)
```

## Configuration Map

`{bm} /(Kinds\/Configuration Map)_TOPIC/`

A configuration map is a type of resource comprised of key-value pairs intended to configure the main application of a container (or many containers). By decoupling configurations from the containers themselves, the same configuration map (or parts of it) could be used to configure multiple containers within Kubernetes.

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

The key-value pairs of a configuration map resource typically get exposed to a container either as environment variables, files, or command-line arguments. Keys are limited to certain characters: alphabet, numbers, dashes, underscores, and dots.

## Secret

`{bm} /(Kinds\/Secret)_TOPIC/`

```{prereq}
Kinds/Configuration Map_TOPIC
```

A secret object is a type of resource comprised of key-value pairs, similar to a config map, but oriented towards security rather than just configuration (e.g. for storing things like access tokens, passwords, certificates). As opposed to a config map, Kubernetes takes extra precautions to ensure that a secret object is stored and used in a secure manner.

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

```{prereq}
Kinds/Pod_TOPIC
```

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

## Volume

`{bm} /(Kinds\/Volume)_TOPIC/i`

Volumes are disks where data can be persisted across container restarts. Normally, Kubernetes resets a container's filesystem each time that container restarts (e.g. after a crash or a pod getting moved to a different node). While that works for some types of applications, other application types such as database servers need to retain state across restarts.

Volumes in Kubernetes are broken down into "persistent volumes" and "persistent volume claims". A ...

* persistent volume is the volume itself.
* persistent volume claim is the assignment of a volume.

The idea is that a persistent volume itself is just a floating block of disk space. Only when its claimed does it have an assignment. Pods can then latch on to those assignments.

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
Persistent volumes themselves are cluster-level resources while persistent volume claims are namespace-level resources. All volumes are available for claims regardless of the namespace that claim is in. Maybe you can limit which volumes can be claimed by using labels / label selectors?
```

```{note}
Part of the reasoning for doing it like this is decoupling: volumes are independent from pods and a volume can be have shared access across pods.

Another reasons is that a developer should only be responsible for claiming a volume while the cluster administrator should be responsible for setting up those volumes and dealing with backend details like the specifics of the volume type and how large each volume is. As a developer, you only have to make a "claim" while the administrator is responsible for ensuring those resources exist.
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

Dynamic provisioning only requires that you make a persistent volume claim with a specific `spec.storageClassName`. The administrator is responsible for ensuring a provisioner exists for that storage class and it automatically creates a volume of that type when a claim comes in. Each storage class can have different characteristics such as volume type (e.g. HDD vs SSD), volume read/write speeds, backup policies, etc.

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

The capacity of a persistent volume is set through `spec.capacity.storage`.

```yaml
spec:
  capacity:
    storage: 10Gi
```

A persistent volume claim can then be set to require a specific amount of capacity via `spec.resources.request.storage`. Specifically, `requests` defines the minimum required capacity and `limits` defines the maximum required capacity.

```yaml
spec:
  resources:
    requests:
      storage: 1Gi  # volume must have at least this much space
    limits:
      storage: 5Gi  # volume can't have more than this much space
```

### Access Modes

`{bm} /(Kinds\/Volume\/Access Modes)_TOPIC/i`

A persistent volume can support multiple access modes:

* `ReadWriteOnce` - volume is mountable by a single node in read-write mode.
* `ReadWriteOncePod` - volume is mountable by a single pod in read-write mode.
* `ReadWriteMany` - volume is mountable by many nodes in read-write mode.
* `ReadOnlyMany` - volume is mountable by many nodes in read-only mode.

The available access modes of a persistent volume is set through `spec.accessModes`.

```yaml
spec:
  accessModes:
  - ReadWriteOnce
  - ReadOnlyMany
```

A persistent volume claim can then be set to target on or more access modes.

```yaml
spec:
  accessModes:
  - ReadWriteOnce  # volume must have this access mode
```

```{note}
A claim takes a list of access modes, so is it that a claim needs to get a volume with all access modes present or just one of the access modes present?
```

```{note}
Not all persistent volume types support all access modes. Types are discussed further below.
```

### Reclaim Policy

`{bm} /(Kinds\/Volume\/Reclaim Policy)_TOPIC/i`

A persistent volume claim, once released, may or may not make the persistent volume claimable again depending on what `spec.persistentVolumeReclaimPolicy` was set to.

```yaml
spec:
  persistentVolumeReclaimPolicy: Recycle 
```

The options available are ...

* `Retain` - keep all existing data on the persistent volume and prevent a new persistent volume claim from claiming it again.
* `Recycle` - delete all existing data on the persistent volume and allow a new persistent volume claim to claim it again.
* `Delete` - delete the persistent volume object itself.

If the data on disk is critical to operations, the option to choose will likely be `Retain`.

```{note}
For retain specifically, once the existing persistent volume claim is released, the persistent volume itself goes into "Released" status. If it were available reclamation, it would go into "Available" status. The book mentions that there is no way to "recycle" a persistent volume that's in "Released" status without destroying and recreating it.

According to the k8s docs, this is the way it is so that users have a chance to manually pull out data considered precious before it gets destroyed.
```

```{note}
Not all persistent volume types support all reclaim policies. Types are discussed further below.
```

### Types

`{bm} /(Kinds\/Volume\/Types)_TOPIC/i`

A persistent volume needs to come from somewhere, either via a cloud provider or using some internally networked (or even local) disks. There are many volume types: AWS elastic block storage, Azure file, Azure Disk, GCE persistent disk, etc.. Each type has its own set of restrictions such as what access modes it supports or the types of nodes it can be mounted.

The configuration for each type is unique and goes directly under `spec`. The following are sample configurations for popular types...

```{note}
The documentation says that a lot of these types are deprecated and being moved over to something called CSI (container storage interface), so these examples may need to be updated in the future
```

```yaml
# Amazon Elastic Block Storage
spec:
  awsElasticBlockStore:
    volumeID: volume-id  # a volume with this ID must already exist in AWS
    fsType: ext4
```

```yaml
# Google Compute Engine Persistent Disk
spec:
  gcePersistentDisk:
    pdName: test-vol  # a disk with this name must already exist in GCE
    fsType: ext4
```

```yaml
# Azure Disk
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
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
reclaimPolicy: Retain
allowVolumeExpansion: true
```

`provisioner` and `parameters` define how persistent volumes are to be created and are unique to each volume type. In the example above, the storage class is named `standard` and it provisions new persistent volumes on AWS. Any persistent volume claim with `spec.storageClassName` set to `standard` will call out to this AWS elastic store provisioner to create a persistent volume of type `awsElasticBlockStore` which gets assigned to it.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-vol-claim
spec:
  resources:
    requests:
      storage: 1Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: standard  # use the storage class described above for this claim
```

If `allowVolumeExpansion` is set to `true`, the persistent volume can be resized by editing the persistent volume claim object. Only some volume types support volume expansion. The example above will work because AWS elastic block store volume types do support volume expansion.

`reclaimPolicy` maps to a persistent volume's `spec.persistentVolumeReclaimPolicy`, except that `Recycle` isn't one of the allowed options: only `Delete` and `Retain` are allowed.If unset, the reclaim policy of a dynamically provisioned persistent volume is `Delete`. The example above overrides the reclaim policy to `Retain`.

```{note}
Since these persistent volumes are being dynamically provisioned, it doesn't make sense to have `Recycle`. You can just `Delete` and if a new claim comes in it'll automatically provision a new volume. It's essentially the same thing as `Recycle`.
```

If a persistent volume claim leaves `spec.storageClassName` unset, the persistent volume claim will use whatever storage class Kubernetes has set as its default. Recall that leaving `spec.storageClassName` unset is *not* the same as leaving it as an empty string. To leave unset means to keep it out of the declaration entirely. If `spec.storageClassName` is ...

* set to an empty string, it tells Kubernetes to find any _existing_ persistent volume for the persistent volume claim.
* set to a non-empty string, it tells Kubernetes to use that storage class to dynamically provision a persistent volume for the persistent volume claim.
* unset, it tells Kubernetes to use the default storage class to dynamically provision a persistent volume for the persistent volume claim.

Most Kubernetes installations have a default storage class available, identified by the storage class having the annotation `storageclass.kubernetes.io/is-default-class=true`.

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

## Endpoints

`{bm} /(Kinds\/Endpoints)_TOPIC/i`

Endpoints (plural) is a kind that simply holds a list of IP addresses and ports. It's used by higher-level kinds to simplify routing. For example, an endpoints resource may direct to all the nodes that make up a sharded database server.

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
Internally, an EndPoints object is used to track pods. When you create a service, Kubernetes automatically creates an accompanying EndPoints object that the service makes use of.
```

### Routing

`{bm} /(Kinds\/Service\/Routing)_TOPIC/i`

```{prereq}
Introduction/Labels_TOPIC
Kinds/Endpoints_TOPIC
```

A service determines which pods it should route traffic to via the `spec.selector` manifest path. This manifest path contains key-value mappings, where these key-value mappings are labels that a pod needs before being considered for this service's traffic ...

```yaml
spec:
  selector:
    key1: value1
    key2: value2
    key3: value3
```

Internally, the service creates and manages an endpoints object containing the IP and port for each pod captured by the selector. If no selectors are present, the service expects an endpoints object with the same name to exist, where that endpoints object contains the list of IP and port pairs that the service should route to.

```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: database  # must be same name as the service
subsets: 
  - addresses:
      - ip: 10.10.1.1
      - ip: 10.10.1.2
      - ip: 10.10.1.3
    ports:
      - port: 5432
```

If no selectors are present but `spec.type` is set to `ExternalName`, the service will route to the host specified in `spec.externalName`. This is useful for situations where you want to hide the destination, such as an external API that you also want to mock for development / testing.

```yaml
spec:
  type: ExternalName
  externalName: api.externalcompany.com
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

A service can listen on multiple ports, controlled via the `spec.ports` manifest path.

```yaml
spec:
  ports:
    - name: webapp-port
      protocol: TCP
      port: 80
      targetPort: 9376
    - name: api-port
      protocol: TCP
      port: 8080
      targetPort: 1111
    ...
```

 * `name` is a friendly name to identify the port (optional)
 * `protocol` is either `TCP` or `UDP` (defaults to `TCP`).
 * `port` is the port that the service listens on.
 * `targetPort` is the port that requests are forwarded to on the pod  (defaults to value set for `port`).

```{note}
Not having a name makes it more difficult for pods to discover a service. Discussed further in the service discovery section.
```

The example above forwards requests on two ports. Requests on port ...

 * 80 of the service get forwarded to port 9376 of a pod assigned to that service.
 * 8080 of the service get forwarded to port 1111 of a pod assigned to that service.

Ports may also reference the names of ports in a pod manifest. For example, imagine the pod manifest for a pod assigned to a service provides names for its ports.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - ...
      ports:
        - containerPort: 8080
          name: my-http-port
          protocol: TCP
      ...
```

In the service for that targets this pod manifest, you can use `my_http_port` as a `targetPort`.

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
      targetPort: my-http-port
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
Kinds/Pod/Probes_TOPIC
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
Recall that, when a service has selectors assigned, Kubernetes internally maintains an EndPoints object that contains the addresses of ready and healthy pods. The addresses in this endpoints object is what the service routes to.
```

### Headless

`{bm} /(Kinds\/Service\/Headless)_TOPIC/i`

```{prereq}
Kinds/Service/Routing_TOPIC
Kinds/Service/Health_TOPIC
```

A service that's headless is one which there is no load balancer forwarding requests to pods / endpoints. Instead, the domain for the service will resolve a list of ready IPs for the pods (or endpoints) that the service is for. 

To create a headless service, set `spec.clusterIP` manifest path to `None`.

```yaml
spec:
  clusterIP: None
```

Generally, headless services shouldn't be used because DNS queries are typically cached by the operating system. If the IPs that a service forwards to change, apps that have recently queried the service's DNS will continue to use the old (cached) set of IPs until the operating system purges its DNS cache.

### Session Affinity

`{bm} /(Kinds\/Service\/Session Affinity)_TOPIC/i`

How a service decides to forward incoming requests to the pod instances assigned to it is controlled via `spec.sessionAffinity` manifest path. Assigning a value of ...

 * `None` forwards each request to a randomly selected pod instance (default behaviour).
 * `ClientIP` forwards each request originating from the same IP to the same pod instance.

When using `ClientIP`, you may also provide a maximum session "sticky time" via the manifest path `spec.sessionAffinityConfig.clientIP.timeoutSeconds`. By default, this value is set to 108300 (around 3 hours).

```yaml
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10000
```

```{note}
When using `ClientIP`? What happens when the service runs out memory to track client IPs? LRU algorithm to decide which to keep / discard?
```

```{note}
The book mentions that because services work on the TCP/UDP level and not at HTTP/HTTPS level, forwarding requests by tracking session cookies isn't a thing.
```

### Exposure

`{bm} /(Kinds\/Service\/Exposure)_TOPIC/i`

The service type defines where and how a service gets exposed, controlled via the `spec.type` manifest path. For example, a service may only be accessible within the cluster, to specific parts of the cluster, to an external network, or to the public Internet.

If not specified, the `spec.type` of a resource is `ClusterIP`, meaning that it's exposed only locally within the cluster.

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
Internally, a `ClusterIP` service uses kube-proxy to route requests to relevant pods (EndPoints).
```

```yaml
spec:
  type: ClusterIP
```

#### Node Port

`{bm} /(Kinds\/Service\/Exposure\/Node Port)_TOPIC/i`

Services of type `NodePort` are accessible from outside the cluster. Every worker node opens a port (either user-defined or assigned by the system) that routes requests to the service. Since nodes are transient, there is no single point of access to the service.

When `NodePort` is used as the type, the manifest path `spec.ports[].nodePort` defines the port on the worker node to open.

```yaml
spec:
  type: NodePort
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
      nodePort: 8080
    ...
```

#### Load Balancer

`{bm} /(Kinds\/Service\/Exposure\/Load Balancer)_TOPIC/i`

Services of type `LoadBalancer` are accessible from outside the cluster. When the `LoadBalancer` type is used, the cloud provider running the cluster assigns their version of a load balancer to route external HTTP requests to the Kubernetes Ingress component. Ingress then determines what service that request should be routed to based on details within the HTTP parameters (e.g. Host).

There is no built-in Kubernetes implementation of Ingress. Kubernetes provides the interface but someone must provide the implementation, called an Ingress controller, for the functionality to be there. The reason for this is that load balancers come in multiple forms: software load balancers, cloud provider load balancers, and hardware load balancers. When used directly, each has a unique way it needs to be configured, but the Ingress implementation abstracts that out.

```yaml
spec:
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
      nodePort: 8080
    ...
```

Once provisioned, the object will have the manifest path `status.loadBalancer.ingress.ip[]` added to it, which states the IP of the load balancer forwarding requests to this service.

```yaml
spec:
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
      nodePort: 8080
    ...
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

Similar to a service of type `LoadBalancer`, An Ingress object is a load balancer with a publicly exposed IP. However, rather than load balancing at the TCP/UDP level, an Ingress object acts as a load balancing HTTP proxy server. An HTTP request coming into an Ingress object gets routed to one of many existing services based on host and path HTTP headers. This is useful because the cluster can expose several services under a single public IP address.

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
According to the book, most if not all implementations of Ingress simply query the service for its endpoints and directly load balance across them vs forwarding the request through that service. Note that the port in the example above is still the port that the *service* is listening on, not the port of the pod is listening on.
```

### Hosts

`{bm} /(Kinds\/Ingress\/Hosts)_TOPIC/i`

The host in each rule can be either an exact host or it could contain wildcards (e.g. `*.api.myhost.com`). Each name in the host (split by dot) intended for a wildcard should explicitly have an asterisk in its place. The portion the asterisk is in must exist and it only covers that name. For example, the rule below will match `ONE.api.myhost.com`, but not `TWO.THREE.api.myhost.com` or `api.myhost.com`.

```yaml
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

 * `Exact` - Matches the URL path exactly (case sensitive).
 * `Prefix` - Matches the URL path prefix (case sensitive).
 * `ImplementationSpecific` - Based on the class of the Ingress resource.

```yaml
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
What about `ImplementationSpecific`? There are different types of Ingress controllers, each of which has its own configuration options. An Ingress class is something you can put into your Ingress resource that contains "configuration including the name of the controller that should implement the class." It seems like an advanced topic and I don't know enough to write about it. Probably not something you have to pat attention to if you're doing basic cloud stuff.
```

### TLS Traffic

`{bm} /(Kinds\/Ingress\/TLS Traffic)_TOPIC/i`

```{prereq}
Kinds/Pod/Configuration_TOPIC
```

Assuming you have a TLS certificate and key files for the host configured on the Ingress resource, you can add those into Kubernetes as a secret and configure the Ingress resource to make use of it.

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

For each certificate secret intended to be used by the Ingress resource, there should be an array entry under the `spec.tls[]` manifest path. The certificate secret name must be placed under `secretName` and the domain(s) supported by that certificate must be listed under `hosts`. Hosts must match hosts explicitly listed un the Ingress resource's rules.

```yaml
spec:
  tls:
    - hosts:
        - api.myhost.com
      secretName: my-api-tls
    - hosts:
        - stats.myhost.com
      secretName: my-stats-tls
```

Once an encrypted request comes in to the Ingress controller, it's decrypted. That decrypted request then gets forwarded to the service it was intended for.

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

A namespace is a kind used to avoid resource naming conflicts. For example, it's typical for a Kubernetes cluster to be split up into development, testing, and production namespaces. Each namespace can have resources with the same names as those in the other two namespaces.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
```

Namespaces are cluster-level resources. This is contrary to most other resource types in Kubernetes, which are namespace-level resources, meaning that a namespace can be used to disambiguate resources of that type with the same name...

```yaml
# These are namespace-level resources
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

If a namespace-level resource doesn't set a namespace, the namespace defaults to `default`.

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

Recall that, to link objects together, Kubernetes uses loosely coupled linkages via labels rather than hierarchial parent-child relationships. As such, the pod template should have a unique set of labels assigned that the replica set can look for to determine how many instances are running. Regardless of how those instances were launched (via the replica set or something else), the replica set will account for them. In the example above, the replica set determines pod instances it's responsible for by looking for the label named `app` and ensuring its set to `my-app`.

```{note}
According to the k8s docs, it may be a parent-child relationship. Apparently looking for labels is just a initial step to permanently bringing pods under the control of a specific replica set:

> A ReplicaSet is linked to its Pods via the Pods' metadata.ownerReferences field, which specifies what resource the current object is owned by. All Pods acquired by a ReplicaSet have their owning ReplicaSet's identifying information within their ownerReferences field. It's through this link that the ReplicaSet knows of the state of the Pods it is maintaining and plans accordingly.

What happens when two replica sets try "owning" the same pod?
```

A replica set's job is to ensure that a certain number of copies of a pod template are running. It won't retain state between its copies or do any advanced orchestration. Specifically, a replica set ...

 * won't retain pod IPs / hostnames across time. Each launched pod will have its own unique IP / hostname, even if it's replacing a downed pod (it won't inherit that downed pod's IP / hostname). 
 * will force all pods to use a single persistent volume claim (if one was specified in the pod template), meaning all pods will use a single volume. For horizontally scalable applications (e.g. microservices, databases, etc..), each running instance of an application typically needs its own persistent storage.

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
The same gotchas with replica sets also apply to deployments: all pods will use the same persistent volume claim and IPs / hosts aren't retained when pods are replaced.

Like with replica set, you might have to use `--cascade=false` in `kubectl` if you don't want the pods created by the deployment to get deleted as well (unsure about this).
```

```{seealso}
Kinds/Stateful Set_TOPIC (Like replica sets but supports individual persistent volume claims)
```

### Updates

`{bm} /(Kinds\/Deployment\/Updates)_TOPIC/i`

```{prereq}
Kinds/Pod/Probes_TOPIC
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

You can a rollback via `kubectl rollout undo deployments my-deployment --to-revision=12345`.
```

## Stateful Set

`{bm} /(Kinds\/Stateful Set)_TOPIC/i`

```{prereq}
Kinds/Replica Set_TOPIC
Kinds/Deployment_TOPIC
Kinds/Volume_TOPIC
Kinds/Service/Headless_TOPIC
```

A stateful set is similar to a deployment but the pods it creates are guaranteed to have a stable identity and each pod is able to have its own dedicated storage volumes. In the context of stateful sets, ...

 * stable identity means that if a pod goes down, the stateful set responsible for it will replace it with a new pod has the exact same identification information (same name, IP, etc..). Contrast that to deployments, where replacement pods have completely new identities.
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
  # key-value pairs used for pod template labels of the the stateful set further down.
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

A stateful set will not proceed with scaling until all preceding pods (ordinal suffix) are in a healthy running state. The reason for this is that, if a pod is unhealthy and the stateful set gets scaled down, it's effectively lost two members at once. This goes against the "only one pod can go down at a time" stateful set scaling behavior.

For example, given the same 3 replica `my-stateful-set` example above, scaling down to 1 replica will first shut down pod `my-stateful-set-2` and then pod `my-stateful-set-1`. If `my-stateful-set-2` shuts down but then `my-stateful-set-0` enters into an unhealthy state, `my-stateful-set-1` won't shut down until `my-stateful-set-0` recovers. Likewise, if `my-stateful-set-0` enters into an an unknown state (e.g. the node running it temporarily lost communication with the control plane), `my-stateful-set-1` won't shut down until `my-stateful-set-0` is known and healthy.

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

`OnDelete` is simple but requires user intervention to shutdown pods. `RollingUpdate` is similar to the `RollingUpdate` strategy for deployments, but it supports less parameters and its behavior is slightly different. Specifically, rolling updates for stateful sets support two parameters.

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
Deployments also supported the rolling update parameter `minReadySeconds`. There's a similar feature for stateful sets but it goes under the path `spec.minReadySeconds` (it isn't specific to rolling updates).
```

Rolling updates performed with a pod management policy of `OrderedReady` (the default) may get into a broken state which requires manual intervention to roll back. If an update results in a pod entering into an unhealthy state, the rolling update will pause. Reverting the pod template won't work because it goes against the "only one pod can go down at a time" behavior of stateful sets.

```{seealso}
Kinds/Stateful Set/Scaling_TOPIC (Discussion of pod management policy and only one pod can go down at a time" behavior)
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
Kinds/Pod/Restart Policy_TOPIC
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

The example job attempts to runs 10 pods to successful completion, keeping up to 5 concurrently running at any one time. If a pod fails, the job will retry it up to 4 times before failing the job entirely. Similarly, the job itself runs no more than 99 seconds before failing entirely.

Common gotchas with jobs:

 * *Lingering finished jobs*: By default, neither a job nor its pods are cleaned up after the job ends (regardless of success or failure). This can end up cluttering the Kubernetes servers.

   ```{seealso}
   Kinds/Job/Cleanup (Job cleanup strategies)
   ```

 * *No communication between pods*: By default, a job will automatically pick pod labels and set its label selectors so as not to conflict with other pods in the system. Without consistent labels, the pods of a job can't communicate with each other.

   ```{seealso}
   Kinds/Job/User-defined Labels (Job cleanup strategies)
   ```

 * *Unexpected concurrency*: Even if `spec.concurrency` and `spec.completions` are both set to 1, there are cases where a job may launch more than once. As such, a job's pods should be tolerant of concurrency.

 * *`activeDeadlineSeconds` confusion*: There's an `activeDeadlineSeconds` that can go in the pod template as well which is different from the job's `activeDeadlineSeconds`. Don't confuse the two.

### Cleanup

`{bm} /(Kinds\/Job\/Cleanup)_TOPIC/i`

One common problem with jobs is resource cleanup. With the exception of failed pods that have been retried (`spec.backoffLimit`), a completed job won't delete its pods by default. Those pods are kept around in a non-running state so that their logs can be examined if needed. Likewise, the job itself isn't deleted on completion either.

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

`(bm} /(Kinds\/Job\/User-defined Labels`

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
      image: my-registry.example/tiger/my-container:1.0.1
```

```{seealso}
API Security_TOPIC (Role-based access control to limit a service account's access to the Kubernetes API)
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

The HPA will at-most double the the number of replicas on each iteration. Each scaling iteration has an intentional waiting period. Specifically, scaling ...

 * up will only occur if no previous scaling has occurred in the past 3 mins.
 * down will only occur if no previous scaling has occured in the past 5 mins.

The example above tracked a single metric (CPU utilization), but multiple metrics can be tracked by a single HPA. Metrics can be one of three types:

 * `Resource` metrics cover CPU and memory metrics of the replicas.
 * `Pods` metrics cover other metrics of the replicas (e.g. custom user-defined metrics).
 * `Object` are metrics related to some other object in the same namespace.

```{note}
How do you implement custom user-defined metrics? I would imagine you need to do API calls to the Kubernetes API server (or to the metrics server) from the pod replicas.
```

If there are multiple metrics being tracked by an HPA, as in the example below, that HPA calculates the replica counts for each metric and then chooses the one with the highest.

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

Common gotchas with HPAs:

* *Scale to zero*: Setting the number of minimum replicas to zero isn't supported. See [here](https://github.com/kubernetes/kubernetes/issues/69687).

 * *Scaling memory*: It's easy to autoscale based on CPU, but be careful with autoscaling based on memory. If the number of replicas scale up, the existing replicas need to somehow "release" memory, which can't really be done without killing the pods and starting them back up again.

 * *Scaling on non-linear scaling metrics*: Be careful with scaling based on metrics that don't linearly scale. For example, if you double the number of pods, the value of that metric should cut in half. This may end up becoming an issue when scaling based off of poorly designed custom user-defined metrics.

```{note}
In addition to horizontal pod autoscaler, there's a vertical pod autoscaler (VPA). A VPA will scale a single pod based on metrics and its resource requests / resource limits.

The VPA kind doesn't come built-in with Kubernetes. It's provided as an add-on package found [here](https://github.com/kubernetes/autoscaler).
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
Kinds/Pod Disruption Budget_TOPIC (Prevent rapid killing of pods on scale down)
```

## Pod Disruption Budget

`{bm} /(Kinds\/Pod Disruption Budget)_TOPIC/i`

```{prereq}
Kinds/Cluster Autoscaler_TOPIC
Kinds/Replica Set_TOPIC
Kinds/Deployment_TOPIC
Kinds/Stateful Set_TOPIC
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

> The "intended" number of pods is computed from the .spec.replicas of the workload resource that is managing those pods. The control plane discovers the owning workload resource by examining the .metadata.ownerReferences of the Pod.
```

# Custom Kinds

TODO: write an example python controller here and talk about how to deploy it + ch 18

TODO: write an example python controller here and talk about how to deploy it + ch 18

TODO: write an example python controller here and talk about how to deploy it + ch 18

TODO: write an example python controller here and talk about how to deploy it + ch 18

TODO: write an example python controller here and talk about how to deploy it + ch 18

TODO: write an example python controller here and talk about how to deploy it + ch 18

TODO: write an example python controller here and talk about how to deploy it + ch 18

# API Security

`{bm} /(API Security)_TOPIC/i`

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
API Security/Disable Credentials_TOPIC (Disable volume mounting service account credentials)
```

How access rights are defined depends on how Kubernetes has been set up. By default, Kubernetes is set up to use role-based access control (RBAC), which tightly maps to the REST semantics of the Kubernetes API server. RBAC limits what actions can be performed on which objects: Objects map to REST resources (paths on the REST server) and manipulations of objects map to REST actions (verbs such as `DELETE`, `GET`, `PUT`, etc.. on those REST server paths).

The subsections below detail RBAC as well as other API security related topics.

```{note}
Other types of access control mechanisms exist as well, such as attribute-based access control (ABAC).
```

## Role-based Access Control

`{bm} /(API Security\/Role-based Access Control)_TOPIC/i`

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

`ClusterRole` and `ClusterRoleBinding` are cluster-level kinds while `Role` and `RoleBinding` are namespace-level kinds. RBAC provides provides different permissions based on which role variant (`ClusterRole` vs `Role`) gets used with which role binding variant (`ClusterRoleBinding` vs `RoleBinding`):

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
I suspect that users and groups are cluster-level resources, hence the lack of namespace. Haven't been able to verify this.
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

## Disable Credentials

`{bm} /(API Security\/Disable Credentials)_TOPIC/i`

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
Recall that it's also possible to disable auto-mounting on individual pods. Auto-mounting can't be disabled on individual containers, but it is possible to override the `/var/run/secrets/kubernetes.io/serviceaccount` mount on those containers with something like tmpfs (empty directory).
```

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

```{note}
The option `--from-file` can also point to a directory, in which case an entry will get created for each file in the directory provided that the filenames don't have any disallowed characters.
```

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

 * `{bm} kind/(\bkind)s?\b/i/true/true` - A class of object within Kubernetes (e.g. pod, service, secret, replica set, deployment, etc..).

 * `{bm} object` - An entity orchestrated / managed by Kubernetes, such as a running pod or service.

 * `{bm} manifest` - A declarative configuration (either YAML or JSON) that describes an object. This is effectively a blueprint for an object, similar to how an image is a blueprint for a container.

 * `{bm} image` - An application packaged as an immutable and isolated filesystem. The filesystem typically contains all library dependencies required for the application to run in an isolated and reproducible manner (e.g. library dependencies are the versions expected by the application).

   Images also typically include metadata describing its needs and operational standards (e.g. memory requirements for the application).

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

 * `{bm} master node` - A node responsible for the managing the cluster (control plane).

 * `{bm} worker node` - A node responsible for running application containers.

 * `{bm} pod/\b(pod)s?\b/i/false/true` - A set of containers all bundled together as a single unit, where all containers in that bundle are intended to run on the same node.

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

 * `{bm} endpoints` - A low-level kind that's used to map a service to the pods it routes to. In other words, an endpoints (note the plural) object is an abstraction that references a pod.

 * `{bm} ingress` - A kind that acts as an HTTP-based frontend that routes and load balances incoming external requests to the correct service. This kind is an interface without an implementation, meaning that Kubernetes doesn't have anything built-in to handle ingress. Implementations of this interfaces are referred to as Ingress controllers and are provided by third-parties.

 * `{bm} replica set` - A kind that ensures a certain number of copies of some pod template are running at any time.

 * `{bm} deployment` - A kind that has the same functionality as a replica set but also provides functionality for updating pods to a new version and rolling them back to previous versions.

 * `{bm} stateful set/(stateful set|stable identity)/i` - A kind that has similar functionality to a deployment but also allows its pods to retain a stable identity and dedicated persistent storage.
   
   * Stable identity means that, if a pod dies, it gets replaced with a new pod that has the same identity information (same name, same IP, etc..)
   * Dedicated persistent storage means that each stable identity can have persistent volume claims unique to it (not shared between other pods within the stateful set).

 * `{bm} reconciliation loop` - A loop that continually observes state and attempts to reconcile it to some desired state if it deviates. See declarative configuration.

 * `{bm} daemon set` - A kind that ensures a set of nodes always have an instance of some pod running.

 * `{bm} job` - A kind that launches as a pod to perform some one-off task.

 * `{bm} cron job` - A kind that launches jobs on a repeating schedule.

 * `{bm} configuration map/(config map|configuration map)/i` - A kind for configuring the containers running in a pod.

 * `{bm} secret` - A kind for security-related configurations of the containers running in a pod.

 * `{bm} millicpu/(millicpu|millicore)/i` - A millicpu is 0.001 CPU cores (e.g. 1000 millicpu = 1 core).

 * `{bm} persistent volume` - A kind that represents non-ephemeral disk space.

 * `{bm} persistent volume claim` - A kind that claims a persistent volume, essentially acting as a marker that the persistent volume is claimed and ready to use by containers within the cluster.

 * `{bm} governing service` - A headless service for a stateful set that lets the pods of that stateful set to discover each other (peer discovery).

 * `{bm} control plane` - The distributed software that controls and makes up the functionality of a Kubernetes cluster, including the API server and scheduler used for assigning pods to worker nodes.

 * `{bm} controller` - A piece of software running on the control plane that provides some functionality. This includes doing the work of reconciling observed state to desired state (reconciliation loop) and / or supporting new kinds. Kinds such as pods, stateful sets, nodes, etc.. all have controllers backing them, and custom controllers can be written and deployed by users.

 * `{bm} service account` - A kind used for authenticating pods with the control plane.

 * `{bm} role-based access control/(role[-\s]based access control)/i` `{bm} /(RBAC)/` - The default security mechanism in Kubernetes, which uses roles to limit what users (and service accounts) can access via the Kubernetes API.

 * `{bm} role/(cluster role|role)/i` - A kind specific to RBAC that defines a set of permissions.

 * `{bm} role binding/(role binding|cluster role binding)/i` - A kind specific to RBAC that binds a role to a set of users, groups, and / or service accounts.

* `{bm} horizontal pod autoscaler/(horizontal pod autoscaler|horizontal pod autoscaling)/i` `{bm} /\b(HPA)\b/` - A kind that automatically scales the number of replicas in a deployment, stateful set, or replica set based on how much load existing replicas are under.

 * `{bm} vertical pod autoscaler/(vertical pod autoscaler|vertical pod autoscaling)/i` `{bm} /\b(VPA)\b/` - A kind that automatically scales the resource requirements for some pod based on how much load existing replicas are under.

 * `{bm} cluster autoscaler/(cluster autoscaler|cluster autoscaling)/i` - A component that automatically scales the number of nodes in a cluster based on need.

 * `{bm} pod disruption budget` `{bm} /\b(PDB)\b/` - A kind that defines the minimum number of available pods / maximum number of unavailable pods can be during a cluster resizing event (e.g. when cluster autoscaler is scaling up or down nodes).

`{bm-error} Did you mean endpoints?/(endpoint)/i`

`{bm-error} Use the proper version (e.g. DaemonSet should be Daemon set)/(ConfigMap|ReplicaSetStatefulSet|CronJob|ServiceAccount)/`

`{bm-error} Missing topic reference/(_TOPIC)/i`