import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

kivy.require('1.11.1')

class PongBall(Widget):
    velocity_x, velocity_y = NumericProperty(0), NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx , vy = ball.velocity
            offset = (ball.center_y-self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongGame(Widget):

    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    vel_int = Vector(4,0).rotate(randint(-45,45))
    def serve_ball(self, vel=vel_int):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        #bounce off vertical edges
        if self.ball.y < self.y or self.ball.top > self.height:
            self.ball.velocity_y *= -1

        #bounce off horizontal edges
        # if self.ball.x < self.x or self.ball.right > self.width:
        #     self.ball.velocity_x *= -1

        #score
        if self.ball.x < self.x:
            self.player2.score += 1
            self.ball.pos = self.center
            self.ball.velocity = self.vel_int
        if self.ball.right > self.width:
            self.player1.score += 1
            self.ball.pos = self.center
            self.ball.velocity = self.vel_int * -1

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width * 2 / 3:
            self.player2.center_y = touch.y


class Menu(Screen):
    pass


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game = PongGame()
        self.game.serve_ball()
        self.add_widget(self.game)
        Clock.schedule_interval(self.game.update, 1.0 / 60.0)


class PongApp(App):
    def build(self):
        self.load_kv('pong.kv')
        sm = ScreenManager()
        sm.add_widget(Menu(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm


if __name__ == '__main__':
    PongApp().run()

#IMPORTANTE!!!!!!!
#Fazer um programa para somar vetores baseado no paint em kivy.
#Entender pq não atualiza
