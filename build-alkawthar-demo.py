#!/usr/bin/env python3
"""Adapt the Habana Medical Service demo site into an Al-Kawthar Islamic
Hospital (Tamale) demo site.

Reads ~/workspace/user/files/habana-contact-page-rebuild-small.html and
writes ~/workspace/clinic-websites/alkawthar-islamic-hospital.html.

What changes:
- Branding: Habana Medical Service (Tamale) -> Al-Kawthar Islamic
  Hospital (Tamale); phone, email, address, maps links. WhatsApp is
  assumed to be the main phone number (unconfirmed). Al-Kawthar has NO
  Facebook page and no other socials — social links are removed.
- Colours: teal/amber -> Islamic green/gold, so the demo does not look
  like Habana's. The logo is the hospital's REAL logo (green with Arabic
  script, red cross, crescent), sent by the user 2026-11-21, cropped to
  the logo tile and upscaled. The 5 generated service photos were
  re-edited 2026-11-21 so the doctors and nurses look Islamic (hijab for
  the women, kufi for the male sonographer).
- Services: 15 -> 12 services. Removes Habana-only services (ENT,
  Ophthalmology, Neurosurgery, Endoscopy, Emergency & Critical Care,
  Paediatrics, Counselling, Dietetics, Preventive Healthcare, Diagnostic
  Imaging, Internal Medicine, Fertility Centre, General Surgery, Urology,
  Gynaecology, Rehabilitation) and adds Al-Kawthar services (Outpatient
  Consultation, Inpatient Care, Laboratory, Pharmacy, Dental Clinic,
  Optical Clinic, Ultrasound & Scan, Maternity Services, Mother & Child
  Care, Minor Theatre, Physiotherapy, Health Screenings). Only ultrasound
  is claimed for imaging — no CT, MRI, X-ray, dialysis, fertility/IVF,
  general surgery, ambulance or ICU. No NHIS claim (unconfirmed).
- Removes Habana-only content: founder story, awards, 15-year celebration,
  CT scan / mammography claims, the Friday 9:00 AM cervical clinic time,
  Habana social links, staff sign-in. There is NO founder at Al-Kawthar —
  the About page tells the hospital's own story (opened April 2026, run by
  the Wifaq Foundation) instead.
- Islamic identity (user, 2026-11-21): sold clearly but not saturated —
  the tagline "Compassionate Care. Guided by Faith." leads the hero, the
  About story and the values carry the faith-based care, and the Female
  Ward is a facility card; the clinical content stays clinical. Do NOT
  claim "first Islamic hospital" (disputed) and do NOT mention Anbariya,
  sects or the ownership dispute anywhere.
- Photos: Habana's embedded photos are replaced with the hospital's real
  Google Maps photos (12, downloaded 2026-11-21; the 5 small ones were
  upscaled one by one and verified), five generated photos of Ghanaian
  people (dental, optical, scan, maternity, physio — no signs or text in
  them), and professional stock photos matched to each service
  (del-photos/services/, 3 per service). Stock and generated photos are
  stand-ins for the demo — swap in the hospital's real photos when
  available.
"""
import base64
import json
import re
import urllib.parse
from pathlib import Path

SRC = Path.home() / "workspace/user/files/habana-contact-page-rebuild-small.html"
DST = Path.home() / "workspace/clinic-websites/alkawthar-islamic-hospital.html"
HERE = Path(__file__).resolve().parent


def _data_uri(path, mime="image/jpeg"):
    return "data:%s;base64,%s" % (
        mime, base64.b64encode(Path(path).read_bytes()).decode())


# Al-Kawthar Islamic Hospital photos (Google Maps, downloaded 2026-11-21):
# the real pink two-storey building, the night view, the corridors and the
# services board. The 5 small ones (640x480 / 853x480) were upscaled one
# by one and verified; the originals are kept as *-original.jpg.
ALK_BUILDING_FRONT_WIDE = _data_uri(HERE / "alkawthar-photos" / "alk-building-front-wide.jpg")
ALK_BUILDING_NIGHT = _data_uri(HERE / "alkawthar-photos" / "alk-building-night.jpg")
ALK_BUILDING_STREETVIEW = _data_uri(HERE / "alkawthar-photos" / "alk-streetview-day.jpg")
ALK_BUILDING_FRONT_SIGN = _data_uri(HERE / "alkawthar-photos" / "alk-building-front-sign.jpg")
ALK_BUILDING_FRONT = _data_uri(HERE / "alkawthar-photos" / "alk-building-front.jpg")
ALK_BUILDING_SIDE = _data_uri(HERE / "alkawthar-photos" / "alk-building-side.jpg")
ALK_ENTRANCE_GATE = _data_uri(HERE / "alkawthar-photos" / "alk-entrance-gate.jpg")
ALK_CORRIDOR_BRIGHT = _data_uri(HERE / "alkawthar-photos" / "alk-corridor-bright.jpg")
ALK_CORRIDOR_DOORS = _data_uri(HERE / "alkawthar-photos" / "alk-corridor-doors.jpg")
ALK_PHARMACY_LAB = _data_uri(HERE / "alkawthar-photos" / "alk-pharmacy-lab-balloons.jpg")
ALK_SERVICES_BOARD = _data_uri(HERE / "alkawthar-photos" / "alk-services-board.jpg")
ALK_SIGNBOARD_STREET = _data_uri(HERE / "alkawthar-photos" / "alk-signboard-street.jpg")
# The hospital's logo, REGENERATED 2026-11-21 (user: "regenerate a much
# better one with high quality"). The AI regeneration (v2) is a clean flat
# vector-style logo in the original layout: dark green tile, white border,
# red cross top-left, large white crescent, flowing white Arabic calligraphy
# "Al-Kawthar" across the middle, small white text bottom-right. The first
# regeneration (v1) was rejected: it added three white stars that are not
# in the real logo and moved the calligraphy to the bottom. The faithful
# crop+upscale of the user's photo is kept as alk-logo-real.jpg; the small
# bottom-right text in v2 reads "medical services" in Arabic, which is a
# guess, since that line is unreadable in the original photo.
ALK_LOGO = _data_uri(HERE / "alkawthar-photos" / "alk-logo-regen.jpg")

ALK_PHONE = "024 415 8915"
ALK_PHONE_TEL = "+233244158915"
ALK_PHONE_WA = "233244158915"
# Second contact number, from the hospital's own flyer (Oct 2026). Shown on
# the contact Call card, the emergency banner and the chat panel.
ALK_PHONE2 = "0553 602 241"
ALK_PHONE2_TEL = "+233553602241"
# Email from the hospital's own flyer (Oct 2026).
ALK_EMAIL = "alkawtharhospital@gmail.com"
# WhatsApp is ASSUMED to be the main phone 024 415 8915 (unconfirmed).
ALK_ADDR = "Watherson Area, behind the Northern Regional Coordinating Council, Tamale"
ALK_MAPS_DEST = "Al-Kawthar%20Islamic%20Hospital%2C%20Tamale%2C%20Ghana"
# NOTE: Al-Kawthar has no Facebook page and no other socials — social links
# are removed, never invented.


# ---------------------------------------------------------------- placeholders
def _esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


_GRADS = [("#1d8a4c", "#073d1f"), ("#0e7a3d", "#062b17"),
          ("#27a35c", "#0a4d28"), ("#128a48", "#073d1f")]


def ph(title, sub, w, h, variant=0):
    """Navy placeholder image as a data-URI SVG."""
    g1, g2 = _GRADS[variant % len(_GRADS)]
    cx, cy = w // 2, int(h * 0.30)
    r = max(18, int(h * 0.085))
    tfs = max(20, min(46, w // 26))
    sfs = max(13, tfs // 2)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/>'
        '</linearGradient></defs>'
        '<rect width="{w}" height="{h}" fill="url(#g)"/>'
        '<circle cx="{cx}" cy="{cy}" r="{r2}" fill="rgba(255,255,255,0.13)"/>'
        '<rect x="{x1}" y="{y1}" width="{s}" height="{s2}" rx="4" fill="#ffffff"/>'
        '<rect x="{x2}" y="{y2}" width="{s2}" height="{s}" rx="4" fill="#ffffff"/>'
        '<text x="50%" y="{ty}%" text-anchor="middle" font-family="Georgia, serif" '
        'font-size="{tfs}" font-weight="600" fill="#ffffff">{title}</text>'
        '<text x="50%" y="{sy}%" text-anchor="middle" font-family="Arial, sans-serif" '
        'font-size="{sfs}" fill="rgba(255,255,255,0.82)">{sub}</text>'
        '</svg>'
    ).format(w=w, h=h, g1=g1, g2=g2, cx=cx, cy=cy, r2=r + 26,
             x1=cx - 5, y1=cy - r, s=10, s2=r * 2,
             x2=cx - r, y2=cy - 5,
             ty=62, sy=72, tfs=tfs, sfs=sfs,
             title=_esc(title), sub=_esc(sub))
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="")


def fab_svg():
    """Small 'A' mark for the chat button and the logo (Al-Kawthar green,
    gold ring). SUPERSEDED 2026-11-21: the hospital's real logo is now
    used (ALK_LOGO). Kept only so nothing else breaks."""
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="160" viewBox="0 0 200 160">'
        '<rect x="6" y="6" width="188" height="148" rx="28" fill="#0e7a3d"/>'
        '<rect x="6" y="6" width="188" height="148" rx="28" fill="none" stroke="#c9a227" stroke-width="4"/>'
        '<text x="100" y="112" text-anchor="middle" font-family="Georgia, serif" '
        'font-size="92" font-weight="700" fill="#ffffff">A</text></svg>'
    )
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="")


def map_svg():
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="380" viewBox="0 0 640 380">'
        '<rect width="640" height="380" fill="#e8eef6"/>'
        '<rect x="0" y="60" width="640" height="90" fill="#dce6f2"/>'
        '<rect x="0" y="230" width="640" height="70" fill="#dce6f2"/>'
        '<g stroke="#ffffff" stroke-width="16"><path d="M0 105 H640"/><path d="M0 265 H640"/>'
        '<path d="M150 0 V380"/><path d="M330 0 V380"/><path d="M510 0 V380"/></g>'
        '<g stroke="#ffffff" stroke-width="8"><path d="M0 190 H640"/></g>'
        '<rect x="360" y="120" width="120" height="55" rx="8" fill="#cfe3d4"/>'
        '<circle cx="330" cy="190" r="26" fill="#0e7a3d"/>'
        '<circle cx="330" cy="190" r="26" fill="none" stroke="#c9a227" stroke-width="4"/>'
        '<text x="330" y="199" text-anchor="middle" font-family="Georgia, serif" '
        'font-size="26" font-weight="700" fill="#ffffff">A</text>'
        '<text x="330" y="252" text-anchor="middle" font-family="Arial, sans-serif" '
        'font-size="19" font-weight="700" fill="#062b17">Al-Kawthar Islamic Hospital</text>'
        '<text x="330" y="280" text-anchor="middle" font-family="Arial, sans-serif" '
        'font-size="16" fill="#5a6b7a">Tamale</text></svg>'
    )
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="")


FAB = ALK_LOGO
LOGO = FAB
MAP_IMG = map_svg()

# Live Google Map (user, 2026-11-21): the real Google Map centred on the
# hospital (9.4106762, -0.8226533 — from its Google Maps listing), with
# the pin chip and a clickable "Tap to open map" link. The iframe is
# interactive (pan/zoom); the link opens directions in Google Maps.
MAP_LIVE_HTML = (
    '        <div class="map-embed">\n'
    '          <iframe class="map-live-frame" src="https://www.google.com/maps?q=9.4106762,-0.8226533&amp;z=16&amp;output=embed" style="border:0" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade" title="Map — Al-Kawthar Islamic Hospital, Tamale"></iframe>\n'
    '          <span class="map-pin-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg> Al-Kawthar Islamic Hospital</span>\n'
    '          <a class="map-open-chip" href="https://www.google.com/maps/dir/?api=1&amp;destination=Al-Kawthar%20Islamic%20Hospital%2C%20Tamale%2C%20Ghana" target="_blank" rel="noopener">Tap to open map</a>\n'
    '        </div>'
)


