
## Docker

### Build Base Image

```bash
docker -H tcp://192.168.2.10:2375 build -t todify-base:0.1 -f Dockerfile.base .
```

### Build Image
```bash
docker -H tcp://192.168.2.10:2375 build -t todify:0.1 .
```