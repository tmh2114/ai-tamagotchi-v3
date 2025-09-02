import SwiftUI

struct MiniGamesView: View {
    @ObservedObject var tamagotchi: TamagotchiViewModel
    @State private var selectedGame: GameType? = nil
    @Environment(\.dismiss) var dismiss
    
    enum GameType: String, CaseIterable {
        case guessNumber = "Guess the Number"
        case rockPaperScissors = "Rock Paper Scissors"
        case memoryMatch = "Memory Match"
        case quickMath = "Quick Math"
        
        var icon: String {
            switch self {
            case .guessNumber: return "questionmark.circle"
            case .rockPaperScissors: return "hand.raised"
            case .memoryMatch: return "square.grid.3x3"
            case .quickMath: return "number"
            }
        }
        
        var color: Color {
            switch self {
            case .guessNumber: return .blue
            case .rockPaperScissors: return .red
            case .memoryMatch: return .purple
            case .quickMath: return .green
            }
        }
    }
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    ForEach(GameType.allCases, id: \.self) { game in
                        GameCard(game: game) {
                            selectedGame = game
                        }
                    }
                }
                .padding()
            }
            .navigationTitle("Mini Games")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
            .sheet(item: $selectedGame) { game in
                switch game {
                case .guessNumber:
                    GuessNumberGame(tamagotchi: tamagotchi)
                case .rockPaperScissors:
                    RockPaperScissorsGame(tamagotchi: tamagotchi)
                case .memoryMatch:
                    MemoryMatchGame(tamagotchi: tamagotchi)
                case .quickMath:
                    QuickMathGame(tamagotchi: tamagotchi)
                }
            }
        }
    }
}

struct GameCard: View {
    let game: MiniGamesView.GameType
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            HStack {
                Image(systemName: game.icon)
                    .font(.title2)
                    .foregroundColor(.white)
                    .frame(width: 50, height: 50)
                    .background(Circle().fill(game.color))
                
                VStack(alignment: .leading) {
                    Text(game.rawValue)
                        .font(.headline)
                        .foregroundColor(.primary)
                    Text("Tap to play")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                Image(systemName: "chevron.right")
                    .foregroundColor(.secondary)
            }
            .padding()
            .background(RoundedRectangle(cornerRadius: 12).fill(Color(.systemGray6)))
        }
    }
}

// MARK: - Guess Number Game

struct GuessNumberGame: View {
    @ObservedObject var tamagotchi: TamagotchiViewModel
    @State private var targetNumber = Int.random(in: 1...100)
    @State private var userGuess = ""
    @State private var feedback = "I'm thinking of a number between 1 and 100!"
    @State private var attempts = 0
    @State private var gameWon = false
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 30) {
                Text(feedback)
                    .font(.title3)
                    .multilineTextAlignment(.center)
                    .padding()
                
                if !gameWon {
                    TextField("Enter your guess", text: $userGuess)
                        .keyboardType(.numberPad)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .padding(.horizontal)
                    
                    Button("Guess!") {
                        checkGuess()
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(userGuess.isEmpty)
                    
                    Text("Attempts: \(attempts)")
                        .foregroundColor(.secondary)
                } else {
                    Button("Play Again") {
                        resetGame()
                    }
                    .buttonStyle(.borderedProminent)
                }
                
                Spacer()
            }
            .padding()
            .navigationTitle("Guess the Number")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
    
    private func checkGuess() {
        guard let guess = Int(userGuess) else {
            feedback = "Please enter a valid number!"
            return
        }
        
        attempts += 1
        
        if guess == targetNumber {
            feedback = "🎉 You got it in \(attempts) attempts!"
            gameWon = true
            tamagotchi.happiness = min(100, tamagotchi.happiness + 15)
        } else if guess < targetNumber {
            feedback = "Too low! Try a higher number."
        } else {
            feedback = "Too high! Try a lower number."
        }
        
        userGuess = ""
    }
    
    private func resetGame() {
        targetNumber = Int.random(in: 1...100)
        userGuess = ""
        feedback = "I'm thinking of a number between 1 and 100!"
        attempts = 0
        gameWon = false
    }
}

// MARK: - Rock Paper Scissors Game

