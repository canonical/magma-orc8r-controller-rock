# Contributing

## Build and deploy

```bash
rockcraft pack -v
sudo skopeo --insecure-policy copy oci-archive:magma-orc8r-controller_1.6.1_amd64.rock docker-daemon:magma-orc8r-controller:1.6.1
docker run magma-orc8r-controller:1.6.1
```
