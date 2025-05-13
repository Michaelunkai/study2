#include <SFML/Graphics.hpp>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <ctime>
#include <cmath>

// ------------------------------
// Global Constants
const int WINDOW_WIDTH = 800;
const int WINDOW_HEIGHT = 600;
const float PLAYER_SPEED = 5.f;
const float BULLET_SPEED = 8.f;
const float ENEMY_SPEED = 2.f;
const sf::Time ENEMY_SPAWN_INTERVAL = sf::seconds(1.f);

// ------------------------------
// Player Ship Class
class Player {
public:
    sf::ConvexShape shape;

    Player() {
        // Create a triangle to represent the spaceship.
        shape.setPointCount(3);
        shape.setPoint(0, sf::Vector2f(0.f, -20.f));
        shape.setPoint(1, sf::Vector2f(15.f, 20.f));
        shape.setPoint(2, sf::Vector2f(-15.f, 20.f));
        shape.setFillColor(sf::Color::Cyan);
        shape.setPosition(WINDOW_WIDTH/2.f, WINDOW_HEIGHT - 60.f);
    }

    void move(const sf::Vector2f& delta) {
        shape.move(delta);
        // Clamp to window boundaries.
        sf::Vector2f pos = shape.getPosition();
        if(pos.x < 0) pos.x = 0;
        if(pos.x > WINDOW_WIDTH) pos.x = WINDOW_WIDTH;
        if(pos.y < 0) pos.y = 0;
        if(pos.y > WINDOW_HEIGHT) pos.y = WINDOW_HEIGHT;
        shape.setPosition(pos);
    }
};

// ------------------------------
// Bullet Class
class Bullet {
public:
    sf::RectangleShape shape;
    sf::Vector2f velocity;
    bool active;

    Bullet(sf::Vector2f pos, sf::Vector2f dir) : active(true) {
        shape.setSize(sf::Vector2f(4.f, 12.f));
        shape.setFillColor(sf::Color::Yellow);
        shape.setOrigin(2.f, 6.f);
        shape.setPosition(pos);
        // Normalize direction
        float len = std::sqrt(dir.x * dir.x + dir.y * dir.y);
        if (len != 0.f)
            dir /= len;
        velocity = dir * BULLET_SPEED;
        // Rotate shape to match direction.
        float angle = std::atan2(dir.y, dir.x) * 180.f / 3.14159265f + 90.f;
        shape.setRotation(angle);
    }

    void update() {
        shape.move(velocity);
        // Deactivate if off-screen.
        sf::Vector2f pos = shape.getPosition();
        if (pos.x < 0 || pos.x > WINDOW_WIDTH || pos.y < 0 || pos.y > WINDOW_HEIGHT)
            active = false;
    }
};

// ------------------------------
// Enemy Class
class Enemy {
public:
    sf::RectangleShape shape;
    sf::Vector2f velocity;
    bool active;

    Enemy(sf::Vector2f pos) : active(true) {
        shape.setSize(sf::Vector2f(40.f, 30.f));
        shape.setFillColor(sf::Color::Red);
        shape.setOrigin(20.f, 15.f);
        shape.setPosition(pos);
        // Enemies move downward.
        velocity = sf::Vector2f(0.f, ENEMY_SPEED);
    }

    void update() {
        shape.move(velocity);
        // Deactivate if off-screen (bottom).
        if (shape.getPosition().y > WINDOW_HEIGHT + 30.f)
            active = false;
    }
};

