from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.scraper.models import Source
from apps.scraper.services import fetch_page


class Command(BaseCommand):

    help = "Check official sources and show discovered links"

    def handle(self, *args, **options):

        sources = Source.objects.filter(
            is_active=True
        )

        if not sources.exists():

            self.stdout.write(
                self.style.WARNING(
                    "No active sources found."
                )
            )

            return

        for source in sources:

            self.stdout.write("")
            self.stdout.write(
                self.style.NOTICE(
                    f"Checking: {source.name}"
                )
            )

            try:

                page = fetch_page(source.url)

                soup = page.get("soup")

                self.stdout.write(
                    self.style.SUCCESS(
                        "✓ Source fetched successfully"
                    )
                )

                self.stdout.write(
                    f"Page title: {page.get('title', '')}"
                )

                self.stdout.write(
                    f"Text length: {len(page.get('text', ''))}"
                )

                if soup:

                    links = soup.find_all(
                        "a",
                        href=True
                    )

                    self.stdout.write(
                        f"Links found: {len(links)}"
                    )

                    for link in links[:30]:

                        link_text = link.get_text(
                            " ",
                            strip=True
                        )

                        href = link.get(
                            "href",
                            ""
                        ).strip()

                        self.stdout.write(
                            f"{link_text} => {href}"
                        )

                else:

                    self.stdout.write(
                        "No HTML soup available."
                    )

                source.last_checked = timezone.now()

                source.save(
                    update_fields=[
                        "last_checked"
                    ]
                )

            except Exception as e:

                self.stdout.write(
                    self.style.ERROR(
                        f"✗ Error: {e}"
                    )
                )