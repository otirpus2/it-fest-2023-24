import pygame
import random
import sys

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 473, 736
BACKGROUND_COLOR = (255, 255, 255)
FONT_COLOR = (0, 0, 0)
FONT_SIZE = 30
TIME_LIMIT = 60  # Time limit in seconds

ROAD_WIDTH = 200
ROAD_COLOR = (100, 100, 100)
# Car settings
CAR_WIDTH, CAR_HEIGHT = 100, 100
CAR_COLOR = (255, 0, 0)
CAR_SPEED = 25  # Update car speed to 25

# Math problem settings
OPERATORS = ["+", "-", "*"]
MAX_NUMBER = 10
NUM_CHOICES = 4

# Level settings
NUM_LEVELS = 5
BASE_TIME_LIMIT = 120 # Base time limit for each level in seconds

# Load car and background images
CAR_IMAGE = pygame.image.load("car.png")
BACKGROUND_IMAGE = pygame.image.load("background.jpg")
BACKGROUND_IMAGE = pygame.transform.rotate(BACKGROUND_IMAGE, 90)
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE,(WIDTH,HEIGHT))


# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Racing game(Multiply)")

# Helper function to generate MCQ math problems
def generate_math_problem():
    num1 = random.randint(1, MAX_NUMBER)
    num2 = random.randint(1, MAX_NUMBER)
    operator = random.choice(OPERATORS)

    problem = f"{num1} {operator} {num2}"
    answer = eval(problem)

    # Generate multiple choices with one correct answer
    choices = [answer]
    while len(choices) < NUM_CHOICES:
        choice = random.randint(1, MAX_NUMBER * 2)
        if choice not in choices:
            choices.append(choice)

    random.shuffle(choices)

    return problem, choices, answer

# Helper function to display text on the screen
def display_text(text, x, y):
    font = pygame.font.Font(None, FONT_SIZE)
    text_surface = font.render(text, True, FONT_COLOR)
    window.blit(text_surface, (x, y))

# Main game loop
def main():
    clock = pygame.time.Clock()
    current_level = 1
    time_left = BASE_TIME_LIMIT * 1000

    road_y = HEIGHT - ROAD_WIDTH
    car_y = HEIGHT - CAR_HEIGHT
    car_speed = 0

    correct_answers = []
    incorrect_answers = 0
    all_correct_answers = []  # To store all correct answers from start to end of the game

    while current_level <= NUM_LEVELS:
        start_time = pygame.time.get_ticks()
        time_left = BASE_TIME_LIMIT * 1000

        problem, choices, correct_answer = generate_math_problem()
        selected_answer = None

        while time_left > 0:
            window.fill(BACKGROUND_COLOR)

            # Draw the background image
            window.blit(BACKGROUND_IMAGE, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if selected_answer is None:
                        if event.key == pygame.K_a:
                            selected_answer = choices[0]
                        elif event.key == pygame.K_b:
                            selected_answer = choices[1]
                        elif event.key == pygame.K_c:
                            selected_answer = choices[2]
                        elif event.key == pygame.K_d:
                            selected_answer = choices[3]

            # Calculate the time left
            current_time = pygame.time.get_ticks()
            time_left = max(0, BASE_TIME_LIMIT * 1000 - (current_time - start_time))

            # Draw the road on the screen
            pygame.draw.rect(window, ROAD_COLOR, (0, road_y, WIDTH, ROAD_WIDTH))

            # Draw the car on the screen
            window.blit(CAR_IMAGE, (WIDTH // 2 - CAR_WIDTH // 2, car_y))

            # Draw the math problem and MCQ choices on the screen
            display_text("Level: {}".format(current_level), 10, 10)
            display_text("Time left: {:.1f}".format(time_left / 1000), 10, 40)
            display_text("questions:{}".format(problem, WIDTH // 5 - FONT_SIZE * 2, HEIGHT // 5 - FONT_SIZE),10,70)

            if selected_answer is not None:
                display_text("Your choice: {}".format(selected_answer), 10, HEIGHT - 100)

            display_text("A: {}".format(choices[0]), 10, HEIGHT - 70)
            display_text("B: {}".format(choices[1]), 10, HEIGHT - 40)
            display_text("C: {}".format(choices[2]), 200, HEIGHT - 70)
            display_text("D: {}".format(choices[3]), 200, HEIGHT - 40)

            # Check if the selected answer is correct
            if selected_answer is not None:
                if selected_answer == correct_answer:
                    # Correct answer, move the car forward five steps
                    car_y -= CAR_SPEED * 5

                    # If the car reaches the end of the road, move to the next level
                    if car_y <= -CAR_HEIGHT:
                        car_y = HEIGHT - CAR_HEIGHT
                        current_level += 1
                        correct_answers.append(problem)

                    # Add the correct answer to the list of all correct answers
                    all_correct_answers.append(problem)

                    selected_answer = None
                    problem, choices, correct_answer = generate_math_problem()
                else:
                    # Incorrect answer, stop the car and display the number of correct answers
                    car_speed = 0
                    selected_answer = None
                    incorrect_answers += 1

                    # If the user gives 3 incorrect answers, end the game
                    if incorrect_answers >= 3:
                        pygame.time.wait(2000)  # Wait for 2 seconds
                        window.fill(BACKGROUND_COLOR)
                        display_text("Sorry, you lose", WIDTH // 2 - FONT_SIZE * 5, HEIGHT // 2 - FONT_SIZE)
                        pygame.display.update()
                        pygame.time.wait(2000)  # Wait for 2 seconds
                        pygame.quit()
                        sys.exit()

                    display_text("Incorrect! : {}".format(len(correct_answers)), WIDTH - FONT_SIZE * 15, 10)
                    pygame.display.update()
                    pygame.time.wait(2000)  # Wait for 2 seconds

            pygame.display.update()
            clock.tick(60)

    # Game over screen
    window.fill(BACKGROUND_COLOR)
    display_text("Congratulations! You completed all levels!", WIDTH // 2 - FONT_SIZE * 5, HEIGHT // 2 - FONT_SIZE)
    display_text("Correct Answers:", WIDTH // 2 - FONT_SIZE * 5, HEIGHT // 2)
    y_offset = 0
    for answer in all_correct_answers:
        y_offset += FONT_SIZE
        display_text(answer, WIDTH // 2 - FONT_SIZE * 5, HEIGHT // 2 + y_offset)

    display_text("Incorrect Answers: {}".format(incorrect_answers), WIDTH // 2 - FONT_SIZE * 4, HEIGHT // 2 + (len(all_correct_answers) + 1) * FONT_SIZE)
    pygame.display.update()
    pygame.time.wait(5000)  # Wait for 3 seconds before quitting the game
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
