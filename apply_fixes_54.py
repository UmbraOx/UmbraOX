import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def backup_and_read(fp):
    with open(fp, "r", encoding="utf-8") as f:
        s = f.read()
    with open(fp + f".bak54_{ts}", "w", encoding="utf-8") as f:
        f.write(s)
    return s

# ============================================================
# 1. Resource manager: broaden detection, add manual override
# ============================================================
FP1 = r"C:\Umbra\core\runtime\runtime_resource_manager.py"
src1 = backup_and_read(FP1)

OLD1 = '''GAMING_PROCESS_NAMES = {
    # Games
    "steam.exe", "steamwebhelper.exe", "gameoverlayui.exe",
    "epicgameslauncher.exe", "origin.exe", "gog galaxy.exe",
    "minecraft.exe", "javaw.exe", "robloxplayerbeta.exe",
    "league of legends.exe", "leagueclient.exe", "r5apex.exe",
    "csgo.exe", "cs2.exe", "valorant.exe", "fortnite.exe",
    "GTA5.exe", "RDR2.exe", "Cyberpunk2077.exe",
    # Streaming
    "obs64.exe", "obs32.exe", "streamlabs obs.exe",
    "xsplit.core.exe", "nvidia broadcast.exe",
    # Recording
    "shadowplay.exe", "medal.exe",
}'''

NEW1 = '''GAMING_PROCESS_NAMES = {
    # Launchers - covers the vast majority of PC games regardless of
    # which specific title is running, since a name-based list of
    # individual games can never keep up (this was the actual bug -
    # detection silently found nothing for anything not on the list,
    # so throttling never engaged even during active gameplay)
    "steam.exe", "steamwebhelper.exe", "gameoverlayui.exe",
    "epicgameslauncher.exe", "origin.exe", "eadesktop.exe",
    "gog galaxy.exe", "galaxyclient.exe", "battle.net.exe",
    "ubisoftconnect.exe", "upc.exe", "riotclientservices.exe",
    "riotclientux.exe",
    # Common specific titles (best-effort, not exhaustive)
    "minecraft.exe", "javaw.exe", "robloxplayerbeta.exe",
    "league of legends.exe", "leagueclient.exe", "r5apex.exe",
    "csgo.exe", "cs2.exe", "valorant.exe", "fortnite-win64-shipping.exe",
    "fortniteclient-win64-shipping.exe", "gta5.exe", "rdr2.exe",
    "cyberpunk2077.exe", "eldenring.exe", "starfield.exe",
    "baldursgate3.exe", "helldivers2.exe", "palworld.exe",
    # Streaming / recording
    "obs64.exe", "obs32.exe", "streamlabs obs.exe",
    "xsplit.core.exe", "nvidia broadcast.exe",
    "shadowplay.exe", "medal.exe",
}'''

if OLD1 not in src1:
    print("FAIL: GAMING_PROCESS_NAMES anchor not found")
    sys.exit(1)
if src1.count(OLD1) != 1:
    print("FAIL: GAMING_PROCESS_NAMES anchor not unique")
    sys.exit(1)
src1 = src1.replace(OLD1, NEW1, 1)

OLD2 = '''    def __init__(self, gaming_mode_auto=True, max_memory_pct=85, task_delay_ms=50):
        self.gaming_mode_auto = gaming_mode_auto
        self.max_memory_pct = max_memory_pct
        self.task_delay_ms = task_delay_ms  # ms to sleep between tasks when gaming
        self._monitoring = False
        self._monitor_thread = None
        self._current_status = ResourceStatus()
        self._callbacks = []'''

NEW2 = '''    def __init__(self, gaming_mode_auto=True, max_memory_pct=85, task_delay_ms=50):
        self.gaming_mode_auto = gaming_mode_auto
        self.max_memory_pct = max_memory_pct
        self.task_delay_ms = task_delay_ms  # ms to sleep between tasks when gaming
        self._monitoring = False
        self._monitor_thread = None
        self._current_status = ResourceStatus()
        self._callbacks = []
        # Process-name detection can never cover every possible game -
        # this gives a guaranteed manual override ("gaming mode on"/"off")
        # so throttling isn't left entirely to a best-effort name match.
        self._manual_override = None  # None = auto, True = force on, False = force off

    def set_manual_gaming_mode(self, enabled_or_none):
        """enabled_or_none: True to force gaming mode on, False to force
        it off, None to go back to automatic process-name detection."""
        self._manual_override = enabled_or_none'''

if OLD2 not in src1:
    print("FAIL: constructor anchor not found")
    sys.exit(1)
if src1.count(OLD2) != 1:
    print("FAIL: constructor anchor not unique")
    sys.exit(1)
src1 = src1.replace(OLD2, NEW2, 1)

OLD3 = '''    def check_status(self):
        status = ResourceStatus()
        status.gaming_processes = self.detect_gaming_processes()
        status.gaming_detected = len(status.gaming_processes) > 0
        status.memory_pct = self.get_memory_usage_pct()
        status.throttled = status.gaming_detected or status.memory_pct > self.max_memory_pct
        self._current_status = status
        return status'''

