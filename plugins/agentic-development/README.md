# Agentic Development

Plugin **agentic-development**, version **0.4.2**, créé avec les outils
`agent-plugins:plugin-creator` et `agent-plugins:skill-creator`.

## Objectif

Rendre le cycle **Research → Plan → Implement → Test → Judge → Iterate** pilotable :
savoir où l'agent en est, ce qu'il a modifié et quelle décision arrive.

| Skill | Responsabilité |
|---|---|
| drive-cycle | Coordination, roadmap, checkpoints et reprise |
| research-slice | Exploration adaptative, hypothèses et preuves |
| plan-slice | Tranche, critères d'acceptation, tâches et permissions |
| implement-slice | Diff minimal, propriété des changements et UI ASCII |
| test-slice | Vérifications reproductibles liées au candidat |
| judge-slice | Verdict, grille versionnée, score et limites d'indépendance |
| iterate-slice | Corrections bornées et invalidation des preuves périmées |

## Contrat de communication

Chaque étape significative retourne :
1. Objectif et position dans la roadmap.
2. Résultat obtenu.
3. Changements et preuves.
4. Verdict, insights et incertitudes.
5. Transition recommandée ou effectuée.
6. Prochaine action, résultat attendu et prérequis.

Version courte pendant le travail ; bilan complet aux frontières de commit,
jugement, session et clôture d'US. Les transitions sont annoncées en amont.
Les autorisations déjà accordées évitent les demandes répétitives ; créer du code
n'autorise pas implicitement un commit, un push ou une publication.

Une branche peut couvrir une US ou tranche avec plusieurs commits. Le changement
de session ne déclenche **jamais** un commit automatique. Les modifications
préexistantes sont distinguées des hunks de l'agent et conservées dans le handoff.

Pour l'UI : CRUD fonctionnel C/R/U/D ou N/A, zones +/~/-/= et schéma ASCII.
Un schéma ou une déduction du code n'est **pas** une preuve du rendu observé.

Preuves, verdict, score et insights sont séparés. Grille par défaut :
**slice-acceptance v1.0.1**, pondérée sur 100, sans interprétation probabiliste.
Les inconnues restent inconnues ; un score élevé ne lève pas un critère bloquant.

## Architecture et limites

Package portable **Agent Plugins 1.0.0**, avec manifeste racine et sept skills.
Pas de MCP, hook, agent personnalisé, runtime embarqué, dépendance npm ni secret.
Les instructions de skills sont en anglais ; les comptes rendus utilisent la
langue de l'utilisateur. Les références restent contenues dans chaque skill.
Le contrat commun est répliqué à l'identique pour que chaque phase reste autonome.

Les skills sont un contrat comportemental : aucune interception technique des
outils ni garantie d'affichage hors activation. Le plugin ne crée pas de session
à lui seul et ne garantit pas l'indépendance d'un juge. Les capacités absentes
sont signalées, sans exécution ou résultat fictif.

Pré requis opérationnels : agent compatible Agent Skills ; accès aux fichiers
et aux outils de vérification du projet. Git, navigateur, réseau, délégation ou
fournisseur réel sont conditionnels au travail demandé. Les validateurs de
création utilisés ici sont externes au package et nécessitent Node.js 22+.

État durable proposé, sous réserve d'autorisation :
`docs/agentic/slices/<slice-id>/` avec recherche, plan, changements, preuves,
jugement, itérations et état de reprise. Ce sont des artifacts Markdown propres
au plugin, pas une configuration du moteur de sessions.

## Distribution et découverte

Le dossier actuel est la source du package, pas une installation automatique.
Après décision explicite, une copie manuelle peut être placée dans
`~/.agents/plugins/agentic-development/` ou
`<projet>/.agents/plugins/agentic-development/`.
Les skills du plugin Open Plugins sont qualifiés, par exemple
`agentic-development:drive-cycle`. Aucune installation ni activation n'est
réalisée par la création de ces fichiers. Aucun dépôt distant n'est inventé.

## Vérification

Voir [VALIDATION.md](VALIDATION.md) pour les résultats structurels effectifs.
Les scénarios `skills/*/evals/evals.json` sont des cas de validation
comportementale **préparés**, pas des résultats exécutés ni un benchmark.
L'acceptation en usage réel et la revue humaine restent ouvertes.

