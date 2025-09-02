# AI Tamagotchi iOS App

A modern iOS implementation of the classic Tamagotchi virtual pet, enhanced with AI personality and interactive features.

## Features

### Core Functionality
- **Virtual Pet Care**: Feed, play with, and put your Tamagotchi to sleep
- **Health System**: Monitor happiness, health, energy, and hunger levels
- **AI Personality**: Dynamic mood system that responds to care and interactions
- **Chat Interface**: Have conversations with your AI pet that responds based on its current mood and needs
- **Persistence**: Your Tamagotchi's state is saved automatically

### Interactive Elements
- **8 Different Moods**: Happy, Sad, Angry, Sleepy, Hungry, Playful, Sick, and Neutral
- **Real-time Stats**: Watch your pet's stats change over time
- **Age Tracking**: Your Tamagotchi ages in days with milestone celebrations
- **Death & Rebirth**: If neglected, your Tamagotchi can pass away but can be reset

### Mini Games
- **Guess the Number**: Test your luck with number guessing
- **Rock Paper Scissors**: Classic game against your Tamagotchi
- **Memory Match**: Match emoji pairs to test your memory
- **Quick Math**: Solve math problems to keep your mind sharp

### Additional Features
- **Dark Mode Support**: Toggle between light and dark themes
- **Push Notifications**: Reminders to care for your pet (optional)
- **Statistics Tracking**: Monitor total meals, playtime, and sleep sessions
- **Customizable Name**: Give your Tamagotchi a unique name

## Technical Details

### Architecture
- **SwiftUI**: Modern declarative UI framework
- **MVVM Pattern**: Clean separation of concerns with ViewModel
- **UserDefaults**: Persistent storage for game state
- **Combine Framework**: Reactive programming for state management

### Requirements
- iOS 17.0+
- Xcode 15.0+
- Swift 5.9+

### Project Structure
```
AITamagotchi/
├── AITamagotchiApp.swift       # App entry point
├── ContentView.swift           # Main game interface
├── TamagotchiViewModel.swift   # Game logic and state management
├── ChatView.swift              # AI chat interface
├── SettingsView.swift          # Settings and customization
├── MiniGamesView.swift         # Collection of mini games
└── NotificationManager.swift   # Push notification handling
```

## Installation

1. Clone the repository
2. Open the project in Xcode
3. Build and run on iOS Simulator or device

## Usage

### Getting Started
1. Launch the app to meet your new AI Tamagotchi
2. Monitor the status bars to track your pet's needs
3. Use action buttons to care for your pet
4. Chat with your Tamagotchi to build a relationship

### Care Guidelines
- **Feed**: When hunger is above 30%
- **Play**: When your pet has enough energy (>30%)
- **Sleep**: When energy drops below 70%
- **Chat**: Anytime to increase happiness

### Game Mechanics
- Stats naturally decay over time
- Neglecting needs affects health and happiness
- Low health can lead to your Tamagotchi passing away
- Mini games provide happiness boosts
- Age increments every minute of real time

## Features in Detail

### Mood System
The Tamagotchi's mood changes based on its stats:
- **Happy**: High happiness and health
- **Sad**: Low happiness
- **Hungry**: High hunger level
- **Sleepy**: Low energy
- **Sick**: Low health
- **Playful**: High energy
- **Neutral**: Balanced stats

### AI Chat System
- Context-aware responses based on current mood
- Recognizes keywords and responds appropriately
- Remembers conversation history
- Affects happiness through interaction

### Lifecycle System
- Stats update every 30 seconds
- Age increments every minute
- Milestone alerts at every 10 days
- Automatic state persistence

## Future Enhancements
- Multiple Tamagotchi breeds
- Evolution system
- Achievements and badges
- Social features
- More mini games
- Weather effects on mood
- Seasonal events

## License
MIT License

## Credits
Inspired by the original Tamagotchi by Bandai
Built with SwiftUI and love for virtual pets