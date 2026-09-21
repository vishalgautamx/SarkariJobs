from django.core.management.base import BaseCommand

from apps.scraper.automation import run_all_sources


class Command(BaseCommand):

    help = "Run SarkariJobs automatic source checking"

    def handle(self, *args, **options):

        self.stdout.write("")
        self.stdout.write(
            self.style.NOTICE(
                "================================"
            )
        )

        self.stdout.write(
            self.style.NOTICE(
                "SARKARIJOBS AUTOMATION"
            )
        )

        self.stdout.write(
            self.style.NOTICE(
                "================================"
            )
        )

        try:

            results = run_all_sources()

            for source_name, result in results.items():

                self.stdout.write("")
                self.stdout.write(
                    self.style.NOTICE(
                        f"========== {source_name} =========="
                    )
                )

                if result.get("status") == "adapter_not_connected":

                    self.stdout.write(
                        self.style.WARNING(
                            result.get(
                                "message",
                                "Adapter not connected."
                            )
                        )
                    )

                    continue

                self.stdout.write(
                    self.style.SUCCESS(
                        "Automation completed."
                    )
                )

                self.stdout.write(
                    f"Notices found: "
                    f"{result.get('found', 0)}"
                )

                self.stdout.write(
                    f"New notices: "
                    f"{result.get('new', 0)}"
                )

                self.stdout.write(
                    f"Drafts created: "
                    f"{result.get('created', 0)}"
                )

                self.stdout.write(
                    f"Duplicates: "
                    f"{result.get('duplicates', 0)}"
                )

                self.stdout.write(
                    f"Errors: "
                    f"{result.get('errors', 0)}"
                )

        except Exception as e:

            self.stdout.write(
                self.style.ERROR(
                    f"Automation failed: {e}"
                )
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Automation command completed."
            )
        )