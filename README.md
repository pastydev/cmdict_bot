# `cmdict_bot`: cmdict as Telegram bot

[![Deploy Bot in Heroku](https://github.com/pasty-dev/cmdict_bot/actions/workflows/deploy.yml/badge.svg)](https://github.com/pasty-dev/cmdict_bot/actions/workflows/deploy.yml)

Send `cmdict_bot` an English word and receive its definitions.

<p align="center">
  <img width="600" src="img/light-demo.png">
</p>

The homepage of `cmdict` is https://github.com/pasty-dev/cmdict.

<details><summary>Click to see notes for developers.</summary>
<p>

To fix Python version:

```sh
$ pyenv local 3.8.13

$ poetry config virtualenvs.in-project true

$ poetry env use $(pyenv which python)
```

To export `requirements.txt` using `Poetry`:

```sh
$ poetry export -f requirements.txt --output requirements.txt --without-hashes
```

To enable `Heroku` worker:

```sh
$ heroku ps:scale worker=1 -a cmdict
```

</p>
</details>
