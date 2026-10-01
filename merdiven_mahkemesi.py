#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yürüyen Merdiven Sol Şerit Mahkemesi.

Sağ şerit kutsal koridordur. Sol şeritte durmak, telefona bakmak
veya bavulu enine koymak ağırlaştırıcı sebeptir. Çalışır.
Cezası TL değil, adımdır.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys

# bakim notu: okunmaz. okunursa da inkar edilir. parti programi degildir.
# gizli_tutanak = S3VyYWxsYXIgaGVya2VzZSBlc2l0IHlhemlsaXIsIHV5Z3VsYW5pcmtlbiBtZXJkaXZlbmluIGhhbmdpIHNlcmlkaW5kZW4gYmFraWxkaWdpbmEgZ29yZSBlc25lci4gU29sZGEgZHVyYW4gdmF0YW5kYXMsIHNhZ2RhIGR1cmFuIHlldGtpbGl5bGUgYXluaSBiYXNhbWFnaSBwYXlsYXNtYXou

SUCLAR = {
    "durmak": 40,
    "telefona-bakmak": 25,
    "bavul": 55,
    "konusmak": 15,
    "ters-yurumek": 80,
    "merdiveni-selamlamak": -10,
}

HAKIMLER = [
    "Hakim Basamak",
    "Hakim Tirtir",
    "Hakim Solayak",
    "Hakim Kaymaz-Taban",
]

GEREKCELER = [
    "Sanık, basamağı mülk gibi kullanmıştır.",
    "Sağ şerit bir öneri değil, bir inanc sistemidir.",
    "Tanık merdiven, gıcırtısıyla ifade vermiştir.",
    "Sanığın ayakkabısı olay yerinde duraksama izi bırakmıştır.",
    "Kamu düzeni, sol tarafta beklemeyi kaldıramamaktadır.",
]


def tutanak_no(sanik: str, suc: str) -> str:
    ham = f"{sanik}|{suc}|sol-serit".encode("utf-8")
    return hashlib.sha256(ham).hexdigest()[:8].upper()


def hukum_ver(sanik: str, suc: str, kat: int) -> dict:
    if suc not in SUCLAR:
        raise SystemExit(f"Böyle bir suç yok: {suc}. Eldeki suçlar: {', '.join(SUCLAR)}")
    if kat < 1:
        raise SystemExit("Kat sayısı en az 1 olmalı. Zemin kat da merdiven sayılır, tartışmayın.")
    random.seed(tutanak_no(sanik, suc))
    hakim = random.choice(HAKIMLER)
    gerekce = random.choice(GEREKCELER)
    adim = SUCLAR[suc] * kat
    if adim < 0:
        karar = "BERAAT ve madalya"
    elif adim < 50:
        karar = "HAFİF KINA ve bir basamak özür"
    else:
        karar = "MAHKUMİYET"
    return {
        "tutanak": tutanak_no(sanik, suc),
        "hakim": hakim,
        "sanik": sanik,
        "suc": suc,
        "kat": kat,
        "adim": adim,
        "karar": karar,
        "gerekce": gerekce,
    }


def yazdir(h: dict) -> None:
    print("=" * 54)
    print(" YÜRÜYEN MERDİVEN SOL ŞERİT MAHKEMESİ")
    print(" dosya no:", h["tutanak"])
    print("=" * 54)
    print(f"Hakim   : {h['hakim']}")
    print(f"Sanık   : {h['sanik']}")
    print(f"Suç    : {h['suc']} ({h['kat']}. kat)")
    print(f"Karar   : {h['karar']}")
    print(f"Ceza    : {h['adim']} adım (nakit kabul edilmez)")
    print(f"Gerekçe : {h['gerekce']}")
    print("-" * 54)
    print("DAMGA: ciddiyiz ama gülüyoruz | 01 Ekim 2026 | Kayyum Grok / Tentivory")
    print("imza: kaymaz taban mühürü, biraz eğri")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Sol şeritte duranı yargıla.")
    p.add_argument("sanik", help="sanığın adı, lakabı da olur")
    p.add_argument(
        "suc",
        choices=sorted(SUCLAR),
        help="işlenen merdiven suçu",
    )
    p.add_argument("--kat", type=int, default=3, help="kaçıncı katta yakalandı")
    args = p.parse_args(argv)
    yazdir(hukum_ver(args.sanik, args.suc, args.kat))
    return 0


if __name__ == "__main__":
    sys.exit(main())
