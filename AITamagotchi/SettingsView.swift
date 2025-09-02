import SwiftUI

struct SettingsView: View {
    @ObservedObject var tamagotchi: TamagotchiViewModel
    @EnvironmentObject var appState: AppState
    @State private var newName = ""
    @State private var showingResetAlert = false
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationStack {
            Form {
                Section("Tamagotchi Info") {
                    HStack {
                        Text("Name")
                        Spacer()
                        Text(tamagotchi.name)
                            .foregroundColor(.secondary)
                    }
                    
                    HStack {
                        Text("Age")
                        Spacer()
                        Text("\(tamagotchi.age) days")
                            .foregroundColor(.secondary)
                    }
                    
                    HStack {
                        Text("Status")
                        Spacer()
                        Text(tamagotchi.isAlive ? "Alive" : "Passed Away")
                            .foregroundColor(tamagotchi.isAlive ? .green : .red)
                    }
                }
                
                Section("Customize") {
                    HStack {
                        TextField("New Name", text: $newName)
                        Button("Change") {
                            if !newName.isEmpty {
                                tamagotchi.changeName(to: newName)
                                newName = ""
                            }
                        }
                        .disabled(newName.isEmpty)
                    }
                    
                    Toggle("Dark Mode", isOn: $appState.darkMode)
                }
                
                Section("Statistics") {
                    StatRow(label: "Total Meals", value: "\(UserDefaults.standard.integer(forKey: "total_meals"))")
                    StatRow(label: "Total Playtime", value: "\(UserDefaults.standard.integer(forKey: "total_plays"))")
                    StatRow(label: "Total Sleep Sessions", value: "\(UserDefaults.standard.integer(forKey: "total_sleeps"))")
                    StatRow(label: "Total Chats", value: "\(tamagotchi.chatHistory.count)")
                }
                
                Section {
                    Button("Reset Tamagotchi") {
                        showingResetAlert = true
                    }
                    .foregroundColor(.red)
                }
                
                Section("About") {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.secondary)
                    }
                    
                    Link("Support", destination: URL(string: "https://github.com/yourusername/ai-tamagotchi")!)
                }
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
            .alert("Reset Tamagotchi", isPresented: $showingResetAlert) {
                Button("Cancel", role: .cancel) { }
                Button("Reset", role: .destructive) {
                    tamagotchi.reset()
                    dismiss()
                }
            } message: {
                Text("This will create a new Tamagotchi and reset all stats. This action cannot be undone.")
            }
        }
    }
}

struct StatRow: View {
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(label)
            Spacer()
            Text(value)
                .foregroundColor(.secondary)
        }
    }
}