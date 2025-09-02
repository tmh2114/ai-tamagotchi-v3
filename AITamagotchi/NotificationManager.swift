import Foundation
import UserNotifications

class NotificationManager: NSObject, UNUserNotificationCenterDelegate {
    static let shared = NotificationManager()
    
    private override init() {
        super.init()
        UNUserNotificationCenter.current().delegate = self
    }
    
    func requestAuthorization() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, error in
            if granted {
                print("Notification permission granted")
                self.scheduleNotifications()
            } else if let error = error {
                print("Notification permission error: \(error)")
            }
        }
    }
    
    func scheduleNotifications() {
        // Remove existing notifications
        UNUserNotificationCenter.current().removeAllPendingNotificationRequests()
        
        // Schedule feeding reminder
        scheduleDailyNotification(
            identifier: "feed_reminder",
            title: "Your Tamagotchi is Hungry!",
            body: "Don't forget to feed your Tamagotchi!",
            hour: 8,
            minute: 0
        )
        
        // Schedule play reminder
        scheduleDailyNotification(
            identifier: "play_reminder",
            title: "Playtime!",
            body: "Your Tamagotchi wants to play with you!",
            hour: 14,
            minute: 0
        )
        
        // Schedule sleep reminder
        scheduleDailyNotification(
            identifier: "sleep_reminder",
            title: "Bedtime!",
            body: "Your Tamagotchi is getting sleepy!",
            hour: 20,
            minute: 0
        )
    }
    
    private func scheduleDailyNotification(identifier: String, title: String, body: String, hour: Int, minute: Int) {
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default
        
        var dateComponents = DateComponents()
        dateComponents.hour = hour
        dateComponents.minute = minute
        
        let trigger = UNCalendarNotificationTrigger(dateMatching: dateComponents, repeats: true)
        let request = UNNotificationRequest(identifier: identifier, content: content, trigger: trigger)
        
        UNUserNotificationCenter.current().add(request) { error in
            if let error = error {
                print("Error scheduling notification: \(error)")
            }
        }
    }
    
    func scheduleHealthAlert(health: Double) {
        guard health < 30 else { return }
        
        let content = UNMutableNotificationContent()
        content.title = "Health Alert!"
        content.body = "Your Tamagotchi's health is low! Please take care of them!"
        content.sound = .default
        
        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 1, repeats: false)
        let request = UNNotificationRequest(identifier: "health_alert", content: content, trigger: trigger)
        
        UNUserNotificationCenter.current().add(request)
    }
    
    // MARK: - UNUserNotificationCenterDelegate
    
    func userNotificationCenter(_ center: UNUserNotificationCenter, willPresent notification: UNNotification, withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        completionHandler([.banner, .sound])
    }
}