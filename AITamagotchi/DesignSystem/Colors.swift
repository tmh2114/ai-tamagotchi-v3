import SwiftUI

extension Color {
    static let theme = ColorTheme()
}

struct ColorTheme {
    let primary = Color("PrimaryColor")
    let secondary = Color("SecondaryColor")
    let accent = Color("AccentColor")
    let background = Color("BackgroundColor")
    let surface = Color("SurfaceColor")
    let text = Color("TextColor")
    let textSecondary = Color("TextSecondaryColor")
    let success = Color.green
    let warning = Color.orange
    let error = Color.red
    let info = Color.blue
    
    let healthBar = Color.red
    let happinessBar = Color.yellow
    let hungerBar = Color.orange
    let energyBar = Color.blue
    
    let moodHappy = Color.yellow
    let moodSad = Color.blue
    let moodAngry = Color.red
    let moodSleepy = Color.purple
    let moodHungry = Color.orange
    let moodPlayful = Color.green
    let moodSick = Color.gray
    let moodNeutral = Color.gray
}

extension Color {
    static let petBackground = LinearGradient(
        gradient: Gradient(colors: [
            Color(red: 0.9, green: 0.95, blue: 1.0),
            Color(red: 0.8, green: 0.9, blue: 0.95)
        ]),
        startPoint: .top,
        endPoint: .bottom
    )
    
    static let skyGradient = LinearGradient(
        gradient: Gradient(colors: [
            Color(red: 0.5, green: 0.8, blue: 1.0),
            Color(red: 0.3, green: 0.6, blue: 0.9)
        ]),
        startPoint: .top,
        endPoint: .bottom
    )
    
    static let grassGradient = LinearGradient(
        gradient: Gradient(colors: [
            Color(red: 0.4, green: 0.8, blue: 0.3),
            Color(red: 0.3, green: 0.6, blue: 0.2)
        ]),
        startPoint: .top,
        endPoint: .bottom
    )
}