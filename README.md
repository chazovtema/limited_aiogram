# What is it?

Limited aiogram is an add-on for the original aiogram Bot. This package allows you to limit how often your bot sends messages

# Telegram api limits

Telegram has a number of restrictions for sending messages:

- 30 messages per second to multiple users
- 20 requests/sec to group
- 1 message per second to individual chat

# Main Features

The following restrictions are currently implemented:

- Limit 30 requests per second for all users
-  1 message/sec to individual chats

# Usage

The code below patches the original Bot class from aiogram, these changes are not reversible!
```python
import limit_aiogram
limit_aiogram.path_bot()
```
It is also possible to use a separate class `LimitedBot``, without changing the original class

```python
import limit_aiogram
bot = limit_aiogram.LimitedBot('your token')
```

# Work in progress

A restriction for sending messages to groups will be added soon
