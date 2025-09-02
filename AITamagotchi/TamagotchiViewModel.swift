import SwiftUI
import Combine

enum Mood: String, CaseIterable {
    case happy = "Happy"
    case sad = "Sad"
    case angry = "Angry"
    case sleepy = "Sleepy"
    case hungry = "Hungry"
    case playful = "Playful"
    case sick = "Sick"
    case neutral = "Neutral"
}

@MainActor
class TamagotchiViewModel: ObservableObject {
    @Published var name: String = "Tama"
    @Published var age: Int = 0
    @Published var happiness: Double = 75
    @Published var health: Double = 100
    @Published var energy: Double = 100
    @Published var hunger: Double = 50
    @Published var currentMood: Mood = .happy
    @Published var chatHistory: [ChatMessage] = []
    @Published var showingAlert = false
    @Published var alertMessage = ""
    @Published var isAlive = true
    
    private var lifecycleTimer: Timer?
    private var ageTimer: Timer?
    private let userDefaults = UserDefaults.standard
    
    init() {
        loadState()
        updateMood()
    }
    
    func startLifecycle() {
        // Update stats every 30 seconds
        lifecycleTimer = Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { _ in
            Task { @MainActor in
                self.updateStats()
            }
        }
        
        // Age every minute
        ageTimer = Timer.scheduledTimer(withTimeInterval: 60, repeats: true) { _ in
            Task { @MainActor in
                self.incrementAge()
            }
        }
    }
    
    func updateStats() {
        guard isAlive else { return }
        
        // Natural stat decay
        happiness = max(0, happiness - 2)
        energy = max(0, energy - 3)
        hunger = min(100, hunger + 4)
        health = max(0, health - 1)
        
        // Health impacts from other stats
        if hunger > 80 {
            health = max(0, health - 2)
            happiness = max(0, happiness - 3)
        }
        
        if energy < 20 {
            happiness = max(0, happiness - 2)
            health = max(0, health - 1)
        }
        
        if happiness < 20 {
            health = max(0, health - 1)
        }
        
        // Check if tamagotchi dies
        if health <= 0 {
            isAlive = false
            alertMessage = "\(name) has passed away. They lived for \(age) days. Create a new friend to start again."
            showingAlert = true
            lifecycleTimer?.invalidate()
            ageTimer?.invalidate()
        }
        
        updateMood()
        saveState()
    }
    
    func incrementAge() {
        age += 1
        
        // Milestone messages
        if age % 10 == 0 {
            alertMessage = "\(name) is now \(age) days old! 🎉"
            showingAlert = true
        }
    }
    
    func updateMood() {
        if !isAlive {
            currentMood = .sick
            return
        }
        
        if health < 30 {
            currentMood = .sick
        } else if hunger > 70 {
            currentMood = .hungry
        } else if energy < 30 {
            currentMood = .sleepy
        } else if happiness < 30 {
            currentMood = .sad
        } else if happiness > 80 && health > 70 {
            currentMood = .happy
        } else if energy > 80 {
            currentMood = .playful
        } else {
            currentMood = .neutral
        }
    }
    
    func feed() {
        guard isAlive else {
            alertMessage = "Create a new Tamagotchi to continue."
            showingAlert = true
            return
        }
        
        if hunger < 20 {
            alertMessage = "\(name) is not hungry right now!"
            showingAlert = true
            happiness = max(0, happiness - 5)
        } else {
            hunger = max(0, hunger - 30)
            happiness = min(100, happiness + 10)
            health = min(100, health + 5)
            alertMessage = "\(name) enjoyed the meal! 🍽️"
            showingAlert = true
            
            // Track feeding stats
            var totalMeals = UserDefaults.standard.integer(forKey: "total_meals")
            totalMeals += 1
            UserDefaults.standard.set(totalMeals, forKey: "total_meals")
        }
        updateMood()
        saveState()
    }
    
    func play() {
        guard isAlive else {
            alertMessage = "Create a new Tamagotchi to continue."
            showingAlert = true
            return
        }
        
        if energy < 30 {
            alertMessage = "\(name) is too tired to play!"
            showingAlert = true
            happiness = max(0, happiness - 5)
        } else {
            energy = max(0, energy - 20)
            happiness = min(100, happiness + 25)
            hunger = min(100, hunger + 10)
            alertMessage = "\(name) had fun playing! 🎮"
            showingAlert = true
            
            // Track play stats
            var totalPlays = UserDefaults.standard.integer(forKey: "total_plays")
            totalPlays += 1
            UserDefaults.standard.set(totalPlays, forKey: "total_plays")
        }
        updateMood()
        saveState()
    }
    
    func sleep() {
        guard isAlive else {
            alertMessage = "Create a new Tamagotchi to continue."
            showingAlert = true
            return
        }
        
        if energy > 70 {
            alertMessage = "\(name) is not tired yet!"
            showingAlert = true
            happiness = max(0, happiness - 5)
        } else {
            energy = min(100, energy + 50)
            health = min(100, health + 10)
            happiness = min(100, happiness + 5)
            alertMessage = "\(name) had a good rest! 😴"
            showingAlert = true
            
            // Track sleep stats
            var totalSleeps = UserDefaults.standard.integer(forKey: "total_sleeps")
            totalSleeps += 1
            UserDefaults.standard.set(totalSleeps, forKey: "total_sleeps")
        }
        updateMood()
        saveState()
    }
    
