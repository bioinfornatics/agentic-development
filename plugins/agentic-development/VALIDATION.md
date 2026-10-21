# Validation du candidat 0.4.2

## Résultats exécutés

- Plugin : portable-load accepted ; strict-authoring pass.
- Format des sept skills : 7/7 pass. Audits : 7/7 pass, zéro finding.
- Conception des scénarios : 7/7 pass. Total : 23 contrôles officiels réussis.
- Contrats et policies : copies identiques ; trois grilles identiques.
- 41 liens contenus, toutes les fixtures/navigation existantes.
- Exemples chiffrés vérifiés : conformité 75/100 ; partiel 71.25, couverture 95, global null.
- Exemple de checkpoint : PASS distinct d’acceptation pending Judge.
- Source Beads inchangée, hash contrôlé.

88 cas explain préparés, 76 prompts distincts après neutralisation des noms de
skills, cinq scénarios d’intégration. Ces chiffres ne sont pas un benchmark ni
un taux de réussite comportementale. Les fixtures sont hypothétiques, pas des
preuves de tests ou commandes Beads réels.

## Limites

Évaluation comportementale appariée : NOT RUN. Réévaluation adversariale du
candidat corrigé : NOT RUN. Revue humaine : pending. Score de Judge : non évalué.
Les cas d’activation/non-activation et l’exécution réelle des gates restent à
évaluer dans agentic-devlopment-ecv. Aucun runtime de manifeste n’est embarqué.
Avertissement strict non bloquant : dossier agentic-devlopment différent du nom
agentic-development. Aucun renommage, commit, push, sync ou activation effectué.

## Artifacts et historique

Rapports officiels et cohérence : docs/validation/summary.json et rapports voisins.
Sources actuelles : docs/validation/source-hashes.json.
Historique avant corrections : docs/validation/validation-history-through-0.3.0.md.
Rapports adversariaux 0.3.0 inchangés : docs/reviews/adversarial-0.3.0/.
Mapping de traitement : docs/reviews/adversarial-0.3.0/REMEDIATION.md.

## État du dépôt

État horodaté dans summary.json. Branche main, aucun remote observé. Le plugin
reste non suivi/non commité ; .beads/interactions.jsonl est déjà modifié. Le skill
Beads local, AGENTS.md et CLAUDE.md ne sont pas modifiés par ces corrections.
Les changements de suivi Beads restent locaux, sans sync distante.

## Setup Beads documenté

Procédure conditionnelle dans drive-cycle/references/beads-initialization.md,
flags vérifiés contre bd 1.1.2 --help. Aucun bd init exécuté. Deux scénarios explain
ajoutés : setup autorisé et workspace existant à préserver. 23 contrôles officiels
réexécutés avec succès ; comportement de setup non testé en sandbox.

## Profils guidance/hooks

Intégration minimale recommandée ; hooks Git optionnels après examen/autorisation.
Cinq contrôles réexécutés pour cette modification : deux profils plugin et
validate/audit/design du coordinateur. Les six autres skills sont inchangés,
avec leurs preuves précédentes conservées. Tous les contrôles relancés passent.
Les hooks existants ont été inspectés/listés, pas modifiés ni exécutés par setup.
Aucun init, install de hook, commit ou sync effectué.

## Installation locale du candidat 0.4.2

Copie opérationnelle installée dans ~/.agents/plugins/agentic-development :
plugin.json et sept skills avec references/assets. Dépôt, Beads, intégrations
host, evals et preuves de recherche ne sont pas copiés. 49 fichiers vérifiés
identiques à la source. Validation portable-load et strict-authoring installées
réussies, sans avertissement de nom de dossier. goose skills list découvre les
sept chemins installés ; cette CLI affiche les noms courts. Le chargement par
nom qualifié documenté et le comportement en session ne sont pas encore vérifiés.
Installation manuelle : pas de source Git ni auto-update configurés.

AGENTS.md et CLAUDE.md nettoyés et identiques (44 lignes), originaux sauvegardés
hors dépôt. Skill Beads et hooks inchangés. Aucun commit/push/sync effectué.
Reçu et sauvegarde : docs/validation/local-installation.json. Installation locale
ne constitue pas une approbation de release ni une évaluation comportementale.