struct RockPaperScissorsGame: View {
    @ObservedObject var tamagotchi: TamagotchiViewModel
    @State private var playerChoice: Choice?
    @State private var tamagotchiChoice: Choice?
    @State private var result = ""
    @State private var score = 0
    @Environment(\.dismiss) var dismiss
    
    enum Choice: String, CaseIterable {
        case rock = "Rock"
        case paper = "Paper"
        case scissors = "Scissors"
        
        var emoji: String {
            switch self {
            case .rock: return "🪨"
            case .paper: return "📄"
            case .scissors: return "✂️"
            }
        }
    }
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 30) {
                Text("Score: \(score)")
                    .font(.title2)
                    .fontWeight(.bold)
                
                if let tamagotchiChoice = tamagotchiChoice {
                    VStack {
                        Text("\(tamagotchi.name) chose:")
                        Text(tamagotchiChoice.emoji)
                            .font(.system(size: 60))
                    }
                }
                
                if !result.isEmpty {
                    Text(result)
                        .font(.title3)
                        .fontWeight(.semibold)
                        .foregroundColor(result.contains("Win") ? .green : result.contains("Lose") ? .red : .orange)
                }
                
                Text("Make your choice:")
                    .font(.headline)
                
                HStack(spacing: 20) {
                    ForEach(Choice.allCases, id: \.self) { choice in
                        Button(action: { play(choice) }) {
                            VStack {
                                Text(choice.emoji)
                                    .font(.system(size: 50))
                                Text(choice.rawValue)
                                    .font(.caption)
                            }
                            .padding()
                            .background(RoundedRectangle(cornerRadius: 12).fill(Color(.systemGray6)))
                        }
                    }
                }
                
                Spacer()
            }
            .padding()
            .navigationTitle("Rock Paper Scissors")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
    
    private func play(_ choice: Choice) {
        playerChoice = choice
        tamagotchiChoice = Choice.allCases.randomElement()
        
        guard let playerChoice = playerChoice, let tamagotchiChoice = tamagotchiChoice else { return }
        
        if playerChoice == tamagotchiChoice {
            result = "It's a Draw!"
        } else if (playerChoice == .rock && tamagotchiChoice == .scissors) ||
                  (playerChoice == .paper && tamagotchiChoice == .rock) ||
                  (playerChoice == .scissors && tamagotchiChoice == .paper) {
            result = "You Win! 🎉"
            score += 1
            tamagotchi.happiness = min(100, tamagotchi.happiness + 10)
        } else {
            result = "You Lose! 😔"
            score = max(0, score - 1)
        }
    }
}

// MARK: - Memory Match Game

struct MemoryMatchGame: View {
    @ObservedObject var tamagotchi: TamagotchiViewModel
    @State private var cards: [Card] = []
    @State private var flippedCards: Set<Int> = []
    @State private var matchedCards: Set<Int> = []
    @State private var attempts = 0
    @State private var firstFlippedIndex: Int?
    @Environment(\.dismiss) var dismiss
    
    struct Card {
        let id: Int
        let emoji: String
    }
    
    let emojis = ["🎮", "🎨", "🎭", "🎪", "🎯", "🎲"]
    
    var body: some View {
        NavigationStack {
            VStack {
                Text("Attempts: \(attempts)")
                    .font(.headline)
                
                LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible()), GridItem(.flexible())], spacing: 15) {
                    ForEach(0..<cards.count, id: \.self) { index in
                        CardView(
                            card: cards[index],
                            isFlipped: flippedCards.contains(index) || matchedCards.contains(index),
                            isMatched: matchedCards.contains(index)
                        ) {
                            flipCard(at: index)
                        }
                    }
                }
                .padding()
                
                if matchedCards.count == cards.count {
                    Text("🎉 You Won in \(attempts) attempts!")
                        .font(.title2)
                        .fontWeight(.bold)
                    
                    Button("Play Again") {
                        setupGame()
                    }
                    .buttonStyle(.borderedProminent)
                }
                