// ------------------------------
// Main Function
int main() {
    std::srand(static_cast<unsigned int>(std::time(nullptr)));
    
    sf::RenderWindow window(sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "Space Shooter");
    window.setFramerateLimit(60);

    // Create the player.
    Player player;

    // Vectors for bullets and enemies.
    std::vector<Bullet> bullets;
    std::vector<Enemy> enemies;

    // Enemy spawn timer.
    sf::Clock enemySpawnClock;

    // Score variables.
    int score = 0;
    int highScore = 0;
    
    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) {
        // If font load fails, text won't be shown.
    }
    sf::Text scoreText;
    scoreText.setFont(font);
    scoreText.setCharacterSize(20);
    scoreText.setFillColor(sf::Color::White);

    sf::Text gameOverText;
    gameOverText.setFont(font);
    gameOverText.setCharacterSize(40);
    gameOverText.setFillColor(sf::Color::Red);
    gameOverText.setPosition(WINDOW_WIDTH/2.f - 200.f, WINDOW_HEIGHT/2.f - 50.f);

    bool gameOver = false;
    sf::Clock gameOverClock;

    while (window.isOpen()) {
        sf::Event event;
        while(window.pollEvent(event)){
            if(event.type == sf::Event::Closed)
                window.close();

            // Restart game if game over and R pressed.
            if(gameOver && event.type == sf::Event::KeyPressed && event.key.code == sf::Keyboard::R) {
                gameOver = false;
                score = 0;
                player.shape.setPosition(WINDOW_WIDTH/2.f, WINDOW_HEIGHT - 60.f);
                bullets.clear();
                enemies.clear();
                enemySpawnClock.restart();
            }
        }
        
        // Only update game objects if not game over.
        if (!gameOver) {
            // --- Player Movement ---
            sf::Vector2f movement(0.f, 0.f);
            if(sf::Keyboard::isKeyPressed(sf::Keyboard::Left) || sf::Keyboard::isKeyPressed(sf::Keyboard::A))
                movement.x -= PLAYER_SPEED;
            if(sf::Keyboard::isKeyPressed(sf::Keyboard::Right) || sf::Keyboard::isKeyPressed(sf::Keyboard::D))
                movement.x += PLAYER_SPEED;
            if(sf::Keyboard::isKeyPressed(sf::Keyboard::Up) || sf::Keyboard::isKeyPressed(sf::Keyboard::W))
                movement.y -= PLAYER_SPEED;
            if(sf::Keyboard::isKeyPressed(sf::Keyboard::Down) || sf::Keyboard::isKeyPressed(sf::Keyboard::S))
                movement.y += PLAYER_SPEED;
            player.move(movement);

            // --- Shooting Bullets ---
            // Press Space to shoot.
            static bool spacePressedLastFrame = false;
            if(sf::Keyboard::isKeyPressed(sf::Keyboard::Space)) {
                if(!spacePressedLastFrame) {
                    // Shoot bullet upward.
                    bullets.push_back(Bullet(player.shape.getPosition(), sf::Vector2f(0.f, -1.f)));
                }
                spacePressedLastFrame = true;
            } else {
                spacePressedLastFrame = false;
            }

            // --- Spawn Enemies ---
            if(enemySpawnClock.getElapsedTime() > ENEMY_SPAWN_INTERVAL) {
                float ex = static_cast<float>(std::rand() % (WINDOW_WIDTH - 40) + 20);
                enemies.push_back(Enemy(sf::Vector2f(ex, -30.f)));
                enemySpawnClock.restart();
            }

            // --- Update Bullets ---
            for(auto &bullet : bullets) {
                bullet.update();
            }
            // Remove inactive bullets.
            bullets.erase(std::remove_if(bullets.begin(), bullets.end(), 
                [](const Bullet &b){ return !b.active; }), bullets.end());

            // --- Update Enemies ---
            for(auto &enemy : enemies) {
                enemy.update();
            }
            // Remove inactive enemies.
            enemies.erase(std::remove_if(enemies.begin(), enemies.end(), 
                [](const Enemy &e){ return !e.active; }), enemies.end());

            // --- Collision Detection ---
            // Check bullet-enemy collisions.
            for(auto &bullet : bullets) {
                for(auto &enemy : enemies) {
                    if(bullet.active && enemy.active && bullet.shape.getGlobalBounds().intersects(enemy.shape.getGlobalBounds())) {
                        bullet.active = false;
                        enemy.active = false;
                        score += 10;
                    }
                }
            }
            // Check enemy-player collisions.
            for(auto &enemy : enemies) {
                if(enemy.active && enemy.shape.getGlobalBounds().intersects(player.shape.getGlobalBounds())) {
                    gameOver = true;
                    gameOverClock.restart();
                    // Update high score.
                    if(score > highScore)
                        highScore = score;
                    std::stringstream ss;
                    ss << "GAME OVER\nScore: " << score << "\nHigh Score: " << highScore << "\nPress R to Restart";
                    gameOverText.setString(ss.str());
                }
            }
            // Also, if an enemy reaches bottom of the screen, game over.
            for(auto &enemy : enemies) {
                if(enemy.active && enemy.shape.getPosition().y - enemy.shape.getSize().y/2.f > WINDOW_HEIGHT) {
                    gameOver = true;
                    gameOverClock.restart();
                    if(score > highScore)
                        highScore = score;
                    std::stringstream ss;
                    ss << "GAME OVER\nScore: " << score << "\nHigh Score: " << highScore << "\nPress R to Restart";
                    gameOverText.setString(ss.str());
                }
            }
        }
        
        // Update score display.
        std::stringstream scoreStream;
        scoreStream << "Score: " << score;
        sf::Text currentScore;
        currentScore.setFont(font);
        currentScore.setCharacterSize(20);
        currentScore.setFillColor(sf::Color::White);
        currentScore.setString(scoreStream.str());
        currentScore.setPosition(10.f, 10.f);
        
        // Rendering.
        window.clear(sf::Color(10, 10, 30));
        // Draw player.
        window.draw(player.shape);
        // Draw bullets.
        for(auto &bullet : bullets)
            window.draw(bullet.shape);
        // Draw enemies.
        for(auto &enemy : enemies)
            window.draw(enemy.shape);
        // Draw score.
        window.draw(currentScore);
        // Draw game over screen if applicable.
        if(gameOver)
            window.draw(gameOverText);
        window.display();
    }
    
    return 0;
}
