import Foundation
import NaturalLanguage

class AIService: ObservableObject {
    @Published var isProcessing = false
    private let personalityModel = PersonalityModel()
    private let sentimentAnalyzer = NLModel()
    
    func generateResponse(for input: String, petState: PetState) -> String {
        isProcessing = true
        defer { isProcessing = false }
        
        let sentiment = analyzeSentiment(input)
        let context = buildContext(from: petState)
        let personality = personalityModel.traits
        
        return generatePersonalizedResponse(
            input: input,
            sentiment: sentiment,
            context: context,
            personality: personality
        )
    }
    
    private func analyzeSentiment(_ text: String) -> Double {
        let tagger = NLTagger(tagSchemes: [.sentimentScore])
        tagger.string = text
        
        var sentimentScore = 0.0
        tagger.enumerateTags(in: text.startIndex..<text.endIndex,
                            unit: .paragraph,
                            scheme: .sentimentScore) { tag, _ in
            if let tag = tag,
               let score = Double(tag.rawValue) {
                sentimentScore = score
            }
            return true
        }
        
        return sentimentScore
    }
    
    private func buildContext(from state: PetState) -> PetContext {
        return PetContext(
            health: state.health,
            happiness: state.happiness,
            hunger: state.hunger,
            energy: state.energy,
            mood: state.mood,
            age: state.age,
            lastInteraction: state.lastInteraction
        )
    }
    
    private func generatePersonalizedResponse(
        input: String,
        sentiment: Double,
        context: PetContext,
        personality: [PersonalityTrait: Double]
    ) -> String {
        
        let dominantTrait = personality.max(by: { $0.value < $1.value })?.key ?? .neutral
        
        var response = ""
        
        if context.hunger > 70 {
            response = hungerResponses[dominantTrait] ?? "I'm hungry!"
        } else if context.energy < 30 {
            response = tiredResponses[dominantTrait] ?? "I'm tired..."
        } else if sentiment < -0.5 {
            response = comfortResponses[dominantTrait] ?? "Are you okay?"
        } else if sentiment > 0.5 {
            response = happyResponses[dominantTrait] ?? "That's great!"
        } else {
            response = neutralResponses[dominantTrait] ?? "Hi there!"
        }
        
        return personalizeResponse(response, with: personality)
    }
    
    private func personalizeResponse(_ base: String, with personality: [PersonalityTrait: Double]) -> String {
        var response = base
        
        if let playfulness = personality[.playful], playfulness > 0.7 {
            response += " 🎮"
        }
        
        if let caring = personality[.caring], caring > 0.7 {
            response = "💖 " + response
        }
        
        return response
    }
    
    func predictNextNeed(from state: PetState) -> PetNeed {
        let needs: [(PetNeed, Double)] = [
            (.food, Double(state.hunger) / 100.0),
            (.sleep, 1.0 - Double(state.energy) / 100.0),
            (.play, 1.0 - Double(state.happiness) / 100.0),
            (.medicine, state.health < 50 ? 1.0 : 0.0)
        ]
        
        return needs.max(by: { $0.1 < $1.1 })?.0 ?? .play
    }
    
    private let hungerResponses: [PersonalityTrait: String] = [
        .playful: "Can we eat and then play?",
        .caring: "I'm hungry, could you feed me please?",
        .energetic: "Need food for energy!",
        .calm: "I'm getting a bit hungry...",
        .shy: "Um... I'm hungry..."
    ]
    
    private let tiredResponses: [PersonalityTrait: String] = [
        .playful: "Even I need sleep sometimes!",
        .caring: "I should rest now...",
        .energetic: "Running out of energy!",
        .calm: "Time for a peaceful nap...",
        .shy: "I'm sleepy..."
    ]
    
    private let comfortResponses: [PersonalityTrait: String] = [
        .playful: "Hey, let's play to cheer up!",
        .caring: "Is everything alright? I'm here for you!",
        .calm: "Take a deep breath, it'll be okay.",
        .shy: "Um... do you need a hug?"
    ]
    
    private let happyResponses: [PersonalityTrait: String] = [
        .playful: "Yay! Let's celebrate with a game!",
        .caring: "That makes me so happy for you!",
        .energetic: "Awesome! High five!",
        .calm: "That's wonderful news.",
        .curious: "Tell me more about it!"
    ]
    
    private let neutralResponses: [PersonalityTrait: String] = [
        .playful: "Want to play?",
        .caring: "How are you today?",
        .curious: "What's on your mind?",
        .calm: "Nice to see you.",
        .shy: "Hi..."
    ]
}

struct PetContext {
    let health: Int
    let happiness: Int
    let hunger: Int
    let energy: Int
    let mood: String
    let age: Int
    let lastInteraction: Date
}

struct PetState {
    let health: Int
    let happiness: Int
    let hunger: Int
    let energy: Int
    let mood: String
    let age: Int
    let lastInteraction: Date
}

enum PetNeed {
    case food
    case sleep
    case play
    case medicine
    case attention
}