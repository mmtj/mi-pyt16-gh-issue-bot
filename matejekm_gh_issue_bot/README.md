# matejekm-github-issue-bot
Yet Another GitHub Issue Bot.

Disclaimer: Use at own risk as it could drink all your milk, ride your motorcycle or make your computer explode :-)

## Why?
Because we can. Also written for MI-PYT course at CTU in Prague.

## What is it's goal?
This is simple GitHub issue bot which labels unlabeled issues based on regular expression-based rules.

## How does it work?
Bot search patterns in title or issue body.

## How do I use it?
Just add webhook to URL below and bot will take care of the rest.

Example:

    http://<sample.domain>/hook

## Current default rules
So far bot use these regular expressions:

    bug|BUG -> bug
    feature|FEATURE -> enhancement

Defaulting to label `unconfirmed` when no rules apply.

You can override these rules by your custom `rules` files. See `rules.sample` for details.

## Sample config files

Create your own config files based on sample config files

### auth.cfg

    [github]
    token = xxxxxxxxx
    repo = user/repo

### settings.cfg

    [general]
    sleep = 30
    debug = False

### rules

	[labels]
	bug=bug|BUG
	enhancement=feature|FEATURE

	[default]
	label=unconfirmed

### flask.cfg

	[hook]
	base_url=sample.domain
