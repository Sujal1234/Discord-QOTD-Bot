# Overview

This is a Discord bot for managing a "Question of the Day" (QOTD) system. The bot allows authorized users to set daily questions with images, track user scores, and manage question announcements. It's designed for educational servers where moderators can post daily challenges and track member participation and performance.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework
- **Discord.py**: Uses the discord.py library with command extensions for handling Discord interactions
- **Command Prefix**: Uses "-" as the command prefix for bot commands
- **Permissions**: Role-based access control using "qotd creator" role for administrative commands

## Data Storage
- **Primary Database**: MongoDB cluster hosted on MongoDB Atlas
- **Connection**: Direct MongoDB connection using pymongo driver
- **Schema**: Simple document structure storing user IDs, scores, and attempt counts
- **Temporary Storage**: JSON file (temp.json) for storing current QOTD image links and answers

## Core Features
- **Score Management**: Track user scores and reset functionality for new questions
- **Image Handling**: Support for Discord image attachments as QOTD content
- **User Tracking**: Automatic attempt tracking when new questions are set
- **Bulk Operations**: Mass score resets and user attempt updates

## Service Architecture
- **Keep-Alive Service**: Flask web server running on port 8080 to maintain bot uptime
- **Threading**: Separate thread for the keep-alive web service to prevent blocking
- **Environment Configuration**: Secure credential management through environment variables

# External Dependencies

## Database Services
- **MongoDB Atlas**: Cloud-hosted MongoDB cluster for persistent data storage
- **Connection String**: Multi-shard cluster configuration for high availability

## Discord Integration
- **Discord API**: Full bot intents for comprehensive server access
- **Image CDN**: Discord's CDN for storing and serving QOTD images

## Hosting Infrastructure
- **Flask**: Lightweight web server for keep-alive functionality
- **Threading**: Python threading for concurrent web service operation

## Development Libraries
- **discord.py**: Discord bot framework and API wrapper
- **pymongo**: MongoDB driver for database operations
- **flask**: Web framework for keep-alive service