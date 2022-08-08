import math
import TwoBodyView

gravity_force = 6.673 * (10**(-11))

class TwoBodyModel:

    def __init__(self, mass_1, mass_2):
        self.mass_1 = mass_1
        self.mass_2 = mass_2
        self.m12 = mass_1 + mass_2
        self.u = [1, 0, 0, 0]
        self.dimensions = [[0, 0], [0, 0]]


class TwoBodyController:

    def __init__(self, mass_1, mass_2, eccentricity = 0.7):
        self.new_model = TwoBodyModel(mass_1, mass_2)
        self.new_model.u[3] = eccentricity
        self.q = mass_1/mass_2

    def derivative(self):
        du = [0, 0, 0, 0]
        cordinate = self.new_model.u[0], self.new_model.u[1]
        distance = math.sqrt(math.pow(cordinate[0], 2) + math.pow(cordinate[1], 2))

        for i in range(2):
            du[i] = self.new_model.u[i + 2]
            du[i + 2] = -(1 + self.q) * cordinate[i] / (math.pow(distance, 3))
        return du

    def update_position(self):
        time_step = 0.001
        self.runge_kutta(time_step)
        self.calculate_new_position()

    def runge_kutta(self, h):
        a = [h/2, h/2, h, 0]
        b = [h/6, h/3, h/3, h/6]
        u_0 = []
        u_t = []
        for i in range(len(self.new_model.u)):
            u_0.append(self.new_model.u[i])
            u_t.append(0)

        for i in range(4):
            du = self.derivative()
            for j in range(len(self.new_model.u)):
                self.new_model.u[j] = u_0[j] + (a[i]*du[j])
                u_t[j] = u_t[j] + (b[i]*du[j])
        for i in range(len(self.new_model.u)):
            self.new_model.u[i] = u_0[i] + u_t[i]

    def write_to_file(self):
        string = "f% f% f%\n"%(self.u[0], self.u[1], self.u[2], self.u[3])
        with open("data.txt", "a", encoding = "utf-8") as file:
            file.write(string)

    def calculate_new_position(self):
        r = 1
        a1 = (self.new_model.mass_2 / self.new_model.m12) * r
        a2 = (self.new_model.mass_1 / self.new_model.m12) * r

        self.new_model.dimensions[0][0] = -a2 * self.new_model.u[0]
        self.new_model.dimensions[0][1] = -a2 * self.new_model.u[1]
        self.new_model.dimensions[1][0] = a1 * self.new_model.u[0]
        self.new_model.dimensions[1][1] = a1 * self.new_model.u[1]

def get_data(file_name):
    data_list = list()
    with open(file_name, "r", encoding = "utf-8") as file:
        reader = file.readlines()
        index = 0
        for i in reader:
            reader[index] = i.rstrip().split(" ")
            data_list.append(reader[index])
    return data_list

def get_input_from_console():
    mass_ratio = 0.0
    fisrt_body_cord = 0
    eccentricity = 0
    while True:
        mass_ratio = float(input("Mass ratio:\n"))
        if 0 < mass_ratio <= 1:
            break
        else:
            print("Give a number between (0, 1]")

    while True:
        first_body_cord = int(input("Please give a number between 200-400:\n"))
        if(200 <= first_body_cord <= 400):
            break

    while True:
        eccentricity = int(input("Please give an eccentricity between mass (50-150):\n"))
        if(50 <= eccentricity <= 150):
            break
    return first_body_cord, eccentricity, mass_ratio


inputs = get_input_from_console()
with open("data.txt", "w", encoding="utf-8") as file:
    control = TwoBodyController(1, inputs[2])
    control.positions = [inputs[0], 250, inputs[0] + inputs[1], 200]
    step = 0
    while step < 100000:
        control.update_position()
        current_data = control.new_model.dimensions
        #print(control.new_model.dimensions, "dimension")
        #print(control.positions, "position")
        string = str(current_data[0][0]) + " " + str(current_data[0][1]) + " " + str(current_data[1][0]) + " " + str(current_data[1][1]) + "\n"
        file.write(string)
        step += 1
model = TwoBodyModel(control.new_model.mass_1, control.new_model.mass_2)
two_body = TwoBodyView.TwoBodyView(inputs[0], 350, inputs[0] + inputs[1], 300, int(15 * inputs[2]), 15)
data = get_data("data.txt")
two_body.circulation(data)


