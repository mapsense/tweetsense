## Tweetsense

Tweetsense is a Heroku application for streaming live Twitter data to Mapsense. Using Mapsense's innovative geodata analysis tools, anyone can slice and dice Twitter data like a trained data analyst. 

Before you get started, make sure you have a Mapsense API key with the 'api' scope, as well as some Twitter credentials.

When you're ready, start up your own Tweetsense instance by hitting the button:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

After the application has booted, you'll need to scale up some Tweetsense workers using the Heroku dashboard. Alternatively, you may use the CLI to start up a single (free) worker dyno:

```bash
heroku ps:scale worker=1 --app {your-tweetsense-heroku-app}
```

Be aware that free Heroku dynos must sleep for a few hours each day, so to get the most of your Tweetsense deployment, make sure to use a Hobby ($7/month) dyno or better.

### Common Issues

- **I set everything up, but my universe didn't get created.** Make sure the Mapsense API key has the 'api' scope, or Tweetsense will be unable to create universes or push data.
- **Something went wrong, how do I debug the application?** You can use the Heroku CLI to tail Tweetsense's error logs with `heroku logs --tail --app {your-tweetsense-app}`.

For general help and support, feel free to e-mail us at support@mapsense.co.
