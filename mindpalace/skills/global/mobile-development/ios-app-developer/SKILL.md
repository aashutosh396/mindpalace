---
name: iOS/macOS App Development (XcodeGen + SwiftUI + SPM)
description: Use when building iOS/macOS apps, fixing Xcode build/signing failures, deploying to devices, or configuring CI/CD signing & notarization — covers XcodeGen project.yml, SPM embedding, code signing errors, and Electron osxSign/notarize traps.
tags: [ios, macos, swiftui, xcodegen, spm, code-signing, notarization, xcode, electron, ci-cd]
source: daymade/claude-code-skills
derived_from: developing-ios-apps
---

# iOS App Development

Build, configure, deploy iOS/macOS apps with XcodeGen + SPM.

## Critical warnings
| Issue | Cause | Fix |
|---|---|---|
| "Library not loaded: @rpath/Framework" | XcodeGen doesn't auto-embed SPM dynamic frameworks | Build in Xcode GUI once (Embed & Sign); CLI then works |
| `xcodegen generate` loses signing | overwrites settings | put signing in target settings, not global |
| CLI signing fails | free Apple ID limit | use Xcode GUI or paid account |
| signed adhoc despite cert | `@electron/packager` defaults `continueOnError: true` | set `continueOnError: false` |
| "Cannot use password credentials..." | passing `teamId` to `@electron/notarize` w/ API key | remove `teamId` — notarytool infers from key |
| EMFILE during signing | osx-sign traverses all bundle files | add `ignore` filter + `ulimit -n 65536` |

## XcodeGen project.yml (minimal)
```yaml
name: AppName
options: { bundleIdPrefix: com.company, deploymentTarget: { iOS: "16.0" } }
settings: { base: { SWIFT_VERSION: "6.0" } }
packages: { SomePackage: { url: https://github.com/org/repo, from: "1.0.0" } }
targets:
  AppName:
    type: application; platform: iOS
    sources: [{ path: AppName }]
    settings: { base: { CODE_SIGN_STYLE: Automatic, DEVELOPMENT_TEAM: TEAM_ID } }
    dependencies: [{ package: SomePackage }]
```
Team ID: `security find-identity -v -p codesigning | head -3`.

## SPM dynamic framework not embedded
Root cause: XcodeGen generates link phase but NOT embed phase for SPM dynamic frameworks (RealmSwift etc.); app builds but crashes at launch (`dyld: Library not loaded`). `embed: true` in project.yml errors. **Fix (one-time)**: Xcode GUI → target → General → Frameworks → change "Do Not Embed" → "Embed & Sign", build from GUI once. After that `xcodebuild` works (persisted in pbxproj). Check dynamic: `file <framework>` → "dynamically linked shared library".

## iOS 16 vs 17 compat
`.onChange { new in }` (16) vs `{ old,new in }` (17); custom VStack vs `ContentUnavailableView`; `AVAudioSession` vs `AVAudioApplication`; `@ObservableObject` vs `@Observable`.

## Camera/AVFoundation (real device only)
Disable automatic mirroring BEFORE setting manual: `connection.automaticallyAdjustsVideoMirroring = false` then `isVideoMirrored = true`. UIViewRepresentable in ZStack needs explicit `.frame` (GeometryReader) or zero bounds. Add `NSCameraUsageDescription`; `startRunning()` on background thread.

## macOS signing + notarization (5 steps)
1. CSR in Keychain Access ("Saved to disk"). 2. Request **Developer ID Application** cert (**G2 Sub-CA**). 3. Install `.cer` to **login keychain** (else Error -25294). 4. Export P12 w/ password, base64. 5. App Store Connect API Key (Developer role), download `.p8` once, record Key ID + Issuer ID.
GitHub secrets (5): `MACOS_CERT_P12`, `MACOS_CERT_PASSWORD`, `APPLE_API_KEY`, `APPLE_API_KEY_ID`, `APPLE_API_ISSUER`. **No `APPLE_TEAM_ID`** — notarytool infers from key.
Electron osxSign: `continueOnError: false` (CRITICAL — default silently adhoc), `hardenedRuntime: true`, `ignore` filter for large runtimes, explicit `keychain` in CI.
Verify: `security find-identity -v -p codesigning | grep "Developer ID Application"`.
