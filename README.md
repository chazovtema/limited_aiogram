# What is it?

Limited aiogram is an add-on for the original aiogram Bot. This package allows you to limit how often your bot sends messages

# Telegram api limits

Telegram has a number of restrictions for sending messages:

- 30 messages per second to multiple users
- 20 requests/sec to group
- 1 message per second to individual chat

# Installation

`pip install limited_aiogram`

# Usage

The code below patches the original Bot class from aiogram, these changes are not reversible!
```python
import limited_aiogram
limited_aiogram.patch_bot()
```
It is also possible to use a separate class `LimitedBot`, without changing the original class

```python
import limited_aiogram
bot = limited_aiogram.LimitedBot('your token')
```
