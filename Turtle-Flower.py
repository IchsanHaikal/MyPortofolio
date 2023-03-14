import turtle
t = turtle.Turtle()
for i in range (180) :
  t.speed(0)
  t.color('#cca9dd')
  t.circle(190 - i, 90)
  t.left(90)
  t.color('#ab71c7')
  t.circle(190 - i, 90)
  t.left(18)