# Bien démarrer

## 1. Décrire le résultat, pas une liste de fichiers

Indiquez l'utilisateur concerné, le comportement attendu et le problème actuel.
Précisez ce qui est exclu et ce que l'agent peut réellement exécuter.

> Corrige l'arrêt d'un flux : quand l'utilisateur clique sur Stop, le transport
> actif doit être annulé exactement une fois. Ne change pas l'interface ni le stockage.
> Tu peux modifier le code et les tests locaux ; ne pousse et ne déploie rien.

Chargez **agentic-development:drive-cycle** pour guider le parcours. Pour une seule phase,
chargez le skill correspondant via le mécanisme de votre outil :

| Intention | Skill à charger | Résultat attendu |
|---|---|---|
| Explorer un besoin ou un risque | agentic-development:research-slice | Constats sourcés et décision à préparer |
| Structurer une roadmap, une US ou des tickets | agentic-development:plan-slice | Plan et tâches prêts ; écritures dans le tracker autorisées et vérifiées |
| Réaliser un plan autorisé | agentic-development:implement-slice | Changement borné et vérifications locales |
| Vérifier un candidat | agentic-development:test-slice | Résultats reproductibles et limites |
| Juger les preuves et le candidat | agentic-development:judge-slice | Verdict sur le périmètre exact |
| Corriger des constats | agentic-development:iterate-slice | Action corrective bornée ou prérequis précis |

Exemple : « Charge agentic-development:plan-slice pour créer une roadmap et les tâches
prioritaires à partir de ce besoin. Tu peux créer des tickets dans le tracker du projet,
mais pas modifier le code. » Ces identifiants ne sont pas des commandes shell.

## 2. Faire clarifier les critères avant de coder

Exigez des **Goals / Non-goals** explicites et des critères observables :

- **Given** : un flux est actif.
- **When** : l'utilisateur demande son arrêt.
- **Then** : le transport est annulé une fois, sans nouveau message.

Ajoutez les erreurs et limites pertinentes : arrêt répété, absence de flux, échec réseau.
Pour une contrainte de performance, précisez la métrique, le seuil approuvé, l'unité,
la charge, la durée, l'environnement et la méthode de mesure. Sans seuil approuvé,
le critère reste à résoudre ; l'agent n'invente pas un chiffre pour fabriquer un succès.

Une recherche ou un changement documentaire utilise plutôt un livrable vérifiable :
ne forcez pas un scénario utilisateur artificiel.

## 3. Vérifier le plan proposé

Contrôlez le périmètre, les fichiers possédés ou préservés, les tests envisagés,
les dépendances et les permissions. Résolvez les décisions bloquantes.
Un plan déjà couvert par votre demande n'exige pas une approbation rituelle.

## 4. Demander un bilan exploitable

Le bilan doit séparer résultat, changements, preuves et jugement. Il indique
les commandes réellement exécutées, les fichiers modifiés, les actions Git réalisées
ou seulement proposées, et la prochaine étape.

Si l'agent est bloqué, demandez le prérequis et un point de reprise précis,
pas une acceptation simulée. Un test local ne prouve pas le comportement en production.

Suite : [piloter le cycle](cycle.md) ou [préparer les intégrations](integrations.md).
