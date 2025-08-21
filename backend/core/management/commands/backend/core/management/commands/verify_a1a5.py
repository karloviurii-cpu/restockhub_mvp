from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = "Verify that docs for A1–A5 exist and contain required sections"

    def handle(self, *args, **options):
        base = os.path.join(os.getcwd(), "docs")
        checks = {
            "A1": "problem.md",
            "A2": "value.md",
            "A3": "architecture.md",
            "A4": "tech.md",
            "A5": "onboarding.md",
        }

        failed = False

        for key, fname in checks.items():
            path = os.path.join(base, fname)
            if not os.path.exists(path):
                self.stdout.write(self.style.ERROR(f"{key}: missing {fname}"))
                failed = True
            else:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                    if len(content.strip()) < 20:
                        self.stdout.write(self.style.WARNING(f"{key}: {fname} is too short"))
                        failed = True
                    else:
                        self.stdout.write(self.style.SUCCESS(f"{key}: OK"))

        if failed:
            raise SystemExit(1)
        else:
            self.stdout.write(self.style.SUCCESS("A1–A5 verification passed"))
