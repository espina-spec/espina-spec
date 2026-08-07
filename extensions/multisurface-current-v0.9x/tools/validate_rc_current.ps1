param(
    [Parameter(Mandatory = $true)]
    [string]$ExamplePath
)

$ErrorActionPreference = "Stop"
$checks = New-Object System.Collections.Generic.List[object]

function Add-Check {
    param([string]$Name, [bool]$Ok, [string]$Detail)
    $script:checks.Add([pscustomobject]@{
        name = $Name
        ok = $Ok
        detail = $Detail
    }) | Out-Null
}

function Read-JsonFile {
    param([string]$Path)
    if (-not (Test-Path -Path $Path)) {
        throw "Missing file: $Path"
    }
    return Get-Content -Raw -Path $Path | ConvertFrom-Json
}

function Has-Property {
    param([object]$Object, [string]$Name)
    return $null -ne $Object.PSObject.Properties[$Name]
}

$worldRegistryPath = Join-Path $ExamplePath "espina\world_registry.json"
$surfaceRegistryPath = Join-Path $ExamplePath "espina\surface_registry.json"
$currentContractPath = Join-Path $ExamplePath "espina\current_contract.json"
$currentPointerPath = Join-Path $ExamplePath "current\CURRENT_POINTER.json"
$currentStatePath = Join-Path $ExamplePath "current\state\CURRENT_STATE.json"
$continuityPath = Join-Path $ExamplePath "current\state\CONTINUITY_STATUS.json"
$eventsDir = Join-Path $ExamplePath "current\events"
$activationDir = Join-Path $ExamplePath "activation"

try {
    $worldRegistry = Read-JsonFile $worldRegistryPath
    $surfaceRegistry = Read-JsonFile $surfaceRegistryPath
    $currentContract = Read-JsonFile $currentContractPath
    $currentPointer = Read-JsonFile $currentPointerPath
    $currentState = Read-JsonFile $currentStatePath
    $continuity = Read-JsonFile $continuityPath
    Add-Check "json_parse" $true "Core JSON files parsed successfully."
} catch {
    Add-Check "json_parse" $false $_.Exception.Message
}

