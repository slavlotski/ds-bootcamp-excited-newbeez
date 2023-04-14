####To deploy: use next steps or see CD pipeline in `.github` folder

1. Launch and create an app on your `fly.io` account or organization 
2. Set up your telegram token
```sh
$ flyctl secrets set TELEGRAM_TOKEN=`$your_token_value`
```
3. Deploy to `fly.io`
```sh
$ flyctl deploy --remote-only -a art-expert-excited-newbeez-bot
```
4. Scale service's memory
```sh
$ flyctl scale memory 512
```
