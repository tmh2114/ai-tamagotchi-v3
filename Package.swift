// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "AITamagotchi",
    platforms: [
        .iOS(.v17)
    ],
    products: [
        .library(
            name: "AITamagotchi",
            targets: ["AITamagotchi"]),
    ],
    dependencies: [],
    targets: [
        .target(
            name: "AITamagotchi",
            dependencies: []),
        .testTarget(
            name: "AITamagotchiTests",
            dependencies: ["AITamagotchi"]),
    ]
)