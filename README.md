# OktaVerse

`OktaVerse` is a unified toolkit for Okta environment analysis, documentation, comparison, and migration.

This repository currently includes multiple utilities under the `OktaVerse` umbrella:

- `OktaCompare`: Compare configuration between two Okta environments and generate a report + CSV export.
- `OktaSnapshot`: Capture and export a structured snapshot of a single Okta org's configuration.
- `OktaEvaluate`: Assessment/readiness utility (currently a placeholder page in this codebase).
- `OktaMigrate`: Migration workflow utility (currently a placeholder page in this codebase).

## OktaVerse Structure

- `OktaCompare` (`/`): Main comparison workflow with report generation and CSV exports.
- `OktaSnapshot` (`/snapshot`): Snapshot guide generation with PDF and DOCX export support.
- `OktaEvaluate` (`/evaluate`): Placeholder route for evaluation workflows.
- `OktaMigrate` (`/migrate`): Placeholder route for migration workflows.

## OktaCompare

Compare configuration between two Okta environments and generate a report + CSV export.

## Docker

You can run `OktaVerse` locally in Docker.

### Prerequisites
- Docker installed and running

### 1. Build the image
```bash
docker build -t oktaverse .
```

### 2. Run the container
```bash
docker run --rm -p 5000:5000 --name oktaverse oktaverse
```

### 3. Open the app
- `http://localhost:5000` (`OktaCompare`)
- `http://localhost:5000/snapshot` (`OktaSnapshot`)
- `http://localhost:5000/evaluate` (`OktaEvaluate`)
- `http://localhost:5000/migrate` (`OktaMigrate`)

### Useful Docker commands

Run in detached mode:
```bash
docker run -d --rm -p 5000:5000 --name oktaverse oktaverse
```

View logs:
```bash
docker logs -f oktaverse
```

Stop the container:
```bash
docker stop oktaverse
```

Use a different host port (example: `8080`):
```bash
docker run --rm -p 8080:5000 --name oktaverse oktaverse
```
Then open `http://localhost:8080`.

Notes:
- The app runs on port `5000` inside the container.
- PDF export (`OktaSnapshot`) is intended to work in Docker because the image installs the required system libraries for `WeasyPrint`.

## OktaCompare Legend
- Critical: high-risk mismatch or missing object in an environment.
- Medium: configuration mismatch for a matched object.
- Low: extra object found in one environment.
- Match: values are identical.

## OktaCompare Entities and Compared Parameters

| Entity | Key / Matching Strategy | Compared Parameters / Notes |
|---|---|---|
| Groups | Group profile name | Description |
| Group Rules | Rule name (group IDs in expressions normalized to group names) | Condition expression |
| Network Zones | Zone name | Type, gateways, proxies, locations, status |
| Applications | App label/name | Existence; group assignments only if `compare_group_assignments=True` |
| Authenticators | Authenticator key/name | Name, type, status |
| Authenticator Enrollment Policies | Policy name | Rule signature (name, status, priority, conditions, actions); mismatch if any rule differs |
| Password Policies | Policy name | Rule signature (name, status, priority, conditions, actions); mismatch if any rule differs |
| App Sign-On Policies | Policy name | Rule signature (name, status, priority, conditions, actions); mismatch if any rule differs |
| IDP Discovery Policies | Policy name | Rule-by-rule comparison (status, conditions, actions) for matching rule names |
| Profile Enrollment Policies | Policy name | Rule signature (name, status, priority, conditions, actions); mismatch if any rule differs |
| Brand Settings | Brand name | Brand properties (`name`, `removePoweredByOkta`, privacy policy fields, `isDefault`) and theme properties (logo/colors/page variants/assets) |
| Brand Pages | Brand name | Sign-in page `pageContent` HTML; error page settings signature (IDs/links excluded); widget customization diffs logged |
| Brand Email Templates | Brand name + template name | Customization subject and body/`htmlBody` |
| Authorization Servers - Settings | Authorization server name | Server settings, claims list, scopes list (IDs/links/timestamps excluded) |
| Authorization Servers - Access Policies | Authorization server name + policy name | Rule signature (name, status, priority, conditions, actions) |
| Custom Admin Roles | Role label/name | Role settings signature (IDs/links/timestamps excluded) |
| Resource Sets | Resource set label/name | Resource set settings signature (IDs/links/timestamps excluded) |
| Admin Assignments | Set comparison (users/groups/apps) | Admin users (`login/email/displayName/userId`), admin groups (`name/groupId`), admin apps (`displayName/appInstanceId`) |
| API Tokens | Token name | Network settings |
| Security General Settings | Sanitized settings object | Threats config, ThreatInsight, security notifications, captcha, user enumeration, user lockout, authenticator settings (IDs/links/timestamps excluded) |
| Org General Settings | `/api/v1/org` (sanitized) | All fields except `id`, `_links`, `created`, `lastUpdated`, `expiresAt`, `subdomain` |
| Identity Providers | IdP name | Status, `protocol.type`, sanitized policy |
| Realms | Realm name/label/displayName | Realm settings signature (IDs/links/timestamps excluded) |
| Realm Assignments | Assignment name/label/displayName | Status, conditions, actions, domains, `isDefault`, priority |
| Profile Schema - User | Attribute name | Full user profile attribute settings (base + custom schemas) |
| Profile Mappings | `source.name -> target.name` (IdP app user mappings only) | Property mappings (`targetField`, source expression, `pushStatus`) |
| Trusted Origins | Origin name (or URL) | Settings signature (IDs/links/timestamps excluded) |

