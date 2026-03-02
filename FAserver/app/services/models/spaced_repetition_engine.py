from datetime import datetime, timedelta


class SpacedRepetitionEngine:
    """
    SM-2 algorithm (Anki-like)
    """

    def update(self, progress, is_correct: bool):

        now = datetime.utcnow()

        if progress.reviewcount == 0:
            interval = 1
        elif progress.reviewcount == 1:
            interval = 3
        else:
            interval = progress.reviewcount * 2

        if not is_correct:
            interval = 1
            progress.successrate *= 0.8
        else:
            progress.successrate = (
                progress.successrate * progress.reviewcount + 1
            ) / (progress.reviewcount + 1)

        progress.reviewcount += 1
        progress.lastreviewed = now
        progress.nextreviewed = now + timedelta(days=interval)

        progress.isknown = progress.successrate > 0.85

        return progress
