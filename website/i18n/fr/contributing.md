# Contribuer à la méthode

## Choisir le bon emplacement

- **plugins/agentic-development/skills/** : instructions en anglais et ressources requises par chaque skill.
- **website/guides/** : guides utilisateur courts, sans logs ni historique.
- **website/tests/** : vérifications reproductibles et sondes explicitement déclenchées.
- Les preuves d'exécution restent séparées de la documentation ; le tracker conserve
  l'état courant du travail.

Commencez par les [instructions du dépôt](../../../AGENTS.md). Vérifiez branche, index,
permissions et changements préexistants. Définissez un objectif et ses exclusions
avant de modifier les sources.

L'anglais est la langue par défaut de tout contenu du dépôt et distribué. Seule une demande
explicite de l'utilisateur autorise une exception linguistique ; la langue de la conversation
ne l'autorise pas. La documentation anglaise est canonique ; les traductions explicitement
sollicitées restent séparées et liées à leur source anglaise. La documentation multilingue
et la configuration/publication GitHub Pages exigent un périmètre de travail distinct
et une autorisation de déploiement.

## Écrire une instruction utile

Centrez les descriptions des skills sur leur rôle et les situations où les utiliser.
Dans le corps, dirigez l'exécution : **intention → prérequis → action → résultat
vérifié → prochaine action ou arrêt**. Nommez l'action à effectuer, ses entrées et
le skill à charger ensuite ; une description de phase ne suffit pas.
Placez les détails conditionnels dans une ressource directement liée. Gardez la méthode
indépendante de l'hôte ; les hooks restent une intégration propre à l'hôte.

Spécifiez Goals/Non-goals, des critères Given/When/Then pour le comportement et des NFRs mesurables
lorsque c'est pertinent. N'inventez pas de chiffres arbitraires, de permissions implicites
ou de preuves simulées. Le [contrat de communication](../../../plugins/agentic-development/skills/drive-cycle/references/communication-contract.md)
fournit les consignes de bilan par phase ; le [cycle](cycle.md) en explique l'usage.

## Vérifier avant de proposer

Depuis la racine du dépôt, exécutez :

    python3 -m unittest discover -s website/tests -v

Ces tests couvrent les contrats du générateur documentaire, pas la qualité du modèle
ni une installation globale. Utilisez aussi les validations officielles disponibles
pour le composant modifié. Un conflit entre un validateur et Goose exige de vérifier
la documentation et le runtime, pas de déclarer automatiquement la compatibilité.

Vérifiez les liens locaux et la cohérence des ressources partagées.
Un changement de runtime exige ses propres tests : cas autorisé, échec, données malformées
et limites pertinentes. Ne lancez une sonde isolée qu'avec un périmètre et des effets
connus ; aucune installation ni campagne n'est implicite.

## Livrer et transmettre

Signalez les fichiers réellement modifiés, le travail préservé, les commandes/résultats,
les limites et le jugement disponible. Pour un commit autorisé, vérifiez message, hash et
contenu. La prochaine étape doit pouvoir être retrouvée à partir de la tâche et d'un prompt autonome.
Ne clôturez pas une US ou une release sur la seule base de tests réussis.