    func chat(message: String) -> String {
        guard isAlive else {
            return "..."
        }
        
        // Add user message to history
        chatHistory.append(ChatMessage(text: message, isUser: true))
        
        // Generate AI response based on mood and stats
        let response = generateAIResponse(to: message)
        chatHistory.append(ChatMessage(text: response, isUser: false))
        
        // Chat interaction affects happiness
        happiness = min(100, happiness + 5)
        updateMood()
        saveState()
        
        return response
    }
    
    private func generateAIResponse(to message: String) -> String {
        let lowercaseMessage = message.lowercased()
        
        // Mood-based responses
        let moodResponses: [Mood: [String]] = [
            .happy: [
                "I'm feeling great! Thanks for spending time with me! 😊",
                "Life is wonderful when you're around! 💖",
                "Every day with you is an adventure! 🌟"
            ],
            .sad: [
                "I'm feeling a bit down... could you cheer me up? 😢",
                "Things haven't been great lately... 😔",
                "I miss being happy... can we play together?"
            ],
            .hungry: [
                "My tummy is rumbling! Can I have something to eat? 🍕",
                "Food would be nice right about now... 🤤",
                "I'm so hungry I could eat everything! 🍔"
            ],
            .sleepy: [
                "Yaaawn... I'm getting sleepy... 😴",
                "I think I need a nap soon... 💤",
                "My eyes are getting heavy... 😪"
            ],
            .playful: [
                "Let's have some fun! Want to play a game? 🎮",
                "I'm full of energy! Let's do something exciting! ⚡",
                "Adventure time! What shall we do? 🚀"
            ],
            .sick: [
                "I don't feel so good... 🤒",
                "Everything hurts... please take care of me... 😷",
                "I need medicine and rest... 🏥"
            ],
            .angry: [
                "I'm upset right now! 😤",
                "Why haven't you been taking care of me properly? 😠",
                "I need better attention! 😡"
            ],
            .neutral: [
                "Things are okay, I suppose. 😐",
                "Just another day in Tamagotchi life. 🤷",
                "I'm here, existing. How are you? 😊"
            ]
        ]
        
        // Check for specific keywords
        if lowercaseMessage.contains("love") || lowercaseMessage.contains("like") {
            happiness = min(100, happiness + 10)
            return "I love you too! You're the best! 💖"
        }
        
        if lowercaseMessage.contains("how are you") || lowercaseMessage.contains("how do you feel") {
            return "I'm feeling \(currentMood.rawValue.lowercased()). My happiness is at \(Int(happiness))% and my health is \(Int(health))%."
        }
        
        if lowercaseMessage.contains("name") {
            return "My name is \(name)! I'm \(age) days old!"
        }
        
        if lowercaseMessage.contains("help") || lowercaseMessage.contains("what do you need") {
            if hunger > 60 {
                return "I'm getting hungry! Could you feed me? 🍽️"
            } else if energy < 40 {
                return "I'm tired... I think I need some sleep. 😴"
            } else if happiness < 50 {
                return "I'm feeling sad. Can we play together? 🎮"
            } else {
                return "I'm doing well! Just keep taking care of me! 😊"
            }
        }
        
        // Return a random mood-based response
        let responses = moodResponses[currentMood] ?? ["Hello!"]
        return responses.randomElement() ?? "Hi there!"
    }
    
    func reset() {
        name = "Tama"
        age = 0
        happiness = 75
        health = 100
        energy = 100
        hunger = 50
        currentMood = .happy
        chatHistory = []
        isAlive = true
        
        saveState()
        startLifecycle()
    }
    
    func changeName(to newName: String) {
        guard !newName.isEmpty else { return }
        name = newName
        saveState()
    }
    
    private func saveState() {
        userDefaults.set(name, forKey: "tamagotchi_name")
        userDefaults.set(age, forKey: "tamagotchi_age")
        userDefaults.set(happiness, forKey: "tamagotchi_happiness")
        userDefaults.set(health, forKey: "tamagotchi_health")
        userDefaults.set(energy, forKey: "tamagotchi_energy")
        userDefaults.set(hunger, forKey: "tamagotchi_hunger")
        userDefaults.set(isAlive, forKey: "tamagotchi_alive")
    }
    
    private func loadState() {
        if userDefaults.object(forKey: "tamagotchi_name") != nil {
            name = userDefaults.string(forKey: "tamagotchi_name") ?? "Tama"
            age = userDefaults.integer(forKey: "tamagotchi_age")
            happiness = userDefaults.double(forKey: "tamagotchi_happiness")
            health = userDefaults.double(forKey: "tamagotchi_health")
            energy = userDefaults.double(forKey: "tamagotchi_energy")
            hunger = userDefaults.double(forKey: "tamagotchi_hunger")
            isAlive = userDefaults.bool(forKey: "tamagotchi_alive")
        }
    }
}

struct ChatMessage: Identifiable {
    let id = UUID()
    let text: String
    let isUser: Bool
    let timestamp = Date()
}