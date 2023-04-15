#### [Link](https://t.me/newbeezzz_bot) to Telegram bot
#### Workflow our Telegram bot 
![Figma diagram](https://cdn.discordapp.com/attachments/1094920487450198046/1096731641952612502/image.png)

#### To deploy the service: follow the next steps or see CI/CD pipeline in the `.github` folder

1. Launch and create an app on your `fly.io` account or organization 
2. Install dependencies
```python
python -m pip install --upgrade pip
pip install -r requirements.txt
```
3. Set up your telegram token
```sh
$ flyctl secrets set TELEGRAM_TOKEN=`$your_token_value`
```
4. Deploy to `fly.io`
```sh
$ flyctl deploy --remote-only -a art-expert-excited-newbeez-bot
```
5. Scale service's memory
```sh
$ flyctl scale memory 512
```
