# Technology Stack

**Analysis Date:** 2026-05-27

## Languages

**Primary:**
- Dart 3.x (SDK `^3.12.0`) - All application logic and UI

**Secondary:**
- Kotlin 2.3.20 - Android platform runner (`android/app/src/`)
- Swift 5.0 - iOS platform runner (`ios/Runner/`)
- C++ - Linux and Windows platform runners (`linux/runner/`, `windows/runner/`)

## Runtime

**Environment:**
- Flutter SDK `>=3.18.0-18.0.pre.54` (minimum, resolved from `pubspec.lock`)
- Dart SDK `>=3.12.0 <4.0.0`

**Package Manager:**
- pub (Flutter's package manager, invoked via `flutter pub`)
- Lockfile: `pubspec.lock` present and committed

## Frameworks

**Core:**
- Flutter (latest stable compatible with SDK constraint) - Cross-platform UI framework; Material Design widgets in use

**Testing:**
- `flutter_test` (SDK-bundled) - Widget and unit test runner
- `fake_async` 1.3.3 - Transitive dependency; available for time-controlled async tests

**Build/Dev:**
- Gradle 9.1.0 - Android build system (`android/gradle/wrapper/gradle-wrapper.properties`)
- Android Gradle Plugin (AGP) 9.0.1 - Android app build (`android/settings.gradle.kts`)
- Kotlin Gradle Plugin 2.3.20 - Kotlin compilation for Android runner
- `flutter_lints` ^6.0.0 (dev) - Lint ruleset wrapping `lints` 6.1.0

## Key Dependencies

**Critical:**
- `flutter` (SDK) - Core framework; all UI built on Material widgets
- `cupertino_icons` ^1.0.8 (resolved 1.0.9) - iOS-style icon font for `CupertinoIcons`

**Infrastructure:**
- All other packages in `pubspec.lock` are transitive test/analysis utilities (`leak_tracker`, `matcher`, `collection`, etc.); none are application-level dependencies beyond the above

## Configuration

**Environment:**
- No `.env` files detected
- No `--dart-define` usage detected in current source
- Android `local.properties` (gitignored by default) must contain `flutter.sdk` path for Gradle builds

**Build:**
- `pubspec.yaml` - Flutter/Dart dependency manifest and app metadata
- `pubspec.lock` - Pinned dependency versions
- `analysis_options.yaml` - Dart analyzer config; includes `package:flutter_lints/flutter.yaml`
- `android/build.gradle.kts` - Root Android build config
- `android/app/build.gradle.kts` - App-level Android build config
- `android/settings.gradle.kts` - Android plugin and project settings

## Platform Requirements

**Development:**
- Flutter SDK installed and on PATH
- Android SDK for Android builds (compileSdk via `flutter.compileSdkVersion`, minSdk via `flutter.minSdkVersion`)
- Xcode for iOS/macOS builds
- CMake for Linux/Windows builds
- Java 17+ for Android Gradle compilation (`compileOptions { sourceCompatibility = JavaVersion.VERSION_17 }`)

**Production:**
- Android: `applicationId = "com.example.what_to_eat_today"` (must be changed before release); release signing config is currently using debug keys — signing config must be configured before publishing
- iOS: Bundle ID `com.example.whatToEatToday`, deployment target iOS 13.0
- Web: PWA-capable (`web/manifest.json` present), standalone display mode, theme color `#0175C2`
- Linux: CMake-based runner (`linux/CMakeLists.txt`)
- Windows: CMake-based runner (`windows/CMakeLists.txt`)
- macOS: Xcode-based runner (`macos/Runner/`)

---

*Stack analysis: 2026-05-27*