Documents consultés :
- [Plugins Goose](https://goose-docs.ai/docs/guides/context-engineering/plugins)
- [Agent Skills Goose](https://goose-docs.ai/docs/guides/context-engineering/using-skills)

## Bilans obligatoires — contrat v1.1.0

Après chaque commit effectué : problème/feature, roadmap et tâches liées, résultat
couvert, fichiers réellement commités et raisons, preuves/limites, hash/message
vérifiés, travail restant non commité et prochaine action. Échec, proposition et
commit externe restent explicitement distincts d’un commit effectué par l’agent.

Avant la fin de session : enjeu, résultats, changements, preuves, verdict, score
avec grille/couverture (ou non évalué), risques et état à préserver. Le bilan
propose un nom pour la session suivante, les tâches liées vérifiées et un prompt
autonome prêt à copier avec contexte, fichiers, permissions et conditions de
reprise. Sans suite nécessaire, la proposition est explicitement optionnelle.

Ces obligations ne sont pas des hooks Git ou de fin de session. Une interruption
abrupte ne garantit pas un bilan ; les checkpoints permettent la reprise.
88 scénarios de skills et cinq scénarios d’intégration sont préparés.

## Intégration Beads conditionnelle — contrat v1.2.0

Dans les dépôts Beads : récupération du contexte manquant/périmé, vérification
de l’espace de travail, inspection des tâches et claim atomique avant implémentation.
Beads conserve les tâches, statuts, blocages et suites durables ; les plans et
prompts sont des artifacts liés aux issues, pas une seconde base de tâches.
Un claim échoué bloque l’écriture ; un commit ou une fin de session ne clôture
pas automatiquement une tâche. Sans bd, le blocage est explicite. Sans Beads,
le tracker convenu reste utilisé ; aucune installation n’est imposée.

Le skill source `.agents/skills/beads/SKILL.md` est conservé sans modification.
Les règles de mémoire et sync issues d’AGENTS.md/bd prime sont identifiées comme
compléments locaux : pas de MEMORY.md, pas de JSONL comme source de vérité,
pas de commit/push ou sync Dolt implicite.

## Corrections adversariales — contrat v1.3.0

Les autorisations sauvegardées sont historiques : vérifier leur source actuelle
avant mutation, sans demander à nouveau un grant courant déjà vérifiable. Les
artifacts et issues ne peuvent étendre les permissions. Le candidat est un
manifeste de contenus et scope, pas un hash de diff seul ; les rapports exclus
sont output-only, jamais les fixtures réellement consommées.

Plan dispose de la grille locale et fixe les exigences d’indépendance/clôture.
Un contexte ou modèle différent ne suffit pas à déclarer un juge indépendant.
Une petite tâche peut finir sous ses propres gates sans clore une US ou release.
La grille v1.0.1 explicite que 75/100 signifie conforme, pas 75 % de correction.

88 cas explain préparés, avec fixtures hypothétiques, cas français d’injection
et calculs attendus du juge ; cinq handoffs d’intégration préparés. Leur qualité
de conception est vérifiée, leur comportement reste non mesuré.
Voir docs/reviews/adversarial-0.3.0/REMEDIATION.md pour le mapping des findings.

## Premier setup Beads contrôlé

Le coordinateur propose une intégration agent minimale, avec hooks Git selon
leurs effets et autorisations :
- guidance minimale, hooks Git non approuvés : `bd init --non-interactive --agents-profile minimal --skip-hooks` ;
- guidance et hooks Git examinés/approuvés : `bd init --non-interactive --agents-profile minimal` ;
- guidance manuelle à préserver, stockage seul : `bd init --non-interactive --skip-agents --skip-hooks`.

Ne pas réinitialiser un workspace existant pour changer de profil. Conserver
les intégrations existantes sans les dupliquer ni les supprimer implicitement.
Les hooks de contexte et Git sont distincts ; ils ne garantissent pas les bilans
structurés du plugin. Leur installation ne donne pas autorisation de commit/sync.
Le skill Beads local reste prioritaire pour les procédures opérationnelles.
