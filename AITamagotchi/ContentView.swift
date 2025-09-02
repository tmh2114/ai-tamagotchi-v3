import SwiftUI

struct ContentView: View {
    @StateObject private var tamagotchi = TamagotchiViewModel()
    @State private var showingChat = false
    @State private var showingSettings = false
    @State private var showingGames = false
    @State private var chatInput = ""
    @State private var animationScale: CGFloat = 1.0
    
    var body: some View {
        NavigationStack {
            ZStack {
                LinearGradient(
                    colors: [Color.purple.opacity(0.3), Color.blue.opacity(0.2)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
                
                VStack(spacing: 20) {
                    // Status bars
                    VStack(spacing: 12) {
                        StatusBar(
                            title: "Happiness",
                            value: tamagotchi.happiness,
                            color: .yellow
                        )
                        StatusBar(
                            title: "Health",
                            value: tamagotchi.health,
                            color: .red
                        )
                        StatusBar(
                            title: "Energy",
                            value: tamagotchi.energy,
                            color: .blue
                        )
                        StatusBar(
                            title: "Hunger",
                            value: tamagotchi.hunger,
                            color: .green
                        )
                    }
                    .padding(.horizontal)
                    
                    // Tamagotchi Character
                    ZStack {
                        Circle()
                            .fill(
                                RadialGradient(
                                    colors: [Color.white, Color.gray.opacity(0.3)],
                                    center: .center,
                                    startRadius: 5,
                                    endRadius: 100
                                )
                            )
                            .frame(width: 200, height: 200)
                            .shadow(radius: 10)
                        
                        TamagotchiCharacter(mood: tamagotchi.currentMood)
                            .scaleEffect(animationScale)
                            .animation(
                                .easeInOut(duration: 1.5).repeatForever(autoreverses: true),
                                value: animationScale
                            )
                    }
                    
                    // Mood and Age Display
                    VStack(spacing: 8) {
                        Text(tamagotchi.name)
                            .font(.title2)
                            .fontWeight(.bold)
                        
                        Text("Mood: \(tamagotchi.currentMood.rawValue)")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        
                        Text("Age: \(tamagotchi.age) days")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    
                    // Action Buttons
                    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 15) {
                        ActionButton(
                            icon: "fork.knife",
                            title: "Feed",
                            color: .green,
                            action: { tamagotchi.feed() }
                        )
                        
                        ActionButton(
                            icon: "gamecontroller",
                            title: "Play",
                            color: .blue,
                            action: { tamagotchi.play() }
                        )
                        
                        ActionButton(
                            icon: "moon.zzz",
                            title: "Sleep",
                            color: .purple,
                            action: { tamagotchi.sleep() }
                        )
                        
                        ActionButton(
                            icon: "bubble.left.and.bubble.right",
                            title: "Chat",
                            color: .orange,
                            action: { showingChat = true }
                        )
                    }
                    .padding(.horizontal)
                    
                    Spacer()
                }
                .padding(.top)
            }
            .navigationTitle("AI Tamagotchi")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button(action: { showingGames = true }) {
                        Image(systemName: "gamecontroller")
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingSettings = true }) {
                        Image(systemName: "gearshape")
                    }
                }
            }
            .onAppear {
                animationScale = 1.1
                tamagotchi.startLifecycle()
            }
            .sheet(isPresented: $showingChat) {
                ChatView(tamagotchi: tamagotchi)
            }
            .sheet(isPresented: $showingSettings) {
                SettingsView(tamagotchi: tamagotchi)
            }
            .sheet(isPresented: $showingGames) {
                MiniGamesView(tamagotchi: tamagotchi)
            }
            .alert("Tamagotchi Alert", isPresented: $tamagotchi.showingAlert) {
                Button("OK") { }
            } message: {
                Text(tamagotchi.alertMessage)
            }
        }
    }
}

struct StatusBar: View {
    let title: String
    let value: Double
    let color: Color
    
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack {
                Text(title)
                    .font(.caption)
                    .foregroundColor(.secondary)
                Spacer()
                Text("\(Int(value))%")
                    .font(.caption)
                    .fontWeight(.semibold)
            }
            
            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    RoundedRectangle(cornerRadius: 4)
                        .fill(Color.gray.opacity(0.2))
                        .frame(height: 8)
                    
                    RoundedRectangle(cornerRadius: 4)
                        .fill(color)
                        .frame(width: geometry.size.width * (value / 100), height: 8)
                        .animation(.easeInOut, value: value)
                }
            }
            .frame(height: 8)
        }
    }
}

struct ActionButton: View {
    let icon: String
    let title: String
    let color: Color
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.title2)
                Text(title)
                    .font(.caption)
                    .fontWeight(.medium)
            }
            .frame(maxWidth: .infinity)
            .padding()
            .background(color.opacity(0.15))
            .foregroundColor(color)
            .cornerRadius(12)
        }
    }
}

struct TamagotchiCharacter: View {
    let mood: Mood
    
    var eyeExpression: String {
        switch mood {
        case .happy: return "😊"
        case .sad: return "😢"
        case .angry: return "😠"
        case .sleepy: return "😴"
        case .hungry: return "🤤"
        case .playful: return "😄"
        case .sick: return "🤢"
        case .neutral: return "😐"
        }
    }
    
    var body: some View {
        Text(eyeExpression)
            .font(.system(size: 80))
    }
}

#Preview {
    ContentView()
}