# External Integrations

**Analysis Date:** 2026-05-27

## APIs & External Services

None detected. The current codebase is a Flutter scaffold (default counter app in `lib/main.dart`) with no calls to external APIs or third-party SDKs beyond the Flutter framework itself.

## Data Storage

**Databases:**
- None. No local database package (`sqflite`, `drift`, `hive`, `isar`, etc.) is declared in `pubspec.yaml`.

**File Storage:**
- None. No file I/O or asset storage beyond bundled icon assets.

**Caching:**
- None. No caching layer (`shared_preferences`, `flutter_cache_manager`, etc.) is present.

## Authentication & Identity

**Auth Provider:**
- None. No authentication package (`firebase_auth`, `supabase_flutter`, `google_sign_in`, etc.) is declared.

## Monitoring & Observability

**Error Tracking:**
- None. No crash reporting SDK (`firebase_crashlytics`, `sentry_flutter`, etc.) is present.

**Logs:**
- `debugPrint` / `print` available via Flutter stdlib; no structured logging package configured.

## CI/CD & Deployment

**Hosting:**
- Not configured. No deployment target or hosting platform is set up.

**CI Pipeline:**
- Not detected. No `.github/workflows/`, `.gitlab-ci.yml`, or equivalent CI config files found.

## Environment Configuration

**Required env vars:**
- None currently required by application code.
- Android builds require `flutter.sdk` set in `android/local.properties` (standard Flutter tooling requirement, not application-specific).

**Secrets location:**
- No secrets management in place. Release signing for Android is currently using debug keys (`android/app/build.gradle.kts` — `signingConfig = signingConfigs.getByName("debug")`); a proper signing config must be added before production release.

## Webhooks & Callbacks

**Incoming:**
- None.

**Outgoing:**
- None.

---

*Integration audit: 2026-05-27*
