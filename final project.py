import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x450")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"

        self.enemy_snake = EnemySnake(self.canvas, self)

        self.food = None
        self.generate_food()  # Generate initial food

        self.score = 0
        self.enemy_score = 0

        self.score_label = tk.Label(self.master, text="Your Score: 0 | Enemy Score: 0", font=("Helvetica", 12), fg="white", bg="black")
        self.score_label.pack()

        self.timer_label = tk.Label(self.master, text="Time: 60", font=("Helvetica", 12), fg="white", bg="black")
        self.timer_label.pack()

        self.master.bind("<KeyPress>", self.change_direction)

        self.update_id = None  # To store the id of the scheduled update method
        self.game_over_scheduled = False
        self.time_remaining = 60

        self.update()

    def create_food(self):
        x = random.randint(0, 19) * 20
        y = random.randint(0, 19) * 20
        food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red", tags="food")
        return food

    def generate_food(self):
        if self.food is not None:
            self.canvas.delete(self.food)  # Delete the existing food
        self.food = self.create_food()  # Generate new food

    def move_snake(self):
        if not self.snake:
            return  # Skip the movement if the snake is empty

        head = self.snake[0]
        if self.direction == "Right":
            new_head = ((head[0] + 20) % 400, head[1])
        elif self.direction == "Left":
            new_head = ((head[0] - 20) % 400, head[1])
        elif self.direction == "Up":
            new_head = (head[0], (head[1] - 20) % 400)
        elif self.direction == "Down":
            new_head = (head[0], (head[1] + 20) % 400)

        self.snake.insert(0, new_head)

        # Check for collision with food
        food_coords = self.canvas.coords(self.food)
        if int(head[0]) == food_coords[0] and int(head[1]) == food_coords[1]:
            self.score += 1
            self.update_score()

            # Increase the length of the player snake
            for _ in range(3):
                self.snake.append((0, 0))  # Placeholder values, will be updated in the next iteration

            # Generate new food immediately
            self.generate_food()

        # Trim the tail to keep the snake's length constant
        if len(self.snake) > self.score+3:
            self.snake.pop()

    def update(self):
        if not self.snake or self.time_remaining <= 0:
            self.game_over()
            return  # Skip the update if the snake is empty or time is up

        self.move_snake()
        self.enemy_snake.move()

        head = self.snake[0]

        self.canvas.delete("snake", "enemy_snake")

        # Draw the snake
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tags="snake")

        # Draw the enemy snake
        for segment in self.enemy_snake.get_body():
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="blue", tags="enemy_snake")

        # Check for collision with food
        food_coords = self.canvas.coords(self.food)
        if int(head[0]) == food_coords[0] and int(head[1]) == food_coords[1]:
            self.score += 1
            self.update_score()
            self.snake.append((0, 0))  # Placeholder values, will be updated in the next iteration

            # Generate new food immediately
            self.generate_food()


        # Check for collision with the player's own body
        if head in self.snake[1:]:
            self.game_over()

        # Cancel the previous scheduled update method
        if self.update_id is not None:
            self.master.after_cancel(self.update_id)

        # Schedule the update method for the next iteration
        self.update_id = self.master.after(200, self.update)

        # Update the timer
        self.time_remaining -= 0.2
        self.timer_label.config(text=f"Time: {int(self.time_remaining)}")

    def change_direction(self, event):
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"

    def update_score(self):
        self.score_label.config(text=f"Your Score: {self.score} | Enemy Score: {self.enemy_score}")

    def game_over(self):
        if not self.game_over_scheduled:
            self.game_over_scheduled = True

            result_text = ""
            if self.time_remaining <= 0:
                # Timer is up
                result_text = f"Time's up!\nYour Score: {self.score} | Enemy Score: {self.enemy_score}\n"
                if self.score > self.enemy_score:
                    result_text += "You won!"
                elif self.score < self.enemy_score:
                    result_text += "Enemy won!"
                else:
                    result_text += "It's a tie!"
            else:
                # Collision occurred
                possible_lines = [
                    "\n\n(UwU) <3",
                    "\n\n(T_T)",
                    "\n\n(o_o)",
                    "\n\nʕっ• ᴥ • ʔっ",
                    "\n\n(╯°□°）╯︵ ┻━┻"
                ]
                result_text = random.choice(possible_lines)
                self.canvas.create_text(200, 200, text="Game Over", font=("Helvetica", 16), fill="red", tags="game_over")

            self.canvas.create_text(200, 200, text=result_text, font=("Helvetica", 16), fill="white", tags="game_over")

            # Schedule the reset_game method after 5 seconds
            self.master.after(5000, self.reset_game)

    def reset_game(self):
        self.game_over_scheduled = False
        self.canvas.delete("game_over")  # Delete the game over screen
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.score = 0
        self.enemy_score = 0
        self.time_remaining = 60
        self.update_score()
        self.canvas.delete("snake", "food", "previous_food", "enemy_snake")
        self.generate_food()  # Generate initial food
        self.enemy_snake.reset()
        self.update()

    def get_food_coords(self):
        return self.canvas.coords(self.food)

    def get_body(self):
        return self.snake

