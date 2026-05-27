<!-- refreshed: 2026-05-27 -->
# Architecture

**Analysis Date:** 2026-05-27

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                    Flutter App (lib/)                        │
│                  Entry: lib/main.dart                        │
├──────────────────┬──────────────────┬───────────────────────┤
│   screens/       │   widgets/       │    providers/         │
│  (pages/UI)      │  (reusable UI)   │  (state management)   │
└────────┬─────────┴────────┬─────────┴──────────┬────────────┘
         │                  │                     │
         ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      services/                               │
│              (API calls, business logic)                     │
│              lib/services/api_service.dart                   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                      models/                                 │
│           (data classes: User, Dish, Review, etc.)           │
│                   lib/models/                                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (external)                      │
│         http://server/api/v1  — REST + JWT                   │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| MyApp | Root widget, theme, routing | `lib/main.dart` |
| screens/ | Full-page UI for each feature | `lib/screens/` (planned) |
| widgets/ | Reusable UI components | `lib/widgets/` (planned) |
| providers/ | State management via Provider | `lib/providers/` (planned) |
| services/ | HTTP client, API abstraction | `lib/services/` (planned) |
| models/ | Data transfer objects (DTOs) | `lib/models/` (planned) |

## Pattern Overview

**Overall:** Layered MVC-style Flutter architecture with Provider state management

**Key Characteristics:**
- Single entry point at `lib/main.dart` — `runApp(const MyApp())`
- Provider package for state management (UserProvider, DishProvider)
- Centralized `ApiService` class for all HTTP communication
- Screens consume providers; providers consume services; services consume models
- JWT token persisted via `shared_preferences`, attached to every API request

## Layers

**Presentation Layer:**
- Purpose: Render UI, handle user interactions
- Location: `lib/screens/`, `lib/widgets/`
- Contains: StatelessWidget and StatefulWidget subclasses, screen-level logic
- Depends on: providers/, widgets/
- Used by: Nothing (top of the tree)

**State Management Layer:**
- Purpose: Hold and expose application state to the widget tree
- Location: `lib/providers/` (planned)
- Contains: ChangeNotifier subclasses (UserProvider, DishProvider)
- Depends on: services/, models/
- Used by: screens/

**Service Layer:**
- Purpose: Encapsulate all network calls and external integrations
- Location: `lib/services/` (planned)
- Contains: ApiService (HTTP), image upload helpers, FCM integration
- Depends on: models/
- Used by: providers/

**Model Layer:**
- Purpose: Define data structures matching the backend API
- Location: `lib/models/` (planned)
- Contains: User, Dish, Review, Canteen, Window, Wish data classes with fromJson/toJson
- Depends on: Nothing (pure Dart)
- Used by: services/, providers/

## Data Flow

### Primary Request Path

1. User taps UI element in a screen (`lib/screens/dish_detail_screen.dart`)
2. Screen calls a method on the relevant Provider via `context.read<DishProvider>()`
3. Provider calls `ApiService` method (e.g., `ApiService.getDishReviews(dishId)`)
4. `ApiService` makes HTTP GET to `http://server/api/v1/dishes/{id}/reviews` with JWT header
5. Response JSON is deserialized into `Review` model objects
6. Provider updates its state and calls `notifyListeners()`
7. Widgets listening via `context.watch<DishProvider>()` rebuild

### Authentication Flow

1. User submits credentials on `lib/screens/login_screen.dart`
2. `UserProvider.login()` calls `ApiService.login(email, password)`
3. Backend returns JWT `access_token`
4. Token stored in `shared_preferences` via `UserProvider`
5. All subsequent `ApiService` calls attach `Authorization: Bearer <token>` header
6. On app start, `main.dart` checks `shared_preferences` for existing token to auto-login

### Recommendation Flow