# ---------------------------------------------------------------- Al-Kawthar services
# Each entry: name, blurb (grid card), tag, about (2 paras), helps (6),
# who, know, photos (3 PH keys).
SERVICES = [
    {
        "name": "Outpatient Consultation",
        "blurb": "General consultations for adults and families — walk in and see a doctor, any day.",
        "tag": "General consultations for adults and families — walk in and see a doctor, any day, without an appointment.",
        "about": [
            "Our outpatient department (OPD) is the first door for most patients. A doctor listens to your symptoms, examines you and, where needed, arranges tests in our own laboratory or an ultrasound scan — so the cause of a problem is found rather than guessed at.",
            "Many everyday problems are treated right here: fevers including malaria, coughs and colds, stomach upsets, skin problems and minor injuries. If you need a specialist, your doctor will refer you to the right clinic in the hospital.",
        ],
        "helps": [
            "Fevers, including malaria",
            "Coughs, colds and flu",
            "Stomach upsets and diarrhoea",
            "Skin rashes and minor injuries",
            "Headaches and body pains",
            "Referrals to our specialists when you need them",
        ],
        "who": "Anyone who feels unwell or has a health concern — walk in, no appointment needed.",
        "know": "Bring a list of medicines you are taking and any previous test results. In an emergency, come straight in — no appointment needed.",
        "photos": ["internal1", "internal2", "internal3"],
    },
    {
        "name": "Inpatient Care",
        "blurb": "Comfortable wards with caring nurses, day and night.",
        "tag": "Comfortable wards with caring nurses, day and night — so you can recover in peace.",
        "about": [
            "When you need to stay with us, our wards give you a clean, comfortable bed, regular nursing care and daily doctor's rounds. Our nurses check on you through the day and night, and your family is welcome to visit.",
            "We care for patients recovering from illness or a minor operation, and for people who need fluids, medicines or close monitoring for a few days.",
        ],
        "helps": [
            "Recovery after illness or a minor operation",
            "Intravenous fluids and medicines",
            "Close monitoring by our nurses",
            "Daily doctor's rounds on the ward",
            "Comfortable beds in clean wards",
            "Family visits while you recover",
        ],
        "who": "Patients whose doctor has asked them to stay for treatment or observation.",
        "know": "Bring your medicines and any previous test results. If you are coming for a planned stay, your doctor will tell you what to bring.",
        "photos": ["alk-corridor-bright", "alk-corridor-doors", "surgery2"],
    },
    {
        "name": "Laboratory",
        "blurb": "Accurate blood, urine and other laboratory tests with prompt results.",
        "tag": "Accurate blood, urine and other laboratory tests, with prompt results your doctor can act on.",
        "about": [
            "Good treatment starts with the right diagnosis. Our laboratory scientists run a wide range of tests on blood, urine and other samples, following careful quality procedures so your doctor can trust the result.",
            "Because the laboratory is here in the hospital, results come back quickly — often the same day — and go straight to your care team.",
        ],
        "helps": [
            "Full blood count and malaria tests",
            "Blood sugar and diabetes monitoring",
            "Liver and kidney function tests",
            "Pregnancy tests",
            "Urine and stool examinations",
            "Pre-surgery and antenatal test panels",
        ],
        "who": "Patients whose doctor has ordered tests, expectant mothers doing antenatal panels, and anyone preparing for a minor operation.",
        "know": "Some blood tests need you to fast — your doctor or the laboratory will tell you if yours does. Bring your request form if you were given one.",
        "photos": ["lab1", "lab2", "lab3"],
    },
    {
        "name": "Pharmacy",
        "blurb": "An on-site pharmacy — collect your medicines before you leave.",
        "tag": "An on-site pharmacy, so you can collect your prescribed medicines before you leave — with clear advice on how to take them.",
        "about": [
            "Our pharmacy is inside the hospital, steps from the consulting rooms. After your appointment you can collect your prescribed medicines straight away — no separate trip across town.",
            "Our pharmacists check every prescription, explain how and when to take your medicine, and answer questions about side effects or medicines you are already taking.",
        ],
        "helps": [
            "Dispensing prescribed medicines after your visit",
            "Advice on how to take your medicine safely",
            "Checking that medicines are safe to take together",
            "Refills for long-term conditions like diabetes and hypertension",
            "Advice for older people and children on their medicines",
            "Storage and expiry guidance",
        ],
        "who": "Every patient with a prescription — and anyone on long-term medication who wants their medicines reviewed.",
        "know": "Bring your prescription and a list of any other medicines you take, including herbal ones, so the pharmacist can check they are safe together.",
        "photos": ["pharmacy1", "pharmacy2", "pharmacy3"],
    },
    {
        "name": "Dental Clinic",
        "blurb": "Check-ups, cleaning, fillings, extractions and other dental treatment.",
        "tag": "Check-ups, cleaning, fillings, extractions and other dental treatment — for healthy teeth and a confident smile.",
        "about": [
            "Our dental clinic treats toothache and decay, cares for your gums and helps you keep your natural teeth for life. We explain what each treatment involves and what it will feel like before we begin.",
            "Regular check-ups catch small problems — a tiny cavity, early gum disease — while they are still simple and less costly to fix.",
        ],
        "helps": [
            "Dental check-ups and professional cleaning",
            "Fillings for decayed teeth",
            "Tooth extraction, including painful wisdom teeth",
            "Toothache and dental abscesses",
            "Gum disease treatment",
            "Dental advice for children and adults",
        ],
        "who": "Adults and children — anyone with tooth pain, a broken or decayed tooth, bleeding gums, or who is simply due a check-up.",
        "know": "Dental pain with swelling of the face, or difficulty opening your mouth, needs same-day care — call us or come in.",
        "photos": ["alk-gen-dental", "dental", "dental2"],
    },
    {
        "name": "Optical Clinic",
        "blurb": "Eye tests, glasses and care for your sight.",
        "tag": "Eye tests, glasses and care for your sight — so you can see clearly and comfortably.",
        "about": [
            "Our optical clinic checks your eyesight and cares for common eye problems. We test your vision, explain what we find in plain language, and help you get the glasses you need.",
            "If your eyes need treatment beyond the clinic, we will refer you to the right care — and we treat eye infections and minor eye injuries here.",
        ],
        "helps": [
            "Eye tests and vision checks",
            "Glasses for short and long sight",
            "Eye infections and irritation",
            "Minor eye injuries",
            "Vision screening for children and adults",
            "Advice on caring for your eyes",
        ],
        "who": "Anyone whose vision is blurred, whose eyes are painful, red or itchy, or who needs glasses.",
        "know": "Bring your current glasses if you have them. If something has entered your eye, do not rub it — come in straight away.",
        "photos": ["alk-gen-optical", "counsel1", "counsel2"],
    },
    {
        "name": "Ultrasound & Scan",
        "blurb": "Ultrasound scans for pregnancy, abdomen and other organs.",
        "tag": "Ultrasound scans for pregnancy, abdomen and other organs — clear pictures that guide your treatment.",
        "about": [
            "Our ultrasound room offers scans that let your doctor see inside the body without surgery — for pregnancy, the abdomen, the pelvis and other organs.",
            "Scans support almost every other service here — from antenatal care and maternity to minor theatre — and results are reported promptly to your doctor.",
        ],
        "helps": [
            "Pregnancy (obstetric) ultrasound",
            "Ultrasound of the abdomen and pelvis",
            "Scans to guide your doctor's treatment",
            "Results reported promptly to your doctor",
            "Antenatal scans at every stage of pregnancy",
            "Call ahead so we can prepare for your scan",
        ],
        "who": "Anyone whose doctor needs a clearer picture — expectant mothers, patients with unexplained pain, and people preparing for a minor operation.",
        "know": "For some scans, call ahead so we can prepare — a few need you to fast or drink water beforehand, and we will explain when you book.",
        "photos": ["alk-gen-scan", "imaging1", "imaging2"],
    },
    {
        "name": "Maternity Services",
        "blurb": "Antenatal care, safe delivery and care for mothers and babies — with privacy and respect.",
        "tag": "Antenatal care, safe delivery and care for mothers and babies — with privacy and respect, from the first visit to the weeks after birth.",
        "about": [
            "Our maternity team cares for mothers through pregnancy, birth and the weeks after delivery. Antenatal visits track your health and your baby's growth, with ultrasound and laboratory tests available on site, so concerns are picked up early.",
            "Our maternity care respects your privacy and your faith — with a dedicated female ward and female staff available. When the time comes, our maternity department is ready day and night — and after delivery we check both mother and baby before you go home.",
        ],
        "helps": [
            "Antenatal (pregnancy) care and ultrasound scans",
            "Safe delivery, with surgical support if a caesarean is needed",
            "Postnatal checks for mother and baby",
            "Family planning advice",
            "Extra care when a pregnancy needs closer watching",
            "Advice on feeding and caring for your newborn",
        ],
        "who": "Expectant mothers, women planning a pregnancy, and new mothers in the weeks after delivery.",
        "know": "For antenatal booking, come with any previous pregnancy records if you have them. If you notice bleeding, severe headache or reduced movement of the baby, come straight in.",
        "photos": ["alk-gen-maternity", "maternity", "maternity2"],
    },
    {
        "name": "Mother & Child Care",
        "blurb": "Care for mothers and children — from birth through the early years.",
        "tag": "Care for mothers and children — from birth through the early years, with guidance at every step.",
        "about": [
            "Our mother and child care looks after the health of mothers and their young children together — from the first weeks of life through the early years.",
            "We support breastfeeding, track your child's growth and development, give immunisations, and treat the common illnesses of childhood early, before they become serious.",
        ],
        "helps": [
            "Immunisation for babies and children",
            "Growth and development checks",
            "Breastfeeding support and advice",
            "Care for childhood fevers, coughs and diarrhoea",
            "Nutrition advice for mothers and children",
            "Health talks for mothers",
        ],
        "who": "Mothers with babies and young children, and any parent worried about their child's health or growth.",
        "know": "Bring your child's weighing card and immunisation record when you visit. If your child has a high fever or is unusually sleepy, come in early.",
        "photos": ["preventive3", "counsel3", "maternity2"],
    },
    {
        "name": "Minor Theatre",
        "blurb": "Minor surgical procedures in a clean, safe theatre.",
        "tag": "Minor surgical procedures in a clean, safe theatre — with careful aftercare on the ward.",
        "about": [
            "Our minor theatre handles small surgical procedures that do not need a major operation. Before any procedure, the team explains what is wrong, what the procedure involves and what recovery will look like, so you can decide with full information.",
            "After your procedure our nurses care for you until you are ready to go home, and we review your wound as it heals.",
        ],
        "helps": [
            "Removal of lumps and cysts",
            "Drainage of abscesses",
            "Cleaning and stitching of wounds",
            "Dressing changes and wound care",
            "Care for minor injuries",
            "Follow-up reviews after your procedure",
        ],
        "who": "Anyone whose doctor has recommended a minor procedure, and patients with wounds or swellings that need attention.",
        "know": "Some procedures need blood tests or a scan first — both are done here. Follow the instructions you are given about eating and drinking before your procedure.",
        "photos": ["surgery", "surgery2", "surgery3"],
    },
    {
        "name": "Physiotherapy",
        "blurb": "Rehabilitation after injury or surgery — helping you move again.",
        "tag": "Rehabilitation after injury or surgery — helping you move again, with confidence.",
        "about": [
            "Our physiotherapy team helps you recover movement and strength after injury, surgery or illness, with a treatment plan built around your body and your goals.",
            "We care for back, neck and joint pain, sports injuries and stroke recovery — with guided exercise and hands-on treatment, step by step.",
        ],
        "helps": [
            "Back, neck and joint pain",
            "Recovery after surgery or a fracture",
            "Stroke rehabilitation",
            "Sports injuries — sprains, strains and overuse",
            "Guided exercise and strength training",
            "Advice to prevent the problem coming back",
        ],
        "who": "Anyone recovering from injury or surgery, living with back or joint pain, rebuilding strength after a stroke, or hurt playing sport.",
        "know": "Wear comfortable clothes you can move in. Bring any referral letters from your doctor.",
        "photos": ["alk-gen-physio", "physio1", "physio2"],
    },
    {
        "name": "Health Screenings",
        "blurb": "Check-ups that catch problems early — for you and your family.",
        "tag": "Check-ups that catch problems early — for you and your family, before small problems become big ones.",
        "about": [
            "Many serious illnesses give no warning until they are advanced. Our health screenings check the basics — blood pressure, blood sugar, cholesterol and more — so problems are found early, when they are easiest to treat.",
            "Screenings are for everyone, not only people who feel unwell. Come with your family, and our team will explain your results in plain language.",
        ],
        "helps": [
            "Blood pressure checks",
            "Blood sugar and diabetes screening",
            "Cholesterol checks",
            "General health check-ups",
            "Medical reports for work or school",
            "Health education for you and your family",
        ],
        "who": "Everyone — especially adults over 40, people with diabetes or high blood pressure in the family, and anyone who has not had a check-up in a while.",
        "know": "Some screening tests need you to fast — we will tell you when you book. Bring a list of medicines you take.",
        "photos": ["preventive1", "preventive2", "preventive3"],
    },
]

# Photo gallery entries: key -> (alt, caption). src is a placeholder built from caption.
# Photo gallery entries: key -> (alt, caption). src is a placeholder built from caption.
PH = {
    "internal1": ("A physician checking the blood pressure of a patient in a consulting room",
                  "Blood pressure and long-term condition checks"),
    "internal2": ("A doctor reviewing test results on a screen together with a patient",
                  "Reviewing your results together, in plain language"),
    "internal3": ("A physician listening to the chest of a patient during a ward round",
                  "Daily ward rounds for patients in our care"),
    "lab1": ("A laboratory scientist looking through a microscope at a sample, with test tubes beside her",
             "Samples examined carefully in our laboratory"),
    "lab2": ("A laboratory scientist loading samples into an automated analyser machine",
             "Modern analysers for fast, accurate results"),
    "lab3": ("A nurse taking a blood sample from the arm of a seated patient",
             "Blood samples taken gently, here at the hospital"),
    "pharmacy1": ("A pharmacist handing medicine to a patient across the pharmacy counter",
                  "Collect your medicine before you leave"),
    "pharmacy2": ("Shelves of medicines in the hospital pharmacy, with a pharmacist checking stock",
                  "Well-stocked shelves, checked daily"),
    "pharmacy3": ("A pharmacist checking a prescription carefully at a computer",
                  "Every prescription checked before it is dispensed"),
    "dental": ("A dentist in scrubs examining a patient reclined in the dental chair",
               "Treatment in the dental clinic"),
    "dental2": ("A smiling child in the dental chair giving a thumbs up beside the dentist",
                "Friendly visits that help children relax"),
    "preventive1": ("A nurse checking the blood pressure of a woman at a health screening",
                    "A careful check-up at your first visit"),
    "preventive2": ("A health educator giving a talk to families at a community health session",
                    "Clear explanations, in plain language"),
    "preventive3": ("A nurse giving a child an immunisation while the mother holds the child",
                    "Care for the whole family"),
    "maternity": ("A midwife checking a smiling pregnant mother, with an ultrasound machine behind her",
                  "An antenatal check, with ultrasound on hand"),
    "maternity2": ("A new mother holding her newborn baby in the maternity ward, with a midwife beside her",
                   "First moments with your baby, on the maternity ward"),
    "counsel1": ("A doctor listening attentively during a private consultation",
                 "A private consultation, at your own pace"),
    "counsel2": ("A calm, comfortable consultation room with two armchairs by a window",
                 "A calm, private room for your consultation"),
    "counsel3": ("A doctor talking gently with a couple during a consultation",
                 "Time to ask your questions, together"),
    "surgery": ("A surgical team in theatre scrubs operating under bright surgical lights",
                "Inside the operating theatre during a planned operation"),
    "surgery2": ("A nurse caring for a patient recovering in a hospital bed after surgery",
                 "Careful recovery care on the ward after your operation"),
    "surgery3": ("The gloved hands of a surgical team working together under operating lights",
                 "Experienced hands in theatre"),
    "physio1": ("A physiotherapist guiding a patient through an exercise",
                "Guided exercise, built around you"),
    "physio2": ("Hands-on physiotherapy treatment for a painful shoulder",
                "Hands-on treatment for pain and stiffness"),
    "imaging1": ("A doctor performing an ultrasound scan, with the image on the monitor",
                 "Ultrasound scans by skilled staff"),
    "imaging2": ("A sonographer performing a pregnancy ultrasound, with the baby visible on screen",
                 "Pregnancy scans, with your baby on screen"),
    "alk-corridor-bright": ("A bright corridor inside Al-Kawthar Islamic Hospital, with doors and windows along both sides",
                            "Inside the hospital — bright, clean corridors"),
    "alk-corridor-doors": ("A corridor inside Al-Kawthar Islamic Hospital, with brown wooden doors and cream walls",
                           "Inside the hospital — on the way to the wards"),
    "alk-gen-dental": ("A dentist talking with a smiling patient in the dental chair",
                       "A friendly visit, with your smile in mind"),
    "alk-gen-optical": ("An optometrist examining a patient's eyes with a handheld light",
                        "An eye test, with your sight in mind"),
    "alk-gen-scan": ("A sonographer performing a pregnancy ultrasound, with the baby visible on the monitor",
                     "Pregnancy scans, with your baby on screen"),
    "alk-gen-maternity": ("A midwife with a new mother holding her newborn baby in the maternity ward",
                          "First moments with your baby, on the maternity ward"),
    "alk-gen-physio": ("A physiotherapist guiding a patient through a leg exercise",
                       "Guided exercise, built around you"),
}

