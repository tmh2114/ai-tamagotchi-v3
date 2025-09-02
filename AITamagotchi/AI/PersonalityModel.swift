import Foundation
import CoreML

enum PersonalityTrait: String, CaseIterable {
    case playful
    case caring
    case energetic
    case calm
    case curious
    case shy
    case brave
    case clever
}

enum Mood: String, CaseIterable {
    case happy
    case sad
    case angry
    case sleepy
    case hungry
    case playful
    case sick
    case neutral
    case excited
    case lonely
    case content
    case anxious
}

class PersonalityModel: ObservableObject {
    @Published var traits: [PersonalityTrait: Double] = [:]
    @Published var currentMood: Mood = .neutral
    @Published var moodIntensity: Double = 0.5
    
    private var interactionHistory: [InteractionType] = []
    private let maxHistorySize = 100
    
    init() {
        initializePersonality()
    }
    
    private func initializePersonality() {
        for trait in PersonalityTrait.allCases {
            traits[trait] = Double.random(in: 0.3...0.7)
        }
    }
    
    func processInteraction(_ interaction: InteractionType) {
        interactionHistory.append(interaction)
        if interactionHistory.count > maxHistorySize {
            interactionHistory.removeFirst()
        }
        
        updatePersonalityTraits(for: interaction)
        updateMood(for: interaction)
    }
    
    private func updatePersonalityTraits(for interaction: InteractionType) {
        let learningRate = 0.01
        
        switch interaction {
        case .play:
            traits[.playful] = min(1.0, (traits[.playful] ?? 0.5) + learningRate)
            traits[.energetic] = min(1.0, (traits[.energetic] ?? 0.5) + learningRate)
        case .feed:
            traits[.caring] = min(1.0, (traits[.caring] ?? 0.5) + learningRate)
        case .pet:
            traits[.calm] = min(1.0, (traits[.calm] ?? 0.5) + learningRate)
        case .talk:
            traits[.curious] = min(1.0, (traits[.curious] ?? 0.5) + learningRate)
            traits[.clever] = min(1.0, (traits[.clever] ?? 0.5) + learningRate)
        case .medicine:
            traits[.brave] = min(1.0, (traits[.brave] ?? 0.5) + learningRate)
        case .sleep:
            traits[.calm] = min(1.0, (traits[.calm] ?? 0.5) + learningRate)
        case .clean:
            traits[.caring] = min(1.0, (traits[.caring] ?? 0.5) + learningRate)
        case .explore:
            traits[.curious] = min(1.0, (traits[.curious] ?? 0.5) + learningRate)
            traits[.brave] = min(1.0, (traits[.brave] ?? 0.5) + learningRate)
        }
    }
    
    private func updateMood(for interaction: InteractionType) {
        let previousMood = currentMood
        
        switch interaction {
        case .play:
            if currentMood == .bored || currentMood == .neutral {
                currentMood = .playful
            } else if currentMood == .sad {
                currentMood = .happy
            }
        case .feed:
            if currentMood == .hungry {
                currentMood = .content
            }
        case .pet:
            if currentMood == .anxious || currentMood == .sad {
                currentMood = .calm
            } else {
                currentMood = .happy
            }
        case .sleep:
            if currentMood == .sleepy {
                currentMood = .content
            }
        default:
            break
        }
        
        if currentMood != previousMood {
            moodIntensity = 0.7
        }
    }
    
    func getMoodBasedResponse() -> String {
        let trait = traits.max(by: { $0.value < $1.value })?.key ?? .neutral
        let responses = moodResponses[currentMood] ?? defaultResponses
        return responses.randomElement() ?? "..."
    }
    
    private let moodResponses: [Mood: [String]] = [
        .happy: ["I'm so happy to see you!", "This is wonderful!", "You make me so happy!"],
        .sad: ["I'm feeling a bit down...", "Could you cheer me up?", "I miss playing with you..."],
        .playful: ["Let's play a game!", "I'm full of energy!", "Want to have some fun?"],
        .hungry: ["I'm getting hungry...", "Could I have something to eat?", "My tummy is rumbling!"],
        .sleepy: ["*yawn* I'm getting tired...", "Time for a nap?", "So sleepy..."],
        .content: ["Life is good!", "I'm feeling great!", "Everything is perfect!"]
    ]
    
    private let defaultResponses = ["Hello!", "Hi there!", "Nice to see you!"]
}

enum InteractionType {
    case play
    case feed
    case pet
    case talk
    case medicine
    case sleep
    case clean
    case explore
}