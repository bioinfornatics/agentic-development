# Piloter le cycle de développement

Choisissez une tranche cohérente : un résultat que vous pouvez vérifier et reprendre
indépendamment. Ne créez pas une tâche par fichier ou par phase.

## Étapes et résultats attendus

| Étape | Action | Résultat attendu |
|---|---|---|
| Research | Établir le contexte produit avant de planifier, puis explorer les sources utiles | Finalité, utilisateurs/résultat, comportement actuel, contraintes, faits et inconnues |
| Plan | Définir le périmètre, les critères, les responsabilités et la vérification | Plan exécutable, dépendances et permissions |
| Implement | Réaliser le plus petit changement cohérent | Diff expliqué, travail préservé et tests ciblés |
| Test | Exécuter les vérifications sur le candidat identifié | Commandes, résultats, environnement et limites |
| Judge | Comparer les preuves, les exigences et les standards | Verdict, constats, score applicable et indépendance |
| Iterate | Corriger un défaut ou résoudre un prérequis | Correction bornée et preuves à reproduire |

Commencez chaque nouvel objectif de développement par Research, même avec une demande claire ou du code familier.
Research → Plan → Implement (RPI) évite une planification fondée sur des hypothèses produit non vérifiées.
Le coordinateur choisit la prochaine étape et finalise la traçabilité.
Réutilisez une recherche après vérification de sa couverture du contexte et de sa fraîcheur ; conservez un plan encore valide. Ne recommencez pas tout le cycle
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

Le bilan final utilise cinq sections, dans cet ordre :
1. **current goal {step: …}** : l'objectif traité et la phase réelle, avec la tâche vérifiée.
2. **roadmap position** : les références vérifiées de roadmap/epic/US, un repère visuel du cycle, la prochaine action et le statut/blocage.
3. **modified files** : les chemins modifiés, ou N/A.
4. **closed tasks** : les identifiants des tâches dont la clôture est confirmée, ou N/A.
5. **explanation** : les actions, raisons, preuves, limites et prochaine porte.

Les états blocked, done et loop again ne sont pas des phases ; ils restent dans roadmap position.
N'inventez pas la progression de la roadmap. Si elle est indisponible, indiquez-le et montrez uniquement le cycle connu.
Exemple : `Research [reused] → Plan [active] → Implement [pending] → Test [pending] → Judge [pending]`.
La roadmap décrit les résultats ; le cycle décrit les phases. Expliquez les transitions hors ordre habituel et leurs prérequis.
Les libellés restent fixes ; les valeurs utilisent la langue de l'utilisateur. L'explication conserve les critères, vérifications et verdict.
Un résultat bloqué ou inchangé conserve les cinq sections.

Lisez les exigences avant les actions qu'elles gouvernent. Lisez les contrats de sortie commun et de livraison de phase après investigation, avant de rédiger le retour.

Un commit proposé n'a pas de hash. Une session recommandée n'a pas été lancée.
Le bilan distingue les fichiers modifiés des fichiers réellement commités.

## Juger et corriger sans changer les règles

Figez le candidat et les critères avant le jugement. Les tests sont des preuves,
pas une acceptation. Une indépendance requise mais indisponible reste une limite.
Choisissez le mode de notation avant l'implémentation ; un score numérique demandé
ne disparaît pas parce que la tâche est petite.

Corrigez le défaut le plus précis, puis relancez ses vérifications et les régressions.
Conservez les preuves encore valides ; invalidez celles dont les entrées ont changé.
Ne baissez pas un seuil et ne supprimez pas un test pour obtenir un succès.
Le budget par défaut est de trois tentatives autorisées ; l'attente et le diagnostic
ne consomment pas de tentative. En cas de blocage ou de budget épuisé, arrêtez-vous
et préparez la transmission. Ne clôturez que le périmètre réellement vérifié et autorisé.

Suite : [gérer tâches, commits et sessions](integrations.md).
