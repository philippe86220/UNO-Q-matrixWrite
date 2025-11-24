# UNO Q – Éditeur de matrice de LEDs 13x8 (Python + Tkinter)

Ce dépôt contient un petit outil graphique écrit en Python (Tkinter)  
permettant de **dessiner des motifs sur une matrice 13x8**   
et de générer automatiquement les **4 mots de 32 bits** à transmettre à la fonction :

```c
extern "C" void matrixWrite(const uint32_t *buf);
```
sur l’Arduino UNO Q (cœur STM32).

# Fonctionnalités :

- Affichage d’une grille **13 colonnes × 8 lignes** représentant la matrice de LEDs de la UNO Q.
- Clic sur une “LED” pour l’allumer / l’éteindre (LEDs bleues lorsqu’elles sont actives).
- Bouton « **Générer les 4 mots** » :
  - calcule les 4 uint32_t correspondant à l’état de la matrice,
  - affiche un bloc de code C prêt à coller dans un sketch Arduino.
- Bouton « **Effacer** » : remet toutes les LEDs à 0.
- Bouton « **Copier** » : copie le bloc C généré dans le presse-papiers.

  ---
  
# Prérequis :
- Python 3 installé (3.8 ou plus, par exemple).
- Tkinter installé (inclus par défaut avec Python sur la plupart des systèmes) :
  - macOS : fourni avec Python officiel,
  - Windows : fourni avec l’installateur Python standard,
  - Linux : parfois besoin d’installer **python3-tk** via le gestionnaire de paquets.

# Lancer l’éditeur :

Dans un terminal, à la racine du projet :

```bash
python3 matrix.py
```




