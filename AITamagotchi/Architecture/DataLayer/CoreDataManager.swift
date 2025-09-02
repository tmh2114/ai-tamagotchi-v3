import Foundation
import CoreData

class CoreDataManager: ObservableObject {
    static let shared = CoreDataManager()
    
    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "AITamagotchi")
        container.loadPersistentStores { storeDescription, error in
            if let error = error as NSError? {
                fatalError("Unresolved error \(error), \(error.userInfo)")
            }
        }
        container.viewContext.automaticallyMergesChangesFromParent = true
        return container
    }()
    
    private init() {}
    
    func save() {
        let context = persistentContainer.viewContext
        
        if context.hasChanges {
            do {
                try context.save()
            } catch {
                let nsError = error as NSError
                fatalError("Unresolved error \(nsError), \(nsError.userInfo)")
            }
        }
    }
    
    func delete(_ object: NSManagedObject) {
        persistentContainer.viewContext.delete(object)
        save()
    }
    
    func fetchPet() -> PetEntity? {
        let request: NSFetchRequest<PetEntity> = PetEntity.fetchRequest()
        request.fetchLimit = 1
        
        do {
            let pets = try persistentContainer.viewContext.fetch(request)
            return pets.first
        } catch {
            print("Error fetching pet: \(error)")
            return nil
        }
    }
    
    func createPet(name: String) -> PetEntity {
        let pet = PetEntity(context: persistentContainer.viewContext)
        pet.id = UUID()
        pet.name = name
        pet.createdAt = Date()
        pet.health = 100
        pet.happiness = 100
        pet.hunger = 0
        pet.energy = 100
        pet.mood = "happy"
        pet.age = 0
        save()
        return pet
    }
}