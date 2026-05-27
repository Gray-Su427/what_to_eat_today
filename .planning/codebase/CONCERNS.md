# Codebase Concerns

**Analysis Date:** 2026-05-27

## Tech Debt

**Unimplemented application — scaffold only:**
- Issue: `lib/main.dart` contains the default Flutter counter demo, not the actual "今天吃什么" app. The entire planned feature set (canteen browsing, dish reviews, recommendations, auth) has zero implementation.
- Files: `lib/main.dart`
- Impact: Nothing in the planned product exists in code yet. All development work is ahead.
- Fix approach: Replace `lib/main.dart` with the actual app entry point and build out the `lib/` structure described in `开发指南-v1.md` section 6.1.

**No project structure in place:**
- Issue: The `lib/` directory contains only `main.dart`. The planned directories (`models/`, `services/`, `providers/`, `screens/`, `widgets/`) do not exist.
- Files: `lib/`
- Impact: No feature code can be written without first establishing the directory layout.
- Fix approach: Create the directory skeleton from `开发指南-v1.md` section 6.1 before any feature work begins.

**App title and branding not set:**
- Issue: `main.dart` uses `'Flutter Demo'` as the app title and `'Flutter Demo Home Page'` as the home page title. The app name in `pubspec.yaml` is the snake_case package identifier `what_to_eat_today`, not a display name.
- Files: `lib/main.dart`, `pubspec.yaml`
- Impact: Any build or demo will show generic Flutter branding.
- Fix approach: Set `title: '今天吃什么'` in `MaterialApp` and update `pubspec.yaml` `description` field.

**README not updated:**
- Issue: `README.md` is the default Flutter starter README with no project-specific content.
- Files: `README.md`
- Impact: New team members have no onboarding information from the README itself (the guide is in `开发指南-v1.md` instead).
- Fix approach: Replace with project-specific setup instructions, or at minimum add a pointer to `开发指南-v1.md`.

## Known Bugs

**ColorScheme constructor call is incomplete:**
- Symptoms: `lib/main.dart` line 31 calls `.fromSeed(seedColor: Colors.deepPurple)` without the `ColorScheme` prefix — this is a display artifact from the file read, but should be verified as `ColorScheme.fromSeed(...)` in the actual file.
- Files: `lib/main.dart`
- Trigger: Build / `flutter analyze`
- Workaround: Confirm the actual source; if the prefix is missing the app will not compile.

**MainAxisAlignment constructor call is incomplete:**
- Symptoms: `lib/main.dart` line 105 calls `.center` without the `MainAxisAlignment` prefix — same issue as above.
- Files: `lib/main.dart`
- Trigger: Build / `flutter analyze`
- Workaround: Confirm the actual source; if the prefix is missing the app will not compile.

## Security Considerations

**JWT token storage plan uses SharedPreferences:**
- Risk: `开发指南-v1.md` section 6.2 specifies storing the JWT token in `shared_preferences`. On Android, SharedPreferences is stored in plaintext XML and is accessible to other apps on rooted devices. On iOS it maps to NSUserDefaults, which is not encrypted.
- Files: Not yet implemented — risk is in the design document `开发指南-v1.md`
- Current mitigation: None — not yet implemented.
- Recommendations: Use `flutter_secure_storage` instead. It uses Android EncryptedSharedPreferences and iOS Keychain. This is a one-package swap with no API complexity increase.

