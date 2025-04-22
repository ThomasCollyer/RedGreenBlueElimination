import tkinter as tk
import random

class Agent:
    def __init__(self,canvas,entity_type,x,y):
        self.canvas = canvas
        self.entity_type = entity_type
        #self.entity_type = entity_options[random.randint(0,len(entity_options)-1)]
        self.x = 100+random.randint(0,250)
        self.y = 100+random.randint(0,250)
        self.size = 30
        self.rect = canvas.create_rectangle( (self.x,self.y,self.x+self.size,self.y+self.size),
                                             fill=self.entity_type)


    def agent_move(self):
        dx = random.randint(-5,5)
        dy = random.randint(-5,5)
        self.canvas.move(self.rect, dx, dy) 

        self.x += dx
        self.y += dy

    def update_entity_type(self,new_entity_type):
        self.entity_type == new_entity_type
        self.canvas.itemconfig(self.rect, fill=new_entity_type)

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=700, height=700, bg="white")
        self.canvas.pack()

        self.entity_options = ['red','green','blue']
        self.entity_id_list = []

        self.play_pause_btn = tk.Button(root, text="Press me", command=self.create_agent)
        self.play_pause_btn.pack()

        self.move_btn = tk.Button(root, text="Move", command=self.move_agents)
        self.move_btn.pack()

        self.collide_btn = tk.Button(root, text="Collision Detection", command=self.agent_conversion)
        self.collide_btn.pack()

    def create_agent(self):
        self.entity_id_list.append(Agent(self.canvas,self.entity_options[random.randint(0,len(self.entity_options)-1)],1,1))

    def activate_movement(self):
        for agent in self.entity_id_list:
            agent.agent_move()

    def agent_conversion(self):
        #Check if any two agents are touching. If they are change their 'team' in the following way:
        #If Red and Green collide, then change the Green agent to be Red
        #If Green and Blue collide, then change the Blue agent to be Green
        #If Blue and Red collide, then change the Blue agent to be Green
        self.new_colours = []

        for agent in self.entity_id_list:
            for incident_agent in self.entity_id_list:
                if agent == incident_agent:
                    #Do nothing
                    pass
                else:
                    x1,y1,x2,y2 = agent.canvas.bbox(agent.rect)
                    a1,b1,a2,b2 = incident_agent.canvas.bbox(incident_agent.rect)

                    #We then check if the bouding boxes overlap at all
                    #This will return true or false
                    if (x1 < a2 and x2 > a1 and
                    y1 < b2 and y2 > b1):
                        if ((agent.entity_type == 'red') and (incident_agent.entity_type == 'green')) or ((agent.entity_type == 'green') and (incident_agent.entity_type == 'red')):
                            agent.update_entity_type('red')
                            incident_agent.update_entity_type('red')
                        elif ((agent.entity_type == 'green') and (incident_agent.entity_type == 'blue')) or ((agent.entity_type == 'blue') and (incident_agent.entity_type == 'green')):
                            agent.update_entity_type('green')
                            incident_agent.update_entity_type('green')
                        elif ((agent.entity_type == 'blue') and (incident_agent.entity_type == 'red')) or ((agent.entity_type == 'red') and (incident_agent.entity_type == 'blue')):
                            agent.update_entity_type('blue')
                            incident_agent.update_entity_type('blue')

    def move_agents(self):
        for agent in self.entity_id_list:
            agent.agent_move()

        self.agent_conversion()
        
        # Call this function again after 100ms
        self.root.after(200, self.move_agents)

root = tk.Tk()
game = Game(root)
root.mainloop()