## OktaSnapshot Extracted Entities

| OktaSnapshot Section | Type | Notes |
|---|---|---|
| Organization Settings | Extracted | Key-value settings from org configuration |
| Security General Settings | Extracted | Security settings rows |
| Groups | Extracted | Group inventory for snapshot guide/export |
| Group Rules | Extracted | Rule inventory/details |
| Network Zones | Extracted | Zone definitions |
| Identity Providers | Extracted | IdP configurations |
| Authenticators | Extracted | Authenticator inventory/settings |
| Authorization Servers - Settings | Extracted | Authorization server settings entries |
| Authorization Server Claims | Extracted | Claims inventory |
| Authorization Server Scopes | Extracted | Scopes inventory |
| Authorization Servers - Access Policies | Extracted | Policies and rules combined in one section (`Entry Type`) |
| Applications | Extracted | Application inventory/details |
| Password Policies | Extracted | Policies and rules combined (`Entry Type`) |
| Global Session Policies | Extracted | Policies and rules combined (`Entry Type`) |
| Authentication Policies | Extracted | Policies and rules combined (`Entry Type`) |
| MFA Enrollment Policies | Extracted | Policies and rules combined (`Entry Type`) |
| IDP Discovery Policies | Extracted | Policies and rules combined (`Entry Type`) |
| Profile Enrollment Policies | Extracted | Policies and rules combined (`Entry Type`) |
| Brand Settings | Extracted | Brand/theme settings rows |
| Brand Pages | Extracted | Brand page content/settings rows |
| Brand Email Templates | Extracted | Template customization rows |
| Custom Admin Roles | Extracted | Role definitions |
| Resource Sets | Extracted | Resource sets, resources, and bindings combined (`Entry Type`) |
| Admin Assignments - Users | Extracted | Admin user assignments |
| Admin Assignments - Groups | Extracted | Admin group assignments |
| Admin Assignments - Apps | Extracted | Admin app assignments |
| API Tokens | Extracted | Token inventory/settings |
| Realms | Extracted | Realm definitions |
| Realm Assignments | Extracted | Realm assignment rows |
| Profile Schema - User | Extracted | User schema attributes |
| Profile Mappings | Extracted | Mapping rows (filtered snapshot view) |
| Trusted Origins | Extracted | Trusted origin rows |

## OktaCompare Export Behavior
- Triggered by the “Export Comparison Report” button on the report page.
- Exports a CSV with columns: Category, Object, Attribute, Env A Value, Env B Value, Difference Type, Impact, Recommended Action, Priority.
- Priority values are text only (Critical/Medium/Low/Match); icons are not included.
- Export is generated in-memory from the latest comparison run and is not persisted.
