import json
import os
import sys


def main() -> int:
    test_name = "TEST_06_vbox_output_parser"
    about = "VBoxManage output parser extracts only sandbox-relevant fields"
    try:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if root not in sys.path:
            sys.path.insert(0, root)

        from core.modules.vbox_output_parser import (
            parse_list_vms,
            parse_showvminfo,
            parse_snapshot_list,
        )

        # --- parse_list_vms ---
        list_stdout = (
            '"WindowsSandbox" {8e6277b9-72b9-4e35-ba9c-46cf2b24fe87}\n'
            '"Spare_Kali" {10bc36ea-19bd-4768-b2dd-b61aa60de2eb}\n'
        )
        vms = parse_list_vms(list_stdout)
        if vms != [
            {"name": "WindowsSandbox", "uuid": "8e6277b9-72b9-4e35-ba9c-46cf2b24fe87"},
            {"name": "Spare_Kali", "uuid": "10bc36ea-19bd-4768-b2dd-b61aa60de2eb"},
        ]:
            print(f"[{test_name}] FAIL")
            print(f"About: {about}")
            print("Reason: List VM parsing mismatch")
            print("Output:")
            print(json.dumps(vms))
            return 1

        # --- parse_showvminfo (simplified) ---
        show_stdout = (
            'name="WindowsSandbox"\n'
            'UUID="8e6277b9-72b9-4e35-ba9c-46cf2b24fe87"\n'
            'ostype="Windows 7 (64-bit)"\n'
            'VMState="poweroff"\n'
            'VMStateChangeTime="2026-02-22T21:03:35.000000000"\n'
            'memory=3028\n'
            'cpus=2\n'
            'hwvirtex="on"\n'
            'nestedpaging="on"\n'
            'boot1="disk"\n'
            'nic1="nat"\n'
            'natnet1="nat"\n'
            'macaddress1="080027416E0E"\n'
            'cableconnected1="on"\n'
            'nic2="hostonly"\n'
            'hostonlyadapter2="vboxnet0"\n'
            'macaddress2="080027EE2590"\n'
            'cableconnected2="on"\n'
            'nic3="none"\n'
            'CurrentSnapshotName="After debloating"\n'
            'CurrentSnapshotUUID="06388c39-2f71-406b-8dd4-872ba6d7fe5e"\n'
            'SharedFolderNameGlobalMapping1="SandboxShare"\n'
            'SharedFolderPathGlobalMapping1="/home/user/SandboxShare"\n'
            'clipboard="bidirectional"\n'
            'recording_enabled="off"\n'
        )
        info = parse_showvminfo(show_stdout)

        checks = [
            ("name", info.get("name") == "WindowsSandbox"),
            ("uuid", info.get("uuid") == "8e6277b9-72b9-4e35-ba9c-46cf2b24fe87"),
            ("os", info.get("os") == "Windows 7 (64-bit)"),
            ("state", info.get("state") == "poweroff"),
            ("memory_mb", info.get("memory_mb") == 3028),
            ("cpus", info.get("cpus") == 2),
            ("2 NICs (nic3=none excluded)", len(info["network"]) == 2),
            ("nic1 type", info["network"][0]["type"] == "nat"),
            ("nic2 type", info["network"][1]["type"] == "hostonly"),
            ("snapshot", info.get("snapshot") == "After debloating"),
            ("shared_folders count", len(info["shared_folders"]) == 1),
            ("shared_folders name", info["shared_folders"][0]["name"] == "SandboxShare"),
            # hwvirtex, boot, clipboard, recording should NOT be in output
            ("no hwvirtex", "hwvirtex" not in info),
            ("no boot", "boot" not in info and "boot1" not in info),
            ("no clipboard", "clipboard" not in info),
        ]

        for label, ok in checks:
            if not ok:
                print(f"[{test_name}] FAIL")
                print(f"About: {about}")
                print(f"Reason: Check failed: {label}")
                print("Output:")
                print(json.dumps(info, indent=2, default=str))
                return 1

        # --- parse_snapshot_list ---
        snap_stdout = (
            'SnapshotName="Best Version"\n'
            'SnapshotUUID="358ac90e-9444-46a2-85b2-c15e896c2975"\n'
            'SnapshotName-1="Before Debloating"\n'
            'SnapshotUUID-1="39d46343-1d61-4a7f-bb28-d875470f02c2"\n'
            'CurrentSnapshotName="Before Debloating"\n'
            'CurrentSnapshotUUID="39d46343-1d61-4a7f-bb28-d875470f02c2"\n'
        )
        snaps = parse_snapshot_list(snap_stdout)
        snap_checks = [
            ("2 snapshots", len(snaps["snapshots"]) == 2),
            ("current name", snaps["current"] == "Before Debloating"),
            ("snap 0 name", snaps["snapshots"][0]["name"] == "Best Version"),
        ]
        for label, ok in snap_checks:
            if not ok:
                print(f"[{test_name}] FAIL")
                print(f"About: {about}")
                print(f"Reason: Snapshot check failed: {label}")
                print("Output:")
                print(json.dumps(snaps, indent=2))
                return 1

        print(f"[{test_name}] PASS")
        print(f"About: {about}")
        print("Output:")
        print(json.dumps({"info_keys": list(info.keys()), "nic_count": len(info["network"]), "snapshot_count": len(snaps["snapshots"])}))
        return 0
    except Exception as exc:  # noqa: BLE001
        import traceback
        print(f"[{test_name}] FAIL")
        print(f"About: {about}")
        print(f"Reason: {exc}")
        print("Output:")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
