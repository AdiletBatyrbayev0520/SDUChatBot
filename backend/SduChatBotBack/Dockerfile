FROM gradle:8.5-jdk21 AS builder

WORKDIR /app

COPY gradlew .
COPY gradle gradle
COPY build.gradle.kts .
COPY settings.gradle.kts .

RUN chmod +x ./gradlew

RUN apt-get update \
  && apt-get install -y --no-install-recommends dos2unix curl \
  && rm -rf /var/lib/apt/lists/*

COPY src src

RUN ./gradlew build -x test

FROM eclipse-temurin:21-jre-alpine

RUN addgroup -g 1001 -S spring
RUN adduser -S spring -u 1001

WORKDIR /app

COPY --from=builder /app/build/libs/*.jar app.jar

RUN chown -R spring:spring /app

USER spring

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"] 