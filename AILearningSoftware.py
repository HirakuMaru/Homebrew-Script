import numpy as np
import random
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import torch

# Define the QLearningAgent class
class QLearningAgent:
    def __init__(self, state_space, action_space):
        self.state_space = state_space
        self.action_space = action_space
        self.q_table = np.zeros((state_space, action_space))

    def choose_action(self, state, epsilon):
        if random.random() < epsilon:
            return random.randint(0, self.action_space - 1)
        else:
            return np.argmax(self.q_table[state, :])

    def update_q_table(self, state, action, reward, next_state, learning_rate, discount_factor):
        current_q = self.q_table[state, action]
        max_next_q = np.max(self.q_table[next_state, :])
        updated_q = current_q + learning_rate * (reward + discount_factor * max_next_q - current_q)
        self.q_table[state, action] = updated_q

# Define the environment
class Environment:
    def __init__(self):
        self.state_space = 5  # Number of possible states
        self.action_space = 2  # Number of possible actions

    def step(self, action):
        # Simulate the environment's response to the agent's action
        if action == 0:  # "Good" action
            reward = 1
            next_state = random.randint(0, self.state_space - 1)
        else:  # "Bad" action
            reward = -1
            next_state = random.randint(0, self.state_space - 1)
        return next_state, reward

# Define hyperparameters
epsilon = 0.1
learning_rate = 0.1
discount_factor = 0.9
num_episodes = 1000

# Create environment and agent
env = Environment()
agent = QLearningAgent(state_space=env.state_space, action_space=env.action_space)

# Set up the web driver (for Opera GX)
options = webdriver.ChromeOptions()
options.binary_location = r'<Change This to your Browser Path>'
options.add_argument('--disable-gpu')

# Set the path to the chromedriver executable
chromedriver_path = r'<PUT YOUR ChromeDriverPath>'
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

# Define the environment (webpage interaction)
class WebEnvironment:
    def __init__(self, driver, agent):
        self.driver = driver
        self.agent = agent
        self.target_url = "https://bloxflip.com/crash"
        self.cashout_button_text = "Cashout"
        self.multiplier_center_x = 960  # X-coordinate of the center of the screen
        self.multiplier_speed = 0.01  # Multiplier increase per time step

    def get_multiplier(self):
        # Simulate getting the current multiplier value (example)
        # Replace this with actual code to read the multiplier from the webpage
        current_x = self.multiplier_center_x + random.uniform(0, 10)
        current_multiplier = 1.0 + (current_x - self.multiplier_center_x) * self.multiplier_speed
        return current_multiplier

    def step(self, action):
        if self.driver.current_url != self.target_url:
            self.driver.get(self.target_url)
            time.sleep(3)  # Allow time for the page to load

        # Check if "Cashout" button is present
        cashout_button_present = self.cashout_button_text in self.driver.page_source

        if cashout_button_present:
            current_multiplier = self.get_multiplier()
            predicted_outcome = 1.05  # Replace with actual agent's prediction
            
            if current_multiplier >= 2.5:
                reward = 1
                if current_multiplier >= 10.0:
                    reward = 2  # Super reward for multiplier >= 10.0
            elif current_multiplier < 1.35:
                reward = -1
            else:
                reward = -2  # Penalize for not cashing out in time

            if predicted_outcome >= current_multiplier:
                cashout_button = self.driver.find_element_by_partial_link_text(self.cashout_button_text)
                actions = ActionChains(self.driver)
                actions.click(cashout_button).perform()

        screenshot = self.capture_screenshot()
        return screenshot, reward

    def capture_screenshot(self):
        screenshot_path = 'screenshot.png'
        self.driver.save_screenshot(screenshot_path)
        return Image.open(screenshot_path)

# Set up the environment
web_env = WebEnvironment(driver, agent)

# Training loop
for episode in range(num_episodes):
    state = random.randint(0, env.state_space - 1)
    for _ in range(100000):  # Maximum episode length
        action = agent.choose_action(state, epsilon)
        screenshot, reward = web_env.step(action)
        agent.update_q_table(state, action, reward, next_state, learning_rate, discount_factor)
        state = next_state

# Close the web driver when done
driver.quit()
