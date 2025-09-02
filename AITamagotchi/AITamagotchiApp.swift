import SwiftUI

@main
struct AITamagotchiApp: App {
    @StateObject private var appState = AppState()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .preferredColorScheme(appState.darkMode ? .dark : .light)
        }
    }
}

class AppState: ObservableObject {
    @Published var darkMode: Bool {
        didSet {
            UserDefaults.standard.set(darkMode, forKey: "darkMode")
        }
    }
    
    init() {
        self.darkMode = UserDefaults.standard.bool(forKey: "darkMode")
    }
}