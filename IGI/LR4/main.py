from fourth_task import *

if __name__ == "__main__":
    side_length = float(input("Введите длину стороны ромба: "))
    while True:
        angle = float(input("Введите угол ромба в градусах: "))
        if 0 < angle < 180:
            break
    color = input("Введите цвет ромба: ")

    rhombus = Rhombus(side_length, angle, color)
    print(rhombus.get_info())
    rhombus.draw()
    plt.title(rhombus.name)
    plt.show()
    plt.savefig("data/rhombus.png")
    