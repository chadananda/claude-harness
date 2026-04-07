"""
Comprehensive Bahá'í diacritical restoration with fuzzy OCR error correction.

Two layers:
1. Fuzzy patterns — catch common Tesseract garbles (u→w, space insertion, apostrophe drops)
2. Clean patterns — match correctly-spelled-but-missing-diacriticals forms

Tesseract's most common garble patterns on Bahá'í texts:
  - u → w  (Baha'wllah, Abdwu'l)
  - space insertion (Baha'u llah, 'Abdu' l-Bahá)
  - apostrophe drop or substitution (Bahau'llah, Baha`u`llah)
  - í → i, { , t, [, |  (Baha'{, Baha't)
  - á → a  (standard diacritical loss)
  - ® © appearing (footnote misreads)
  - ) appearing in middle of words
"""

import re


def _build_patterns():
    """Build all pattern→replacement pairs, ordered longest-first."""

    patterns = []

    def add(pat, repl, flags=0):
        patterns.append((re.compile(pat, re.UNICODE | flags), repl))

    # ================================================================
    # BAHÁ'U'LLÁH — the most commonly garbled word
    # Tesseract variants: Baha'wllah, Baha'u llah, Baha'uwllah,
    #   Baha'u lah, Bahaw llah, Baha w llah, etc.
    # ================================================================
    # Possessive forms first (longer match)
    add(r"\bBah[aá][''`]?\s*[uwv][''`]?\s*ll[aá]h[''`]?s\b", "Bahá'u'lláh's")
    # Main form — very fuzzy: Bah + a/á + optional quote + u/w/v (1-2 chars) + optional quote/space + ll + a/á + h
    add(r"\bBah[aá][''`]?\s*[uwv]{1,2}[''`]?\s*ll[aá]h\b", "Bahá'u'lláh")
    # Even more garbled: missing the u entirely
    add(r"\bBah[aá][''`]?ll[aá]h\b", "Bahá'u'lláh")

    # ================================================================
    # 'ABDU'L-BAHÁ
    # Variants: Abdwu'l, 'Abdu' l-, Abdu'l, Abdul-, Abdu l-
    # ================================================================
    add(r"[''`]?Abd[uwv]{1,2}[''`]?\s*l-Bah[aá]\b", "'Abdu'l-Bahá")
    add(r"\bAbdul-Bah[aá]\b", "'Abdu'l-Bahá")
    add(r"[''`]?Abd[uwv]{1,2}[''`]?\s*l-Bah[aá][''`]?s\b", "'Abdu'l-Bahá's")

    # ================================================================
    # THE BÁB
    # ================================================================
    add(r"\bthe B[aá]b\b", "the Báb")
    add(r"\bThe B[aá]b\b", "The Báb")
    add(r"\bthe B[aá]b[''`]s\b", "the Báb's")
    add(r"\bB[aá]b[ií]\b", "Bábí")
    add(r"\bB[aá]b[ií]s\b", "Bábís")
    add(r"\bB[aá]b[''`]s\b", "Báb's")

    # ================================================================
    # BAHÁ'Í / BAHÁ'ÍS
    # Variants: Baha'i, Baha'{, Baha't, Baha'|, Baha i, Bahai
    # ================================================================
    add(r"\bBah[aá][''`]?[ií{t|\[]\b", "Bahá'í")
    add(r"\bBah[aá][''`]?[ií{t|\[]s\b", "Bahá'ís")
    add(r"\bBah[aá][''`]?\s+[ií]\b", "Bahá'í")  # space before i
    add(r"\bBah[aá]i\b", "Bahá'í")
    add(r"\bBah[aá]is\b", "Bahá'ís")
    add(r"\bBah[aá][''`]\s(?=[a-z])", "Bahá'í ")  # "Baha' identity" → "Bahá'í identity"
    add(r"\bBah[aá][''`][ií][''`]?s\b", "Bahá'ís")

    # ================================================================
    # MAJOR WORKS
    # ================================================================
    add(r"\bKit[aá]b-i-[IÍií]q[aá]n\b", "Kitáb-i-Íqán")
    add(r"\bKit[aá]b-i-Aqdas\b", "Kitáb-i-Aqdas")
    add(r"\bLaw[hḥ]-i-[HḤh]ikmat\b", "Lawḥ-i-Ḥikmat")
    add(r"\bLaw[hḥ]\b", "Lawḥ")
    add(r"\bIshr[aá]q[aá]t\b", "Ishráqát")
    add(r"\bBish[aá]r[aá]t\b", "Bishárát")
    add(r"\b[TṬ]ar[aá]z[aá]t\b", "Ṭarázát")
    add(r"\bTajall[ií]y[aá]t\b", "Tajallíyát")
    add(r"\bKalim[aá]t\b", "Kalimát")
    add(r"\bS[uú]riy-i-Haykal\b", "Súriy-i-Haykal")
    add(r"\bS[uú]riy-i-Mul[uú]k\b", "Súriy-i-Mulúk")

    # ================================================================
    # INSTITUTIONS
    # ================================================================
    add(r"\bMashriqu[''`]l-Adhk[aá]r\b", "Mashriqu'l-Adhkár")
    add(r"\b[HḤ]a[zẓ][ií]ratu[''`]l-Quds\b", "Ḥaẓíratu'l-Quds")
    add(r"\b[HḤ]uq[uú]qu[''`]ll[aá]h\b", "Ḥuqúqu'lláh")

    # ================================================================
    # HOLY DAYS
    # ================================================================
    add(r"\bRi[dḍ]v[aá]n\b", "Riḍván")
    add(r"\bNaw-?R[uú]z\b", "Naw-Rúz")
    add(r"\bAyy[aá]m-i-H[aá]\b", "Ayyám-i-Há")

    # ================================================================
    # PLACES (fuzzy for OCR)
    # ================================================================
    add(r"\b[TṬ]ihr[aá]n\b", "Ṭihrán")
    add(r"\bTehran\b", "Ṭihrán")
    add(r"[''`]Akk[aá]\b", "'Akká")
    add(r"\bAkk[aá]\b", "'Akká")
    add(r"\bSh[ií]r[aá]z\b", "Shíráz")
    add(r"\bBaghd[aá]d\b", "Baghdád")
    add(r"\bI[sṣ]fah[aá]n\b", "Iṣfahán")
    add(r"\bTabr[ií]z\b", "Tabríz")
    add(r"\bM[aá]zindar[aá]n\b", "Mázindarán")
    add(r"\bBahj[ií]\b", "Bahjí")
    add(r"\bAdrianaople\b", "Adrianople")
    add(r"\bAdrian[oó]p[ol]e\b", "Adrianople")

    # ================================================================
    # PERSONS
    # ================================================================
    add(r"\b[TṬ][aá]hirih\b", "Ṭáhirih")
    add(r"\bQudd[uú]s\b", "Quddús")
    add(r"\bMull[aá]\s+[HḤ]usayn\b", "Mullá Ḥusayn")
    add(r"\bMull[aá]\b", "Mullá")
    add(r"\bM[ií]rz[aá]\b", "Mírzá")
    add(r"\b[HḤ][aá]j[ií]\b", "Ḥájí")
    add(r"\bSul[tṭ][aá]n\b", "Sulṭán")
    add(r"\bNab[ií]l\b", "Nabíl")
    add(r"\bNab[ií]l-i-A[''`]?[zẓ]am\b", "Nabíl-i-A'ẓam")
    add(r"\bBad[ií][''`]?\b", "Badí'")

    # ================================================================
    # ISLAMIC / ARABIC TERMS
    # ================================================================
    add(r"\bQur[''`]?[aá]n\b", "Qur'án")
    add(r"\bQuran\b", "Qur'án")
    add(r"\b[HḤ]ad[ií]th\b", "Ḥadíth")
    add(r"\bhadith\b", "ḥadíth")
    add(r"\bShar[ií][''`]?ah\b", "Sharí'ah")
    add(r"\b[SṢ][uú]f[ií]\b", "Ṣúfí")
    add(r"\bIm[aá]m\b", "Imám")
    add(r"\bim[aá]m\b", "imám")
    add(r"\bMu[hḥ]ammad\b", "Muḥammad")
    add(r"\b[''`]?Ulam[aá]\b", "'Ulamá")
    add(r"\bF[aá][tṭ]imih\b", "Fáṭimih")
    add(r"\b[HḤ]usayn\b", "Ḥusayn")
    add(r"\b[HḤ]asan\b", "Ḥasan")

    # ================================================================
    # PUBLICATION-SPECIFIC
    # ================================================================
    add(r"[''`]Irf[aá]n\b", "'Irfán")
    add(r"\bIrfan\b", "'Irfán")
    add(r"\bSaf[ií]n[ie]h?-yi\s+[''`]?Irf[aá]n\b", "Safínih-yi 'Irfán")

    # ================================================================
    # COMMON BAHÁ'Í TERMS
    # ================================================================
    add(r"\bBay[aá]n\b", "Bayán")
    add(r"\bNuq[tṭ]ih\b", "Nuqṭih")
    add(r"\b[HḤ]a[dḍ]rat\b", "Ḥaḍrat")
    add(r"\bQayy[uú]mu[''`]l-Asm[aá][''`]?\b", "Qayyúmu'l-Asmá'")
    add(r"\bDawn-?Breakers\b", "Dawn-Breakers")
    add(r"\bKhayru[''`]ll[aá]h\b", "Khayru'lláh")

    # Ziyárat variations (very common in this corpus)
    add(r"\bzi[yv]?[aá]rat\b", "ziyárat")
    add(r"\bZi[yv]?[aá]rat\b", "Ziyárat")
    add(r"\bzidrat\b", "ziyárat")
    add(r"\bZidrat\b", "Ziyárat")

    # Munáját (prayers)
    add(r"\bmun[aá]j[aá]t\b", "munáját")
    add(r"\bmuna\s*j[aá]t\b", "munáját")

    # ================================================================
    # OCR ARTIFACT CLEANUP (non-diacritical)
    # ================================================================
    # ® and © are OCR misreads of footnote superscripts
    add(r"®", "")
    add(r"©", "")
    # Stray ) attached to words from OCR noise
    add(r"\bB[aá]b\)", "Báb")
    add(r"\bBáb\)", "Báb")
    # ~— is OCR misread of dash
    add(r"~—", "—")
    add(r"~-", "—")

    return patterns


