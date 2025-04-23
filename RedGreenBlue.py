import tkinter as tk
import random
import time

class Agent:
    def __init__(self,canvas,entity_type,x,y,size):
        self.canvas = canvas
        self.entity_type = entity_type
        #self.entity_type = entity_options[random.randint(0,len(entity_options)-1)]
        self.x = x#100+random.randint(0,250)
        self.y = y#100+random.randint(0,250)
        self.size = size
        self.rect = canvas.create_rectangle( (self.x,self.y,self.x+self.size,self.y+self.size),
                                             fill=self.entity_type)

        self.dx = random.choice([-1,1])
        self.dy = random.choice([-1,1])

    def agent_move(self):
        next_x = self.x + self.dx
        next_y = self.x + self.dy

        #Keep the agent within the canvas bounds
        #Gives us the coordinates of the agent
        x1, y1, x2, y2 = self.canvas.coords(self.rect)

        #Check if the next move would force the agent 'off-screen', if so, reverse it's direction
        if x1 + self.dx < 0 or x2 + self.dx > self.canvas.winfo_width():
            self.dx *= -1
        if y1 + self.dy < 0 or y2 + self.dy > self.canvas.winfo_height():
            self.dy *= -1

        self.canvas.move(self.rect, self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy

    def update_entity_type(self,new_entity_type):
        self.entity_type == new_entity_type
        self.canvas.itemconfig(self.rect, fill=new_entity_type)

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas_width = 700
        self.canvas_height = 700
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.entity_options = ['red','green','blue']
        self.entity_id_list = []

        self.play_pause_btn = tk.Button(root, text="Press me", command=self.create_agent)
        self.play_pause_btn.pack()

        self.move_btn = tk.Button(root, text="Move", command=self.move_agents)
        self.move_btn.pack()

        self.collide_btn = tk.Button(root, text="Collision Detection", command=self.agent_conversion)
        self.collide_btn.pack()

        self.agent_size = 100

    def create_agent(self):
        found_location_flag = False
        overlap_tries_limit = 0
        if not self.entity_id_list:
            x1,y1 = 1,1
            self.entity_id_list.append(Agent(self.canvas,self.entity_options[random.randint(0,len(self.entity_options)-1)],x1,y1,self.agent_size))
        else:
            while found_location_flag != True:
                if overlap_tries_limit >=1000:
                    print("Not enough space left")
                    break
                
                current_x = random.randint(1,self.canvas_width-self.agent_size)
                current_y = random.randint(1,self.canvas_height - self.agent_size)
                print(current_x, current_y)

                #Draw a square to see if it will fit
                self.test_rect = self.canvas.create_rectangle( (current_x,
                                                      current_y,
                                                      current_x+self.agent_size,
                                                      current_y+self.agent_size),
                            fill='yellow')

                for agent in self.entity_id_list:
                    x1,y1,x2,y2 = agent.canvas.bbox(agent.rect)
                    a1,b1,a2,b2 = self.canvas.bbox(self.test_rect)

                    #We then check if the bouding boxes overlap at all
                    #This will return true or false
                    if x1 < a2 and x2 > a1 and y1 < b2 and y2 > b1:
                        self.canvas.delete(self.test_rect)
                        overlap_tries_limit +=1
                        break
                    else:
                        if agent == self.entity_id_list[-1]:
                            found_location_flag = True
                            x1 = current_x
                            y1 = current_y
                            self.canvas.delete(self.test_rect)
                            self.entity_id_list.append(Agent(self.canvas,self.entity_options[random.randint(0,len(self.entity_options)-1)],x1,y1,self.agent_size))
                            break
        

    def activate_movement(self):
        for agent in self.entity_id_list:
            agent.agent_move()

    def handle_collision(self,agent,other_agent):
        x1, y1, x2, y2 = agent.canvas.bbox(agent.rect)
        a1, b1, a2, b2 = other_agent.canvas.bbox(other_agent.rect)

        if x1 < a2 and x2 > a1 and y1 < b2 and y2 > b1:
            # Simple bounce: reverse both agents
            agent.dx *= -1
            agent.dy *= -1
            other_agent.dx *= -1
            other_agent.dy *= -1

    def collision_fixer(self):
        for agent in self.entity_id_list:
            for incident_agent in self.entity_id_list:
                if agent!=incident_agent:
                    #Check if they are already colliding
                    x1,y1,x2,y2 = agent.canvas.bbox(agent.rect)
                    a1,b1,a2,b2 = incident_agent.canvas.bbox(incident_agent.rect)

                    #We then check if the bouding boxes overlap at all
                    #This will return true or false
                    if x1 < a2 and x2 > a1 and y1 < b2 and y2 > b1:
                        #print(True)
                        agent.dx *= -1
                        agent.dy *= -1
                        incident_agent.dx *= -1
                        incident_agent.dy *= -1
                        return (
                        x1 < a2 and x2 > a1 and
                        y1 < b2 and y2 > b1
                    )
                else:
                    pass
                    #else:
                     #   print(False)

    
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

##                        x1, y1, x2, y2 = agent.canvas.bbox(agent.rect)
##                        a1, b1, a2, b2 = incident_agent.canvas.bbox(incident_agent.rect)
##
##                        if x1 < a2 and x2 > a1 and y1 < b2 and y2 > b1:
##                            # Simple bounce: reverse both agents
##                            agent.dx *= -1
##                            agent.dy *= -1
##                            incident_agent.dx *= -1
##                            incident_agent.dy *= -1


    def move_agents(self):
        for agent in self.entity_id_list:
            self.collision_fixer()
            agent.agent_move()
            #self.collision_fixer()
        #self.collision_fixer()

        
        # Call this function again after 100ms
        self.root.after(10, self.move_agents)

root = tk.Tk()

###########################################
###########################################
###########################################
#Squares now get made correctly
#Issue seems to be getting them to collide correctly with each other
#Need to investigate why the first 2 squares will collide but the rest won't



game = Game(root)
root.mainloop()
