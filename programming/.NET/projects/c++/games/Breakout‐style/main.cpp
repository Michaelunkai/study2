#include <SFML/Graphics.hpp>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <ctime>

// Window dimensions
const int WINDOW_WIDTH = 800;
const int WINDOW_HEIGHT = 600;

// Brick settings
const int BRICK_ROWS = 5;
const int BRICK_COLUMNS = 10;
const float BRICK_WIDTH = 60.f;
const float BRICK_HEIGHT = 20.f;
const float BRICK_PADDING = 5.f;
const float BRICK_OFFSET_TOP = 50.f;
const float BRICK_OFFSET_LEFT = 35.f;

// Paddle settings
const sf::Vector2f PADDLE_SIZE(100.f, 20.f);
const float PADDLE_Y = WINDOW_HEIGHT - 50.f;

// Ball settings
const float BALL_RADIUS = 10.f;
const float BALL_SPEED = 5.f;

int main() {
    std::srand(static_cast<unsigned int>(std::time(nullptr)));
    
    sf::RenderWindow window(sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "Breakout Game");
    window.setFramerateLimit(60);

    // Paddle
    sf::RectangleShape paddle(PADDLE_SIZE);
    paddle.setFillColor(sf::Color::White);
    paddle.setOrigin(PADDLE_SIZE.x / 2.f, PADDLE_SIZE.y / 2.f);
    paddle.setPosition(WINDOW_WIDTH / 2.f, PADDLE_Y);

    // Ball
    sf::CircleShape ball(BALL_RADIUS);
    ball.setFillColor(sf::Color::Red);
    ball.setOrigin(BALL_RADIUS, BALL_RADIUS);
    ball.setPosition(WINDOW_WIDTH / 2.f, WINDOW_HEIGHT / 2.f);
    sf::Vector2f ballVelocity(-BALL_SPEED, -BALL_SPEED);

    // Create bricks
    std::vector<sf::RectangleShape> bricks;
    for (int i = 0; i < BRICK_ROWS; ++i) {
        for (int j = 0; j < BRICK_COLUMNS; ++j) {
            sf::RectangleShape brick(sf::Vector2f(BRICK_WIDTH, BRICK_HEIGHT));
            brick.setFillColor(sf::Color(
                std::rand() % 256,
                std::rand() % 256,
                std::rand() % 256));
            float x = BRICK_OFFSET_LEFT + j * (BRICK_WIDTH + BRICK_PADDING);
            float y = BRICK_OFFSET_TOP + i * (BRICK_HEIGHT + BRICK_PADDING);
            brick.setPosition(x, y);
            bricks.push_back(brick);
        }
    }

    // Score text
    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) {
        // If the font fails to load, score may not be displayed.
    }
    sf::Text scoreText;
    scoreText.setFont(font);
    scoreText.setCharacterSize(20);
    scoreText.setFillColor(sf::Color::White);
    int score = 0;
    
    // Game Over text
    sf::Text gameOverText;
    gameOverText.setFont(font);
    gameOverText.setCharacterSize(40);
    gameOverText.setFillColor(sf::Color::Red);
    gameOverText.setPosition(WINDOW_WIDTH / 2.f - 250.f, WINDOW_HEIGHT / 2.f - 50.f);

    bool gameOver = false;
    sf::Clock gameOverClock;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Only update game logic if not game over
        if (!gameOver) {
            // Paddle follows mouse X
            sf::Vector2i mousePos = sf::Mouse::getPosition(window);
            paddle.setPosition(static_cast<float>(mousePos.x), PADDLE_Y);

            // Update ball position
            ball.move(ballVelocity);

            // Bounce off left/right walls
            if (ball.getPosition().x - BALL_RADIUS < 0.f) {
                ball.setPosition(BALL_RADIUS, ball.getPosition().y);
                ballVelocity.x = -ballVelocity.x;
            }
            if (ball.getPosition().x + BALL_RADIUS > WINDOW_WIDTH) {
                ball.setPosition(WINDOW_WIDTH - BALL_RADIUS, ball.getPosition().y);
                ballVelocity.x = -ballVelocity.x;
            }
            // Bounce off top
            if (ball.getPosition().y - BALL_RADIUS < 0.f) {
                ball.setPosition(ball.getPosition().x, BALL_RADIUS);
                ballVelocity.y = -ballVelocity.y;
            }
            // Ball falls below window -> Game Over
            if (ball.getPosition().y - BALL_RADIUS > WINDOW_HEIGHT) {
                gameOver = true;
                gameOverClock.restart();
                std::stringstream ss;
                ss << "Game Over! Score: " << score << "\nRestarting...";
                gameOverText.setString(ss.str());
            }

            // Paddle collision
            if (ball.getGlobalBounds().intersects(paddle.getGlobalBounds())) {
                ball.setPosition(ball.getPosition().x, paddle.getPosition().y - PADDLE_SIZE.y / 2.f - BALL_RADIUS);
                ballVelocity.y = -ballVelocity.y;
            }

            // Brick collision
            for (auto it = bricks.begin(); it != bricks.end(); ) {
                if (ball.getGlobalBounds().intersects(it->getGlobalBounds())) {
                    ballVelocity.y = -ballVelocity.y;
                    score += 10;
                    it = bricks.erase(it);
                } else {
                    ++it;
                }
            }
        } else {
            // Auto-restart after 3 seconds when game over.
            if (gameOverClock.getElapsedTime().asSeconds() > 3.f) {
                // Reset ball
                ball.setPosition(WINDOW_WIDTH / 2.f, WINDOW_HEIGHT / 2.f);
                ballVelocity = sf::Vector2f(-BALL_SPEED, -BALL_SPEED);
                // Reset paddle
                paddle.setPosition(WINDOW_WIDTH / 2.f, PADDLE_Y);
                // Recreate bricks
                bricks.clear();
                for (int i = 0; i < BRICK_ROWS; ++i) {
                    for (int j = 0; j < BRICK_COLUMNS; ++j) {
                        sf::RectangleShape brick(sf::Vector2f(BRICK_WIDTH, BRICK_HEIGHT));
                        brick.setFillColor(sf::Color(
                            std::rand() % 256,
                            std::rand() % 256,
                            std::rand() % 256));
                        float x = BRICK_OFFSET_LEFT + j * (BRICK_WIDTH + BRICK_PADDING);
                        float y = BRICK_OFFSET_TOP + i * (BRICK_HEIGHT + BRICK_PADDING);
                        brick.setPosition(x, y);
                        bricks.push_back(brick);
                    }
                }
                score = 0;
                gameOver = false;
            }
        }

        // Update score text.
        std::stringstream ss;
        ss << "Score: " << score;
        scoreText.setString(ss.str());
        scoreText.setPosition(10.f, 10.f);

        // Rendering
        window.clear(sf::Color::Black);
        window.draw(paddle);
        window.draw(ball);
        for (const auto &brick : bricks)
            window.draw(brick);
        window.draw(scoreText);
        if (gameOver)
            window.draw(gameOverText);
        window.display();
    }
    return 0;
}
