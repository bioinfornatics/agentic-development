# Piloter le cycle de développement

Choisissez une tranche cohérente : un résultat que vous pouvez vérifier et reprendre
indépendamment. Ne créez pas une tâche par fichier ou par phase.

## Étapes et résultats attendus

| Étape | Action | Résultat attendu |
|---|---|---|
| Research | Explorer les sources et tester les hypothèses | Question, faits, options et inconnues |
| Plan | Définir le périmètre, les critères, les responsabilités et la vérification | Plan exécutable, dépendances et permissions |
| Implement | Réaliser le plus petit changement cohérent | Diff expliqué, travail préservé et tests ciblés |
| Test | Exécuter les vérifications sur le candidat identifié | Commandes, résultats, environnement et limites |
| Judge | Comparer les preuves, les exigences et les standards | Verdict, constats, score applicable et indépendance |
| Iterate | Corriger un défaut ou résoudre un prérequis | Correction bornée et preuves à reproduire |

Le coordinateur choisit la prochaine étape et finalise la traçabilité.
Réutilisez une recherche ou un plan encore valides. Ne recommencez pas tout le cycle
à chaque reprise, mais ne sautez pas une vérification nécessaire.

## Développer avec un retour rapide

Pour un comportement exécutable :
1. Écrivez ou réutilisez un test à une interface publique.
2. Observez un échec qui reproduit réellement le défaut (**red**).
3. Réalisez la correction minimale et observez le succès (**green**).
4. Refactorisez sans changer le comportement, puis relancez les tests.
5. Passez au comportement suivant et aux régressions pertinentes.

Les résultats attendus proviennent de l'exigence ou d'un oracle indépendant, pas du code testé.
Une vérification du format documentaire ne prouve pas le comportement d'un agent.

## Lire le bilan de chaque étape

Le bilan suit six sections, dans cet ordre :
1. **Objectif et position dans la roadmap** : jalon, epic, US, tranche, phase, périmètre et tâche.
2. **Résultat** : ce qui est terminé, incomplet ou inchangé.
3. **Changements et preuves** : fichiers, branches, commits, commandes et limites.
4. **Verdict et incertitudes** : faits, risques, indépendance et score applicable.
5. **Transition** : prochaine phase et recommandation de session, distinctes de l'action.
6. **Prochaine action et reprise** : prérequis et première étape concrète.

Un commit proposé n'a pas de hash. Une session recommandée n'a pas été lancée.
Le bilan distingue les fichiers modifiés des fichiers réellement commités.

## Juger et corriger sans changer les règles

Figez le candidat et les critères avant le jugement. Les tests sont des preuves,
pas une acceptation. Une indépendance requise mais indisponible reste une limite.
Figez la grille de jugement v1.0.1 ou un remplacement explicitement approuvé avant
l'implémentation. La méthode embarquée utilise un score pondéré et préserve les critères
inconnus ; cette documentation n'introduit pas de mode de notation pour petites tâches.

Corrigez le défaut le plus précis, puis relancez ses vérifications et les régressions.
Conservez les preuves encore valides ; invalidez celles dont les entrées ont changé.
Ne baissez pas un seuil et ne supprimez pas un test pour obtenir un succès.
Le budget par défaut du coordinateur est de trois tours de correction. Iterate enregistre
le compteur de tours et s'arrête lorsqu'une capacité requise est indisponible. Suivez la
politique de tours embarquée ; cette documentation n'ajoute pas d'exemption pour le diagnostic ou l'attente.
En cas de blocage ou de budget épuisé, arrêtez-vous et préparez la reprise. Ne clôturez que
le périmètre réellement vérifié et autorisé.

Suite : [gérer tâches, commits et sessions](integrations.md).
