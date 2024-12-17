import pygame
import sys
import random

pygame.init()

# Dimensions de la fenêtre
Width, Height = 1920, 1080
fenêtre = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("SNAKE !!!")

# Couleurs
Noir = (0, 0, 0)
Blanc = (255, 255, 255)
Vert_foncé = (0, 100, 0)
Jaune = (255, 255, 0)
Rouge = (255, 0, 0)
Bleu = (0, 0, 255)

# Taille des blocs
taille_block = 20

# Vitesse du jeu
Clock = pygame.time.Clock()
FPS = 15

# Initialisation du jeu
Serpent_position = [[Width // 2, Height // 2]]
Serpent_direction = (0, 0)
Nourriture_pos = [0, 0]
direction_precedente = (0, 0)
message = ""
durée_message = 0
etat = "menu"
score = 0
collision_active = True
dernière_touche = None
dernier_deplacement = None
shift_appuyé = False

# Font pour le texte
font = pygame.font.SysFont("Arial", 24)

# Générer une position aléatoire pour la nourriture
def générer_nourriture():
    """Génère une position aléatoire pour la nourriture en évitant les bords."""
    return [
        random.randrange(taille_block, Width - taille_block, taille_block),
        random.randrange(taille_block, Height - taille_block, taille_block),
    ]

# Initialisation de la nourriture
Nourriture_pos = générer_nourriture()

def ecrire_texte(text, font, color, surface, x, y):
    """Affiche du texte sur l'écran."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def bouton(text, x, y, w, h, color, action=None):
    """Crée un bouton cliquable."""
    pygame.draw.rect(fenêtre, color, (x, y, w, h))
    ecrire_texte(text, font, Blanc, fenêtre, x + 10, y + 10)
    souris = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < souris[0] < x + w and y < souris[1] < y + h:
        if click[0] == 1 and action:
            pygame.time.wait(200)
            action()

def quitter():
    """Quitte le jeu."""
    pygame.quit()
    sys.exit()

def changer_etat(nouvel_etat):
    """Change l'état du jeu."""
    global etat
    etat = nouvel_etat

def reset_game():
    """Réinitialise le jeu."""
    global Serpent_position, Serpent_direction, Nourriture_pos,score,collision_active,dernier_deplacement
    Serpent_position = [[Width // 2, Height // 2]]
    Serpent_direction = (0, 0)
    Nourriture_pos = générer_nourriture()
    score = 0
    collision_active = True
    dernier_deplacement = None
    
    
def draw_borders():
    """Dessine les bords de l'écran."""
    pygame.draw.rect(fenêtre, Noir, pygame.Rect(0, 0, Width, taille_block)) #Bord haut
    pygame.draw.rect(fenêtre, Noir, pygame.Rect(0, 0, taille_block, Height)) #Bord gauche
    pygame.draw.rect(fenêtre, Noir, pygame.Rect(0, Height - taille_block, Width, taille_block)) #Bord bas
    pygame.draw.rect(fenêtre, Noir, pygame.Rect(Width - taille_block, 0, taille_block, Height)) #Bord droit

def draw_snake():
    """Dessine le serpent."""
    for pos in Serpent_position:
        pygame.draw.rect(fenêtre, Jaune, pygame.Rect(pos[0], pos[1], taille_block, taille_block))



def directions_opposés(touche1,touche2):
    paires_opposées = [(pygame.K_z, pygame.K_s),(pygame.K_s,pygame.K_z),(pygame.K_d,pygame.K_q),(pygame.K_q,pygame.K_d)]
    return (touche1,touche2) in paires_opposées



def vérifier_collisions_bords(tête):
    if(tête[0] < 0 or tête[0] >= Width or tête[1] < 0 or tête[1] >= Height):
        return True
    return False
    
    
def commencer_jeu():
    reset_game()
    changer_etat("jeu")    
    
    
    
def changer_vitesse():
    """Change la vitesse du jeu cycliquement entre 15, 50, et 100 FPS."""
    global FPS, message, durée_message
    if FPS == 15:
        FPS = 50
        message = "Rapide"
    elif FPS == 50:
        FPS = 100
        message = "Très rapide"
    else:
        FPS = 15
        message = "Lent"
    durée_message = 100

def menu():
    """Affiche le menu principal."""
    global score
    while etat == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter()

        fenêtre.fill(Noir)
        ecrire_texte("Snake !!!", font, Jaune, fenêtre, Width // 2 - 100, Height // 4)
        ecrire_texte(f"Score :  {score}",font,Bleu,fenêtre,10,10)
        bouton("Jouer", Width // 4, Height // 2, 80, 50, Bleu, lambda: commencer_jeu())
        bouton("Quitter", Width // 2 + 100, Height // 2, 80, 50, Rouge, quitter)
        pygame.display.update()
        Clock.tick(15)


def main():
    #Boucle principale du jeu.
    global direction_precedente, score, Serpent_direction, Nourriture_pos,message,durée_message,demi_tour_effectue,collision_active,dernier_deplacement,FPS

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter()

            if etat == "jeu" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    changer_etat("menu")
                    
                    
                if dernier_deplacement and directions_opposés(dernier_deplacement,event.key):
                    collision_active = False
                else:
                    collision_active = True
                
                if event.key == pygame.K_z:
                    Serpent_direction = (0, -taille_block)
                    dernier_deplacement = pygame.K_z
                elif event.key == pygame.K_s:
                    Serpent_direction = (0, taille_block)
                    dernier_deplacement = pygame.K_s
                elif event.key == pygame.K_q:
                    Serpent_direction = (-taille_block, 0)
                    dernier_deplacement = pygame.K_q
                elif event.key == pygame.K_d:
                    Serpent_direction = (taille_block, 0)
                    dernier_deplacement = pygame.K_d
                elif event.key == pygame.K_LSHIFT:
                    changer_vitesse()
                    shift_appuyé = True
                else:
                    message = "Ce n'est pas une touche valide !"
                    durée_message = 10


            elif event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
                shift_appuyé = False  

        if etat == "jeu" and Serpent_position:
            # Mise à jour de la position du serpent
            if Serpent_direction != (0, 0):
                nouvelle_tête = [
                    Serpent_position[0][0] + Serpent_direction[0],
                    Serpent_position[0][1] + Serpent_direction[1],
                ]
                Serpent_position.insert(0, nouvelle_tête)
                
                if vérifier_collisions_bords(nouvelle_tête) or (collision_active and nouvelle_tête in Serpent_position[1:]):
                    changer_etat("menu")
                

                # Vérifier si le serpent mange la nourriture
                if nouvelle_tête == Nourriture_pos:
                    Nourriture_pos = générer_nourriture()
                    score += 1
                else:
                    Serpent_position.pop()

                
                if collision_active and nouvelle_tête in Serpent_position[1:]:
                    changer_etat("menu")
                    reset_game()
                
                
                
            fenêtre.fill(Vert_foncé)
            draw_borders()
            draw_snake()
            pygame.draw.rect(fenêtre, Rouge, pygame.Rect(Nourriture_pos[0], Nourriture_pos[1], taille_block, taille_block))
            ecrire_texte(f"Score : {score}", font, Blanc, fenêtre, 10, 10)
            
            if durée_message > 1:
                ecrire_texte(f"{message}", font,Rouge,fenêtre,10,35)
                durée_message -= 1
            pygame.display.update()
            Clock.tick(FPS)

        elif etat == "menu":
            menu()
            
if __name__ == '__main__':
    main()