COMPILED_PATTERNS = _build_patterns()


def normalize_quotes(text):
    """Normalize curly/smart quotes to ASCII. MUST run before diacritical dictionary."""
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u2032', "'").replace('\u2033', '"')
    text = text.replace('\u00b4', "'")
    text = text.replace('\u0060', "'")
    return text


def restore_diacriticals(text):
    """Apply diacritical restoration to text."""
    for pattern, replacement in COMPILED_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def fix_ocr_punctuation(text):
    """Fix common OCR punctuation errors."""
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r' ([.,;:!?])', r'\1', text)
    return text


def normalize_macrons(text):
    """Convert macrons to acute accents (standard Bahá'í transliteration uses acute)."""
    macron_to_acute = str.maketrans('āēīōūĀĒĪŌŪ', 'áéíóúÁÉÍÓÚ')
    return text.translate(macron_to_acute)


if __name__ == "__main__":
    # Test all the fuzzy patterns
    tests = [
        ("The Baha'i Faith and Baha'u'llah.", "The Bahá'í Faith and Bahá'u'lláh."),
        ("Baha'wllah was a prophet.", "Bahá'u'lláh was a prophet."),
        ("Baha'uwllah and 'Abdwu'l-Baha", "Bahá'u'lláh and 'Abdu'l-Bahá"),
        ("Baha'u llah in Baghdad", "Bahá'u'lláh in Baghdád"),
        ("Baha'w llah and Baha't Faith", "Bahá'u'lláh and Bahá'í Faith"),
        ("the Bab in Shiraz", "the Báb in Shíráz"),
        ("Kitab-i-Iqan and Qur'an", "Kitáb-i-Íqán and Qur'án"),
        ("Tahirih and Quddus and Mulla Husayn", "Ṭáhirih and Quddús and Mullá Ḥusayn"),
        ("Ridvan and Naw-Ruz", "Riḍván and Naw-Rúz"),
        ("the zidrat to Akka", "the ziyárat to 'Akká"),
        ("Shrine of the Bab) ~— Universal", "Shrine of the Báb —  Universal"),
    ]

    print("=== Fuzzy Pattern Tests ===\n")
    passed = 0
    for input_text, expected in tests:
        input_text = normalize_quotes(input_text)
        result = restore_diacriticals(input_text)
        result = normalize_macrons(result)
        ok = "✓" if result.strip() == expected.strip() else "✗"
        if ok == "✓":
            passed += 1
        else:
            print(f"  {ok} Input:    {input_text}")
            print(f"     Expected: {expected}")
            print(f"     Got:      {result}")
            print()

    print(f"\n{passed}/{len(tests)} tests passed")
