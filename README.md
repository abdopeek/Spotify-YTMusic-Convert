# Spotify to YouTube Playlist Converter

A web application that seamlessly converts your Spotify playlists into YouTube playlists.

## 🎵 Overview

This tool allows users to convert their favorite Spotify playlists into YouTube playlists with just a few clicks. Perfect for when you want to enjoy your music on YouTube or share playlists with friends who don't use Spotify.

## ✨ Features

- **Simple Conversion**: Convert any Spotify playlist to YouTube with a single click
- **Accurate Matching**: Advanced algorithms to find the best matching YouTube videos
- **Playlist Management**: Create, save, and manage your converted playlists
- **User Authentication**: Secure login with Spotify and YouTube accounts
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- Spotify Developer Account
- YouTube Data API credentials

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/abdopeek/Spotify-YTMusic-Convert.git
   cd Spotify-YTMusic-Convert
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your API keys:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   YOUTUBE_CLIENT_ID=your_youtube_client_id
   YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
   ```

5. Run the Flask application:
   ```bash
   flask run
   ```

6. Open `http://localhost:5000` in your browser

## 📦 Dependencies

```
flask
flask_session
spotipy
google-auth
google-auth-oauthlib
google-api-python-client
```

## 🔧 How It Works

1. **Connect Accounts**: Sign in with your Spotify and YouTube accounts
2. **Select Playlist**: Choose the Spotify playlist you want to convert
3. **Convert**: Click the "Convert" button to transform it into a YouTube playlist
4. **Save or Share**: Save the playlist to your YouTube account or share it with friends

## 🔍 Implementation Details

### Spotify Integration
The application uses the Spotipy library to interact with the Spotify Web API:
- OAuth authentication for users
- Retrieve user playlists
- Extract track information from playlists

### YouTube Integration
The Google API Python Client is used to interact with the YouTube Data API:
- OAuth 2.0 authentication for users
- Search for matching videos based on track information
- Create new playlists and add videos to them

### Flask Web Framework
The web application is built using Flask:
- Session management with Flask-Session
- Template rendering for the UI
- OAuth flow handling for both services

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



Project Link: [https://github.com/abdopeek/Spotify-YTMusic-Convert](https://github.com/abdopeek/Spotify-YTMusic-Convert)