ALIASES = [
    ["Outpatient Consultation", ["opd", "outpatient", "consultation", "see a doctor", "see the doctor",
                                 "general consultation", "check-up", "checkup", "check up"]],
    ["Inpatient Care", ["inpatient", "admission", "admitted", "ward", "stay in hospital", "stay overnight"]],
    ["Laboratory", ["laboratory", "lab", "blood test", "test result", "sample", "urine test"]],
    ["Pharmacy", ["pharmacy", "pharmacist", "prescription", "medication", "medicines", "medicine", "refill"]],
    ["Dental Clinic", ["dental", "dentist", "tooth", "teeth", "toothache"]],
    ["Optical Clinic", ["optical", "optometrist", "eye test", "eye", "eyes", "glasses", "vision", "sight"]],
    ["Ultrasound & Scan", ["scan", "ultrasound", "imaging", "sonographer"]],
    ["Maternity Services", ["maternity", "pregnan-", "antenatal", "delivery",
                            "give birth", "baby", "babies", "newborn", "midwife",
                            "caesarean", "cesarean"]],
    ["Mother & Child Care", ["mother and child", "mother & child", "child health", "immunisation",
                             "immunization", "vaccination", "growth", "breastfeeding", "child"]],
    ["Minor Theatre", ["minor theatre", "minor theater", "theatre", "theater", "small operation",
                       "lump", "cyst", "abscess", "wound", "stitches"]],
    ["Physiotherapy", ["physiotherapy", "physio", "rehabilitation", "rehab",
                        "back pain", "sports injury", "stroke rehab"]],
    ["Health Screenings", ["screening", "health check", "blood pressure", "diabetes screening",
                           "medical report", "general check"]],
]

# "Our story" gallery: the real Al-Kawthar Islamic Hospital photos from
# Google Maps — the building, the corridors, the services board.
SLIDES = [
    {"label": "Our hospital",
     "alt": "The Al-Kawthar Islamic Hospital building in Tamale"},
    {"label": "Our hospital at night",
     "alt": "Al-Kawthar Islamic Hospital at night, with the illuminated sign"},
    {"label": "Our services",
     "alt": "Al-Kawthar's 24-hour services board"},
    {"label": "Our entrance",
     "alt": "The entrance gate of Al-Kawthar Islamic Hospital"},
    {"label": "Inside the hospital",
     "alt": "A bright corridor inside Al-Kawthar Islamic Hospital"},
    {"label": "Our corridors",
     "alt": "A corridor inside Al-Kawthar Islamic Hospital"},
    {"label": "Pharmacy & laboratory",
     "alt": "The pharmacy and laboratory fronts of Al-Kawthar Islamic Hospital"},
    {"label": "Find us",
     "alt": "The Al-Kawthar Islamic Hospital sign board on the street"},
    {"label": "Our building",
     "alt": "The side of the Al-Kawthar Islamic Hospital building"},
]

GO_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

FB_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>')


def svc_card(i, svc):
    n = i + 1
    thumb = _photo_uri(svc["photos"][0])
    alt = PH[svc["photos"][0]][0]
    name = svc["name"].replace("&", "&amp;")
    return (
        '<button type="button" class="svc-card" data-service="{name}">'
        '<img class="svc-thumb" src="{thumb}" alt="{alt}" />'
        '<span class="svc-num">{num:02d}</span><h3>{name}</h3><p>{blurb}</p>'
        '<span class="go">Learn more {go}</span></button>'
    ).format(name=name, thumb=thumb, alt=_esc(alt), num=n,
             blurb=svc["blurb"], go=GO_SVG)


# Patient reviews (2026-11-21): five-star reviews on the home page,
# after the About teaser. SAMPLE reviews — Al-Kawthar's real patient words
# should replace them before the site goes live. The hospital only opened
# in April 2026 and has no public patient reviews yet — do not present
# these samples as real.
REVIEWS_SECTION = (
    '  <section class="block wrap">\n'
    '    <p class="eyebrow">Patient reviews</p>\n'
    '    <h2>What our patients say.</h2>\n'
    '    <p class="intro">Here is what patients and families say about their care at Al-Kawthar.</p>\n'
    '    <div class="reviews-grid">\n'
    '      <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cThe nurses were so kind and the ward was very clean. I felt safe the whole time I was there.\u201d</p><p class="review-name">Aisha S. \u2014 Inpatient</p></article>\n'
    '      <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cThe team explained everything clearly and answered all our questions. We always felt supported.\u201d</p><p class="review-name">Ibrahim &amp; Fatima \u2014 Outpatients</p></article>\n'
    '      <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cI was seen quickly and the doctor took time to listen. The whole visit was smooth from start to finish.\u201d</p><p class="review-name">Mariam M. \u2014 Outpatient</p></article>\n'
    '    </div>\n'
    '    <div class="review-form-wrap">\n'
    '      <h3>Share your experience</h3>\n'
    '      <p>Visited Al-Kawthar? Tell us how it went. Your words help other families choose their hospital.</p>\n'
    '      <form class="review-form">\n'
    '        <label>Your name<input type="text" class="rv-name" required placeholder="e.g. Fatima A."></label>\n'
    '        <span class="rv-stars-label">Your rating</span>\n'
    '        <span class="rv-stars" role="radiogroup" aria-label="Your rating">\n'
    '          <button type="button" data-v="1" aria-label="1 star">\u2605</button>\n'
    '          <button type="button" data-v="2" aria-label="2 stars">\u2605</button>\n'
    '          <button type="button" data-v="3" aria-label="3 stars">\u2605</button>\n'
    '          <button type="button" data-v="4" aria-label="4 stars">\u2605</button>\n'
    '          <button type="button" data-v="5" aria-label="5 stars">\u2605</button>\n'
    '        </span>\n'
    '        <label>Your review<textarea class="rv-text" required rows="4" placeholder="Tell us about your visit..."></textarea></label>\n'
    '        <button type="submit" class="btn">Submit review</button>\n'
    '        <p class="rv-thanks" hidden>Thank you! Your review has been added below.</p>\n'
    '      </form>\n'
    '    </div>\n'
    '  </section>'
)

# Customer review form script (user, 2026-11-21): visitors write a review
# and it is added to the reviews grid on the page, with a thank-you.
# It works for every review form on the page (home + about).
REVIEW_FORM_JS = (
    '  <script>\n'
    '  // Customer review form: adds the visitor review to the grid.\n'
    '  document.querySelectorAll(".review-form").forEach(function (form) {\n'
    '    var stars = form.querySelectorAll(".rv-stars button");\n'
    '    var rating = 5;\n'
    '    function paint() {\n'
    '      stars.forEach(function (b) { b.classList.toggle("on", +b.dataset.v <= rating); });\n'
    '    }\n'
    '    stars.forEach(function (b) {\n'
    '      b.addEventListener("click", function () { rating = +b.dataset.v; paint(); });\n'
    '    });\n'
    '    paint();\n'
    '    form.addEventListener("submit", function (e) {\n'
    '      e.preventDefault();\n'
    '      var name = form.querySelector(".rv-name").value.trim();\n'
    '      var text = form.querySelector(".rv-text").value.trim();\n'
    '      if (!name || !text) return;\n'
    '      var section = form.closest("section");\n'
    '      var grid = section ? section.querySelector(".reviews-grid") : null;\n'
    '      if (!grid) return;\n'
    '      var card = document.createElement("article");\n'
    '      card.className = "value-card review-card";\n'
    '      var starsText = "\\u2605".repeat(rating) + "\\u2606".repeat(5 - rating);\n'
    '      function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }\n'
    '      card.innerHTML = `<p class="stars" aria-label="${rating} out of 5 stars">${starsText}</p><p>\u201c${esc(text)}\u201d</p><p class="review-name">${esc(name)} \u2014 Patient</p>`;\n'
    '      grid.appendChild(card);\n'
    '      var thanks = form.querySelector(".rv-thanks");\n'
    '      if (thanks) thanks.hidden = false;\n'
    '      form.reset();\n'
    '      rating = 5; paint();\n'
    '      card.scrollIntoView({ behavior: "smooth", block: "center" });\n'
    '    });\n'
    '  });\n'
    '  </script>\n'
)

# Reviews in the contact page's left column, under the form (user, 2026-11-21).
# Same sample reviews as the home/about sections, stacked vertically.
# The third review lives in the contact page's RIGHT column, under the map
# card (user, 2026-11-21): it fills the empty space there and balances the
# two columns. Same sample review as the other sections.
CONTACT_REVIEW_RIGHT = (
    '      <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cI was seen quickly and the doctor took time to listen. The whole visit was smooth from start to finish.\u201d</p><p class="review-name">Mariam M. \u2014 Outpatient</p></article>'
)

CONTACT_REVIEWS = (
    '      <div class="contact-reviews">\n'
    '        <p class="eyebrow">Patient reviews</p>\n'
    '        <h3>What our patients say.</h3>\n'
    '        <div class="reviews-stack">\n'
    '          <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cThe nurses were so kind and the ward was very clean. I felt safe the whole time I was there.\u201d</p><p class="review-name">Aisha S. \u2014 Inpatient</p></article>\n'
    '          <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cThe team explained everything clearly and answered all our questions. We always felt supported.\u201d</p><p class="review-name">Ibrahim &amp; Fatima \u2014 Outpatients</p></article>\n'
    '        </div>\n'
    '      </div>'
)

