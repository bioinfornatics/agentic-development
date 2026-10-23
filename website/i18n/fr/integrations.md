# Relier tâches, commits et sessions

Ces intégrations sont facultatives. Vérifiez leurs outils et permissions dans le
projet courant ; leur présence ne prouve ni leur activation ni leur compatibilité.

## Beads : retrouver le travail

Dans un projet utilisant Beads, consultez les instructions locales, la tâche, son responsable
et ses dépendances avant d'écrire. Vérifiez le résultat de sa prise en charge ;
une tâche attribuée n'est pas un verrou de fichier.

La tâche doit suffire à retrouver l'objectif, le périmètre, les critères, les entrées,
la vérification et le contexte de reprise. Conservez résultats et liens utiles dans le tracker.
Un parent exprime une hiérarchie ; une dépendance exprime un prérequis. Ne dupliquez pas
les statuts dans un autre carnet Markdown. Ne réinitialisez pas un espace existant.

## Git : enregistrer un changement explicable

Avant une action, vérifiez dépôt, branche, index et travail préexistant.
Annoncez la branche ou le commit proposés et leurs permissions. Une branche peut
couvrir plusieurs tâches liées ; une tâche peut produire plusieurs commits.

Avant un commit autorisé, inspectez les fichiers et les hunks exacts dans l'index.
Après succès, enregistrez le hash, le message et les chemins réellement commités, puis liez
le résultat à la tâche. Si le tracker ne peut pas être mis à jour, dites-le et
conservez le commit avec une action de reprise. Ne prétendez pas que la transmission
a été enregistrée. Ne poussez pas automatiquement.

## Sessions et Entire : transmettre le contexte

Gardez l'implémentation, les tests et les corrections liées dans la même session tant que
l'objectif reste clair. Recommandez une nouvelle session pour un objectif indépendant,
un autre dépôt, des hypothèses périmées ou un jugement nécessitant un contexte distinct.
Un commit ou une compaction seuls n'exigent pas une nouvelle session.

À une frontière de session, fournissez : objectif, tâche, candidat, fichiers à préserver,
preuves et limites, permissions à revalider, prochaine action et prompt autonome.
Proposez un nom et un objectif pour la prochaine session ; indiquez si elle a
réellement été lancée. Une transmission n'accorde aucune nouvelle permission.

Entire capture facultativement le contexte ; ce n'est ni le tracker ni le juge.
Vérifiez sa configuration et son intégration avec l'agent. Ne signalez que les sessions
et checkpoints réellement observés ; s'il est indisponible, expliquez pourquoi.
N'inventez pas un lien avec un commit et n'ajoutez pas de faux trailer.

## Intégration à l'hôte : périmètre distinct

Le [cœur de phases portable](../../../plugins/agentic-development/README.md) est distinct
du harness existant, facultatif et expérimental, ainsi que des hooks de l'hôte. Leur présence
ne prouve ni activation, ni compatibilité, ni acceptation d'une release. Ce changement
documentaire n'installe ni ne modifie les composants d'exécution. Inspectez les
[frontières d'intégration](../../../docs/convergence/host-boundary-and-bridge.md)
avant de demander l'activation du runtime. La documentation ne fournit ni acceptation
indépendante ni lanceur automatique de sessions.
