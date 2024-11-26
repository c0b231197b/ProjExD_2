import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def check_bound(rct:pg.Rect) -> tuple[bool,bool]:
    """
    引数で与えられたrectが画面の外か中かを判定
    引数:こうかとんRect爆弾
    戻り値:真理値タプル(横、縦)/画面内Ture,画面外False
    """
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20)) #爆弾用の空のSuraface
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0, 0, 0))#赤に染める
    bb_rct = bb_img.get_rect()#爆弾Rectの抽出
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx = 5
    vy = 5 # 爆弾速度ベクトル
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        # こうかとんが画面外なら、元の位置にももどす
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy) #爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:#横にはみでる
            vx *= -1
        if not tate:#縦にはみ出る
            vy *= -1
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
