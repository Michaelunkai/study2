#!/bin/ 

# =============================================================================
# Script Name: setup_and_run_karate_fixed.sh
# Description: Automates installation of JDK, Maven, sets up Karate Framework
#              project with updated Java configurations, creates necessary files,
#              and runs tests on Ubuntu.
# Tools Used: Java JDK, Apache Maven, Karate Framework, Bash Scripting
# =============================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# Function to install Java JDK
install_java() {
    echo "Installing Java JDK..."
    sudo apt install -y default-jdk
    echo "Java installed successfully."
}

# Function to install Apache Maven
install_maven() {
    echo "Installing Apache Maven..."
    sudo apt install -y maven
    echo "Maven installed successfully."
}

# Function to verify installations
verify_installations() {
    echo "Verifying Java installation..."
    java -version
    echo "Verifying Maven installation..."
    mvn -version
}

# Function to create Maven project
create_maven_project() {
    echo "Creating Maven project 'karate-demo'..."
    mkdir -p ~/projects
    cd ~/projects
    mvn archetype:generate \
        -DgroupId=com.example \
        -DartifactId=karate-demo \
        -DarchetypeArtifactId=maven-archetype-quickstart \
        -DinteractiveMode=false
    echo "Maven project 'karate-demo' created successfully."
}

# Function to update pom.xml with Java version and add Karate dependencies
update_pom_xml() {
    echo "Updating pom.xml with Java version and Karate dependencies..."
    cd ~/projects/karate-demo

    # Backup existing pom.xml
    cp pom.xml pom.xml.backup

    # Add properties for Java version
    # Insert inside the <project> tag, preferably after <modelVersion>
    sed -i '/<modelVersion>/a \
    \ \ <properties>\n\
    \ \ \ \ <maven.compiler.source>1.8<\/maven.compiler.source>\n\
    \ \ \ \ <maven.compiler.target>1.8<\/maven.compiler.target>\n\
    \ \ <\/properties>' pom.xml

    # Add Karate dependency inside <dependencies>
    # Remove existing test dependencies (e.g., JUnit 4)
    sed -i '/<dependency>/{
        /junit\.jupiter\.api/d
        /junit\.jupiter\.engine/d
    }' pom.xml

    # Insert Karate dependency before closing </dependencies> tag
    sed -i '/<\/dependencies>/i \
        <!-- Karate Core -->\n\
        <dependency>\n\
            <groupId>com.intuit.karate</groupId>\n\
            <artifactId>karate-junit5</artifactId>\n\
            <version>1.4.0</version>\n\
            <scope>test</scope>\n\
        </dependency>' pom.xml

    # Add Maven Compiler Plugin with updated Java versions
    # Insert before closing </project> tag
    sed -i '/<\/project>/i \
    \ \ <build>\n\
    \ \ \ \ <plugins>\n\
    \ \ \ \ \ \ <plugin>\n\
    \ \ \ \ \ \ \ \ <groupId>org.apache.maven.plugins<\/groupId>\n\
    \ \ \ \ \ \ \ \ <artifactId>maven-compiler-plugin<\/artifactId>\n\
    \ \ \ \ \ \ \ \ <version>3.8.1<\/version>\n\
    \ \ \ \ \ \ \ \ <configuration>\n\
    \ \ \ \ \ \ \ \ \ \ <source>1.8<\/source>\n\
    \ \ \ \ \ \ \ \ \ \ <target>1.8<\/target>\n\
    \ \ \ \ \ \ \ \ <\/configuration>\n\
    \ \ \ \ \ \ <\/plugin>\n\
    \ \ \ \ <\/plugins>\n\
    \ \ <\/build>' pom.xml

    echo "pom.xml updated successfully."
}

# Function to create feature file
create_feature_file() {
    echo "Creating feature file 'example.feature'..."
    mkdir -p src/test/java/karate
    cat > src/test/java/karate/example.feature <<EOL
Feature: Sample API Test

  Scenario: Get user details
    Given url 'https://jsonplaceholder.typicode.com/users/1'
    When method GET
    Then status 200
    And print response
EOL
    echo "Feature file created successfully."
}

# Function to create test runner Java class
create_test_runner() {
    echo "Creating test runner 'ExampleTest.java'..."
    cat > src/test/java/karate/ExampleTest.java <<EOL
package karate;

import com.intuit.karate.junit5.Karate;

class ExampleTest {

    @Karate.Test
    Karate testSample() {
        return Karate.run("example").relativeTo(getClass());
    }
}
EOL
    echo "Test runner created successfully."
}

# Function to run Maven tests
run_tests() {
    echo "Running Karate tests with Maven..."
    mvn test
    echo "Tests executed successfully."
}

# Function to open test report
open_report() {
    REPORT_PATH="target/surefire-reports/karate-summary.html"
    if [ -f "\$REPORT_PATH" ]; then
        echo "Opening test report..."
        xdg-open "\$REPORT_PATH"
    else
        echo "Test report not found at \$REPORT_PATH"
    fi
}

# Main execution flow
main() {
    install_java
    install_maven
    verify_installations
    create_maven_project
    update_pom_xml
    create_feature_file
    create_test_runner
    run_tests
    open_report
    echo "Karate Framework setup and test execution completed successfully."
}

# Invoke main function
main
