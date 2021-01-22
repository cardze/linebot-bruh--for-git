# linebot-bruh--for-git
 author : cardze 出品，必屬佳品
 conf/conf.json

```
{
    "Channel_Access_Token": "YOUR OWN CHANNEL'S TOKEN", 
    "Channel_Secret": "YOU OWN CHANNEL'S SECRET",
    "password":"WHATEVER YOU WANT"
}
```

what you need to deploy this CUTE BOT :
  heroku : 
    heroku FREE account : https://signup.heroku.com/
    prepare heroku on your CLI : https://devcenter.heroku.com/articles/heroku-cli
  line :
    step by step official tutorial : https://developers.line.biz/en/docs/messaging-api/building-bot/
    
deploy command:
  first deployment:
    ```
    git init
    heroku login
    heroku create
    git push heroku master
    ```
  every time you update and deploy :
    ```
    git add .
    git commit -am "make it better"
    git push heroku master // or git push -f heroku $(BRANCH_NAME)::master , if you work on different branch
    ```
Enjoy!!