NEW3 = '''    def check_status(self):
        status = ResourceStatus()
        if self._manual_override is True:
            status.gaming_processes = ["manual override"]
            status.gaming_detected = True
        elif self._manual_override is False:
            status.gaming_processes = []
            status.gaming_detected = False
        else:
            status.gaming_processes = self.detect_gaming_processes()
            status.gaming_detected = len(status.gaming_processes) > 0
        status.memory_pct = self.get_memory_usage_pct()
        status.throttled = status.gaming_detected or status.memory_pct > self.max_memory_pct
        self._current_status = status
        return status'''

if OLD3 not in src1:
    print("FAIL: check_status anchor not found")
    sys.exit(1)
if src1.count(OLD3) != 1:
    print("FAIL: check_status anchor not unique")
    sys.exit(1)
src1 = src1.replace(OLD3, NEW3, 1)

with open(FP1, "w", encoding="utf-8") as f:
    f.write(src1)

try:
    ast.parse(src1)
    print("runtime_resource_manager.py AST OK")
except SyntaxError as e:
    print("AST FAIL (resource manager): " + str(e))
    sys.exit(1)

# ============================================================
# 2. Umbra.py: wire "gaming mode on/off/auto" commands + fix NPC
#    constructor crash (same ValueError-on-invalid-arg pattern as
#    the Player fix in batch38, just never applied to NPC)
# ============================================================
FP2 = r"C:\Umbra\Umbra.py"
src2 = backup_and_read(FP2)

OLD4 = '''    if cmd in ("voice on", "continuous voice on", "always listen"):'''
NEW4 = '''    if cmd in ("gaming mode on", "force gaming mode"):
        _rm = runtime.get("resource_manager")
        if _rm:
            _rm.set_manual_gaming_mode(True)
            _umbra_print("  [RESOURCES] Gaming mode forced ON - Umbra will throttle itself regardless of process detection.\\n")
        else:
            _umbra_print("  [RESOURCES] Resource manager not available.\\n")
        return

    if cmd in ("gaming mode off",):
        _rm = runtime.get("resource_manager")
        if _rm:
            _rm.set_manual_gaming_mode(False)
            _umbra_print("  [RESOURCES] Gaming mode forced OFF.\\n")
        else:
            _umbra_print("  [RESOURCES] Resource manager not available.\\n")
        return

    if cmd in ("gaming mode auto", "gaming mode automatic"):
        _rm = runtime.get("resource_manager")
        if _rm:
            _rm.set_manual_gaming_mode(None)
            _umbra_print("  [RESOURCES] Gaming mode back to automatic detection.\\n")
        else:
            _umbra_print("  [RESOURCES] Resource manager not available.\\n")
        return

    if cmd in ("voice on", "continuous voice on", "always listen"):'''

if OLD4 not in src2:
    print("FAIL: gaming-mode-command anchor not found")
    sys.exit(1)
if src2.count(OLD4) != 1:
    print("FAIL: gaming-mode-command anchor not unique")
    sys.exit(1)
src2 = src2.replace(OLD4, NEW4, 1)

# NPC constructor safety: same "agent's __init__ validates and raises"
# pattern already fixed for Player in batch38. Never applied to NPC.
OLD5 = '''# UMBRA_ENEMY_PATCH'''
NEW5 = '''# UMBRA_NPC_PATCH
# Same issue as UMBRA_PLAYER_PATCH: an agent's NPC.__init__ may validate
# its own arguments (e.g. reject a job name it doesn't recognize) and
# raise, which used to propagate straight up and crash spawn_world_entities
# the instant the world tried to populate. Retry with safe fallbacks
# instead of ever letting NPC construction crash the game.
try:
    if 'NPC' in dir():
        _onpc = NPC.__init__
        def _nnpc(self,*a,**kw):
            try:
                _onpc(self,*a,**kw)
            except Exception:
                _fallback_jobs = ["Villager","Merchant","Farmer","Guard","Innkeeper"]
                _ok=False
                for _fj in _fallback_jobs:
                    try:
                        if len(a) >= 4:
                            _onpc(self,a[0],a[1],a[2],_fj,*a[4:],**kw)
                        else:
                            _onpc(self,*a,**kw)
                        _ok=True; break
                    except Exception:
                        continue
                if not _ok:
                    try:
                        _onpc(self)
                    except Exception:
                        pass
            for _at,_dv in [('name',a[0] if a else 'Villager'),
                            ('x',a[1] if len(a)>1 else 0.0),
                            ('y',a[2] if len(a)>2 else 0.0),
                            ('job',a[3] if len(a)>3 else 'Villager'),
                            ('alive',True)]:
                if not hasattr(self,_at): setattr(self,_at,_dv)
        NPC.__init__ = _nnpc
except Exception:
    pass
# UMBRA_ENEMY_PATCH'''

if OLD5 not in src2:
    print("FAIL: NPC patch insertion anchor not found")
    sys.exit(1)
if src2.count(OLD5) != 1:
    print("FAIL: NPC patch insertion anchor not unique")
    sys.exit(1)
src2 = src2.replace(OLD5, NEW5, 1)

with open(FP2, "w", encoding="utf-8") as f:
    f.write(src2)

try:
    ast.parse(src2)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print("AST FAIL (Umbra.py): " + str(e))
    sys.exit(1)

print("Fix applied: gaming mode detection broadened + manual override, NPC construction crash-safe (batch54)")