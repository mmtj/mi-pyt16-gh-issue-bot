# mi-pyt16-github-issue-bot
Yet Another GitHub Issue Bot

## Why?
Primary written for MI-PYT course at CTU in Prague.

## What is it's goal?
This is simple GitHub issue bot which labels unlabeled issues based on regular expression-based rules.

## How do I use it?
Just add webhook to URL below and bot will take care of the rest.

Example:

    http://<sample.domain>/hook

## Current rules
So far bot use these regular expressions:

    bug|BUG -> bug
    feature|FEATURE -> enhancement

Defaulting to label `unconfirmed` when no rules apply.
