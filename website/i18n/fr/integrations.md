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

## Hooks Goose : observer les événements

Les hooks exécutent des scripts locaux. Relisez la documentation Goose et testez
la version réellement utilisée, sans déduire sa compatibilité du standard.
Le plugin regroupe ses règles dans **hooks/hooks.json** et leur handler dans
**scripts/observe.py**, avec ses Skills. Aucun adaptateur ni second manifeste.
L'observateur ne modifie ni Git, ni Beads, ni Entire. Il observe les événements et
la structure des bilans sans juger leur contenu. Le source n'est pas une installation.
Avant activation, examinez scripts, dépendances, confidentialité et configuration ;
consultez le [guide des hooks](../../../hooks/README.md).

Ne confondez pas un hook d'observation avec une protection de sécurité, une
acceptation indépendante ou un lanceur automatique de sessions.

Référence : [documentation officielle Goose des hooks](https://goose-docs.ai/docs/guides/context-engineering/hooks).

## Évaluer un commit après la clôture d'une tâche

Après chaque clôture Beads nouvellement confirmée, évaluez les changements source associés.
Choisissez perform si un diff cohérent vérifié et une autorisation de commit existent ;
propose si l'autorisation manque ; skip si le travail est déjà committé ou sans diff source ;
blocked si la propriété, les vérifications ou une capacité empêchent un commit sûr.
Consignez la raison dans l'explication finale et un hash réel uniquement après succès.
La clôture n'autorise pas le commit ; aucun push automatique ni synchronisation Dolt ne suit.
