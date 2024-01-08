<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

It's advised that you use `amazon-efs-utils` to deal with EFS, but you aren't forced to use it. You can also use the standard NFS utilities that come with your Linux distro:

```sh
sudo yum -y install nfs-utils
sudo mkdir ./my-efs
sudo mount -t nfs -o rsize=..,wsize=..,... {efs-dns-name}:/ ./my-efs
```

```sh
sudo apt-get -y install nfs-common
sudo mkdir ./my-efs
sudo mount -t nfs -o rsize=..,wsize=..,... {efs-dns-name}:/ ./my-efs
```
</div>