1. Home screen requests recommendations from `UserProvider` or dedicated `RecommendProvider`
2. Provider calls `ApiService.getRecommendations()`
3. Backend computes content-based recommendations (tag cosine similarity)
4. Returns up to 10 `Dish` objects with recommendation scores
5. Home screen renders recommendation cards

**State Management:**
- Provider package (`ChangeNotifier` + `ChangeNotifierProvider`)
- `UserProvider`: auth state, JWT token, user preferences
- `DishProvider`: current window's dish list, dish detail cache
- State persisted across sessions via `shared_preferences` (JWT token only)

## Key Abstractions

**ApiService:**
- Purpose: Single HTTP client wrapping all backend endpoints
- Examples: `lib/services/api_service.dart` (planned)
- Pattern: Class with static or instance methods per endpoint group; baseURL + timeout + auth header configured once

**Provider classes:**
- Purpose: Observable state containers bridging services and UI
- Examples: `lib/providers/user_provider.dart`, `lib/providers/dish_provider.dart` (planned)
- Pattern: `ChangeNotifier` subclass; exposes getters for state, async methods for mutations

**Model classes:**
- Purpose: Typed representations of backend JSON payloads
- Examples: `lib/models/dish.dart`, `lib/models/review.dart`, `lib/models/user.dart` (planned)
- Pattern: Dart class with `fromJson(Map<String, dynamic>)` factory and `toJson()` method

## Entry Points

**App Entry:**
- Location: `lib/main.dart`
- Triggers: `flutter run` / app launch
- Responsibilities: Initialize Flutter binding, set up Provider tree, configure MaterialApp theme and routing

**Android Native Entry:**
- Location: `android/app/src/main/kotlin/com/example/what_to_eat_today/MainActivity.kt`
- Triggers: Android OS launches the app
- Responsibilities: Extends `FlutterActivity`, delegates everything to Flutter engine

## Architectural Constraints

- **Threading:** Flutter single-threaded UI with async/await for I/O; no isolates planned
- **Global state:** Provider tree at root of widget tree; no module-level singletons except `ApiService` instance
- **Circular imports:** Not applicable — layers have clear one-way dependency direction
- **Platform targets:** Android and iOS primary; web, Windows, macOS, Linux scaffolded but not targeted

## Anti-Patterns

### Direct HTTP calls from widgets

**What happens:** A screen widget calls `http.get()` directly in `initState` or `build`
**Why it's wrong:** Mixes UI and network concerns; untestable; no shared state
**Do this instead:** Call a Provider method from the screen; let the Provider call `ApiService`

### Storing JWT in plain SharedPreferences without expiry check

**What happens:** Token is read from `shared_preferences` and used without checking `exp` claim
**Why it's wrong:** Expired tokens cause 401 errors mid-session with no graceful recovery
**Do this instead:** Decode the JWT `exp` field on read; redirect to login if expired; see `开发指南-v1.md` §11 Q6

### setState for cross-widget state

**What happens:** `setState` used in a screen to update data that other screens also need
**Why it's wrong:** State is lost on navigation; sibling screens cannot access it
**Do this instead:** Lift state into a `ChangeNotifier` Provider registered above the navigator

## Error Handling

**Strategy:** Centralized in `ApiService`; propagated as exceptions or null returns to Providers; Providers expose error state to UI

**Patterns:**
- `ApiService` catches HTTP errors and throws typed exceptions (e.g., `AuthException`, `NetworkException`)
- Providers catch exceptions from service calls and set an `errorMessage` field
- Screens check Provider error state and show `SnackBar` or inline error widgets
- Loading states tracked with `isLoading` boolean in each Provider

## Cross-Cutting Concerns

**Logging:** `debugPrint()` during development; no structured logging library planned
**Validation:** Client-side form validation in screens before API calls; server-side validation enforced by FastAPI
**Authentication:** JWT Bearer token attached by `ApiService` to all non-auth endpoints; `UserProvider` manages token lifecycle

---

*Architecture analysis: 2026-05-27*