if (($checks | Where-Object { $_.name -eq "json_parse" }).ok) {
    $rcIds = @(@(
        $worldRegistry.rc_id,
        $surfaceRegistry.rc_id,
        $currentContract.rc_id,
        $currentPointer.rc_id
    ) | Sort-Object -Unique)
    Add-Check "rc_id_consistency" ($rcIds.Count -eq 1) ("rc_ids=" + ($rcIds -join ", "))

    $activeWorld = $currentState.active_world
    Add-Check "active_world_declared" (Has-Property $worldRegistry.worlds $activeWorld) "active_world=$activeWorld"

    $activeSurface = $currentState.active_surface
    Add-Check "active_surface_declared" (Has-Property $surfaceRegistry.surfaces $activeSurface) "active_surface=$activeSurface"

    $contractStates = @($currentContract.continuity_states)
    Add-Check "state_continuity_allowed" ($contractStates -contains $currentState.continuity_status) "state_continuity=$($currentState.continuity_status)"
    Add-Check "continuity_file_allowed" ($contractStates -contains $continuity.status) "continuity_status=$($continuity.status)"

    $eventsOk = $true
    $eventCount = 0
    $eventError = ""
    if (-not (Test-Path -Path $eventsDir)) {
        $eventsOk = $false
        $eventError = "Missing events directory."
    } else {
        foreach ($file in Get-ChildItem -Path $eventsDir -File -Filter "*.jsonl") {
            foreach ($line in Get-Content -Path $file.FullName) {
                if ([string]::IsNullOrWhiteSpace($line)) { continue }
                try {
                    $event = $line | ConvertFrom-Json
                    $eventCount += 1
                    if ($event.rc_id -ne $currentPointer.rc_id) {
                        $eventsOk = $false
                        $eventError = "Event with wrong rc_id: $($event.event_id)"
                    }
                } catch {
                    $eventsOk = $false
                    $eventError = $_.Exception.Message
                }
            }
        }
    }
    Add-Check "events_jsonl_parse" $eventsOk "events=$eventCount $eventError"

    $permissionLevel = [int]$surfaceRegistry.surfaces.$activeSurface.permission_level
    Add-Check "active_surface_permission_present" ($permissionLevel -ge 0 -and $permissionLevel -le 5) "permission_level=$permissionLevel"

    $activationOk = $true
    $activationCount = 0
    $activationError = ""
    if (-not (Test-Path -Path $activationDir)) {
        $activationOk = $false
        $activationError = "Missing activation directory."
    } else {
        foreach ($file in Get-ChildItem -Path $activationDir -File -Filter "*.json") {
            try {
                $package = Read-JsonFile $file.FullName
                $activationCount += 1

                if ($package.rc_id -ne $currentPointer.rc_id) {
                    $activationOk = $false
                    $activationError = "Package $($file.Name) has wrong rc_id."
                    continue
                }

                if ($package.current_context.current_id -ne $currentPointer.current_id) {
                    $activationOk = $false
                    $activationError = "Package $($file.Name) targets unexpected current_id."
                    continue
                }

                if ($package.current_context.active_world -ne $currentState.active_world) {
                    $activationOk = $false
                    $activationError = "Package $($file.Name) active_world does not match CURRENT_STATE."
                    continue
                }

                if ($package.current_context.active_surface -ne $currentState.active_surface) {
                    $activationOk = $false
                    $activationError = "Package $($file.Name) active_surface does not match CURRENT_STATE."
                    continue
                }

                if (-not (Has-Property $worldRegistry.worlds $package.current_context.active_world)) {
                    $activationOk = $false
                    $activationError = "Package $($file.Name) references undeclared active world."
                    continue
                }

                if (-not (Has-Property $surfaceRegistry.surfaces $package.surface_context.surface_id)) {
                    $activationOk = $false
                    $activationError = "Package $($file.Name) references undeclared surface."
                    continue
                }

                $objectCount = @($package.retrieved_objects).Count
                if ($package.package_metadata.object_count -ne $objectCount) {
                    $activationOk = $false
                    $activationError = "Package $($file.Name) object_count mismatch."
                    continue
                }

                if (-not ($package.safety_frame.is_context_not_mandate -and $package.safety_frame.no_canonical_write -and $package.safety_frame.membrane_status_present -and $package.safety_frame.provenance_required)) {
                    $activationOk = $false
                    $activationError = "Package $($file.Name) safety_frame is incomplete."
                    continue
                }

                foreach ($object in @($package.retrieved_objects)) {
                    if (-not (Has-Property $worldRegistry.worlds $object.world)) {
                        $activationOk = $false
                        $activationError = "Package $($file.Name) object $($object.id) references undeclared world."
                        break
                    }
                    if (@("HOLD", "BLOCK", "ESCALATE") -contains $object.membrane_status) {
                        $activationOk = $false
                        $activationError = "Package $($file.Name) includes non-passable object $($object.id) with membrane_status=$($object.membrane_status)."
                        break
                    }
                }
            } catch {
                $activationOk = $false
                $activationError = $_.Exception.Message
            }
        }
    }
    Add-Check "activation_packages_valid" $activationOk "packages=$activationCount $activationError"
}

$okCount = ($checks | Where-Object { $_.ok }).Count
$failCount = ($checks | Where-Object { -not $_.ok }).Count
$status = if ($failCount -eq 0) { "PASS" } else { "FAIL" }

foreach ($check in $checks) {
    $mark = if ($check.ok) { "OK" } else { "FAIL" }
    Write-Output "$mark $($check.name): $($check.detail)"
}

[pscustomobject]@{
    status = $status
    checks_passed = $okCount
    checks_failed = $failCount
}