                Spacer()
            }
            .navigationTitle("Memory Match")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
            .onAppear {
                setupGame()
            }
        }
    }
    
    private func setupGame() {
        cards = []
        for (index, emoji) in emojis.enumerated() {
            cards.append(Card(id: index * 2, emoji: emoji))
            cards.append(Card(id: index * 2 + 1, emoji: emoji))
        }
        cards.shuffle()
        flippedCards = []
        matchedCards = []
        attempts = 0
        firstFlippedIndex = nil
    }
    
    private func flipCard(at index: Int) {
        guard !matchedCards.contains(index) else { return }
        
        if let firstIndex = firstFlippedIndex {
            if firstIndex == index { return }
            
            flippedCards.insert(index)
            attempts += 1
            
            if cards[firstIndex].emoji == cards[index].emoji {
                matchedCards.insert(firstIndex)
                matchedCards.insert(index)
                if matchedCards.count == cards.count {
                    tamagotchi.happiness = min(100, tamagotchi.happiness + 20)
                }
            } else {
                DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
                    flippedCards.remove(firstIndex)
                    flippedCards.remove(index)
                }
            }
            firstFlippedIndex = nil
        } else {
            flippedCards.insert(index)
            firstFlippedIndex = index
        }
    }
}

struct CardView: View {
    let card: MemoryMatchGame.Card
    let isFlipped: Bool
    let isMatched: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            ZStack {
                RoundedRectangle(cornerRadius: 12)
                    .fill(isMatched ? Color.green.opacity(0.3) : (isFlipped ? Color.blue.opacity(0.2) : Color.gray))
                    .frame(height: 80)
                
                if isFlipped {
                    Text(card.emoji)
                        .font(.system(size: 40))
                } else {
                    Text("?")
                        .font(.system(size: 40))
                        .foregroundColor(.white)
                }
            }
        }
        .disabled(isMatched)
    }
}

// MARK: - Quick Math Game

struct QuickMathGame: View {
    @ObservedObject var tamagotchi: TamagotchiViewModel
    @State private var num1 = Int.random(in: 1...20)
    @State private var num2 = Int.random(in: 1...20)
    @State private var operation = "+"
    @State private var userAnswer = ""
    @State private var score = 0
    @State private var feedback = ""
    @State private var feedbackColor = Color.black
    @Environment(\.dismiss) var dismiss
    
    var correctAnswer: Int {
        switch operation {
        case "+": return num1 + num2
        case "-": return num1 - num2
        case "×": return num1 * num2
        default: return 0
        }
    }
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 30) {
                Text("Score: \(score)")
                    .font(.title2)
                    .fontWeight(.bold)
                
                Text("\(num1) \(operation) \(num2) = ?")
                    .font(.largeTitle)
                    .fontWeight(.semibold)
                
                TextField("Your answer", text: $userAnswer)
                    .keyboardType(.numberPad)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .frame(width: 150)
                
                Button("Submit") {
                    checkAnswer()
                }
                .buttonStyle(.borderedProminent)
                .disabled(userAnswer.isEmpty)
                
                if !feedback.isEmpty {
                    Text(feedback)
                        .font(.title3)
                        .foregroundColor(feedbackColor)
                }
                
                Spacer()
            }
            .padding()
            .navigationTitle("Quick Math")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
            .onAppear {
                generateNewProblem()
            }
        }
    }
    
    private func checkAnswer() {
        guard let answer = Int(userAnswer) else {
            feedback = "Please enter a valid number"
            feedbackColor = .red
            return
        }
        
        if answer == correctAnswer {
            score += 1
            feedback = "Correct! 🎉"
            feedbackColor = .green
            tamagotchi.happiness = min(100, tamagotchi.happiness + 5)
            
            DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
                generateNewProblem()
            }
        } else {
            feedback = "Try again! The answer was \(correctAnswer)"
            feedbackColor = .red
            
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                generateNewProblem()
            }
        }
    }
    
    private func generateNewProblem() {
        num1 = Int.random(in: 1...20)
        num2 = Int.random(in: 1...20)
        operation = ["+", "-", "×"].randomElement()!
        
        // Ensure non-negative results for subtraction
        if operation == "-" && num2 > num1 {
            swap(&num1, &num2)
        }
        
        userAnswer = ""
        feedback = ""
    }
}