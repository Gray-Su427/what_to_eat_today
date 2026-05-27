# Testing Patterns

**Analysis Date:** 2026-05-27

## Overview

The project is at initial Flutter scaffold stage. One test file exists:
`test/widget_test.dart` — the default Flutter counter smoke test. No additional
test infrastructure has been added yet. Patterns below describe what exists plus
the conventions to follow as the project grows (informed by the Dart/Flutter
testing rules and the project's development guide).

## Test Framework

**Runner:**
- `flutter_test` (SDK built-in) — version tied to Flutter SDK
- Config: no separate config file; tests are discovered automatically from `test/`
- Dart SDK: `^3.12.0`

**Assertion Library:**
- `flutter_test` built-in matchers (`expect`, `find`, `findsOneWidget`, etc.)

**Mocking:**
- Not yet added. Planned: `mockito` (with `@GenerateMocks`) or `mocktail` (no codegen)

**Run Commands:**
```bash
flutter test                    # Run all tests
flutter test --watch            # Watch mode (not built-in; use flutter_test_runner or IDE)
flutter test --coverage         # Run with coverage (outputs lcov.info)
flutter analyze                 # Static analysis (lint + type check)
dart format --set-exit-if-changed .  # Format check
```

## Test File Organization

**Location:**
- All tests live under `test/` (co-located with project root, not inside `lib/`)
- Integration tests go in `integration_test/` (separate top-level directory)

**Naming:**
- Test files mirror the source file name with `_test` suffix: `dish_service_test.dart`
- Widget tests: `home_screen_test.dart`, `dish_card_test.dart`

**Planned structure (from Dart testing rules):**
```
test/
├── unit/
│   ├── domain/
│   │   └── usecases/
│   └── data/
│       └── repositories/
├── widget/
│   └── presentation/
│       └── screens/
└── golden/
    └── widgets/

integration_test/
└── flows/
    ├── login_flow_test.dart
    └── review_flow_test.dart
```

## Existing Test

**File:** `test/widget_test.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:what_to_eat_today/main.dart';

void main() {
  testWidgets('Counter increments smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const MyApp());

    // Verify that our counter starts at 0.
    expect(find.text('0'), findsOneWidget);
    expect(find.text('1'), findsNothing);

    // Tap the '+' icon and trigger a frame.
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    // Verify that our counter has incremented.
    expect(find.text('0'), findsNothing);
    expect(find.text('1'), findsOneWidget);
  });
}
```

This is the default scaffold smoke test. It should be replaced with real
application tests as features are built.

## Test Structure

**Suite Organization:**
```dart
group('DishService', () {
  late DishService service;
  late MockApiService mockApi;

  setUp(() {
    mockApi = MockApiService();
    service = DishService(mockApi);
  });

  tearDown(() {
    // cleanup if needed
  });

  test('returns dishes for a given window id', () async {
    // Arrange
    when(mockApi.get('/windows/1/dishes')).thenAnswer((_) async => [...]);

    // Act
    final dishes = await service.getDishesByWindow('1');

    // Assert
    expect(dishes, isNotEmpty);
    expect(dishes.first.windowId, equals('1'));
  });
});
```

**Patterns:**
- AAA (Arrange-Act-Assert) structure for all tests
- `setUp` for shared initialization, `tearDown` for cleanup
- `group` to organize related tests by class or feature
- Descriptive test names that state the behavior: `'returns null when dish does not exist'`

## Widget Tests

**Pattern:**
```dart
testWidgets('DishCard shows badge when score is above 4.5', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: DishCard(dish: testDish.copyWith(averageScore: 4.8, reviewCount: 6)),
    ),
  );

  await tester.pump();
  expect(find.text('🔥'), findsOneWidget);
});
```

**Key APIs:**
- `tester.pumpWidget(...)` — build the widget tree
- `tester.pump()` — trigger a frame (use after interactions)
- `tester.pumpAndSettle()` — wait for all animations to complete
- `find.text(...)`, `find.byType(...)`, `find.byIcon(...)` — finders
- `tester.tap(...)` — simulate tap
- `expect(find.xxx, findsOneWidget)` / `findsNothing` / `findsNWidgets(n)`

## Mocking

**Planned framework:** `mocktail` (preferred — no code generation required) or
`mockito` with `@GenerateMocks`.

**Pattern with mocktail:**
```dart
class MockApiService extends Mock implements ApiService {}

setUp(() {
  mockApi = MockApiService();
  when(() => mockApi.get(any())).thenAnswer((_) async => Response(...));
});
```

**What to mock:**
- `ApiService` — all network calls
- `SharedPreferences` — token storage
- `ImagePicker` — file selection

**What NOT to mock:**
- Domain model classes (`Dish`, `Review`, `User`)
- Pure utility functions
- Flutter framework widgets

## Fakes Over Mocks

For complex dependencies (e.g., repositories), prefer hand-written fakes:

```dart
class FakeDishRepository implements DishRepository {
  final _dishes = <String, Dish>{};

  @override
  Future<List<Dish>> getByWindow(String windowId) async =>
      _dishes.values.where((d) => d.windowId == windowId).toList();

  @override
  Future<Dish?> getById(String id) async => _dishes[id];

  void addDish(Dish dish) => _dishes[dish.id] = dish;
}
```

## Async Testing

```dart
test('ApiService throws NetworkException on timeout', () async {
  // Arrange
  final service = ApiService(baseUrl: 'http://localhost:9999');

  // Act & Assert
  expect(
    () => service.get('/dishes'),
    throwsA(isA<NetworkException>()),
  );
});
```

For timer-based logic, use `fake_async` package (add to `dev_dependencies`):
```dart
test('debounce fires after 300ms', () {
  fakeAsync((async) {
    // ... control time explicitly
    async.elapse(const Duration(milliseconds: 300));
    expect(callCount, 1);
  });
});
```

## Test Types

**Unit Tests:**
- Scope: domain logic, `ApiService`, `Provider` state transitions, model `fromJson`/`toJson`
- Location: `test/unit/`
- No Flutter framework dependency — use `dart:test` directly

**Widget Tests:**
- Scope: all screens and reusable widgets with meaningful behavior
- Location: `test/widget/`
- Use `flutter_test` and `WidgetTester`
- Wrap with `MaterialApp` or `ProviderScope` as needed

**Golden Tests:**
- Scope: design-critical components (dish card, rating badge, review tile)
- Location: `test/golden/`
- Update with `flutter test --update-goldens` when intentional visual changes are made

**Integration Tests:**
- Scope: critical user flows on real device/emulator
- Location: `integration_test/`
- Framework: `integration_test` package (add to `dev_dependencies`)
- Key flows to cover: login, browse dishes, submit review, view recommendations

## Coverage

**Requirements:** 80%+ line coverage for business logic (domain + state managers)

**View Coverage:**
```bash
flutter test --coverage
# Generates coverage/lcov.info
# View with lcov or genhtml:
genhtml coverage/lcov.info -o coverage/html
```

**All state transitions must have tests:**
- loading → success
- loading → error
- retry behavior

## Test Naming

Use descriptive, behavior-focused names:

```dart
test('returns empty list when window has no active dishes', () { ... });
test('throws NotFoundException when dish id does not exist', () { ... });
testWidgets('shows loading indicator while fetching dishes', (tester) async { ... });
testWidgets('disables submit button when review text is empty', (tester) async { ... });
```

---

*Testing analysis: 2026-05-27*
