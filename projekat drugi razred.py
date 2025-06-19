import pygame
import random
import sys

pygame.init()

font = pygame.font.SysFont(None, 48)
Sirina, Visina = 1000, 800
Slika = pygame.display.set_mode((Sirina, Visina))
pygame.display.set_caption("Breakout")

sat = pygame.time.Clock()
fps = 60
splatforma, vplatforma = 100, 15
plopta = 10
redkocka, kolkocka = 5, 10
sirkocka = Sirina // kolkocka
viskocka = 30

pozadina = pygame.image.load("pozadina.jpg").convert()
pozadina = pygame.transform.scale(pozadina, (Sirina, Visina))

while True:
    platforma = pygame.Rect(Sirina//2 - splatforma//2, Visina - 40, splatforma, vplatforma) #dimenzije platforme
    lopta = pygame.Rect(Sirina//2, Visina//2, plopta*2, plopta*2) #dimenzije lopte
    loptax, loptay = 5.0, -5.0 #pocetna brzina lopte
    maksbrzina = 12 #maksimalna brzina lopte
    loptax = max(-maksbrzina, min(loptax, maksbrzina))
    loptay = max(-maksbrzina, min(loptay, maksbrzina))
    zivoti = 3
    kocke = []
    for red in range(redkocka):
        for kol in range(kolkocka):
            kocka = pygame.Rect(kol * sirkocka + 5, red*viskocka + 5, sirkocka - 10, viskocka - 10) #stavljanje svake kocke u niz
            kocke.append(kocka)
    pokrece_se = True
    kraj = False
    pobeda = False
    #glavna petlja
    while pokrece_se:
        sat.tick(fps)
        Slika.blit(pozadina, (0, 0))

        kontrole = pygame.key.get_pressed()
        if kontrole[pygame.K_LEFT] and platforma.left > 0:
            platforma.x = platforma.x - 7
        if kontrole[pygame.K_RIGHT] and platforma.right < Sirina:
            platforma.x = platforma.x + 7

        lopta.x = lopta.x + loptax
        lopta.y = lopta.y + loptay

        if lopta.left <= 0 or lopta.right >= Sirina:
            loptax = loptax * -1
        if lopta.top <= 0:
            loptay = loptay * -1
        if lopta.bottom >= Visina:
            zivoti = zivoti - 1
            pygame.time.delay(1000)
            lopta.x, lopta.y = Sirina // 2, Visina // 2
            loptax = random.choice([-5.0, 5.0])
            loptay = -5
        if zivoti < 0:
            kraj = True
            pokrece_se = False

        if lopta.colliderect(platforma):
                loptay = loptay * -1
                loptax = loptax * 1.05
                loptay = loptay * 1.05

        hindex = lopta.collidelist(kocke)
        if hindex != -1:
            del kocke[hindex]
            loptay = loptay * -1
            loptax = loptax * 1.02
            loptay = loptay * 1.02

        pygame.draw.rect(Slika, "Blue", platforma)
        pygame.draw.ellipse(Slika, "White", lopta)
        for kocka in kocke:
            pygame.draw.rect(Slika, "Green", kocka)

        zivotitekst = font.render(f"Zivoti: {zivoti}", True, "White")
        Slika.blit(zivotitekst, (10, 10))

        if not kocke:
            pobeda = True
            pokrece_se = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pokrece_se = False

        pygame.display.flip()

    Slika.fill("Black")
    if pobeda:
        tekst = font.render("Pobedio si! Pritisni R da igras ponovo.", True, "White")
    elif kraj:
        tekst = font.render("Izgubio si! Pritisni R da igras ponovo.", True, "White")
    else:
        tekst = font.render("Kraj igre.", True, "White")
    
    Slika.blit(tekst, (Sirina//2 - tekst.get_width()//2, Visina//2))
    pygame.display.flip()

    ceka_restart = True
    while ceka_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    ceka_restart = False
        
