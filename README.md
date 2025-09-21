# Discord QOTD Bot

This is a bot for managing a "Question of the Day" (QOTD) system on Discord (a social media app).  
The bot allows authorized users to set daily questions with images, track user scores, and manage question announcements.  
It's designed for educational "servers" (groups on Discord) where moderators can post daily challenges and track member participation and performance.

I made this bot in September 2021 and deployed it with Replit. Now (2025) I am uploading the code on Github.

**Warning:** This code is very old and not updated. There have since been changes to the Discord API and maybe to the `discord.py` library. This will probably not work now.

# Bot Framework
- **Discord.py**: This library provides command extensions for handling Discord interactions. 
E.g. Words starting with prefix `-` can be made commands.

- **Permissions**: Role-based access control using "qotd creator" role for administrative commands.

## Features
- **Score Management**: Track user scores and reset functionality for new questions
- **Track attempts**: Keeps track of the number of times a person has attempted a problem and scores them accordingly.
- **Reset score**: Bulk operation where all users' scores can be reset after the end of one season of QOTDs.

# Architecture

## Data Storage
- **Primary Database**: MongoDB cluster hosted on MongoDB Atlas
Direct MongoDB connection using *pymongo* driver
- **Structure**: Simple table storing user IDs, scores, and attempt counts.
- **JSON** file (temp.json) is used to store current QOTD image link and answer.

## Deployment
- **Keep-Alive Service**: Creates a web server with Flask running on port 8080 to maintain bot uptime.  
- **Threading**: The `run()` function is run inside a new thread so that the web server can run parallely to the bot without blocking it.
- **Environment Configuration**: Passwords are secured through environment variables rather than hardcoding.  
# External Dependencies

## Database Services
- **MongoDB Atlas**: Cloud-hosted MongoDB cluster for persistent data storage

## Discord Integration
- **Discord API**: Full bot intents for comprehensive server access
- **CDN**: Discord's CDN for storing and serving QOTD images

## Hosting Infrastructure
- **Flask**: Lightweight web server for keep-alive functionality
- **Threading**: Python threading for concurrent web service operation

## Development Libraries
- **discord.py**: Discord bot framework and API wrapper.
- **pymongo**: MongoDB driver for database operations.
- **flask**: To create a web server.