# Al-Kawthar overrides (2026-11-21), appended last in the stylesheet so they win:
# (a) restore the 24px side padding on every .block.wrap section — the
#     original .block{padding:72px 0} rule was wiping it out, so text sat
#     right on the left edge of the screen on every page;
# (b) shrink the chat button to a logo-only circle;
# (c) style the patient-reviews grid.
ALK_CSS_OVERRIDES = (
    '  /* Al-Kawthar overrides (2026-11-21) */\n'
    '  .wrap.block, section.wrap:not(.band){padding-left:24px;padding-right:24px}\n'
    '  /* Chat button: smooth open/shut (user, 2026-11-21). Only the width\n'
    '     animates — padding, gap, logo position and corner radius never\n'
    '     change, so nothing jumps; the label fades in as the pill opens. */\n'
    '  .chat-fab{width:56px;height:56px;padding:.45rem 1.05rem .45rem .45rem;border-radius:999px;justify-content:flex-start;gap:.55rem;overflow:hidden;transition:width .45s cubic-bezier(.4,0,.2,1),transform .18s ease,background .18s ease,box-shadow .18s ease}\n'
    '  .chat-fab.expanded{width:196px}\n'
    '  .chat-fab .fab-logo{width:40px;height:40px}\n'
    '  .chat-fab>span:last-child{white-space:nowrap;opacity:0;transition:opacity .3s ease}\n'
    '  .chat-fab.expanded>span:last-child{opacity:1}\n'
    '  .reviews-grid{display:grid;gap:16px;margin-top:36px;grid-template-columns:1fr}\n'
    '  @media(min-width:720px){.reviews-grid{grid-template-columns:repeat(3,1fr)}}\n'
    '  .review-card .stars{color:var(--accent);font-size:1.15rem;letter-spacing:.15em;margin-top:0}\n'
    '  .review-card .review-name{font-weight:700;color:var(--teal-ink);margin-top:14px}\n'
    '  .mission-grid{display:grid;gap:20px 32px;margin:28px 0 44px;grid-template-columns:1fr}\n'
    '  @media(min-width:720px){.mission-grid{grid-template-columns:1fr 1fr}}\n'
    '  .mission-grid h3{font-size:1.35rem;color:var(--teal-ink);margin:0 0 8px}\n'
    '  .mission-grid p{color:var(--muted);font-size:1.02rem;line-height:1.6;margin:0}\n'
    '  .contact-reviews{margin-top:48px}\n'
    '  .contact-reviews h3{font-size:1.35rem;color:var(--teal-ink);margin:0 0 16px}\n'
    '  .reviews-stack{display:grid;gap:16px}\n'
    '  /* Booking date + time boxes (user, 2026-11-21): the base rule only\n'
    '     styles text/tel/email inputs, so the date and time boxes fell back\n'
    '     to the browser grey. Give them the exact same look as the other\n'
    '     booking fields. */\n'
    '  input[type="date"],input[type="time"]{width:100%;border:1px solid var(--line);border-radius:12px;background:var(--bg);padding:.72rem .95rem}\n'
  '  /* Preview countdown timer bar (user, 2026-11-21): dark bar at the\n'
    '     very top, above the Open 24/7 bar; the numbers are orange. */\n'
    '  .preview-timer{background:#1c1c1e;color:#e8e8e8;text-align:center;padding:10px 16px;font-size:.82rem;letter-spacing:.1em;display:flex;flex-wrap:wrap;gap:2px 16px;align-items:center;justify-content:center;position:sticky;top:0;z-index:1000}\n'
    '  .preview-timer .pt-label{font-weight:700;color:#f5f5f5}\n'
    '  .preview-timer .pt-count{font-weight:700;white-space:nowrap}\n'
    '  .preview-timer .pt-count b{color:#ff7a1a;font-size:1.05rem}\n'
    '  .preview-timer .pt-count i{color:#8a8a8a;font-style:normal;margin:0 3px}\n'
    '  .preview-timer .pt-count .pt-unit{color:#bdbdbd;font-weight:600}\n'
    '  .preview-timer .pt-note{color:#9a9a9a;letter-spacing:.02em}\n'
    '  /* Transparent header on scroll (user, 2026-11-22): at the top the\n'
    '     header is solid; once you scroll, its background fades to\n'
    '     see-through (with a soft blur) so it stops covering the page,\n'
    '     while the logo, nav links and Book button stay put. */\n'
    '  header.site{transition:background .35s ease,border-color .35s ease,backdrop-filter .35s ease,-webkit-backdrop-filter .35s ease}\n'
    '  header.site.scrolled{background:rgba(247,248,250,0.45);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border-bottom-color:rgba(227,230,234,0.4)}\n'
    '  /* Live Google Map (user, 2026-11-21): the embedded map fills the\n'
    '     map area like the old picture did, and "Tap to open map" is now\n'
    '     a real clickable link, so it needs pointer events back on. */\n'
    '  .map-live-frame{display:block;width:100%;height:300px;border:0}\n'
    '  @media (max-width:1023px){.map-live-frame{height:280px}}\n'
    '  .map-open-chip{pointer-events:auto}\n'
    '  /* Customer review form (user, 2026-11-21): the "Share your\n'
    '     experience" form under the patient reviews. Stars are gold\n'
    '     when picked, grey when not. */\n'
    '  .review-form-wrap{margin-top:36px;border-top:1px solid var(--line);padding-top:28px}\n'
    '  .review-form-wrap h3{margin-bottom:6px}\n'
    '  .review-form-wrap>p{color:var(--muted)}\n'
    '  .review-form{display:grid;gap:12px;max-width:560px;margin-top:16px}\n'
    '  .review-form label{display:grid;gap:6px;font-weight:600}\n'
    '  .review-form input[type="text"],.review-form textarea{width:100%;border:1px solid var(--line);border-radius:12px;background:var(--bg);padding:.72rem .95rem;font:inherit}\n'
    '  .rv-stars-label{font-weight:600}\n'
    '  .rv-stars{display:flex;gap:4px}\n'
    '  .rv-stars button{background:none;border:0;font-size:1.6rem;color:#c9c9c9;cursor:pointer;padding:0 2px;line-height:1}\n'
    '  .rv-stars button.on{color:#c9a227}\n'
    '  .rv-thanks{color:var(--teal-dark);font-weight:600}\n'
    '  /* Sticky header (user, 2026-11-21): the nav (Home, Services, About,\n'
    '     Contact) stays on screen when scrolling, pinned right under the\n'
    '     timer bar. Its top offset is the timer height, set by script,\n'
    '     so it still lines up when the timer wraps to two lines. */\n'
    '  header.site{position:sticky;z-index:999}\n'
  '  /* The "Moments" photo is the services board — show it\n'
    '     whole, never cropped or zoomed. */\n'
    '  .award-photo img{max-height:none;object-fit:contain}\n'
    '  /* Pop-in on load and on scroll (2026-11-21). The animation runs once\n'
    '     per element (fill backwards so the delay period stays hidden); after\n'
    '     it ends the element keeps its own styles, so hover lifts still work. */\n'
    '  .pop{opacity:0}\n'
    '  .pop.in{opacity:1;animation:alkPopIn .7s cubic-bezier(.21,.9,.35,1.05) backwards}\n'
    '  @keyframes alkPopIn{from{opacity:0;transform:translateY(28px) scale(.94)}to{opacity:1;transform:translateY(0) scale(1)}}\n'
    '  @media (prefers-reduced-motion:reduce){.pop{opacity:1}.pop.in{animation:none}}\n'
)

# Pop-in animation script (user, 2026-11-21): cards, stats, photos and list
# items pop in gently when the page loads and when you scroll to them.
POP_IN_JS = (
    '  <script>\n'
    '  // Pop-in on load and on scroll.\n'
    '  (function(){\n'
    '    var els = document.querySelectorAll(".svc-card, .value-card, .stat, .teaser img, .carousel, .why-list li, .mission-grid > div, .block h2, .block .eyebrow, .block .intro, .band-inner, .card, .find-panel, .foot-grid, .contact-reviews");\n'
    '    els.forEach(function(el){\n'
    '      el.classList.add("pop");\n'
    '      var i = Array.prototype.indexOf.call(el.parentElement.children, el);\n'
    '      el.style.animationDelay = Math.min(i, 5) * 70 + "ms";\n'
    '    });\n'
    '    function showAll(){ els.forEach(function(el){ el.classList.add("in"); }); }\n'
    '    if(!("IntersectionObserver" in window)){ showAll(); return; }\n'
    '    var io = new IntersectionObserver(function(entries){\n'
    '      entries.forEach(function(en){\n'
    '        if(en.isIntersecting){ en.target.classList.add("in"); io.unobserve(en.target); }\n'
    '      });\n'
    '    }, {threshold: 0.12});\n'
    '    els.forEach(function(el){ io.observe(el); });\n'
    '  })();\n'
    '  </script>\n'
)

# Chat button behaviour (user, 2026-11-21): it pops open on load showing
# "Chat with us" with the logo, then shrinks to the logo-only circle after
# 3 seconds. Hovering expands it again. Clicking it opens the chat and it
# stays expanded while the chat is open. Clicking away closes the chat, and
# the button shrinks again after 3 seconds.
CHAT_FAB_JS = (
    '  <script>\n'
    '  // Chat button: pops open on load, shrinks to the logo after 3 seconds.\n'
    '  (function(){\n'
    '    var fab = document.getElementById("chatFab");\n'
    '    var panel = document.getElementById("chatPanel");\n'
    '    if (!fab || !panel) return;\n'
    '    var timer = null;\n'
    '    function shrinkSoon(){\n'
    '      clearTimeout(timer);\n'
    '      timer = setTimeout(function(){\n'
    '        if (!panel.classList.contains("open")) fab.classList.remove("expanded");\n'
    '      }, 3000);\n'
    '    }\n'
    '    function expand(){ clearTimeout(timer); fab.classList.add("expanded"); }\n'
    '    function closePanel(){\n'
    '      if (typeof window.closeChat === "function") window.closeChat();\n'
    '      else { panel.classList.remove("open"); panel.setAttribute("aria-hidden", "true"); fab.setAttribute("aria-expanded", "false"); }\n'
    '    }\n'
    '    expand();\n'
    '    shrinkSoon();\n'
    '    fab.addEventListener("mouseenter", expand);\n'
    '    fab.addEventListener("mouseleave", shrinkSoon);\n'
    '    fab.addEventListener("click", function(){\n'
    '      setTimeout(function(){\n'
    '        if (panel.classList.contains("open")) expand(); else shrinkSoon();\n'
    '      }, 0);\n'
    '    });\n'
    '    document.addEventListener("click", function(e){\n'
    '      if (!panel.classList.contains("open")) return;\n'
    '      if (panel.contains(e.target) || fab.contains(e.target)) return;\n'
    '      closePanel();\n'
    '    });\n'
    '    if ("MutationObserver" in window) {\n'
    '      new MutationObserver(function(){\n'
    '        if (panel.classList.contains("open")) expand(); else shrinkSoon();\n'
    '      }).observe(panel, { attributes: true, attributeFilter: ["class"] });\n'
    '    }\n'
    '  })();\n'
    '  </script>\n'
)

# Booking date and time (user, 2026-11-21): the booking form lets the
# customer pick a preferred date and time. The two helpers format them for
# the WhatsApp message and the confirmation text; the script also stops
# the date picker offering past dates.
BOOKING_DATETIME_JS = (
    '  <script>\n'
    '  // Booking date/time helpers (used by the booking form submit handler).\n'
    '  function fmtBookDate(value) {\n'
    '    if (!value) return "";\n'
    '    var parts = value.split("-");\n'
    '    var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];\n'
    '    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];\n'
    '    var d = new Date(+parts[0], +parts[1] - 1, +parts[2]);\n'
    '    return days[d.getDay()] + ", " + d.getDate() + " " + months[d.getMonth()] + " " + d.getFullYear();\n'
    '  }\n'
    '  function fmtBookTime(value) {\n'
    '    if (!value) return "";\n'
    '    var parts = value.split(":");\n'
    '    var h = +parts[0];\n'
    '    var ampm = h >= 12 ? "PM" : "AM";\n'
    '    var h12 = h % 12;\n'
    '    if (h12 === 0) h12 = 12;\n'
    '    return h12 + ":" + parts[1] + " " + ampm;\n'
    '  }\n'
    '  (function () {\n'
    '    var dateInput = document.getElementById("bkDate");\n'
    '    if (!dateInput) return;\n'
    '    var now = new Date();\n'
    '    var mm = String(now.getMonth() + 1).padStart(2, "0");\n'
    '    var dd = String(now.getDate()).padStart(2, "0");\n'
    '    dateInput.min = now.getFullYear() + "-" + mm + "-" + dd;\n'
    '  })();\n'
    '  </script>\n'
)

# Preview countdown timer (user, 2026-11-21): a dark bar at the very top
# of the page, above the Open 24/7 bar, counting down to the preview
# expiry. The user sends the link on Monday 2026-11-23, so the expiry
# is 7 days after that Monday (2026-11-30); on Monday the timer reads
# 07 DAYS. Change PREVIEW_EXPIRY to move it. When the timer reaches
# zero it shows 00s and says the preview has expired.
PREVIEW_EXPIRY = "2026-11-30T23:59:59+00:00"
PREVIEW_TIMER_HTML = (
    '  <div class="preview-timer" id="previewTimer" role="timer">\n'
    '    <span class="pt-label">LIVE PREVIEW EXPIRES IN</span>\n'
    '    <span class="pt-count"><b id="ptDays">07</b> <span class="pt-unit">DAYS</span> <i>:</i> <b id="ptHours">08</b> <span class="pt-unit">HRS</span> <i>:</i> <b id="ptMins">18</b> <span class="pt-unit">MIN</span> <i>:</i> <b id="ptSecs">18</b> <span class="pt-unit">SEC</span></span>\n'
    '    <span class="pt-note">Temporary preview &mdash; taken offline when the timer reaches zero.</span>\n'
    '  </div>\n'
)
PREVIEW_TIMER_JS = (
    '  <script>\n'
    '  // Preview countdown timer: counts down to PREVIEW_EXPIRY.\n'
    '  (function () {\n'
    '    var expiry = new Date("' + PREVIEW_EXPIRY + '").getTime();\n'
    '    var bar = document.getElementById("previewTimer");\n'
    '    if (!bar) return;\n'
    '    var d = document.getElementById("ptDays"), h = document.getElementById("ptHours"),\n'
    '        m = document.getElementById("ptMins"), s = document.getElementById("ptSecs"),\n'
    '        note = bar.querySelector(".pt-note");\n'
    '    function pad(n) { return (n < 10 ? "0" : "") + n; }\n'
    '    function tick() {\n'
    '      var diff = expiry - Date.now();\n'
    '      if (diff <= 0) {\n'
    '        d.textContent = "00"; h.textContent = "00"; m.textContent = "00"; s.textContent = "00";\n'
    '        note.textContent = "This preview has expired.";\n'
    '        return;\n'
    '      }\n'
    '      d.textContent = pad(Math.floor(diff / 86400000));\n'
    '      h.textContent = pad(Math.floor(diff % 86400000 / 3600000));\n'
    '      m.textContent = pad(Math.floor(diff % 3600000 / 60000));\n'
    '      s.textContent = pad(Math.floor(diff % 60000 / 1000));\n'
    '    }\n'
    '    tick();\n'
    '    setInterval(tick, 1000);\n'
    '    // Sticky header: pin the nav right under the timer bar. The timer\n'
    '    // can wrap to two lines on narrow screens, so measure its real\n'
    '    // height and set the header top offset from it, on load and resize.\n'
    '    var header = document.querySelector("header.site");\n'
    '    function stickHeader() {\n'
    '      if (!header) return;\n'
    '      header.style.top = bar.offsetHeight + "px";\n'
    '    }\n'
    '    stickHeader();\n'
    '    window.addEventListener("load", stickHeader);\n'
    '    window.addEventListener("resize", stickHeader);\n'
    '    // Transparent header on scroll (user, 2026-11-22): when the page\n'
    '    // is scrolled the header background fades to see-through so it\n'
    '    // stops covering the page, but the logo, nav links and Book\n'
    '    // button stay visible and clickable. At the top it is solid.\n'
    '    function headerFade() {\n'
    '      if (!header) return;\n'
    '      header.classList.toggle("scrolled", window.scrollY > 8);\n'
    '    }\n'
    '    headerFade();\n'
    '    window.addEventListener("scroll", headerFade, { passive: true });\n'
    '  })();\n'
    '  </script>\n'
)

# Mission + Vision (2026-11-21): short wording from Al-Kawthar's own
# flyer and opening speech — "Compassionate Care. Guided by Faith." and
# holistic care of mind, body and soul, for all. The hospital can adjust
# the exact words.
MISSION_VISION_HTML = (
    '      <div class="mission-grid">\n'
    '        <div><h3>Our Mission</h3><p>To give every patient quality, affordable and ethical healthcare — holistic care of mind, body and soul, guided by faith.</p></div>\n'
    '        <div><h3>Our Vision</h3><p>To be Tamale&rsquo;s most trusted hospital — compassionate care, guided by faith, for everyone.</p></div>\n'
    '      </div>\n'
)

# ---------------------------------------------------------------- transform
def js_services():
    out = []
    for svc in SERVICES:
        entry = {k: svc[k] for k in
                 ("name", "tag", "about", "helps", "who", "know", "photos")}
        out.append("    " + json.dumps(entry, ensure_ascii=False))
    return "  var SERVICES = [\n" + ",\n".join(out) + "\n  ];"


