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

        if time.time() > start_time + 5 * 60:
            process.terminate()
            pytest.fail("Timeout")

    process.terminate()
    pytest.fail("No expected line in test output")


def test_alpine():
    # Welcome to Alpine Linux 3.20
    boot_os("alpine", "Welcome to Alpine Linux")


def test_centos9():
    boot_os("centos9", "CentOS Stream 9")


def test_debian10():
    boot_os("debian10", "Debian GNU/Linux 10 debian ttyAMA0")


def test_debian11():
    boot_os("debian11", "Debian GNU/Linux 11 debian ttyAMA0")


def test_debian12():
    boot_os("debian12", "Debian GNU/Linux 12 localhost ttyAMA0")


def test_fedora():
    # Welcome to Fedora Linux 40 (Server Edition) dracut-059-22.fc40 (Initramfs)!
    boot_os("fedora", "Welcome to Fedora Linux 40")


def test_freebsd14():
    boot_os("freebsd14", "FreeBSD/arm64 (freebsd) (ttyu0)")


def test_freebsd13():
    boot_os("freebsd13", "FreeBSD/arm64 (freebsd) (ttyu0)")


def test_freebsd15():
    boot_os("freebsd15", "FreeBSD/arm64 (freebsd) (ttyu0)")


def test_netbsd10():
    boot_os("netbsd10", "NetBSD/evbarm (arm64) (constty)")


def test_netbsd11():
    boot_os("netbsd11", "NetBSD/evbarm (arm64) (constty)")


def test_netbsd9():
    boot_os("netbsd9", "NetBSD/evbarm (arm64) (constty)")


def test_openbsd73():
    boot_os("openbsd73", "Welcome to the OpenBSD/arm64 7.3 installation program.")


def test_openbsd76():
    boot_os("openbsd76", "Welcome to the OpenBSD/arm64 7.6 installation program.")


#def test_openeuler():
#    boot_os("", "")
