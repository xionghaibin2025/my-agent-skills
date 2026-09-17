#!/usr/bin/env python3
"""
install_scienceplots.py — Environment checker & installer helper for SciencePlots.

Run:
    python install_scienceplots.py

This script checks:
    1. Whether SciencePlots is installed and its version
    2. Whether matplotlib is installed and its version
    3. Whether NumPy is installed and its version
    4. Whether LaTeX is available on PATH
    5. Whether common CJK fonts are available to matplotlib
    6. Whether the 'science' style can be loaded successfully

It prints a summary and suggests installation commands for anything missing.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import textwrap


# ── Colour helpers (graceful degradation on Windows cmd) ─────────────────────

def _supports_color() -> bool:
    """Return True if stdout likely supports ANSI colour codes."""
    try:
        import os
        if os.name == "nt":
            # Windows 10+ supports ANSI if ENABLE_VIRTUAL_TERMINAL_PROCESSING
            # is set, but many terminals (Windows Terminal, VS Code) work anyway.
            return os.environ.get("WT_SESSION") is not None or "ANSICON" in os.environ or True
        return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    except Exception:
        return False


_COLOR = _supports_color()

def _green(text: str) -> str:
    return f"\033[92m{text}\033[0m" if _COLOR else text

def _red(text: str) -> str:
    return f"\033[91m{text}\033[0m" if _COLOR else text

def _yellow(text: str) -> str:
    return f"\033[93m{text}\033[0m" if _COLOR else text

def _bold(text: str) -> str:
    return f"\033[1m{text}\033[0m" if _COLOR else text


# ── Check functions ──────────────────────────────────────────────────────────

def check_matplotlib() -> tuple[bool, str]:
    """Check if matplotlib is installed and return (ok, version_or_error)."""
    try:
        import matplotlib
        return True, matplotlib.__version__
    except ImportError:
        return False, "not installed"
    except Exception as exc:
        return False, f"import error: {exc}"


def check_numpy() -> tuple[bool, str]:
    """Check if numpy is installed and return (ok, version_or_error)."""
    try:
        import numpy
        return True, numpy.__version__
    except ImportError:
        return False, "not installed"
    except Exception as exc:
        return False, f"import error: {exc}"


def check_scienceplots() -> tuple[bool, str]:
    """Check if SciencePlots is installed and return (ok, version_or_error)."""
    try:
        import scienceplots
        version = getattr(scienceplots, "__version__", "unknown")
        return True, version
    except ImportError:
        return False, "not installed"
    except Exception as exc:
        return False, f"import error: {exc}"


def check_latex() -> tuple[bool, str]:
    """Check if a LaTeX distribution is available on PATH."""
    latex_path = shutil.which("latex")
    if latex_path is None:
        # Also check pdflatex and xelatex
        for cmd in ("pdflatex", "xelatex", "lualatex"):
            path = shutil.which(cmd)
            if path:
                try:
                    result = subprocess.run(
                        [cmd, "--version"],
                        capture_output=True, text=True, timeout=10,
                    )
                    first_line = result.stdout.strip().split("\n")[0]
                    return True, f"{cmd} → {first_line}"
                except Exception:
                    return True, f"{cmd} found at {path}"
        return False, "not found on PATH"
    else:
        try:
            result = subprocess.run(
                ["latex", "--version"],
                capture_output=True, text=True, timeout=10,
            )
            first_line = result.stdout.strip().split("\n")[0]
            return True, first_line
        except Exception:
            return True, f"found at {latex_path}"


def check_dvipng() -> tuple[bool, str]:
    """Check if dvipng is available (needed by matplotlib's LaTeX backend)."""
    path = shutil.which("dvipng")
    if path:
        return True, path
    return False, "not found on PATH"


def check_cm_super() -> tuple[bool, str]:
    """Check for cm-super or type1cm (LaTeX font packages)."""
    # This is a best-effort heuristic; checking kpsewhich if available
    kpse = shutil.which("kpsewhich")
    if kpse is None:
        return False, "kpsewhich not found (cannot verify)"
    try:
        result = subprocess.run(
            [kpse, "type1cm.sty"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return True, result.stdout.strip()
        return False, "type1cm.sty not found"
    except Exception as exc:
        return False, str(exc)


def check_cjk_fonts() -> dict[str, bool]:
    """
    Check for common CJK fonts registered with matplotlib.

    Returns a dict of font_name → available (bool).
    """
    cjk_fonts = {
        # Simplified Chinese
        "SimHei": False,
        "Microsoft YaHei": False,
        "Noto Sans CJK SC": False,
        # Traditional Chinese
        "PMingLiU": False,
        "Noto Sans CJK TC": False,
        # Japanese
        "MS Gothic": False,
        "Noto Sans CJK JP": False,
        # Korean
        "Malgun Gothic": False,
        "Noto Sans CJK KR": False,
    }
    try:
        from matplotlib import font_manager
        available_fonts = {f.name for f in font_manager.fontManager.ttflist}
        for name in cjk_fonts:
            if name in available_fonts:
                cjk_fonts[name] = True
    except Exception:
        pass  # matplotlib not installed or font_manager broken
    return cjk_fonts


def check_style_loads() -> tuple[bool, str]:
    """Try to load plt.style.use(['science']) and report success/failure."""
    try:
        import matplotlib.pyplot as plt
        plt.style.use(["science"])
        return True, "style loaded OK"
    except Exception as exc:
        return False, str(exc)


def check_style_no_latex() -> tuple[bool, str]:
    """Try to load plt.style.use(['science', 'no-latex'])."""
    try:
        import matplotlib.pyplot as plt
        plt.style.use(["science", "no-latex"])
        return True, "style loaded OK"
    except Exception as exc:
        return False, str(exc)


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print()
    print(_bold("=" * 60))
    print(_bold("  SciencePlots Environment Check"))
    print(_bold("=" * 60))
    print()

    suggestions: list[str] = []
    all_ok = True

    # ---- 1. NumPy ----
    ok, info = check_numpy()
    status = _green("✓") if ok else _red("✗")
    print(f"  {status}  NumPy            : {info}")
    if not ok:
        all_ok = False
        suggestions.append("pip install numpy")

    # ---- 2. matplotlib ----
    ok, info = check_matplotlib()
    status = _green("✓") if ok else _red("✗")
    print(f"  {status}  matplotlib       : {info}")
    if not ok:
        all_ok = False
        suggestions.append("pip install matplotlib")

    # ---- 3. SciencePlots ----
    ok_sp, info = check_scienceplots()
    status = _green("✓") if ok_sp else _red("✗")
    print(f"  {status}  SciencePlots     : {info}")
    if not ok_sp:
        all_ok = False
        suggestions.append("pip install SciencePlots")

    print()

    # ---- 4. LaTeX ----
    ok_latex, info = check_latex()
    status = _green("✓") if ok_latex else _yellow("△")
    print(f"  {status}  LaTeX            : {info}")
    if not ok_latex:
        suggestions.append(
            "Install a LaTeX distribution:\n"
            "      Windows : MiKTeX  → https://miktex.org/download\n"
            "      macOS   : MacTeX  → https://www.tug.org/mactex/\n"
            "      Linux   : sudo apt install texlive-latex-extra texlive-fonts-recommended"
        )

    # ---- 5. dvipng ----
    ok_dvi, info = check_dvipng()
    status = _green("✓") if ok_dvi else _yellow("△")
    print(f"  {status}  dvipng           : {info}")
    if not ok_dvi and ok_latex:
        suggestions.append(
            "Install dvipng (needed by matplotlib LaTeX backend):\n"
            "      Linux : sudo apt install dvipng\n"
            "      MiKTeX: miktex-console → install dvipng package"
        )

    # ---- 6. cm-super ----
    ok_cm, info = check_cm_super()
    status = _green("✓") if ok_cm else _yellow("△")
    print(f"  {status}  cm-super / t1cm  : {info}")
    if not ok_cm and ok_latex:
        suggestions.append(
            "Install cm-super fonts (avoids bitmap font warnings):\n"
            "      Linux : sudo apt install cm-super\n"
            "      MiKTeX: install via MiKTeX Console"
        )

    print()

    # ---- 7. CJK fonts ----
    cjk = check_cjk_fonts()
    any_cjk = any(cjk.values())
    print(f"  {'✓' if any_cjk else '△'}  CJK Fonts:")
    for name, avail in cjk.items():
        mark = _green("✓") if avail else "·"
        print(f"       {mark}  {name}")
    if not any_cjk:
        suggestions.append(
            "Install CJK fonts for Chinese / Japanese / Korean labels:\n"
            "      All OS : Noto CJK → https://fonts.google.com/noto#702\n"
            "      Windows: SimHei / Microsoft YaHei are usually pre-installed"
        )

    print()

    # ---- 8. Style loading ----
    if ok_sp:
        ok_s, info_s = check_style_loads()
        status = _green("✓") if ok_s else _red("✗")
        print(f"  {status}  style ['science']           : {info_s}")

        ok_snl, info_snl = check_style_no_latex()
        status = _green("✓") if ok_snl else _red("✗")
        print(f"  {status}  style ['science','no-latex'] : {info_snl}")

        if not ok_s and not ok_snl:
            all_ok = False
            suggestions.append(
                "SciencePlots styles failed to load. Try reinstalling:\n"
                "      pip install --force-reinstall SciencePlots"
            )
    else:
        print(f"  {_yellow('△')}  Style loading : skipped (SciencePlots not installed)")

    # ---- Summary ----
    print()
    print(_bold("-" * 60))

    if not suggestions:
        print(_green("  All checks passed! Your environment is ready."))
    else:
        if all_ok:
            print(_yellow("  Environment is functional, but some optional components"))
            print(_yellow("  are missing. See suggestions below."))
        else:
            print(_red("  Some required components are missing."))
        print()
        print(_bold("  Suggested actions:"))
        print()
        for i, s in enumerate(suggestions, 1):
            indented = textwrap.indent(s, "      ")
            # First line gets the number
            lines = indented.split("\n")
            lines[0] = f"    {i}. {s.split(chr(10))[0]}"
            if len(s.split("\n")) > 1:
                rest = "\n".join(f"      {line.strip()}" for line in s.split("\n")[1:])
                print(lines[0])
                print(rest)
            else:
                print(lines[0])
            print()

    print(_bold("=" * 60))
    print()

    # ---- Python info ----
    print(f"  Python : {sys.version}")
    print(f"  Prefix : {sys.prefix}")
    print()


if __name__ == "__main__":
    main()