def js_ph():
    out = []
    for i, (key, (alt, caption)) in enumerate(PH.items()):
        src = _photo_uri(key)
        # Keys must be quoted: Al-Kawthar keys like "alk-gen-dental" contain
        # hyphens, which are not valid bare identifiers in a JS object.
        out.append('    {key}: [{src}, {alt}, {cap}]'.format(
            key=json.dumps(key, ensure_ascii=False),
            src=json.dumps(src, ensure_ascii=False),
            alt=json.dumps(alt, ensure_ascii=False),
            cap=json.dumps(caption, ensure_ascii=False)))
    return "  var PH = {\n" + ",\n".join(out) + "\n  };"


# Every photo the demo embeds, key -> file. Stock photos live in
# del-photos/services/; Al-Kawthar's generated photos in
# alkawthar-photos/generated/; the real Google Maps photos in
# alkawthar-photos/.
_PHOTO_PATHS = {}
for _k in ("dental", "dental2",
           "preventive1", "preventive2", "maternity",
           "counsel1", "counsel2", "surgery",
           "surgery2", "surgery3", "physio1", "physio2"):
    _PHOTO_PATHS[_k] = HERE / "del-photos" / "services" / (_k + ".jpg")
# OPD, Laboratory, Pharmacy, Ultrasound and Mother & Child photos:
# re-edited 2026-11-21 so the people look Islamic (male doctors and
# pharmacists wear a white kufi cap; female doctors, lab scientists,
# sonographers, nurses and patients wear a hijab). The edited copies
# live in alkawthar-photos/ under the same key names; Del's originals
# in del-photos/services/ are untouched.
for _k in ("internal1", "internal2", "internal3", "lab1", "lab2", "lab3",
           "pharmacy1", "pharmacy2", "pharmacy3",
           "imaging1", "imaging2", "preventive3", "counsel3", "maternity2"):
    _PHOTO_PATHS[_k] = HERE / "alkawthar-photos" / (_k + ".jpg")
for _k in ("alk-gen-dental", "alk-gen-optical", "alk-gen-scan",
           "alk-gen-maternity", "alk-gen-physio"):
    _PHOTO_PATHS[_k] = HERE / "alkawthar-photos" / "generated" / (_k + ".jpg")
for _k in ("alk-building-front-wide", "alk-building-night",
           "alk-streetview-day", "alk-building-front-sign",
           "alk-building-front", "alk-building-side", "alk-entrance-gate",
           "alk-corridor-bright", "alk-corridor-doors",
           "alk-pharmacy-lab-balloons", "alk-services-board",
           "alk-signboard-street"):
    _PHOTO_PATHS[_k] = HERE / "alkawthar-photos" / (_k + ".jpg")


def _photo_uri(key):
    return _data_uri(_PHOTO_PATHS[key])


_SLIDE_PHOTOS = {
    "Our hospital": "alk-building-front-wide",
    "Our hospital at night": "alk-building-night",
    "Our services": "alk-services-board",
    "Our entrance": "alk-entrance-gate",
    "Inside the hospital": "alk-corridor-bright",
    "Our corridors": "alk-corridor-doors",
    "Pharmacy & laboratory": "alk-pharmacy-lab-balloons",
    "Find us": "alk-signboard-street",
    "Our building": "alk-building-side",
}


def js_slides():
    out = []
    for i, s in enumerate(SLIDES):
        src = _photo_uri(_SLIDE_PHOTOS[s["label"]])
        out.append('    {{ src: {src}, label: {lab}, alt: {alt} }}'.format(
            src=json.dumps(src, ensure_ascii=False),
            lab=json.dumps(s["label"], ensure_ascii=False),
            alt=json.dumps(s["alt"], ensure_ascii=False)))
    return "  var SLIDES = [\n" + ",\n".join(out) + "\n  ];"


def js_aliases():
    return ("  var SERVICE_ALIASES = " +
            json.dumps(ALIASES, ensure_ascii=False) + ";")


def js_hero_slides():
    return ("  var HERO_SLIDES = [\n"
            '    { label: "Tamale" },\n'
            '    { label: "Open 24 hours" },\n'
            '    { label: "Our hospital" }\n  ];')


def replace_img_by_alt(s, alt_part, new_src, new_alt=None):
    """Replace the src (and optionally alt) of the <img> whose alt contains alt_part."""
    def repl(m):
        tag = m.group(0)
        tag = re.sub(r'src="[^"]*"', 'src="' + new_src + '"', tag, count=1)
        if new_alt is not None:
            tag = re.sub(r'alt="[^"]*"', 'alt="' + _esc(new_alt) + '"', tag, count=1)
        return tag
    pat = re.compile(r'<img[^>]*alt="[^"]*' + re.escape(alt_part) + r'[^"]*"[^>]*>')
    s2, n = pat.subn(repl, s)
    if n == 0:
        raise ValueError("img with alt containing %r not found" % alt_part)
    return s2


def replace_img_by_id(s, el_id, new_src):
    pat = re.compile(r'(<img[^>]*id="' + re.escape(el_id) + r'"[^>]*src=")[^"]*(")')
    s2, n = pat.subn(r'\1' + new_src + r'\2', s, count=1)
    if n == 0:
        raise ValueError("img with id %r not found" % el_id)
    return s2


def sub_block(s, start_re, end_re, replacement, name):
    pat = re.compile(start_re + r'.*?' + end_re, re.DOTALL)
    s2, n = pat.subn(replacement, s, count=1)
    if n == 0:
        raise ValueError("block not found: " + name)
    return s2


