# Cloud Deployment

## Image Creation

Proceed to build the image with the following [format](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling):

```bash
LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE:TAG
```

Example of my image build:

```bash
docker build -t asia-southeast1-docker.pkg.dev/winged-yeti-440908-r9/instagram-repo/instagram-collector-job:v1 .
```

Then proceed to push it to Google's Artifact Registry:

```bash
docker push asia-southeast1-docker.pkg.dev/winged-yeti-440908-r9/instagram-repo/instagram-collector-job:v1
```
This is what it looks like in [Google's Artifact Registry](https://cloud.google.com/artifact-registry/docs/overview) (taking over the soon to be deprecated Container Registry) upon completion:

- Repository:

![cloud-repo](/docs/images/cloud-repo.png)

- Image:

![cloud-image](/docs/images/cloud-image.png)

## 