# Ether - AI-Powered Tarot Reading Application

A modern, interactive tarot reading application that combines traditional tarot wisdom with AI-powered interpretations. Built with React and Flask, Ether provides an immersive experience for both beginners and experienced tarot enthusiasts.

## Features

- **Multiple Spread Types**
  - Single Card Reading
  - Three Card Spread (Past, Present, Future)
  - Celtic Cross (10-card comprehensive spread)
  - Chakra Spread (7-card spiritual alignment)

- **AI-Powered Interpretations**
  - Detailed card interpretations using GPT-4
  - Personalized readings based on your questions
  - Context-aware card meanings
  - Support for reversed cards

- **Interactive UI**
  - Beautiful card animations
  - Cosmic-themed design
  - Responsive layout
  - Support for device notches and safe areas

## Tech Stack

- **Frontend**
  - React
  - CSS3 with modern animations
  - Responsive design

- **Backend**
  - Flask (Python)
  - SQLite database
  - OpenAI API integration

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ether.git
   cd ether
   ```

2. **Set up environment variables**
   Create a `.env` file in the server directory:
   ```
   OPEN_AI_API_KEY=your_openai_api_key
   ```

3. **Install dependencies**
   ```bash
   # Install Python dependencies
   cd server
   pip install -r requirements.txt

   # Install frontend dependencies
   cd ../client
   npm install
   ```

4. **Initialize the database**
   ```bash
   cd server
   python seed.py
   ```

5. **Run the application**
   ```bash
   # Start the backend server (from server directory)
   python main.py

   # Start the frontend (from client directory)
   npm start
   ```

## Usage

1. Choose a spread type from the available options
2. Optionally, enter a specific question for your reading
3. Watch as the cards are drawn with beautiful animations
4. Receive a detailed AI-powered interpretation of your spread
5. Explore the meanings of individual cards

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the AI capabilities
- The Rider-Waite Tarot deck for card imagery and traditional meanings
- All contributors and users of the application 