def transform(s):
    # ---- 1. Logos: the green "A" mark in header/footer + chat head;
    #     the chat button gets the same "A" mark.
    s = re.sub(r'(<span class="(?:brand-mark|head-logo)"[^>]*><img src=")'
               r'data:image/jpeg;base64,[^"]*(")',
               r'\1' + LOGO + r'\2', s)
    s = re.sub(r'(<span class="fab-logo"[^>]*><img src=")'
               r'data:image/jpeg;base64,[^"]*(")',
               r'\1' + FAB + r'\2', s)
    # ---- 2. Hero + story carousel + section photos (by id / alt) ----
    # Real Al-Kawthar photos (Google Maps) where the shot is the hospital
    # itself; generated and stock photos elsewhere until the hospital
    # supplies more real photos.
    # Hero slide order (user, 2026-11-22): the street view shows FIRST
    # and the wide front photo shows LAST (swapped from the original
    # order); the night photo stays in the middle.
    s = replace_img_by_id(s, "heroImg", ALK_BUILDING_STREETVIEW)
    s = replace_img_by_id(s, "heroImg2", ALK_BUILDING_NIGHT)
    # Third hero slide: the cleaned wide front photo of the building.
    s = re.sub(r'(<img id="heroImg2"[^>]*?/>)',
               lambda m: m.group(1) + '\n      <img id="heroImg3" src="' + ALK_BUILDING_FRONT_WIDE + '" alt="" />',
               s, count=1)
    s = replace_img_by_id(s, "carImg", ALK_BUILDING_FRONT_WIDE)
    s = replace_img_by_alt(
        s, "A Habana radiographer guiding a patient into the Siemens CT scanner",
        _photo_uri("alk-gen-scan"),
        "An ultrasound scan at Al-Kawthar Islamic Hospital")
    s = replace_img_by_alt(
        s, "The Siemens SOMATOM CT scanner in the imaging suite",
        _photo_uri("imaging2"),
        "The ultrasound room at Al-Kawthar Islamic Hospital")
    s = replace_img_by_alt(
        s, "Habana Medical Service nurses and staff together on the ward",
        ALK_BUILDING_FRONT_SIGN,
        "The front of Al-Kawthar Islamic Hospital in Tamale")
    s = replace_img_by_alt(
        s, "Moments from the Habana Medical Service story",
        ALK_SERVICES_BOARD,
        "Al-Kawthar's 24-hour services board")
    s = replace_img_by_alt(
        s, "The front of the Habana Medical Service building",
        ALK_BUILDING_FRONT,
        "The front of the Al-Kawthar Islamic Hospital building in Tamale")
    # Live Google Map (user, 2026-11-21): swap the whole drawn-map block
    # for the real Google Map embed. The drawn SVG is no longer used.
    pat = re.compile(r'        <div class="map-embed">.*?</div>', re.DOTALL)
    s2, n = pat.subn(MAP_LIVE_HTML, s, count=1)
    if n == 0:
        raise ValueError("map-embed block not found")
    s = s2

    # ---- 3. Colours: teal -> Islamic green, amber -> gold ----
    css_vars = [
        ("--teal:#0b6e5f", "--teal:#0e7a3d"),
        ("--teal-dark:#07473d", "--teal-dark:#095c2e"),
        ("--teal-deep:#06302a", "--teal-deep:#073d1f"),
        ("--teal-ink:#052e28", "--teal-ink:#062b17"),
        ("--teal-soft:#dff0ea", "--teal-soft:#dff0e4"),
        ("--teal-pale:#e9f4f0", "--teal-pale:#e9f4ec"),
        ("--accent:#e79a35", "--accent:#c9a227"),
        ("--accent-dark:#c97f1d", "--accent-dark:#a8861a"),
        ("--ink:#12211d", "--ink:#12202e"),
        ("--muted:#5a6b65", "--muted:#5a6b7a"),
        ("--bg:#faf8f2", "--bg:#f7f8fa"),
        ("--line:#e3e7e1", "--line:#e3e6ea"),
        ("rgba(4,32,27", "rgba(6,43,23"),
        ("rgba(6,48,42", "rgba(7,61,31"),
        ("rgba(5,46,40", "rgba(6,43,23"),
        ("rgba(18,33,29", "rgba(15,30,55"),
        ("rgba(11,110,95", "rgba(14,122,61"),
        ("rgba(231,154,53", "rgba(201,162,39"),
        ("#0a4a3e", "#0e7a3d"),
    ]
    for old, new in css_vars:
        if old not in s:
            raise ValueError("CSS value not found: " + old)
        s = s.replace(old, new)
    # brand stripe -> green/gold stripe
    s = re.sub(r'\.kente\{[^}]*\}',
               '.stripe{height:10px;margin-top:56px;background:linear-gradient(90deg,'
               'var(--teal-deep) 0%,var(--teal) 45%,var(--accent) 45%,var(--accent) 55%,'
               'var(--teal) 55%,var(--teal-deep) 100%)}', s, count=1)
    s = s.replace('<div class="kente" aria-hidden="true"></div>',
                  '<div class="stripe" aria-hidden="true"></div>')

    # ---- 4. Wholesale blocks ----
    # Stats
    stats = (
        '      <div class="stat"><p class="num">April 2026</p><p>Opened in Tamale</p></div>\n'
        '      <div class="stat"><p class="num">24/7</p><p>Open 24 hours, every day</p></div>\n'
        '      <div class="stat"><p class="num">12</p><p>Medical services</p></div>\n'
        '      <div class="stat"><p class="num">All faiths</p><p>Care for everyone, whatever your faith</p></div>'
    )
    s = sub_block(s, r'<div class="stats" style="margin-top:0">\n',
                  r'\n    </div>\n  </section>',
                  '<div class="stats" style="margin-top:0">\n' + stats +
                  '\n    </div>\n  </section>', "stats")
    # Home service preview grid (first 6 services)
    home_cards = "\n      ".join(svc_card(i, svc) for i, svc in enumerate(SERVICES[:6]))
    s = sub_block(s, r'<div class="svc-grid">\n', r'\n    </div>\n  </section>',
                  '<div class="svc-grid">\n      ' + home_cards +
                  '\n    </div>\n  </section>', "home svc-grid")
    # Services page grid (all 12)
    all_cards = "\n      ".join(svc_card(i, svc) for i, svc in enumerate(SERVICES))
    s = sub_block(s, r'<div class="svc-grid" id="svcGrid">\n', r'\n    </div>\n  </section>',
                  '<div class="svc-grid" id="svcGrid">\n      ' + all_cards +
                  '\n    </div>\n  </section>', "services svc-grid")
    # Diagnostics pills (appears twice, identical)
    old_pills = (
        '            <span class="pill">CT Scan</span>\n'
        '            <span class="pill">Ultrasound</span>\n'
        '            <span class="pill">Mammography</span>\n'
        '            <span class="pill">ECG</span>\n'
        '            <span class="pill">Echocardiography</span>\n'
        '            <span class="pill">Laboratory tests</span>'
    )
    new_pills = (
        '            <span class="pill">Ultrasound</span>\n'
        '            <span class="pill">Laboratory tests</span>\n'
        '            <span class="pill">Health screenings</span>'
    )
    if s.count(old_pills) != 2:
        raise ValueError("expected 2 diagnostics pill rows, found %d" % s.count(old_pills))
    s = s.replace(old_pills, new_pills)
    # Teaser body + awards list
    s = s.replace(
        '<p class="body">Founded in 2011 by Dr Thomas Winsum Anabah, a Consultant '
        'Anaesthesiologist, HMS began as a small day clinic. Today our physicians, '
        'nurses, pharmacists, laboratory scientists and radiographers work together '
        'to give every patient coordinated, compassionate care.</p>',
        '<p class="body">Al-Kawthar Islamic Hospital is a private Islamic hospital in Tamale, '
        'run by the Wifaq Foundation for Development and Community Service. Opened in '
        'April 2026, it gives healthcare guided by Islamic principles of compassion '
        'and ethics — for everyone, whatever your faith. Our physicians, nurses, '
        'pharmacists, laboratory scientists and radiographers work together to give '
        'every patient coordinated, compassionate care.</p>')
    s = sub_block(
        s, r'<ul class="why-list">\n', r'\n        </ul>',
        '        <ul class="why-list">\n'
        '          <li><strong>Faith-based care</strong><span>Healthcare guided by Islamic principles of compassion and ethics — for everyone, whatever your faith</span></li>\n'
        '          <li><strong>Opened April 2026</strong><span>A new hospital in Tamale, run by the Wifaq Foundation for Development and Community Service</span></li>\n'
        '          <li><strong>24/7</strong><span>Open 24 hours, every day, including weekends and public holidays</span></li>\n'
        '        </ul>', "why-list")
    # Awards section -> facilities section
    facilities = (
        '  <section class="block wrap">\n'
        '    <p class="eyebrow">Our facilities</p>\n'
        '    <h2>Everything under one roof.</h2>\n'
        '    <div class="values-grid" style="margin-top:36px">\n'
        '      <article class="value-card"><h3>Female ward</h3><p>A dedicated female ward, with male and female doctors and nurses, so patients can be attended by staff of the same gender.</p></article>\n'
        '      <article class="value-card"><h3>Maternity unit</h3><p>A maternity department with antenatal care and ultrasound on site.</p></article>\n'
        '      <article class="value-card"><h3>Laboratory &amp; scan</h3><p>An on-site laboratory and ultrasound room, so results come back quickly.</p></article>\n'
        '      <article class="value-card"><h3>Pharmacy on site</h3><p>Collect your prescribed medicines before you leave the hospital.</p></article>\n'
        '      <article class="value-card"><h3>Care for all faiths</h3><p>Faith-based care for everyone — our doors are open to all, whatever your religion.</p></article>\n'
        '      <article class="value-card"><h3>Open 24 hours</h3><p>Open 24 hours, every day, including weekends and public holidays.</p></article>\n'
        '    </div>\n'
        '    <p class="award-note">Find us in Watherson Area, behind the Northern Regional Coordinating Council, Tamale.</p>\n'
        '  </section>'
    )
    s = sub_block(s, r'  <section class="block wrap">\n    <p class="eyebrow">Recognition</p>',
                  r'\n  </section>', facilities, "awards section")
    # Contact form + booking modal service selects
    contact_opts = (
        '            <option value="">Choose a service…</option>\n'
        '            <option>Book an appointment</option>\n'
        + "".join('            <option>{}</option>\n'.format(svc["name"].replace("&", "&amp;"))
                   for svc in SERVICES)
        + '            <option>General enquiry</option>'
    )
    s = sub_block(s, r'<select id="service" name="service">\n', r'\n          </select>',
                  '<select id="service" name="service">\n' + contact_opts +
                  '\n          </select>', "contact select")
    book_opts = (
        '            <option value="">Choose a service…</option>\n'
        + "".join('            <option>{}</option>\n'.format(svc["name"].replace("&", "&amp;"))
                   for svc in SERVICES).rstrip("\n")
    )
    s = sub_block(s, r'<select id="bkService" name="bkService">\n', r'\n          </select>',
                  '<select id="bkService" name="bkService">\n' + book_opts +
                  '\n          </select>', "booking select")
    # Hours table: drop the cervical clinic row (Al-Kawthar does not list it);
    # the hospital is open 24 hours every day.
    s = s.replace(
        '<tr><td>Cervical screening clinic</td><td>Fridays, 9:00 AM</td></tr>',
        '')
    # Remove Habana staff sign-in + map credit. Al-Kawthar has no social
    # media pages — the footer social links are removed entirely.
    s = sub_block(s, r'        <div class="foot-social">\n', r'\n        </div>',
                  '', "footer social")
    s = re.sub(r'\s*<li><a class="dim" href="https://habanamedicalservice\.lovable\.app/"[^>]*>Staff sign in</a></li>',
               '', s, count=1)
    s = re.sub(r'\s*<a class="map-credit"[^>]*>[^<]*</a>', '', s, count=1)
    # JS data
    s = sub_block(s, r'  var PH = \{\n', r'\n  \};', js_ph(), "PH map")
    s = sub_block(s, r'  var SERVICES = \[\n', r'\n  \];',
                  js_services(), "SERVICES array")
    s = sub_block(s, r'  var SLIDES = \[\n', r'\n  \];', js_slides(), "SLIDES array")
    s = sub_block(s, r'  var HERO_SLIDES = \[\n', r'\n  \];',
                  js_hero_slides(), "HERO_SLIDES array")
    if 'var heroImgs = [document.getElementById("heroImg"), document.getElementById("heroImg2")];' not in s:
        raise ValueError("heroImgs array not found")
    s = s.replace('var heroImgs = [document.getElementById("heroImg"), document.getElementById("heroImg2")];',
                  'var heroImgs = [document.getElementById("heroImg"), document.getElementById("heroImg2"), document.getElementById("heroImg3")];', 1)
    s = sub_block(s, r'  var SERVICE_ALIASES = \[\n', r'\n  \];',
                  js_aliases(), "SERVICE_ALIASES array")

    # ---- 5. Explicit text replacements (exact strings) ----
    # ---- 5. Explicit text replacements (exact strings) ----
    explicit = [
        ('<title>Habana Medical Service — Tamale</title>',
         '<title>Al-Kawthar Islamic Hospital — Tamale</title>'),
        ('<meta name="description" content="Habana Medical Service, Tamale — a private multidisciplinary hospital open 24/7. Fifteen specialties, diagnostics on site, and care guided by love and honesty." />',
         '<meta name="description" content="Al-Kawthar Islamic Hospital, Tamale — a private Islamic hospital open 24/7. Twelve services, including maternity and mother and child care, and care guided by faith." />'),
        ('<span class="brand-sub">Service · Tamale</span>',
         '<span class="brand-sub">Islamic Hospital · Tamale</span>'),
        ('home: "Habana Medical Service — Tamale",',
         'home: "Al-Kawthar Islamic Hospital — Tamale",'),
        ('services: "Services | Habana Medical Service, Tamale",',
         'services: "Services | Al-Kawthar Islamic Hospital, Tamale",'),
        ('about: "About us | Habana Medical Service, Tamale",',
         'about: "About us | Al-Kawthar Islamic Hospital, Tamale",'),
        ('contact: "Contact & Directions | Habana Medical Service, Tamale"',
         'contact: "Contact & Directions | Al-Kawthar Islamic Hospital, Tamale"'),
        ('Celebrating 15 years of care · 2011–2026',
         'An Islamic hospital in Tamale · Opened April 2026'),
        ('<h1>Care with <em>love</em> and <em>honesty</em>, every hour of the day.</h1>',
         '<h1>Compassionate care, <em>guided by faith</em>, every hour of the day.</h1>'),
        ('Habana Medical Service is one of Northern Ghana&rsquo;s leading private hospitals — specialist doctors, modern diagnostics and a calm, welcoming place to heal, right here in Tamale.',
         'Al-Kawthar Islamic Hospital is a private Islamic hospital in Tamale — specialist doctors, maternity and mother and child care, and a calm, welcoming place to heal, behind the Northern Regional Coordinating Council.'),
        ('<h1>Fifteen years of <em>love and honesty</em> in healthcare.</h1>',
         '<h1>Your health, <em>our mission</em> — care guided by faith.</h1>'),
        ('What began in 2011 as a day clinic in a converted four-bedroom house is now one of Northern Ghana&rsquo;s leading private hospitals.',
         'Opened in April 2026 by the Wifaq Foundation for Development and Community Service, Al-Kawthar Islamic Hospital is a private Islamic hospital in Tamale — care guided by faith, for everyone, whatever your religion.'),
        ('<h2>Founded by a doctor who believed Tamale deserved more.</h2>',
         '<h2>Our story — a hospital built on faith and community.</h2>'),
        ('Habana Medical Service was established in the Tamale metropolis by <strong>Dr Thomas Winsum Anabah</strong>, a Consultant Anaesthesiologist with a Master&rsquo;s in Critical Care and Emergencies. The first patients were walk-in clients living with non-communicable diseases.',
         'Al-Kawthar Islamic Hospital was opened in April 2026 by the <strong>Wifaq Foundation for Development and Community Service</strong>, to give Tamale healthcare guided by Islamic principles of compassion and ethics — affordable, accessible care for everyone, regardless of faith. The hospital is open 24 hours, every day.'),
        ('Today HMS brings together doctors, nurses and support staff across internal medicine, emergency and critical care, paediatrics, public health, obstetrics and gynaecology, ENT, anaesthesia and surgery — with specialists on call around the clock.',
         'Today Al-Kawthar brings together doctors, nurses and support staff across outpatient care, maternity, laboratory, pharmacy, dental and optical care — with specialists on call around the clock.'),
        ('Set in a serene environment, our hospital is designed to feel like a home away from home.',
         'A new two-storey hospital with a pharmacy, laboratory, scan and maternity services — with a dedicated female ward.'),
        ('<p>Health education and prevention for families across the North.</p>',
         '<p>Health education and prevention for families across Tamale and the Northern Region.</p>'),
        ('<span class="cap" id="carCap">1 / 7 · International award ceremony</span>',
         '<span class="cap" id="carCap">1 / 9 · Our hospital</span>'),
        ('<h2>A home away from home — with world-class standards.</h2>',
         '<h2>Compassionate care, guided by faith.</h2>'),
        ('<p class="foot-blurb">A private multidisciplinary hospital serving Tamale and Northern Ghana since 2011. Guided by our motto, &ldquo;Love and Honesty.&rdquo;</p>',
         '<p class="foot-blurb">A private Islamic hospital serving Tamale since April 2026. Guided by our motto, &ldquo;Compassionate Care. Guided by Faith.&rdquo;</p>'),
        ('Bookings, enquiries and emergencies — 24/7.',
         'Bookings, enquiries and emergencies — 24/7. Also 0553 602 241.'),
        # Contact Call card: show the second number under the main line.
        ('        <p class="cbig"><a href="tel:+233233186766">023 318 6766</a></p>',
         '        <p class="cbig"><a href="tel:+233244158915">024 415 8915</a><br><a href="tel:+233553602241">0553 602 241</a></p>'),
        # Services intro: avoid implying a paediatrics department.
        ('From a child&rsquo;s fever at midnight to planned surgery',
         'From a fever at midnight to planned treatment'),
        ('Near Kamina Barracks, off GILLBT Road.',
         'Behind the Northern Regional Coordinating Council, Tamale.'),
        ('Opposite the School of Hygiene, Tamale, Ghana</span></p>',
         'Watherson Area, behind the Northern Regional Coordinating Council, Tamale, Ghana · Plus code C56G+7W</span></p>'),
        ('For CT scan and imaging bookings, call ahead so we can prepare',
         'For ultrasound and scan bookings, call ahead so we can prepare'),
        ('Our imaging and laboratory teams help your doctor diagnose quickly and start the right treatment sooner.',
         'Our scan and laboratory teams help your doctor diagnose quickly and start the right treatment sooner.'),
        ('destination=Nanton%20Road%2C%20Block%20141%2C%20North%20Kanvilli%2C%20Opposite%20School%20of%20Hygiene%2C%20Tamale%2C%20Ghana',
         'destination=' + ALK_MAPS_DEST),
        ('destination=Habana%20Medical%20Service%2C%20Nanton%20Road%2C%20Block%20141%2C%20North%20Kanvilli%2C%20Tamale%2C%20Ghana',
         'destination=' + ALK_MAPS_DEST),
        ('Habana Medical Service Ltd.', 'Al-Kawthar Islamic Hospital'),
        ('/* kente stripe + footer */', '/* brand stripe + footer */'),
        # Al-Kawthar HAS an email (from its own flyer) — keep the email
        # sentence/card/link, just point them at the hospital's address.
        ('Sending opens WhatsApp with your message ready to go — nothing is sent until you press send there. Prefer email? Write to <a href="mailto:habanamedicalservice@gmail.com">habanamedicalservice@gmail.com</a>. Prefer to talk? Call <a href="tel:+233233186766">023 318 6766</a>.',
         'Sending opens WhatsApp with your message ready to go — nothing is sent until you press send there. Prefer email? Write to <a href="mailto:alkawtharhospital@gmail.com">alkawtharhospital@gmail.com</a>. Prefer to talk? Call <a href="tel:+233244158915">024 415 8915</a>.'),
        # Sidebar Facebook button: remove it (Al-Kawthar has no socials).
        ('<a class="btn btn-outline" href="https://web.facebook.com/HabanaMedicalService" target="_blank" rel="noopener">Facebook — @HabanaMedicalService</a>',
         ''),
        # Sidebar email card: keep it, with the hospital's email.
        ('      <article class="card ccard">\n        <span class="cicon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg></span>\n        <p class="clabel">Email</p>\n        <p class="cbig">Write to us</p>\n        <p><a href="mailto:habanamedicalservice@gmail.com">habanamedicalservice@gmail.com</a></p>\n      </article>\n',
         '      <article class="card ccard">\n        <span class="cicon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg></span>\n        <p class="clabel">Email</p>\n        <p class="cbig">Write to us</p>\n        <p><a href="mailto:alkawtharhospital@gmail.com">alkawtharhospital@gmail.com</a></p>\n      </article>\n'),
        # Footer mail link: keep it, with the hospital's email.
        ('          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg><span><a href="mailto:habanamedicalservice@gmail.com">habanamedicalservice@gmail.com</a></span></li>\n',
         '          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg><span><a href="mailto:alkawtharhospital@gmail.com">alkawtharhospital@gmail.com</a></span></li>\n'),
        # Chat panel contact details: keep the email line, with the
        # hospital's email, and both phone numbers.
        ('You can reach the hospital team any time:\\nPhone: 023 318 6766\\nEmail: habanamedicalservice@gmail.com\\nWhatsApp: tap the button below.\\nWe are open 24 hours, every day.',
         'You can reach the hospital team any time:\\nPhone: 024 415 8915 or 0553 602 241\\nEmail: alkawtharhospital@gmail.com\\nWhatsApp: tap the button below.\\nWe are open 24 hours, every day.'),
        # Chat topic 4: cervical clinic (Friday 9:00 AM, not an Al-Kawthar
        # service) -> maternity and antenatal care.
        ('/* 4 — cervical screening clinic */\n    if (containsAny(t, ["cervical", "pap smear", "pap test"])) {\n      var og = SERVICES[findService("Obstetrics & Gynaecology")];\n      return {\n        text: "Our cervical screening clinic runs every Friday at 9:00 AM, under Obstetrics & Gynaecology. Screening checks the neck of the womb for early changes, so problems can be treated early.\\nYou can book ahead, or call us on 023 318 6766 if you have questions.",\n        actions: [bookAction(og.name), callAction()]\n      };\n    }',
         '/* 4 — maternity and antenatal care */\n    if (containsAny(t, ["antenatal", "pregnan", "expecting a baby", "give birth", "delivery", "maternity"])) {\n      var og = SERVICES[findService("Maternity Services")];\n      return {\n        text: "Our maternity team cares for mothers through pregnancy, birth and the weeks after delivery, with antenatal care and ultrasound on site, and a dedicated female ward.\\nYou can book ahead, or call us on 024 415 8915 if you have questions.",\n        actions: [bookAction(og.name), callAction()]\n      };\n    }'),
        # NHIS topic (new): do NOT claim NHIS — the hospital has not
        # confirmed it. Answer honestly and point to the phone.
        ('    /* 8 — prices: never invent figures */',
         '    /* 7b — NHIS */\n    if (containsAny(t, ["nhis", "insurance", "health insurance"])) {\n      return {\n        text: "For NHIS and payment questions, please call or WhatsApp us on 024 415 8915 — the team will explain what applies to your visit.",\n        actions: [callAction(), waAction()]\n      };\n    }\n\n    /* 8 — prices: never invent figures */'),
        # Prices topic: NHIS/insurance now answered by the topic above.
        ('    if (containsAny(t, ["price", "prices", "cost", "how much", "charges", "fees", " nhis ", "insurance", "do you take insurance", "payment"])) {',
         '    if (containsAny(t, ["price", "prices", "cost", "how much", "charges", "fees", "payment"])) {'),
        # HEALTH basics: pregnancy topic points at Maternity Services.
        ('service: "Obstetrics & Gynaecology", urgent: true,',
         'service: "Maternity Services", urgent: true,'),
        ('Our Obstetrics & Gynaecology team provides antenatal care and ultrasound scans here at the hospital.',
         'Our Maternity Services team provides antenatal care and ultrasound scans here at the hospital.'),
        # HEALTH basics: the malaria topic points at the Laboratory service.
        ('service: "Medical Laboratory", urgent: true,',
         'service: "Laboratory", urgent: true,'),
        # HEALTH basics: no Paediatrics service at Al-Kawthar — drop the link
        # and the claim that a paediatrics team sees children.
        ('service: "Paediatrics", urgent: true,',
         'service: "", urgent: true,'),
        ('Our Paediatrics team sees babies, children and teenagers — and we are open 24 hours, every day.',
         'We are open 24 hours, every day — if you are worried about a child, come in early.'),
        # Booking date + time (user, 2026-11-21): the form must let the
        # customer pick the date and time they want to book for.
        ('Fill in your details and choose the service you need',
         'Fill in your details, pick a date and time, and choose the service you need'),
        ('''          <p class="error">Please choose the service you want.</p>
        </div>
        <button class="btn btn-accent" type="submit" style="width:100%">Book now</button>''',
         '''          <p class="error">Please choose the service you want.</p>
        </div>
        <div class="field" id="bf-date">
          <label for="bkDate">Preferred date <span class="req" aria-hidden="true">*</span></label>
          <input type="date" id="bkDate" name="bkDate" />
          <p class="error">Please choose a date for your appointment.</p>
        </div>
        <div class="field" id="bf-time">
          <label for="bkTime">Preferred time <span class="req" aria-hidden="true">*</span></label>
          <input type="time" id="bkTime" name="bkTime" />
          <p class="error">Please choose a time for your appointment.</p>
        </div>
        <button class="btn btn-accent" type="submit" style="width:100%">Book now</button>'''),
        # Booking submit: read and validate the date and time.
        ('''    var service = bkSelect.selectedIndex > 0 ? bkSelect.options[bkSelect.selectedIndex].text : "";
    var ok = true;
    ok = bkInvalid("bf-name", !name) && ok;
    ok = bkInvalid("bf-phone", !phone) && ok;
    ok = bkInvalid("bf-service", !service) && ok;''',
         '''    var service = bkSelect.selectedIndex > 0 ? bkSelect.options[bkSelect.selectedIndex].text : "";
    var dateVal = document.getElementById("bkDate").value;
    var timeVal = document.getElementById("bkTime").value;
    var todayStart = new Date(); todayStart.setHours(0, 0, 0, 0);
    var pickedDate = dateVal ? new Date(dateVal + "T00:00:00") : null;
    var ok = true;
    ok = bkInvalid("bf-name", !name) && ok;
    ok = bkInvalid("bf-phone", !phone) && ok;
    ok = bkInvalid("bf-service", !service) && ok;
    ok = bkInvalid("bf-date", !dateVal || (pickedDate && pickedDate < todayStart)) && ok;
    ok = bkInvalid("bf-time", !timeVal) && ok;'''),
        # Booking WhatsApp message: include the chosen date and time.
        ('    lines.push("Service: " + service);',
         '    lines.push("Service: " + service);\n    lines.push("Preferred date: " + fmtBookDate(dateVal));\n    lines.push("Preferred time: " + fmtBookTime(timeVal));'),
        # Booking confirmation: show the chosen date and time.
        (r'''      "Thank you, " + name.split(" ")[0] + ". Your booking for \u201C" + service +
      "\u201D is ready \u2014 tap below to send the details to the hospital on WhatsApp, or call us on 023 318 6766.";''',
         '''      "Thank you, " + name.split(" ")[0] + ". Your booking for “" + service +
      "” on " + fmtBookDate(dateVal) + " at " + fmtBookTime(timeVal) +
      " is ready — tap below to send the details to the hospital on WhatsApp, or call us on 024 415 8915.";'''),
        # Clear the date/time errors as soon as the customer changes them.
        ('["bkName", "bkPhone", "bkService"]',
         '["bkName", "bkPhone", "bkService", "bkDate", "bkTime"]'),
    ]
    for old, new in explicit:
        if old not in s:
            raise ValueError("explicit string not found: " + old[:80])
        s = s.replace(old, new)

    # ---- 6. Blanket replacements (ordered, longest first) ----
    # NOTE: the main phone 024 415 8915 is used for display + tel: links
    # and for the wa.me links (ASSUMED WhatsApp number, unconfirmed). The
    # tel: form must be replaced before the bare-number form, or it gets
    # corrupted. Al-Kawthar is in Tamale like Habana, so no Tamale/Kumasi
    # swaps are needed.
    blanket = [
        ("Habana Medical Service", "Al-Kawthar Islamic Hospital"),
        ("Habana Medical", "Al-Kawthar"),
        ("habana", "al-kawthar"),
        ("023 318 6766", ALK_PHONE),
        ("+233233186766", ALK_PHONE_TEL),
        ("233233186766", ALK_PHONE_WA),
        ("Nanton Road, Block 141, North Kanvilli", "Watherson Area, behind the Northern Regional Coordinating Council"),
        ("Opposite the School of Hygiene", "Behind the Northern Regional Coordinating Council"),
        ("opposite the School of Hygiene", "behind the Northern Regional Coordinating Council"),
        ("North Kanvilli", "Watherson Area"),
        ("Fifteen", "Twelve"),
        ("fifteen", "twelve"),
        ("15 services", "12 services"),
        ("15 Medical", "12 Medical"),
        ("Habana", "Al-Kawthar"),
    ]
    for old, new in blanket:
        s = s.replace(old, new)
    s = re.sub(r'\bHMS\b', 'Al-Kawthar', s)

    # ---- 7. Safety net: any photo still embedded from Habana -> generic placeholder.
    # Every real photo (building, wards, staff, logo, founder poster, services
    # poster + all stock photos) is kept as-is.
    keep = {ALK_BUILDING_FRONT_WIDE, ALK_BUILDING_NIGHT,
            ALK_BUILDING_STREETVIEW, ALK_BUILDING_FRONT_SIGN,
            ALK_BUILDING_FRONT, ALK_BUILDING_SIDE, ALK_ENTRANCE_GATE,
            ALK_CORRIDOR_BRIGHT, ALK_CORRIDOR_DOORS, ALK_PHARMACY_LAB,
            ALK_SERVICES_BOARD, ALK_SIGNBOARD_STREET, ALK_LOGO}
    keep.update(_photo_uri(k) for k in PH)
    counter = [0]

    def _generic(m):
        if m.group(0) in keep:
            return m.group(0)
        i = counter[0]
        counter[0] += 1
        return ph("Al-Kawthar Islamic Hospital", "Tamale",
                  800, 600, variant=i)

    s = re.sub(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', _generic, s)

    # ---- 8. Al-Kawthar overrides: side padding, logo-only chat button, reviews ----
    # (a) CSS overrides, appended last in the stylesheet so they win.
    if s.count("</style>") != 1:
        raise ValueError("expected exactly one </style>, found %d" % s.count("</style>"))
    s = s.replace("</style>", ALK_CSS_OVERRIDES + "</style>", 1)
    # (a2) Preview countdown timer bar (user, 2026-11-21): at the very top,
    # above the Open 24/7 bar.
    if s.count('<body id="top">') != 1:
        raise ValueError("body tag not found")
    s = s.replace('<body id="top">', '<body id="top">\n\n' + PREVIEW_TIMER_HTML, 1)
    # (b) Reviews section at the end of the home page, after the About teaser.
    rev_anchor = '  </section>\n</div>\n\n<!-- ================= SERVICES ================= -->'
    if s.count(rev_anchor) != 1:
        raise ValueError("reviews anchor not found")
    s = s.replace(rev_anchor,
                  '  </section>\n' + REVIEWS_SECTION +
                  '\n</div>\n\n<!-- ================= SERVICES ================= -->', 1)
    # (c) Reviews on the About page (after the facilities section) and in the
    #     contact page's left column (under the form) — the two yellow-marked gaps.
    about_anchor = '  </section>\n</div>\n\n<!-- ================= CONTACT ================= -->'
    if s.count(about_anchor) != 1:
        raise ValueError("about reviews anchor not found")
    s = s.replace(about_anchor,
                  '  </section>\n' + REVIEWS_SECTION +
                  '\n</div>\n\n<!-- ================= CONTACT ================= -->', 1)
    contact_anchor = '    </div>\n\n    <aside class="panel">'
    if s.count(contact_anchor) != 1:
        raise ValueError("contact reviews anchor not found")
    s = s.replace(contact_anchor,
                  CONTACT_REVIEWS + '\n    </div>\n\n    <aside class="panel">', 1)
    aside_anchor = '      </article>\n    </aside>\n  </section>\n</div>\n</main>'
    if s.count(aside_anchor) != 1:
        raise ValueError("contact aside anchor not found")
    s = s.replace(aside_anchor,
                  '      </article>\n' + CONTACT_REVIEW_RIGHT +
                  '\n    </aside>\n  </section>\n</div>\n</main>', 1)
    # (d) Mission + Vision above the core-values cards; rename the heading.
    if s.count('<h2>Our values</h2>') != 1:
        raise ValueError("values heading not found")
    s = s.replace('<h2>Our values</h2>',
                  MISSION_VISION_HTML + '      <h2>Our core values</h2>', 1)
    # (d) Pop-in + chat button + booking date/time scripts, just before </body>.
    if s.count("</body>") != 1:
        raise ValueError("expected exactly one </body>, found %d" % s.count("</body>"))
    s = s.replace("</body>", POP_IN_JS + CHAT_FAB_JS + BOOKING_DATETIME_JS + PREVIEW_TIMER_JS + REVIEW_FORM_JS + "</body>", 1)
    # (d) Chat button: keep the "Chat with us" text (it expands on load and
    # shrinks to the logo after 3 seconds — user, 2026-11-21); drop only the
    # chat icon SVG. Start expanded in the HTML itself so the button is open
    # from the first paint, with no flash (the script only runs the timer).
    if s.count('<span>Chat with us</span>') != 1:
        raise ValueError("chat fab text not found")
    s = s.replace('<button class="chat-fab" id="chatFab"',
                  '<button class="chat-fab expanded" id="chatFab"', 1)
    s = re.sub(r'(<button class="chat-fab[^"]*"[^>]*>.*?<span class="fab-logo"[^>]*>.*?</span>)\s*<svg[^>]*>.*?</svg>',
               r'\1', s, count=1, flags=re.DOTALL)
    return s


# ---------------------------------------------------------------- verify
FORBIDDEN = [
    "Habana", "habana", "Anabah", "2011", "Siemens", "SOMATOM",
    "mammograph", "Mammograph", "Fifteen", "fifteen", "15 services",
    "Echocardiography", "lovable", "facebook.com", "instagram.com",
    "tiktok.com", "Kamina", "GILLBT", "School of Hygiene", "Nanton Road",
    "North Kanvilli", "kente", "Kente", "Friday at 9:00 AM", "Fridays, 9:00 AM",
    "9:00 AM", "Endoscopy", "Ophthalmology", "Neurosurgery", "Psychology",
    "Paediatrics", "paediatric", "Obstetrics & Gynaecology",
    "delinternationalhospital", "East Legon", "Accra", "Nii Sai",
    "PH Hotel", "Kotoka", "030 254", "Fertility", "fertility", "IVF", "ICSI",
    "IUI", "X-ray", "dialysis", "Dialysis",
    "cervical", "Cervical", "Ridge Hospital", "Kokroko", "El-Yahweh",
    "Emergency & Critical Care", "Diagnostic Imaging", "Dietetics",
    "Counselling", "Preventive Healthcare", "Internal Medicine",
    "Medical Laboratory",
    # City Hospital leftovers (this build must not contain any).
    "Kumasi", "Old Amakom", "Star Junction", "Baba Yara", "032 202",
    "024 662", "020 568", "Adinkra", "Gyesi", "Modern Ghana", "modernghana",
    "50 years", "1976",
    # Al-Kawthar must NOT claim these (unconfirmed or disputed).
    "NHIS accepted", "accept the NHIS", "accepts the NHIS", "NHIS card",
    "first Islamic", "First Islamic", "Anbariya", "Sunni", "Tijania",
    "Shia", "Sheikh",
    # Services Al-Kawthar does not offer.
    "General Surgery", "Urology", "Gynaecology", "Rehabilitation Care",
]
FORBIDDEN_WORDS = [r"\bHMS\b", r"\bENT\b", r"\bCT\b", r"\bMRI\b", r"\bICU\b",
                    r"\bDel\b"]


def verify(s):
    problems = []
    # Strip embedded images first: base64 blobs can contain substrings
    # like "2011" or "CT" by coincidence.
    text = re.sub(r'data:image/[^"\']+;base64,[A-Za-z0-9+/=]+', '', s)
    for token in FORBIDDEN:
        if token in text:
            problems.append("forbidden token present: %r" % token)
    for pat in FORBIDDEN_WORDS:
        if re.search(pat, text):
            problems.append("forbidden word present: %s" % pat)
    checks = {
        "svc-card buttons": s.count('class="svc-card"'),
        "Outpatient Consultation": s.count("Outpatient Consultation"),
        "Inpatient Care": s.count("Inpatient Care"),
        "Laboratory": s.count("Laboratory"),
        "Pharmacy": s.count("Pharmacy"),
        "Dental Clinic": s.count("Dental Clinic"),
        "Optical Clinic": s.count("Optical Clinic"),
        "Ultrasound & Scan": s.count("Ultrasound &amp; Scan"),
        "Maternity Services": s.count("Maternity Services"),
        "Mother & Child Care": s.count("Mother &amp; Child Care"),
        "Minor Theatre": s.count("Minor Theatre"),
        "Physiotherapy": s.count("Physiotherapy"),
        "Health Screenings": s.count("Health Screenings"),
        "Al-Kawthar Islamic Hospital": s.count("Al-Kawthar Islamic Hospital"),
        "024 415 8915": s.count("024 415 8915"),
        "0553 602 241": s.count("0553 602 241"),
        "alkawtharhospital@gmail.com": s.count("alkawtharhospital@gmail.com"),
        "Watherson Area, behind the Northern Regional Coordinating Council": s.count("Watherson Area, behind the Northern Regional Coordinating Council"),
        "C56G+7W": s.count("C56G+7W"),
        "female ward (any case)": s.count("female ward") + s.count("Female ward"),
        "guided by faith": s.count("guided by faith"),
        "Guided by Faith": s.count("Guided by Faith"),
        "building front-wide photo uses": s.count(ALK_BUILDING_FRONT_WIDE),
        "building night photo uses": s.count(ALK_BUILDING_NIGHT),
        "streetview photo uses": s.count(ALK_BUILDING_STREETVIEW),
        "building front-sign photo uses": s.count(ALK_BUILDING_FRONT_SIGN),
        "building front photo uses": s.count(ALK_BUILDING_FRONT),
        "building side photo uses": s.count(ALK_BUILDING_SIDE),
        "entrance gate photo uses": s.count(ALK_ENTRANCE_GATE),
        "corridor bright photo uses": s.count(ALK_CORRIDOR_BRIGHT),
        "corridor doors photo uses": s.count(ALK_CORRIDOR_DOORS),
        "pharmacy lab photo uses": s.count(ALK_PHARMACY_LAB),
        "services board photo uses": s.count(ALK_SERVICES_BOARD),
        "signboard street photo uses": s.count(ALK_SIGNBOARD_STREET),
        "real logo uses": s.count(LOGO),
        "svg placeholders left": s.count("data:image/svg+xml"),
        "patient reviews section": s.count("What our patients say"),
        "chat fab text": s.count("<span>Chat with us</span>"),
        "chat fab script": s.count("// Chat button: pops open on load"),
        "chat fab expanded rule": s.count(".chat-fab.expanded"),
        "chat fab starts expanded": s.count('class="chat-fab expanded"'),
        # The chat-bubble SVG path appears 3 times, all on WhatsApp links.
        # If the fab's bubble icon came back it would be 4.
        "chat bubble icons": s.count('M21 11.5a8.38 8.38 0 0 1-.9 3.8'),
        # Booking date and time (user, 2026-11-21): the form must let the
        # customer pick the date and time they want.
        "booking date field": s.count('id="bkDate"'),
        "booking time field": s.count('id="bkTime"'),
        "booking date in message": s.count('Preferred date: " + fmtBookDate(dateVal)'),
        "booking time in message": s.count('Preferred time: " + fmtBookTime(timeVal)'),
        "booking datetime script": s.count("// Booking date/time helpers"),
        "css overrides": s.count("Al-Kawthar overrides (2026-11-21)"),
        "review cards": s.count('class="value-card review-card"'),
        "pop-in keyframes": s.count("@keyframes alkPopIn"),
        "pop-in script": s.count("// Pop-in on load and on scroll."),
        "our core values": s.count("Our core values"),
        "old values heading": s.count("<h2>Our values</h2>"),
        "our mission": s.count("Our Mission"),
        "our vision": s.count("Our Vision"),
        "mission grid": s.count('class="mission-grid"'),
        "preview timer bar": s.count('id="previewTimer"'),
        "preview timer script": s.count("// Preview countdown timer:"),
        "live map iframe": s.count('class="map-live-frame"'),
        "review forms": s.count('class="review-form"'),
        "review form script": s.count("// Customer review form:"),
        "header fade script": s.count("// Transparent header on scroll (user, 2026-11-22):"),
    }
    if checks["svc-card buttons"] != 18:
        problems.append("svc-card count %d, expected 18" % checks["svc-card buttons"])
    if checks["building front-wide photo uses"] != 3:
        problems.append("building front-wide photo used %d times, expected 3 "
                        "(hero x1, carousel x1, gallery slide 1)"
                        % checks["building front-wide photo uses"])
    if checks["building night photo uses"] != 2:
        problems.append("building night photo used %d times, expected 2 "
                        "(hero slide 2, gallery slide 2)"
                        % checks["building night photo uses"])
    if checks["streetview photo uses"] != 1:
        problems.append("streetview photo used %d times, expected 1 "
                        "(hero slide 3)"
                        % checks["streetview photo uses"])
    if checks["building front-sign photo uses"] != 1:
        problems.append("building front-sign photo used %d times, expected 1 "
                        "(About teaser)"
                        % checks["building front-sign photo uses"])
    if checks["building front photo uses"] != 1:
        problems.append("building front photo used %d times, expected 1 "
                        "(contact find-panel)"
                        % checks["building front photo uses"])
    if checks["building side photo uses"] != 1:
        problems.append("building side photo used %d times, expected 1 "
                        "(gallery slide 9)"
                        % checks["building side photo uses"])
    if checks["entrance gate photo uses"] != 1:
        problems.append("entrance gate photo used %d times, expected 1 "
                        "(gallery slide 4)"
                        % checks["entrance gate photo uses"])
    if checks["corridor bright photo uses"] != 4:
        problems.append("corridor bright photo used %d times, expected 4 "
                        "(gallery slide 5 + Inpatient Care first photo: home grid + services grid + detail)"
                        % checks["corridor bright photo uses"])
    if checks["corridor doors photo uses"] != 2:
        problems.append("corridor doors photo used %d times, expected 2 "
                        "(gallery slide 6 + Inpatient Care)"
                        % checks["corridor doors photo uses"])
    if checks["pharmacy lab photo uses"] != 1:
        problems.append("pharmacy lab photo used %d times, expected 1 "
                        "(gallery slide 7)"
                        % checks["pharmacy lab photo uses"])
    if checks["services board photo uses"] != 2:
        problems.append("services board photo used %d times, expected 2 "
                        "(story section + gallery slide 3)"
                        % checks["services board photo uses"])
    if checks["signboard street photo uses"] != 1:
        problems.append("signboard street photo used %d times, expected 1 "
                        "(gallery slide 8)"
                        % checks["signboard street photo uses"])
    if checks["real logo uses"] != 4:
        problems.append("real logo used %d times, expected 4 "
                        "(header brand-mark + footer brand-mark + chat head-logo + chat fab)"
                        % checks["real logo uses"])
    if checks["our core values"] != 1:
        problems.append("core values heading found %d times, expected 1"
                        % checks["our core values"])
    if checks["old values heading"] != 0:
        problems.append("old values heading still present (%d)"
                        % checks["old values heading"])
    if checks["our mission"] != 1 or checks["our vision"] != 1:
        problems.append("mission/vision found %d/%d times, expected 1/1"
                        % (checks["our mission"], checks["our vision"]))
    if checks["mission grid"] != 1:
        problems.append("mission grid found %d times, expected 1"
                        % checks["mission grid"])
    if checks["pop-in keyframes"] != 1:
        problems.append("pop-in keyframes found %d times, expected 1"
                        % checks["pop-in keyframes"])
    if checks["pop-in script"] != 1:
        problems.append("pop-in script found %d times, expected 1"
                        % checks["pop-in script"])
    if checks["patient reviews section"] != 3:
        problems.append("patient reviews section found %d times, expected 3 "
                        "(home, about, contact)"
                        % checks["patient reviews section"])
    if checks["review cards"] != 9:
        problems.append("review cards %d, expected 9" % checks["review cards"])
    if s.count('class="contact-reviews"') != 1:
        problems.append("contact reviews block found %d times, expected 1"
                        % s.count('class="contact-reviews"'))
    aside_start = s.find('<aside class="panel">')
    if aside_start < 0 or s.find("Mariam M.", aside_start) < 0:
        problems.append("Mariam review not found inside the contact aside")
    if checks["chat fab text"] != 1:
        problems.append("chat fab text found %d times, expected 1"
                        % checks["chat fab text"])
    if checks["chat fab script"] != 1:
        problems.append("chat fab script found %d times, expected 1"
                        % checks["chat fab script"])
    if checks["chat fab expanded rule"] != 2:
        problems.append("chat fab expanded rule found %d times, expected 2"
                        % checks["chat fab expanded rule"])
    if checks["chat fab starts expanded"] != 1:
        problems.append("chat fab starts-expanded found %d times, expected 1"
                        % checks["chat fab starts expanded"])
    if checks["chat bubble icons"] != 3:
        problems.append("chat bubble icons found %d times, expected 3 "
                        "(WhatsApp links only — the fab's bubble icon must "
                        "be gone)" % checks["chat bubble icons"])
    if checks["booking date field"] != 1:
        problems.append("booking date field found %d times, expected 1"
                        % checks["booking date field"])
    if checks["booking time field"] != 1:
        problems.append("booking time field found %d times, expected 1"
                        % checks["booking time field"])
    if checks["booking date in message"] != 1:
        problems.append("booking date missing from WhatsApp message")
    if checks["booking time in message"] != 1:
        problems.append("booking time missing from WhatsApp message")
    if checks["booking datetime script"] != 1:
        problems.append("booking date/time script found %d times, expected 1"
                        % checks["booking datetime script"])
    if checks["css overrides"] != 1:
        problems.append("css overrides found %d times, expected 1"
                        % checks["css overrides"])
    # The only SVG left should be the map (1). The logo is now the real
    # The only SVG left should be none now — the drawn map was replaced
    # by the live Google Map embed (2026-11-21). The logo is the real
    # logo photo (JPEG data URI), used 4 times: header, footer, chat head,
    # chat fab.
    if checks["svg placeholders left"] != 0:
        problems.append("svg data URIs: %d, expected 0 (live map, no drawn map)"
                        % checks["svg placeholders left"])
    if checks["live map iframe"] != 1:
        problems.append("live map iframe found %d times, expected 1"
                        % checks["live map iframe"])
    if checks["review forms"] != 2:
        problems.append("review forms found %d times, expected 2 (home + about)"
                        % checks["review forms"])
    if checks["review form script"] != 1:
        problems.append("review form script found %d times, expected 1"
                        % checks["review form script"])
    if checks["header fade script"] != 1:
        problems.append("header fade script found %d times, expected 1"
                        % checks["header fade script"])
    for k in ("Outpatient Consultation", "Inpatient Care", "Laboratory",
              "Pharmacy", "Dental Clinic", "Optical Clinic",
              "Ultrasound & Scan", "Maternity Services",
              "Mother & Child Care", "Minor Theatre", "Physiotherapy",
              "Health Screenings"):
        if checks[k] < 3:
            problems.append("%s appears only %d times" % (k, checks[k]))
    if checks["Al-Kawthar Islamic Hospital"] < 15:
        problems.append("brand name appears only %d times"
                        % checks["Al-Kawthar Islamic Hospital"])
    if checks["024 415 8915"] < 6:
        problems.append("main phone appears only %d times" % checks["024 415 8915"])
    if checks["0553 602 241"] < 3:
        problems.append("second number 0553 602 241 appears only %d times, expected 3 "
                        "(contact Call card, emergency banner, chat panel)"
                        % checks["0553 602 241"])
    if checks["alkawtharhospital@gmail.com"] < 3:
        problems.append("email appears only %d times" % checks["alkawtharhospital@gmail.com"])
    if checks["Watherson Area, behind the Northern Regional Coordinating Council"] < 2:
        problems.append("address appears only %d times"
                        % checks["Watherson Area, behind the Northern Regional Coordinating Council"])
    if checks["C56G+7W"] < 1:
        problems.append("plus code C56G+7W not found")
    if checks["female ward (any case)"] < 3:
        problems.append("female ward appears only %d times"
                        % checks["female ward (any case)"])
    if checks["guided by faith"] < 3:
        problems.append("'guided by faith' appears only %d times"
                        % checks["guided by faith"])
    if checks["Guided by Faith"] < 1:
        problems.append("'Guided by Faith' (motto) not found")
    if checks["preview timer bar"] != 1:
        problems.append("preview timer bar found %d times, expected 1"
                        % checks["preview timer bar"])
    if checks["preview timer script"] != 1:
        problems.append("preview timer script found %d times, expected 1"
                        % checks["preview timer script"])
    return problems, checks

def js_check(s):
    """Syntax-check every inline <script> block with node."""
    blocks = re.findall(r"<script>(.*?)</script>", s, re.DOTALL)
    if not blocks:
        return "no <script> block found"
    tmp = Path("/tmp/alk-demo-check.js")
    import subprocess
    for i, code in enumerate(blocks):
        tmp.write_text(code, encoding="utf-8")
        r = subprocess.run(["node", "--check", str(tmp)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            return "node --check failed on script block %d:\n%s" % (i, r.stderr)
    return None


def main():
    src = SRC.read_text(encoding="utf-8")
    out = transform(src)
    problems, checks = verify(out)
    if problems:
        print("VERIFY FAILED:")
        for p in problems:
            print(" -", p)
        raise SystemExit(1)
    err = js_check(out)
    if err:
        print("JS CHECK FAILED:")
        print(err)
        raise SystemExit(1)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(out, encoding="utf-8")
    print("OK — wrote", DST, "(%d bytes)" % len(out.encode("utf-8")))
    for k, v in checks.items():
        print("  %-32s %d" % (k, v))


if __name__ == "__main__":
    main()
