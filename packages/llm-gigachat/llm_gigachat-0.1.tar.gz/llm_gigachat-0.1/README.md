# LLM-GigaChat

This is a plugin for [llm CLI utility](https://github.com/simonw/llm) which allows to use [GigaChat](https://github.com/ai-forever/gigachat) model.

## Installation

First, make sure that you have `llm` installed , using `pip`:

```
pip install llm
```

Then install the plugin

```
llm install llm-gigachat
```

## Getting started

Set your GigaChat API key like this:

```
llm keys set gigachat
```

Now that you've saved a key you can run a prompt like this:

```
llm -m gigachat "What is your name?"
```

I also find it useful to use alias `g` instead of `gigachat`. You can set it with

```
llm aliases set g gigachat
```

You can also see you logs in `llm logs path`