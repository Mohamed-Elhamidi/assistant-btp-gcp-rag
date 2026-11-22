# Base documentaire simplifiée pour démarrer le RAG BTP.
# Chaque fiche représente un extrait de document ou de consigne chantier.

FICHES_BTP = [
    {
        "id": "SEC-HAUTEUR-01",
        "titre": "Travail en hauteur et protections collectives (EPC)",
        "categorie": "Sécurité chantier",
        "contenu": (
            "Dès qu'il existe un risque de chute de hauteur, la priorité est donnée aux "
            "équipements de protection collective (garde-corps périphériques, échafaudages "
            "conformes, filets de recueil). Le recours aux EPI (harnais, système d'arrêt de chute) "
            "intervient lorsque la protection collective est techniquement impossible ou en complément. "
            "Toujours vérifier le PPSPS ou le plan de prévention avant intervention."
        ),
    },
    {
        "id": "SEC-FOUILLE-02",
        "titre": "Tranchées et travaux de terrassement",
        "categorie": "Terrassement",
        "contenu": (
            "Pour les fouilles et tranchées présentant un risque d'éboulement, prévoir un "
            "blindage, un talutage ou un blindage par caisson adapté à la nature du sol. "
            "Interdire l'accumulation de déblais trop près du bord de la tranchée et sécuriser "
            "l'accès (échelle dépassant d'au moins 1 mètre) ainsi que le balisage périmétrique."
        ),
    },
    {
        "id": "SEC-ELEC-03",
        "titre": "Travaux à proximité de lignes électriques",
        "categorie": "Risque électrique",
        "contenu": (
            "Identifier la présence de réseaux aériens ou souterrains avant tout terrassement "
            "ou levage (consultation des DT/DICT et marquage-piquetage). Respecter les distances "
            "de sécurité vis-à-vis des lignes et n'habiliter que le personnel formé et autorisé "
            "selon la norme NF C 18-510."
        ),
    },
]
