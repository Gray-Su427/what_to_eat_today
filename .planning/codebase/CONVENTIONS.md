# Coding Conventions

**Analysis Date:** 2026-05-27

## Overview

This is a Flutter/Dart project at initial scaffold stage. The codebase currently contains
only `lib/main.dart` (the default Flutter counter demo). The development guide
(`开发指南-v1.md`) defines the planned architecture and conventions to follow as the
project grows. Conventions below reflect both what exists and what is prescribed by the
project's planned structure.

## Naming Patterns

**Files:**
- `snake_case` for all Dart files: `home_screen.dart`, `dish_detail_screen.dart`, `api_service.dart`
- Screens suffixed with `_screen`: `canteen_list_screen.dart`, `write_review_screen.dart`
- Widgets suffixed with `_widget` or descriptive noun: `rating_card.dart`, `review_tile.dart`
- Models named after the domain entity: `dish.dart`, `review.dart`, `user.dart`
- Services suffixed with `_service`: `api_service.dart`
- Providers suffixed with `_provider`: `user_provider.dart`, `dish_provider.dart`

**Classes:**
- `PascalCase` for all classes, widgets, enums, and typedefs
- State classes prefixed with `_` and suffixed with `State`: `_MyHomePageState`
- Private members prefixed with `_`: `_counter`, `_incrementCounter()`

**Functions and Variables:**
- `camelCase` for all functions, methods, and local variables
- Private methods prefixed with `_`: `_incrementCounter()`
- Boolean variables prefixed with `is`, `has`, `can`, or `should`

**Constants:**
- `SCREAMING_SNAKE_CASE` for top-level `const` values

## Code Style

**Formatting:**
- Tool: `dart format` (enforced via `flutter analyze`)
- Line length: 80 characters (dart format default)
- Trailing commas on multi-line argument/parameter lists

**Linting:**
- Tool: `flutter_lints ^6.0.0` via `analysis_options.yaml`
- Ruleset: `package:flutter_lints/flutter.yaml` (recommended Flutter lint set)
- Run: `flutter analyze`
- No custom lint overrides are active (all commented out in `analysis_options.yaml`)

**Key enforced rules from flutter_lints:**
- `avoid_print` — use a proper logger, not `print()`
- `prefer_const_constructors` — use `const` wherever possible
- `unused_import` — no dead imports

## Import Organization

**Order:**
1. `dart:` core libraries (`dart:async`, `dart:convert`)
2. External `package:` imports (`package:flutter/material.dart`, `package:dio/dio.dart`)
3. Internal `package:` imports using the package name (`package:what_to_eat_today/models/dish.dart`)

**Path style:**
- Use `package:` imports throughout — never relative `../` imports for cross-feature code
- Current example in `lib/main.dart`: `import 'package:flutter/material.dart';`

## Widget Patterns

**StatelessWidget:**
- Use `const` constructor with `super.key`
- Example from `lib/main.dart`:
  ```dart
  class MyApp extends StatelessWidget {
    const MyApp({super.key});
  }
  ```

**StatefulWidget:**
- Widget class holds only `final` configuration fields
- State class holds mutable state and logic
- Example from `lib/main.dart`:
  ```dart
  class MyHomePage extends StatefulWidget {
    const MyHomePage({super.key, required this.title});
    final String title;
    @override
    State<MyHomePage> createState() => _MyHomePageState();
  }
  ```

**State mutations:**
- Always wrap mutations in `setState(() { ... })`
- Keep `setState` bodies minimal — only the mutation, not derived logic

## Immutability

- Prefer `final` for local variables
- Use `const` constructors wherever all fields are `final`
- Widget fields are always `final` (enforced by Flutter framework convention)
- Use `copyWith()` for state mutations in immutable state classes (planned for models)

## Null Safety

- Project targets Dart SDK `^3.12.0` — full sound null safety
- Avoid `!` (bang operator); prefer `?.`, `??`, or null guards
- Use `required` for constructor parameters that must always be provided

## Error Handling

- Specify exception types in `on` clauses — never bare `catch (e)`
- Network errors should be caught at the service layer (`ApiService`) and surfaced
  as typed results or error states to the UI
- Never silently swallow exceptions

## Logging

**Framework:** `print()` is present in the scaffold but `avoid_print` lint is active.
Use a proper logging package (e.g., `logger`) for production code.

**Patterns:**
- Do not log sensitive data (tokens, passwords)
- Log errors with context at the service layer

## Comments

**When to Comment:**
- Explain non-obvious business logic (e.g., recommendation score formula)
- Document public API methods with doc comments (`///`)
- The scaffold uses inline `//` comments to explain Flutter concepts — remove these
  from production code

**Style:**
- Doc comments use `///` (triple-slash), not `/** */`
- Inline comments use `//`

## Planned Directory Structure (from `开发指南-v1.md`)

```
lib/
├── models/       # Data model classes (User, Dish, Review, etc.)
├── services/     # Network request wrappers (ApiService)
├── providers/    # State management (UserProvider, DishProvider)
├── screens/      # Full-page widgets
│   ├── home_screen.dart
│   ├── canteen_list_screen.dart
│   ├── window_dishes_screen.dart
│   ├── dish_detail_screen.dart
│   ├── write_review_screen.dart
│   └── profile_screen.dart
├── widgets/      # Reusable components (rating stars, review cards)
└── main.dart
```

## State Management

**Chosen approach:** `Provider` package (planned, not yet added to `pubspec.yaml`)
- `UserProvider` — login state and user info
- `DishProvider` — current window's dish list
- Providers are registered at the widget tree root in `main.dart`

## Network Layer

**Planned pattern:** A single `ApiService` class in `lib/services/api_service.dart`
- Handles base URL, timeouts, JWT token attachment, and error handling
- Uses `http` or `dio` package (not yet added)
- All API calls go through this class — no direct HTTP calls in widgets or providers

---

*Convention analysis: 2026-05-27*
