from Prisoners_Algorithm.Prisoner import Prisoner
import pygame
import os

pygame.font.init()  # init font
WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Prison Riddle")

prisoner_img = pygame.image.load(os.path.join("Resources","SP1_front.png")).convert_alpha()
box_img = pygame.image.load(os.path.join("Resources","chest_closed.png")).convert_alpha()
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("Resources", "Lunetic_Room.jpg")).convert_alpha(), (600, 900))
#bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("images","bird" + str(x) + ".png"))) for x in range(1,4)]
#base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","base.png")).convert_alpha())


def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def load_images_to_prisoner(prisoner,trgt_box,num_pr_display,num_pr_img):
    list_imgs=[pygame.image.load(os.path.join("Resources",f"SP1{num_pr_img}" + type_img + ".png")) for type_img in ('front,back,side')]
    prisoner=Prisoner(box=trgt_box,num_prisoner_display=num_pr_display,list_imgs=list_imgs)
    return prisoner

def draw_window(win,prisoner_img,box_img): #, birds, pipes, base, score, gen, pipe_ind
    """
    draws the windows for the main game loop
    :param win: pygame window surface
    :param bird: a Bird object
    :param pipes: List of pipes
    :param score: score of the game (int)
    :param gen: current generation
    :param pipe_ind: index of closest pipe
    :return: None
    """
    # if gen == 0:
    #     gen = 1
    win.blit(bg_img, (0,0))
    win.blit(box_img, (0, 0))
    win.blit(prisoner_img,(250,250))

    # for pipe in pipes:
    #     pipe.draw(win)
    #
    # base.draw(win)
    # for bird in birds:
    #     # draw lines from bird to pipe
    #     if DRAW_LINES:
    #         try:
    #             pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
    #             pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
    #         except:
    #             pass
    #     # draw bird
    #     bird.draw(win)
    #
    # # score
    # score_label = STAT_FONT.render("Score: " + str(score),True,(255,255,255))
    # win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))
    #
    # # generations
    # score_label = STAT_FONT.render("Number Prisoners: " + str(gen-1),True,(255,255,255))
    # win.blit(score_label, (10, 10))
    #
    # # alive
    # score_label = STAT_FONT.render("Prisoners Escaped: " + str(len(birds)),True,(255,255,255))
    # win.blit(score_label, (10, 50))

    pygame.display.update()


