#### To deploy the service: follow the next steps or see CI/CD pipeline in the `.github` folder

1. Launch and create an app on your `fly.io` account or organization 
2. Install dependencies
```python
python -m pip install --upgrade pip
pip install --upgrade pip setuptools wheel
pip install "mlem[streamlit,flyio]"
pip install -r requirements.txt
```
3. Build dockerdir via command: 
```python
mlem build docker_dir -m ./models/price_keras_preprocess --target dockerdir --file_conf server=server.mlem
```
4. Deploy to `fly.io`
```sh
$ flyctl deploy --remote-only -a art-expert-excited-newbeez
```
5. Scale service's memory
```sh
$ flyctl scale memory 2048
```
