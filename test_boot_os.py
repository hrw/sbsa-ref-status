#!/usr/bin/python3

import io
import pytest
import subprocess
import time


def boot_os(osname, line_to_check):
    process = subprocess.Popen(["/usr/bin/python3",
                                "boot-sbsa-ref.py",
                                f"--os={osname}"],
                               stdout = subprocess.PIPE,
                               )

    start_time = time.time()

    for line in io.TextIOWrapper(process.stdout, encoding="utf-8"):
        print(line, end="")
        if line.startswith(line_to_check):
            process.terminate()
            return 0

        if time.time() > start_time + 7 * 60:
            process.terminate()
            pytest.fail("Timeout")

    process.terminate()
    pytest.fail("No expected line in test output")


def test_alpine():
    # Welcome to Alpine Linux 3.20
    boot_os("alpine", "Welcome to Alpine Linux")


# instead of RHEL
def test_centos9():
    boot_os("centos9", "CentOS Stream 9")


# debian/stable
def test_debian12():
    boot_os("debian12", "Debian GNU/Linux 12 localhost ttyAMA0")

# debian/oldoldstable which should still boot
def test_debian10():
    boot_os("debian10", "Debian GNU/Linux 10 debian ttyAMA0")

# devel
def test_debian13():
    boot_os("debian13", "Debian GNU/Linux trixie/sid localhost ttyAMA0")

# stable
def test_freebsd14():
    boot_os("freebsd14", "FreeBSD/arm64 (freebsd) (ttyu0)")

# oldstable
def test_freebsd13():
    boot_os("freebsd13", "FreeBSD/arm64 (freebsd) (ttyu0)")

# devel
def test_freebsd15():
    boot_os("freebsd15", "FreeBSD/arm64 (freebsd) (ttyu0)")

# stable
def test_netbsd10():
    boot_os("netbsd10", "NetBSD/evbarm (arm64) (constty)")

# oldstable
def test_netbsd9():
    boot_os("netbsd9", "NetBSD/evbarm (arm64) (constty)")

# devel
def test_netbsd11():
    boot_os("netbsd11", "NetBSD/evbarm (arm64) (constty)")

# current release
def test_openbsd76():
    boot_os("openbsd76", "Welcome to the OpenBSD/arm64 7.6 installation program.")
