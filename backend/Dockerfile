
# Build stage: use Maven with Java 21
FROM maven:3.9-eclipse-temurin-21 AS build

# Set the working directory
WORKDIR /app

# Copy Maven configuration and source code
COPY pom.xml .
COPY src ./src

# Build the Spring Boot executable JAR
RUN mvn -B -DskipTests package

# Runtime stage: Java 21
FROM eclipse-temurin:21-jre

WORKDIR /app

# Copy the built JAR into the runtime image
COPY --from=build /app/target/*.jar app.jar

# Document the default port
EXPOSE 8081

# Use Render's assigned port; default to 8081 locally
ENTRYPOINT ["sh", "-c", "java -Dserver.port=${PORT:-8081} -jar app.jar"]
