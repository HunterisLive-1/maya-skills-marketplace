"""Password Generator — cryptographically secure passwords. stdin: optional length (default 16)."""
import secrets
import string
import sys


def main():
    raw = sys.stdin.read().strip() if not sys.stdin.isatty() else ""
    try:
        length = max(8, min(64, int(raw)))
    except (ValueError, TypeError):
        length = 16

    alphabet = string.ascii_letters + string.digits + "!@#$%^&*-_+="
    print(f"Generated {length}-char passwords (pick any one):")
    for i in range(3):
        # Guarantee at least one of each class
        pwd = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice("!@#$%^&*-_+="),
        ]
        pwd += [secrets.choice(alphabet) for _ in range(length - 4)]
        secrets.SystemRandom().shuffle(pwd)
        print(f"  {i + 1}. {''.join(pwd)}")
    print("Tip: password manager mein save karo, dobara use mat karo.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Password generation error: {e}")