**No HTTPS enforcement planned for development:**
- Risk: `开发指南-v1.md` section 5.1 specifies `http://服务器地址:端口/api/v1` as the base URL format. Using plain HTTP exposes JWT tokens and user data in transit.
- Files: Not yet implemented — risk is in the design document `开发指南-v1.md`
- Current mitigation: None.
- Recommendations: Use HTTPS from day one, even in development (self-signed cert or ngrok's HTTPS tunnel). Configure Android `network_security_config.xml` to block cleartext traffic in release builds.

**Password hashing algorithm not enforced in client:**
- Risk: The guide specifies bcrypt via `passlib` on the backend, but there is no mention of minimum password length or complexity validation on the Flutter side. Weak passwords will be accepted and hashed.
- Files: Not yet implemented.
- Current mitigation: None.
- Recommendations: Add client-side password length validation (minimum 8 characters) before the registration API call.

**Image upload via third-party image hosting (sm.ms fallback):**
- Risk: `开发指南-v1.md` section 11 Q4 suggests using a free public image bed (sm.ms) as a fallback. This means user-uploaded review images would be stored on a third-party service with no access control, and URLs would be permanent and public.
- Files: Not yet implemented.
- Current mitigation: None.
- Recommendations: Use the planned OSS solution (七牛云/阿里云OSS) from the start. Avoid public image beds for user content.

**No rate limiting mentioned for client-side API calls:**
- Risk: The API design has no mention of rate limiting on the Flutter client side. Rapid repeated taps on submit buttons could send duplicate reviews or spam the recommendation endpoint.
- Files: Not yet implemented.
- Current mitigation: None.
- Recommendations: Debounce submit button actions and disable the button after first tap until the API response returns.

## Performance Bottlenecks

**Recommendation endpoint has no pagination:**
- Problem: `GET /recommend` returns up to 10 items with no pagination or cursor. As the dish catalog grows, the backend cosine similarity computation runs over all dishes on every request.
- Files: Not yet implemented — risk is in the design document `开发指南-v1.md`
- Cause: The algorithm design computes similarity at query time with no caching layer.
- Improvement path: Cache recommendation results per user with a short TTL (e.g., 5 minutes). Precompute dish tag vectors at write time rather than at query time.

**No image caching strategy defined for the counter demo:**
- Problem: The current `main.dart` has no images, but the planned app will load dish images and review photos. The guide mentions `cached_network_image` but does not specify cache size limits or eviction policy.
- Files: Not yet implemented.
- Cause: Not yet designed.
- Improvement path: Set explicit cache size and max age when configuring `cached_network_image` to avoid unbounded disk growth on devices.

**1C2G server for all workloads:**
- Problem: The planned deployment target is a 1-core 2GB RAM student server running PostgreSQL, FastAPI (Gunicorn + Uvicorn), and Nginx simultaneously.
- Files: `开发指南-v1.md` section 3.2
- Cause: Budget constraint.
- Improvement path: Acceptable for demo/MVP with low concurrent users. Monitor memory usage. If PostgreSQL and Gunicorn workers compete for RAM, reduce Gunicorn worker count to 2 and tune PostgreSQL `shared_buffers` to 256MB.

## Fragile Areas

**Single-file architecture:**
- Files: `lib/main.dart`
- Why fragile: All current code (app root, theme, home page, state) is in one file. As features are added, this will become a merge conflict hotspot for the 4-person team.
- Safe modification: Immediately split into `lib/app.dart` (MaterialApp), `lib/screens/home_screen.dart`, and keep `lib/main.dart` as the entry point only.
- Test coverage: Only one smoke test in `test/widget_test.dart` covering the counter widget, which will be deleted when the real app is built.

**No error handling layer:**
- Files: `lib/main.dart` (no network layer exists yet)
- Why fragile: The guide mentions wrapping API calls in an `ApiService` class but provides no error handling contract. Without a defined error model, each screen will handle errors differently or not at all.
- Safe modification: Define a sealed `ApiResult<T>` type or use a consistent `try/on` pattern before writing any screen that calls the backend.
- Test coverage: None.

**FCM integration in China:**
- Files: Not yet implemented — `开发指南-v1.md` section 11 Q5
- Why fragile: Firebase Cloud Messaging is unreliable in mainland China. The guide acknowledges this but lists it as a known risk without a committed fallback.
- Safe modification: Decide on 极光推送 or 腾讯云移动推送 before starting push notification work. Switching push providers mid-implementation requires changes to both the Flutter client and the FastAPI backend.
- Test coverage: None.

## Scaling Limits

**PostgreSQL on student server:**
- Current capacity: 1 core, 2GB RAM, shared with app server and Nginx.
- Limit: Estimated ~50 concurrent connections before memory pressure causes slowdowns. With default PostgreSQL settings and Gunicorn workers each holding a connection, this can be reached quickly.
- Scaling path: Use a connection pooler (PgBouncer) in front of PostgreSQL. For the demo/MVP scale (tens of users), this is not urgent but should be planned before the roadshow.

**No database indexing implemented yet:**
- Current capacity: The guide recommends indexes on `dishes.window_id`, `reviews.dish_id`, and `reviews.user_id` but these are not yet created.
- Limit: Full table scans on `reviews` will degrade as review count grows. With 30 dishes and a small user base this is invisible, but will surface during load testing.
- Scaling path: Add the recommended indexes at table creation time, not retroactively.

## Dependencies at Risk

**No state management library added:**
- Risk: `pubspec.yaml` lists only `flutter`, `cupertino_icons`, and dev dependencies. The guide specifies `provider` for state management but it is not in `pubspec.yaml`. The app cannot be built without it.
- Impact: All planned screens that depend on `UserProvider` or `DishProvider` will fail to compile.
- Migration plan: Add `provider: ^6.1.2` to `pubspec.yaml` dependencies immediately.

**No HTTP client library added:**
- Risk: `dio` or `http` is required for all API calls but neither is in `pubspec.yaml`.
- Impact: The `ApiService` class cannot be implemented.
- Migration plan: Add `dio: ^5.7.0` (preferred for interceptors, timeout config, and error handling) or `http: ^1.2.2`.

**No image libraries added:**
- Risk: `cached_network_image`, `image_picker`, and `flutter_rating_bar` are all mentioned in the guide but absent from `pubspec.yaml`.
- Impact: Dish image display, review photo upload, and star rating UI cannot be built.
- Migration plan: Add all three to `pubspec.yaml` before starting screen implementation.

**No secure storage library added:**
- Risk: `flutter_secure_storage` is not in `pubspec.yaml`. If the team follows the guide's `shared_preferences` recommendation instead, JWT tokens will be stored insecurely.
- Impact: Security risk on production builds.
- Migration plan: Add `flutter_secure_storage: ^9.2.2` and use it for token storage from the first auth implementation.

**Flutter SDK constraint uses a pre-release version:**
- Risk: `pubspec.lock` specifies `flutter: ">=3.18.0-18.0.pre.54"` as the minimum Flutter SDK. This is a pre-release version constraint, which may cause issues if team members install different stable Flutter versions.
- Impact: Potential build inconsistencies across team members' machines.
- Migration plan: After confirming the stable Flutter version in use, update the constraint to a stable release (e.g., `>=3.27.0`).

## Missing Critical Features

**No authentication implementation:**
- Problem: JWT-based auth is P0 (required for Demo on June 10) but no auth code exists.
- Blocks: Review submission, personal center, preference saving — all require a logged-in user.

**No network layer:**
- Problem: No `ApiService` or HTTP client setup exists. All screens that fetch data are blocked.
- Blocks: Every screen in the planned app.

**No data models:**
- Problem: No `User`, `Dish`, `Review`, `Canteen`, or `Window` model classes exist.
- Blocks: Cannot write any screen, service, or provider without these.

**No navigation setup:**
- Problem: No named routes or navigation library (go_router or Navigator 2.0) is configured.
- Blocks: Multi-screen app flow cannot be built.

## Test Coverage Gaps

**Only one smoke test, covering deleted functionality:**
- What's not tested: Everything. The single test in `test/widget_test.dart` tests the counter demo widget, which will be removed when real development begins.
- Files: `test/widget_test.dart`
- Risk: Any regression in future code will go undetected. The team has no test infrastructure for the actual app.
- Priority: High — establish test structure before writing feature code.

**No unit tests for planned business logic:**
- What's not tested: Recommendation algorithm (cosine similarity), badge threshold logic (score ≥ 4.5 and count ≥ 5), preference weight update logic.
- Files: None exist yet.
- Risk: The recommendation algorithm is the core differentiator. Bugs in the similarity calculation or weight update will silently produce wrong recommendations.
- Priority: High — write unit tests for the recommendation logic as it is implemented.

**No integration tests planned:**
- What's not tested: API contract between Flutter client and FastAPI backend.
- Files: `integration_test/` directory does not exist.
- Risk: Breaking API changes will only be caught during manual testing.
- Priority: Medium — add at least one integration test covering the login → browse → review flow before the roadshow.

---

*Concerns audit: 2026-05-27*
