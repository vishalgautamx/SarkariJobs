from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.posts.models import Post
from apps.posts.sources.registry import (
    SOURCE_REGISTRY,
    run_source,
)


class Command(BaseCommand):

    help = (
        "Fetch and process automatic "
        "SarkariJobs updates from all "
        "enabled official sources."
    )

    def handle(self, *args, **options):

        started_at = timezone.now()

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "   SARKARIJOBS AUTO UPDATE ENGINE"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )

        self.stdout.write(
            f"Started: {started_at}"
        )

        self.stdout.write("")

        total_created = 0
        total_updated = 0
        total_items = 0

        successful_sources = 0
        failed_sources = 0
        skipped_sources = 0

        # -----------------------------------
        # RUN ALL REGISTERED SOURCES
        # -----------------------------------

        for source_name, config in SOURCE_REGISTRY.items():

            self.stdout.write(
                ""
            )

            self.stdout.write(
                self.style.WARNING(
                    f"[SOURCE] {source_name}"
                )
            )

            if not config.get("enabled"):

                self.stdout.write(
                    "Status: DISABLED"
                )

                skipped_sources += 1

                continue

            try:

                result = run_source(
                    source_name,
                    config
                )

            except Exception as error:

                failed_sources += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"{source_name} ERROR: "
                        f"{error}"
                    )
                )

                continue

            if not result.get("success"):

                failed_sources += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"{source_name} FAILED"
                    )
                )

                if result.get("error"):

                    self.stdout.write(
                        f"Error: "
                        f"{result.get('error')}"
                    )

                continue

            successful_sources += 1

            created = result.get(
                "created",
                0
            )

            updated = result.get(
                "updated",
                0
            )

            total = result.get(
                "total",
                0
            )

            total_created += created
            total_updated += updated
            total_items += total

            self.stdout.write(
                self.style.SUCCESS(
                    f"{source_name}: "
                    f"{total} update(s)"
                )
            )

            self.stdout.write(
                f"Created: {created}"
            )

            self.stdout.write(
                f"Updated: {updated}"
            )

            # --------------------------------
            # PRINT INDIVIDUAL POSTS
            # --------------------------------

            items = result.get(
                "items",
                []
            )

            for item in items:

                title = item.get(
                    "title",
                    "Unknown"
                )

                category = item.get(
                    "category",
                    ""
                )

                status = item.get(
                    "status",
                    ""
                )

                self.stdout.write(
                    f"  [{status.upper()}] "
                    f"[{category}] "
                    f"{title}"
                )

        # -----------------------------------
        # UPDATE LAST CHECKED
        # -----------------------------------

        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING(
                "Updating automation timestamps..."
            )
        )

        automated_posts = Post.objects.filter(
            is_automated=True
        )

        checked = 0

        for post in automated_posts:

            post.last_checked = timezone.now()

            post.save(
                update_fields=[
                    "last_checked"
                ]
            )

            checked += 1

        # -----------------------------------
        # FINAL SUMMARY
        # -----------------------------------

        finished_at = timezone.now()

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "        AUTOMATION COMPLETED"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )

        self.stdout.write(
            f"Sources successful : "
            f"{successful_sources}"
        )

        self.stdout.write(
            f"Sources failed     : "
            f"{failed_sources}"
        )

        self.stdout.write(
            f"Sources disabled   : "
            f"{skipped_sources}"
        )

        self.stdout.write(
            f"Updates received   : "
            f"{total_items}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Posts created      : "
                f"{total_created}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Posts updated      : "
                f"{total_updated}"
            )
        )

        self.stdout.write(
            f"Automated posts    : "
            f"{checked}"
        )

        self.stdout.write(
            f"Finished: {finished_at}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                "SarkariJobs automation "
                "finished successfully."
            )
        )