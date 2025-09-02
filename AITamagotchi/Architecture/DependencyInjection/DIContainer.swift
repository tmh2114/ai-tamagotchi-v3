import Foundation
import SwiftUI

protocol DIContainerProtocol {
    func register<T>(_ type: T.Type, factory: @escaping () -> T)
    func resolve<T>(_ type: T.Type) -> T?
}

class DIContainer: DIContainerProtocol {
    static let shared = DIContainer()
    private var services: [String: Any] = [:]
    private var factories: [String: () -> Any] = [:]
    
    private init() {
        registerDependencies()
    }
    
    func register<T>(_ type: T.Type, factory: @escaping () -> T) {
        let key = String(describing: type)
        factories[key] = factory
    }
    
    func resolve<T>(_ type: T.Type) -> T? {
        let key = String(describing: type)
        
        if let service = services[key] as? T {
            return service
        }
        
        if let factory = factories[key] {
            let service = factory() as? T
            services[key] = service
            return service
        }
        
        return nil
    }
    
    private func registerDependencies() {
        register(CoreDataManager.self) {
            CoreDataManager.shared
        }
        
        register(AIService.self) {
            AIService()
        }
        
        register(NotificationManager.self) {
            NotificationManager.shared
        }
        
        register(GameService.self) {
            GameService()
        }
    }
}

struct DIContainerKey: EnvironmentKey {
    static let defaultValue: DIContainer = DIContainer.shared
}

extension EnvironmentValues {
    var diContainer: DIContainer {
        get { self[DIContainerKey.self] }
        set { self[DIContainerKey.self] = newValue }
    }
}