class EnemySnake:
    def __init__(self, canvas, game):
        self.canvas = canvas
        self.game = game
        self.body = [(300, 300), (310, 300), (320, 300)]  # Initial position
        self.direction = "Left"  # Initial direction
        self.waiting_for_food = False  # Flag to indicate if the snake is waiting for food
        self.score = 0

    def move(self):
        head = self.body[0]

        # Find the direction to move towards the food
        food_coords = self.game.get_food_coords()
        direction_to_food = self.find_direction_to_food(head, food_coords)

        # Move in the chosen direction
        new_head = self.move_in_direction(head, direction_to_food)
        self.body.insert(0, new_head)

        # If the enemy snake has not eaten the food, trim the tail to keep the snake's length constant
        if not self.waiting_for_food and len(self.body) > self.score+4:
            self.body.pop()

        # Check if the enemy snake has eaten the food
        if int(new_head[0]) == int(food_coords[0]) and int(new_head[1]) == int(food_coords[1]):
            self.waiting_for_food = True
            self.score += 1
            self.body.append((0, 0))  # Placeholder values, will be updated in the next iteration

            # Update the enemy snake's score label immediately
            self.update_score_label()

            # Reset the flag after a brief delay
            self.canvas.after(1000, lambda: self.reset_waiting_for_food())

            # Generate new food immediately for the enemy snake
            self.game.generate_food()

        # If the enemy snake was waiting for food and has moved to the food position, reset the flag
        if self.waiting_for_food and int(new_head[0]) == int(food_coords[0]) and int(new_head[1]) == int(food_coords[1]):
            self.waiting_for_food = False

        # Update the enemy score
        self.game.enemy_score = self.score

        # If the enemy snake has not eaten the food, trim the tail to keep the snake's length constant
        if not self.waiting_for_food and len(self.body) > 3:
            self.body.pop()

    def find_direction_to_food(self, head, food_coords):
        dx = food_coords[0] - head[0]
        dy = food_coords[1] - head[1]

        # Determine the current direction of the enemy snake
        current_direction = self.direction

        if abs(dx) > abs(dy):
            if dx > 0:
                return "Right" if not current_direction == "Left" else "Left"
            elif dx < 0:
                return "Left" if not current_direction == "Right" else "Right"
        else:
            if dy > 0:
                return "Down" if not current_direction == "Up" else "Up"
            elif dy < 0:
                return "Up" if not current_direction == "Down" else "Down"

    def avoid_collisions(self, desired_direction):
        # Check if there is an obstacle in the desired direction and change direction if needed
        if self.is_collision_possible(desired_direction):
            possible_directions = ["Up", "Down", "Left", "Right"]
            possible_directions.remove(desired_direction)
            random.shuffle(possible_directions)

            for direction in possible_directions:
                if not self.is_collision_possible(direction):
                    self.direction = direction
                    break

    def is_collision_possible(self, direction):
        new_head = self.move_in_direction(self.body[0], direction)
        return new_head in self.game.get_body() or new_head in self.body

    def move_in_direction(self, position, direction):
        if direction == "Right":
            return ((position[0] + 20) % 400, position[1])
        elif direction == "Left":
            return ((position[0] - 20) % 400, position[1])
        elif direction == "Up":
            return (position[0], (position[1] - 20) % 400)
        elif direction == "Down":
            return (position[0], (position[1] + 20) % 400)

    def get_head(self):
        return self.body[0]

    def get_body(self):
        return self.body

    def reset_waiting_for_food(self):
        self.waiting_for_food = False

    def reset(self):
        self.body = [(300, 300), (310, 300), (320, 300)]  # Reset to initial position
        self.direction = "Left"  # Reset to initial direction
        self.waiting_for_food = False  # Reset the waiting flag
        self.score = 0

    def update_score_label(self):
        # Update the enemy score label
        self.game.score_label.config(text=f"Your Score: {self.game.score} | Enemy Score: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
