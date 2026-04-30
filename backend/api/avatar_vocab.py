"""
Default on-device avatar vocabulary. 120 PSL signs curated from:
  - WLASL (American SL, overlapping PSL signs by translation)
  - ISL (Indian SL) — shares ~55% vocabulary with PSL per linguistic surveys
  - Core daily-life + medical + classroom terms gathered from the
    Pakistan Association of the Deaf PSL dictionary, 2021 ed.

This list bounds what the text-to-sign planner can emit. The 3D avatar ships
with one .bvh animation per entry (see mobile/litert_android/assets).
"""

DEFAULT_VOCAB: list[str] = [
    # Greetings
    "HELLO", "SALAAM", "GOODBYE", "THANK-YOU", "PLEASE", "SORRY", "WELCOME",
    # Pronouns
    "I", "YOU", "HE", "SHE", "WE", "THEY", "MY", "YOUR",
    # Question words
    "WHAT", "WHERE", "WHEN", "WHY", "HOW", "WHO", "HOW-MUCH",
    # Common verbs
    "GO", "COME", "EAT", "DRINK", "SLEEP", "WORK", "STUDY", "WRITE", "READ",
    "UNDERSTAND", "KNOW", "WANT", "NEED", "HELP", "GIVE", "TAKE", "SEE",
    "HEAR", "SPEAK", "LOVE", "LIKE", "STOP", "WAIT", "LIVE",
    # Modals / time
    "YES", "NO", "NOT", "MAYBE", "TODAY", "TOMORROW", "YESTERDAY",
    "NOW", "LATER", "MORNING", "NIGHT", "WEEK", "MONTH", "YEAR",
    # Family
    "FATHER", "MOTHER", "BROTHER", "SISTER", "SON", "DAUGHTER",
    "FAMILY", "FRIEND", "TEACHER", "STUDENT", "DOCTOR", "NURSE",
    # Places
    "HOME", "SCHOOL", "HOSPITAL", "MOSQUE", "MARKET", "OFFICE", "CITY",
    "VILLAGE", "LAHORE", "KARACHI", "ISLAMABAD",
    # Medical essentials
    "PAIN", "FEVER", "HEAD", "STOMACH", "CHEST", "MEDICINE", "WATER",
    "FOOD", "HUNGRY", "THIRSTY", "TIRED", "SICK", "OK", "EMERGENCY",
    "PREGNANT", "BABY", "BLOOD", "COUGH", "BREATHE",
    # Numbers
    "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT",
    "NINE", "TEN", "HUNDRED",
    # Classroom
    "BOOK", "PEN", "QUESTION", "ANSWER", "YES-CORRECT", "WRONG",
    "CLASS", "LESSON", "EXAM", "HOMEWORK",
    # Meta
    "REPEAT", "SLOW", "FAST", "AGAIN", "FINISH",
]


def fingerspell(token: str) -> list[str]:
    """Fallback for out-of-vocabulary proper nouns or numbers."""
    cleaned = "".join(c for c in token.upper() if c.isalnum())
    if not cleaned:
        return []
    return [f"FS-{c}" for c in cleaned]
