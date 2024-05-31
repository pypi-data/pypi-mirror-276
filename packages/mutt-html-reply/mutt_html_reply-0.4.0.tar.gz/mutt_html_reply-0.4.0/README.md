## mutt-html-reply

Create an Outlook-style HTML reply

This utility is meant to fill a gap in neomutt functionality when it comes to dealing with HTML emails. In a corporate email environment, most people use Microsoft Outlook, which uses HTML by default, and includes the original message along with some header information.

This tool can be used as part of neomutt custom keybinds to easily craft a response as you might using Outlook.

## Installation

```
pip install mutt-html-reply
```

## Usage

This command is meant to be embedded in a neomutt macro when replying, but can also be used as a standalone program. The original message ("-m" flag) must be a file. The reply and output can either come from a file or stdin/stdout.

```
mutt-html-reply [-h] [-m [MESSAGE]] [-r REPLY] [-o [OUTPUT]]
```
